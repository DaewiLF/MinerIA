# app/api/analysis.py
import json
import os
import shutil
from decimal import Decimal
from typing import Any, Dict, List
from uuid import uuid4

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Depends,
    HTTPException,
)
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.mysql_connection import get_db
from app.db import models as db_models
from app.core.security import get_current_user
from app.ml.models.cnn_model import copper_model
from app.ml.utils.report_generator import generate_pdf_report

router = APIRouter(prefix="/api/analysis", tags=["analysis"])

UPLOAD_DIR = "uploads"
REPORTS_DIR = "reports"


# --------- SCHEMAS DE RESPUESTA (alineados con el front) ---------

class AnalysisSummaryResponse(BaseModel):
    id: int
    date: str
    zone: str
    category: str
    riskLevel: str
    copperGrade: str
    status: str


class AnalysisDetailResponse(BaseModel):
    id: int
    date: str
    zone: str
    category: str
    riskLevel: str
    copperGrade: str
    aiSummary: str
    recommendations: List[str]
    metadata: Dict[str, Any]
    imageUrl: str
    status: str
# ---------------------------------------------------------------


@router.post("/upload", response_model=AnalysisDetailResponse)
async def upload_analysis(
    file: UploadFile = File(...),
    metadata: str = Form(...),
    db: Session = Depends(get_db),
    current_user: db_models.Usuario = Depends(get_current_user),
):
    """
    Recibe archivo + metadata desde el front, ejecuta la IA, guarda en BD
    y genera un reporte + PDF.
    """
    # 1) Parsear metadata (JSON)
    try:
        meta_dict = json.loads(metadata)
        if not isinstance(meta_dict, dict):
            raise ValueError
    except Exception:
        raise HTTPException(status_code=400, detail="Metadata inválida")

    # 2) Validar tipo de archivo
    if file.content_type not in ("image/jpeg", "image/png"):
        raise HTTPException(status_code=400, detail="Solo se aceptan PNG o JPEG")

    # 3) Guardar archivo en disco
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    ext = os.path.splitext(file.filename)[1].lower() or ".jpg"
    unique_name = f"{uuid4().hex}{ext}"
    disk_path = os.path.join(UPLOAD_DIR, unique_name)
    web_url = f"/uploads/{unique_name}"

    with open(disk_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 4) Ejecutar IA
    predicted_class, confidence = copper_model.predict(disk_path)
    if predicted_class is None:
        raise HTTPException(
            status_code=500,
            detail="Error al procesar la imagen con el modelo",
        )

    # 5) Guardar imagen y clasificación en BD
    tamano = os.path.getsize(disk_path)

    imagen = db_models.Imagen(
        id_usuario=current_user.id_usuario,
        ruta_archivo=disk_path,
        tamano=tamano,
        formato=file.content_type,
        estado="procesada",
    )
    db.add(imagen)
    db.commit()
    db.refresh(imagen)

    clasificacion = db_models.Clasificacion(
        id_imagen=imagen.id_imagen,
        resultado=predicted_class,
        confianza=Decimal(str(confidence)),
        es_correcto=None,
        modelo_usado="CNN",
    )
    db.add(clasificacion)
    db.commit()
    db.refresh(clasificacion)

    # 6) Construir textos según metadata + resultado IA
    category = str(meta_dict.get("category") or "No especificada")
    risk_level = str(meta_dict.get("riskLevel") or "No especificado")
    zone = str(meta_dict.get("location") or "Zona no especificada")
    gps = str(meta_dict.get("coordinates") or "")
    responsable = str(meta_dict.get("responsible") or "")
    personal = meta_dict.get("personnel")

    conf_pct = round(confidence * 100, 2)
    hay_cobre = predicted_class == "con_cobre"

    if hay_cobre:
        copper_grade_text = f"Presencia de cobre detectada ({conf_pct} % de confianza)"
        ai_summary = (
            f"Se detecta PRESENCIA de vetas de cobre en la imagen con una "
            f"confianza de {conf_pct}%. Zona: {zone}. Nivel de riesgo declarado: {risk_level}. "
            f"Responsable del registro: {responsable or 'N/D'}. "
            f"Personal involucrado: {personal or 'N/D'}."
        )
        recommendations = [
            "Derivar el registro al área de geología para evaluación detallada.",
            "Actualizar el modelo geológico de la zona con esta evidencia.",
            "Priorizar esta zona en el plan de explotación según los lineamientos de la faena.",
        ]
        status = "con_cobre"
    else:
        copper_grade_text = f"Sin evidencia significativa de cobre ({conf_pct} % de confianza)"
        ai_summary = (
            f"No se detecta presencia significativa de vetas de cobre en la imagen "
            f"(confianza {conf_pct}%). Zona: {zone}. Nivel de riesgo declarado: {risk_level}. "
            f"Responsable del registro: {responsable or 'N/D'}. "
            f"Personal involucrado: {personal or 'N/D'}."
        )
        recommendations = [
            "Archivar el registro como caso sin presencia de cobre.",
            "Utilizar esta imagen como ejemplo negativo para seguir entrenando el modelo.",
        ]
        status = "sin_cobre"

    meta_out: Dict[str, Any] = dict(meta_dict)
    meta_out.update(
        {
            "coordinates": gps,
            "responsible": responsable,
            "personnel": personal,
            "modelo": "CopperCNN",
            "confianza_porcentaje": conf_pct,
        }
    )

    detail_payload: Dict[str, Any] = {
        "id": clasificacion.id_clasificacion,
        "date": clasificacion.fecha_clasificacion.isoformat()
        if clasificacion.fecha_clasificacion
        else "",
        "zone": zone,
        "category": category,
        "riskLevel": risk_level,
        "copperGrade": copper_grade_text,
        "aiSummary": ai_summary,
        "recommendations": recommendations,
        "metadata": meta_out,
        "imageUrl": web_url,
        "status": status,
    }

    # 7) Generar PDF + guardar en reportes
    os.makedirs(REPORTS_DIR, exist_ok=True)
    pdf_filename = f"reporte_{clasificacion.id_clasificacion}.pdf"
    pdf_path = os.path.join(REPORTS_DIR, pdf_filename)

    generate_pdf_report(detail_payload, pdf_path)

    # Guardar ruta del PDF dentro del JSON
    detail_payload["pdfPath"] = pdf_path

    reporte = db_models.Reporte(
        id_clasificacion=clasificacion.id_clasificacion,
        contenido=json.dumps(detail_payload, ensure_ascii=False),
        formato_reporte="pdf",
    )
    db.add(reporte)
    db.commit()

    return AnalysisDetailResponse(**detail_payload)


@router.get("/history", response_model=List[AnalysisSummaryResponse])
def get_history(
    db: Session = Depends(get_db),
    current_user: db_models.Usuario = Depends(get_current_user),
):
    """
    Devuelve una lista de resúmenes de análisis para el usuario logueado.
    """
    rows = (
        db.query(db_models.Clasificacion, db_models.Imagen, db_models.Reporte)
        .join(
            db_models.Imagen,
            db_models.Clasificacion.id_imagen == db_models.Imagen.id_imagen,
        )
        .outerjoin(
            db_models.Reporte,
            db_models.Reporte.id_clasificacion
            == db_models.Clasificacion.id_clasificacion,
        )
        .filter(db_models.Imagen.id_usuario == current_user.id_usuario)
        .order_by(db_models.Clasificacion.fecha_clasificacion.desc())
        .limit(200)
        .all()
    )

    items: List[AnalysisSummaryResponse] = []

    for clasif, imagen, reporte in rows:
        payload: Dict[str, Any] = {}
        if reporte and reporte.contenido:
            try:
                payload = json.loads(reporte.contenido)
            except Exception:
                payload = {}

        items.append(
            AnalysisSummaryResponse(
                id=clasif.id_clasificacion,
                date=payload.get(
                    "date",
                    clasif.fecha_clasificacion.isoformat()
                    if clasif.fecha_clasificacion
                    else "",
                ),
                zone=payload.get("zone", "Zona no especificada"),
                category=payload.get("category", "No especificada"),
                riskLevel=payload.get("riskLevel", "No especificado"),
                copperGrade=payload.get("copperGrade", clasif.resultado),
                status=payload.get(
                    "status",
                    "con_cobre"
                    if clasif.resultado == "con_cobre"
                    else "sin_cobre",
                ),
            )
        )

    return items


@router.get("/{clasificacion_id}", response_model=AnalysisDetailResponse)
def get_analysis_detail(
    clasificacion_id: int,
    db: Session = Depends(get_db),
    current_user: db_models.Usuario = Depends(get_current_user),
):
    """
    Devuelve el detalle completo de un análisis (para AnalysisDetailPage).
    """
    row = (
        db.query(db_models.Clasificacion, db_models.Imagen, db_models.Reporte)
        .join(
            db_models.Imagen,
            db_models.Clasificacion.id_imagen == db_models.Imagen.id_imagen,
        )
        .outerjoin(
            db_models.Reporte,
            db_models.Reporte.id_clasificacion
            == db_models.Clasificacion.id_clasificacion,
        )
        .filter(
            db_models.Clasificacion.id_clasificacion == clasificacion_id,
            db_models.Imagen.id_usuario == current_user.id_usuario,
        )
        .first()
    )

    if not row:
        raise HTTPException(status_code=404, detail="Análisis no encontrado")

    clasif, imagen, reporte = row
    payload: Dict[str, Any] = {}
    if reporte and reporte.contenido:
        try:
            payload = json.loads(reporte.contenido)
        except Exception:
            payload = {}

    date = payload.get(
        "date",
        clasif.fecha_clasificacion.isoformat()
        if clasif.fecha_clasificacion
        else "",
    )
    zone = payload.get("zone", "Zona no especificada")
    category = payload.get("category", "No especificada")
    risk = payload.get("riskLevel", "No especificado")
    copper_grade = payload.get("copperGrade", clasif.resultado)
    ai_summary = payload.get("aiSummary", "")
    recommendations = payload.get("recommendations") or []
    metadata = payload.get("metadata") or {}
    status = payload.get(
        "status",
        "con_cobre" if clasif.resultado == "con_cobre" else "sin_cobre",
    )

    image_url = payload.get(
        "imageUrl",
        f"/uploads/{os.path.basename(imagen.ruta_archivo)}" if imagen else "",
    )

    return AnalysisDetailResponse(
        id=clasif.id_clasificacion,
        date=date,
        zone=zone,
        category=category,
        riskLevel=risk,
        copperGrade=copper_grade,
        aiSummary=ai_summary,
        recommendations=recommendations,
        metadata=metadata,
        imageUrl=image_url,
        status=status,
    )


@router.get("/{clasificacion_id}/pdf")
def download_pdf(
    clasificacion_id: int,
    db: Session = Depends(get_db),
    current_user: db_models.Usuario = Depends(get_current_user),
):
    """
    Devuelve el PDF del reporte asociado a una clasificación.
    """
    row = (
        db.query(db_models.Reporte, db_models.Clasificacion, db_models.Imagen)
        .join(
            db_models.Clasificacion,
            db_models.Reporte.id_clasificacion
            == db_models.Clasificacion.id_clasificacion,
        )
        .join(
            db_models.Imagen,
            db_models.Clasificacion.id_imagen == db_models.Imagen.id_imagen,
        )
        .filter(
            db_models.Clasificacion.id_clasificacion == clasificacion_id,
            db_models.Imagen.id_usuario == current_user.id_usuario,
        )
        .first()
    )

    if not row:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    reporte, clasif, imagen = row
    payload = {}
    if reporte.contenido:
        try:
            payload = json.loads(reporte.contenido)
        except Exception:
            payload = {}

    pdf_path = payload.get("pdfPath")
    if not pdf_path or not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF no disponible")

    filename = os.path.basename(pdf_path)
    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=filename,
    )
