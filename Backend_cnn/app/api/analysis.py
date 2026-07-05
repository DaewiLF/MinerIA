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
    BackgroundTasks,
)
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.mysql_connection import get_db
from app.db import models as db_models
from app.core.security import get_current_user
from app.ml.models.model_registry import (
    DEFAULT_MODEL_ID,
    get_analysis_model,
    list_analysis_models,
)
from app.ml.utils.report_generator import generate_pdf_report
from app.ml.inference_queue import run_queue_background

router = APIRouter(prefix="/api/analysis", tags=["analysis"])
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")


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
    gradcamUrl: str | None = None
    status: str


class ModelOptionResponse(BaseModel):
    id: str
    name: str
    description: str


class QueueItemResponse(BaseModel):
    id: int
    estado: str
    error: str | None
    fecha_creacion: str
    fecha_procesamiento: str | None


class BatchUploadResponse(BaseModel):
    total: int
    items: List[QueueItemResponse]


class DashboardStatsResponse(BaseModel):
    analisis_hoy: int
    analisis_semana: int
    confianza_promedio: float
    alertas_criticas: int
    en_cola: int
    modelos_activos: int
    actividad_semanal: list[dict]
    distribucion_mineral: list[dict]
    ultimos_analisis: list[dict]
# ---------------------------------------------------------------


@router.get("/stats", response_model=DashboardStatsResponse)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: db_models.Usuario = Depends(get_current_user),
):
    from datetime import datetime, timedelta
    from sqlalchemy import func

    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_ago = today_start - timedelta(days=7)
    user_id = current_user.id_usuario

    # Base: clasificaciones del usuario vía imágenes
    base = (
        db.query(db_models.Clasificacion)
        .join(db_models.Imagen, db_models.Clasificacion.id_imagen == db_models.Imagen.id_imagen)
        .filter(db_models.Imagen.id_usuario == user_id)
    )

    total_hoy = base.filter(db_models.Clasificacion.fecha_clasificacion >= today_start).count()

    total_semana = base.filter(db_models.Clasificacion.fecha_clasificacion >= week_ago).count()

    conf_prom = (
        base.with_entities(func.avg(db_models.Clasificacion.confianza))
        .filter(db_models.Clasificacion.confianza.isnot(None))
        .scalar()
    )
    confianza_promedio = round(float(conf_prom) * 100, 2) if conf_prom else 0.0

    # Distribución por resultado (con_cobre / sin_cobre / mineral)
    mineral_dist = (
        base.with_entities(
            db_models.Clasificacion.resultado, func.count().label("total")
        )
        .group_by(db_models.Clasificacion.resultado)
        .all()
    )

    # Actividad diaria últimos 7 días
    daily = (
        base.with_entities(
            func.date(db_models.Clasificacion.fecha_clasificacion).label("fecha"),
            func.count().label("total"),
        )
        .filter(db_models.Clasificacion.fecha_clasificacion >= week_ago)
        .group_by(func.date(db_models.Clasificacion.fecha_clasificacion))
        .order_by(func.date(db_models.Clasificacion.fecha_clasificacion))
        .all()
    )

    # Cola pendientes
    cola_pendientes = (
        db.query(func.count())
        .filter(
            db_models.ColaAnalisis.id_usuario == user_id,
            db_models.ColaAnalisis.estado == "pendiente",
        )
        .scalar()
    ) or 0

    # Alertas críticas (riskLevel = "Alto" en el JSON del reporte)
    alertas = (
        db.query(db_models.Reporte)
        .join(
            db_models.Clasificacion,
            db_models.Reporte.id_clasificacion == db_models.Clasificacion.id_clasificacion,
        )
        .join(db_models.Imagen)
        .filter(db_models.Imagen.id_usuario == user_id)
        .all()
    )
    alertas_criticas = 0
    for r in alertas:
        try:
            c = json.loads(r.contenido)
            if c.get("riskLevel") == "Alto":
                alertas_criticas += 1
        except Exception:
            pass

    # Últimos 5 análisis
    ultimos_rows = (
        db.query(db_models.Clasificacion, db_models.Imagen, db_models.Reporte)
        .join(db_models.Imagen)
        .outerjoin(db_models.Reporte)
        .filter(db_models.Imagen.id_usuario == user_id)
        .order_by(db_models.Clasificacion.fecha_clasificacion.desc())
        .limit(5)
        .all()
    )
    ultimos_analisis = []
    for clasif, imagen, reporte in ultimos_rows:
        p = {}
        if reporte and reporte.contenido:
            try:
                p = json.loads(reporte.contenido)
            except Exception:
                p = {}
        ultimos_analisis.append(
            {
                "id": clasif.id_clasificacion,
                "zone": p.get("zone", "Zona no especificada"),
                "copperGrade": p.get("copperGrade", clasif.resultado),
                "confidence": round(float(clasif.confianza) * 100, 1) if clasif.confianza else 0,
                "riskLevel": p.get("riskLevel", "No especificado"),
                "date": p.get(
                    "date",
                    clasif.fecha_clasificacion.isoformat()
                    if clasif.fecha_clasificacion
                    else "",
                ),
            }
        )

    # Modelos activos
    modelos = list_analysis_models()
    modelos_activos = len(modelos)

    # Rellenar días sin actividad en la semana
    actividad_semanal = []
    for i in range(7):
        day = (today_start - timedelta(days=6 - i)).date()
        match = [d for d in daily if d.fecha == day]
        actividad_semanal.append(
            {"fecha": day.isoformat(), "total": match[0].total if match else 0}
        )

    return DashboardStatsResponse(
        analisis_hoy=total_hoy,
        analisis_semana=total_semana,
        confianza_promedio=confianza_promedio,
        alertas_criticas=alertas_criticas,
        en_cola=cola_pendientes,
        modelos_activos=modelos_activos,
        actividad_semanal=actividad_semanal,
        distribucion_mineral=[
            {"nombre": r.resultado, "total": r.total} for r in mineral_dist
        ],
        ultimos_analisis=ultimos_analisis,
    )


@router.get("/models", response_model=List[ModelOptionResponse])
def get_models():
    return [ModelOptionResponse(**model) for model in list_analysis_models()]


@router.post("/upload", response_model=AnalysisDetailResponse)
async def upload_analysis(
    file: UploadFile = File(...),
    metadata: str = Form(...),
    model_id: str | None = Form(None),
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

    selected_model_id = str(model_id or meta_dict.get("modelId") or DEFAULT_MODEL_ID)
    try:
        analysis_model = get_analysis_model(selected_model_id)
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

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
    prediction = analysis_model.analyze(disk_path)
    if prediction is None:
        raise HTTPException(
            status_code=500,
            detail="Error al procesar la imagen con el modelo",
        )
    predicted_class = prediction.result
    confidence = prediction.confidence

    gradcam_url = analysis_model.generate_heatmap(disk_path, prediction)

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
        modelo_usado=prediction.model_name[:50],
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

    if prediction.model_id == "minerals":
        mineral = str(prediction.metadata.get("mineral_predicho") or prediction.raw_label)
        copper_probability = float(prediction.metadata.get("probabilidad_cobre") or 0)
        copper_pct = round(copper_probability * 100, 2)

        if hay_cobre:
            copper_grade_text = f"Mineral detectado: copper ({conf_pct} % de confianza)"
            ai_summary = (
                f"El modelo multiclase clasifico la muestra como copper con una "
                f"confianza de {conf_pct}%. Zona: {zone}. Nivel de riesgo declarado: {risk_level}. "
                f"Responsable del registro: {responsable or 'N/D'}. "
                f"Personal involucrado: {personal or 'N/D'}."
            )
            recommendations = [
                "Derivar el registro al area de geologia para validacion del mineral.",
                "Usar la clase predicha para la revision Grad-CAM del modelo multiclase.",
                "Contrastar el resultado con el modelo binario de cobre si se requiere confirmacion.",
            ]
            status = "con_cobre"
        else:
            copper_grade_text = f"Mineral probable: {mineral} ({conf_pct} % de confianza)"
            ai_summary = (
                f"El modelo multiclase clasifico la muestra como {mineral} con una "
                f"confianza de {conf_pct}%. Probabilidad asignada a copper: {copper_pct}%. "
                f"Zona: {zone}. Nivel de riesgo declarado: {risk_level}. "
                f"Responsable del registro: {responsable or 'N/D'}. "
                f"Personal involucrado: {personal or 'N/D'}."
            )
            recommendations = [
                "Revisar la clase mineral predicha antes de tomar decisiones operativas.",
                "Usar Grad-CAM para inspeccionar que zonas de la imagen explican la prediccion.",
                "Ejecutar el modelo binario de cobre si el objetivo es solo confirmar presencia de cobre.",
            ]
            status = "sin_cobre"
    else:
        if hay_cobre:
            copper_grade_text = f"Presencia de cobre detectada ({conf_pct} % de confianza)"
            ai_summary = (
                f"Se detecta PRESENCIA de vetas de cobre en la imagen con una "
                f"confianza de {conf_pct}%. Zona: {zone}. Nivel de riesgo declarado: {risk_level}. "
                f"Responsable del registro: {responsable or 'N/D'}. "
                f"Personal involucrado: {personal or 'N/D'}."
            )
            recommendations = [
                "Derivar el registro al area de geologia para evaluacion detallada.",
                "Actualizar el modelo geologico de la zona con esta evidencia.",
                "Priorizar esta zona en el plan de explotacion segun los lineamientos de la faena.",
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
            "modelo": prediction.model_name,
            "modelo_id": prediction.model_id,
            "confianza_porcentaje": conf_pct,
            "resultado_modelo": prediction.result,
            "etiqueta_predicha": prediction.raw_label,
            "probabilidades": prediction.probabilities,
        }
    )
    meta_out.update(prediction.metadata)

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
        "gradcamUrl": gradcam_url,
        "status": status,
        "coordinates": gps,
        "responsible": responsable,
        "personnel": personal,
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


@router.post("/upload-batch", response_model=BatchUploadResponse)
async def upload_batch(
    files: List[UploadFile] = File(...),
    metadata: str = Form(...),
    model_id: str | None = Form(None),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db),
    current_user: db_models.Usuario = Depends(get_current_user),
):
    try:
        meta_dict = json.loads(metadata)
        if not isinstance(meta_dict, dict):
            raise ValueError
    except Exception:
        raise HTTPException(status_code=400, detail="Metadata inválida")

    selected_model_id = str(model_id or meta_dict.get("modelId") or DEFAULT_MODEL_ID)

    if len(files) == 0:
        raise HTTPException(status_code=400, detail="No se enviaron archivos")

    queue_items: List[QueueItemResponse] = []
    metadata_str = json.dumps(meta_dict, ensure_ascii=False)

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    for file in files:
        if file.content_type not in ("image/jpeg", "image/png"):
            continue

        ext = os.path.splitext(file.filename)[1].lower() or ".jpg"
        unique_name = f"{uuid4().hex}{ext}"
        disk_path = os.path.join(UPLOAD_DIR, unique_name)

        with open(disk_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        tamano = os.path.getsize(disk_path)

        cola = db_models.ColaAnalisis(
            id_usuario=current_user.id_usuario,
            ruta_archivo=disk_path,
            tamano=tamano,
            formato=file.content_type,
            metadata_json=metadata_str,
            modelo_id=selected_model_id,
            estado="pendiente",
        )
        db.add(cola)
        db.commit()
        db.refresh(cola)

        queue_items.append(
            QueueItemResponse(
                id=cola.id_cola,
                estado=cola.estado,
                error=None,
                fecha_creacion=cola.fecha_creacion.isoformat()
                if cola.fecha_creacion else "",
                fecha_procesamiento=None,
            )
        )

    background_tasks.add_task(run_queue_background)

    return BatchUploadResponse(total=len(queue_items), items=queue_items)


@router.get("/queue", response_model=List[QueueItemResponse])
def get_user_queue(
    db: Session = Depends(get_db),
    current_user: db_models.Usuario = Depends(get_current_user),
):
    items = (
        db.query(db_models.ColaAnalisis)
        .filter(db_models.ColaAnalisis.id_usuario == current_user.id_usuario)
        .order_by(db_models.ColaAnalisis.fecha_creacion.desc())
        .limit(100)
        .all()
    )

    return [
        QueueItemResponse(
            id=item.id_cola,
            estado=item.estado,
            error=item.error,
            fecha_creacion=item.fecha_creacion.isoformat()
            if item.fecha_creacion else "",
            fecha_procesamiento=item.fecha_procesamiento.isoformat()
            if item.fecha_procesamiento else None,
        )
        for item in items
    ]


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
