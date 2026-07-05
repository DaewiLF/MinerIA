import asyncio
import json
import os
from decimal import Decimal
from typing import Any, Dict

from sqlalchemy.orm import Session

from app.db.mysql_connection import SessionLocal
from app.db import models as db_models
from app.ml.models.model_registry import (
    DEFAULT_MODEL_ID,
    get_analysis_model,
)
from app.ml.utils.report_generator import generate_pdf_report

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")


def process_single_item(db: Session, item: db_models.ColaAnalisis) -> None:
    user = item.usuario

    item.estado = "procesando"
    db.commit()

    try:
        analysis_model = get_analysis_model(item.modelo_id)
    except KeyError:
        item.estado = "error"
        item.error = f"Modelo no soportado: {item.modelo_id}"
        item.fecha_procesamiento = db_models.func.now()
        db.commit()
        return

    prediction = analysis_model.analyze(item.ruta_archivo)
    if prediction is None:
        item.estado = "error"
        item.error = "Error al procesar la imagen con el modelo"
        item.fecha_procesamiento = db_models.func.now()
        db.commit()
        return

    predicted_class = prediction.result
    confidence = prediction.confidence

    gradcam_url = analysis_model.generate_heatmap(item.ruta_archivo, prediction)

    meta_dict = {}
    try:
        meta_dict = json.loads(item.metadata_json)
        if not isinstance(meta_dict, dict):
            meta_dict = {}
    except Exception:
        meta_dict = {}

    imagen = db_models.Imagen(
        id_usuario=item.id_usuario,
        ruta_archivo=item.ruta_archivo,
        tamano=item.tamano,
        formato=item.formato,
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

    web_url = f"/uploads/{os.path.basename(item.ruta_archivo)}"

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
    }

    os.makedirs(REPORTS_DIR, exist_ok=True)
    pdf_filename = f"reporte_{clasificacion.id_clasificacion}.pdf"
    pdf_path = os.path.join(REPORTS_DIR, pdf_filename)

    generate_pdf_report(detail_payload, pdf_path)
    detail_payload["pdfPath"] = pdf_path

    reporte = db_models.Reporte(
        id_clasificacion=clasificacion.id_clasificacion,
        contenido=json.dumps(detail_payload, ensure_ascii=False),
        formato_reporte="pdf",
    )
    db.add(reporte)

    item.estado = "completado"
    item.fecha_procesamiento = db_models.func.now()
    db.commit()


def process_pending_queue() -> None:
    db = SessionLocal()
    try:
        while True:
            item = (
                db.query(db_models.ColaAnalisis)
                .filter(db_models.ColaAnalisis.estado == "pendiente")
                .order_by(db_models.ColaAnalisis.fecha_creacion.asc())
                .first()
            )
            if item is None:
                break
            process_single_item(db, item)
    finally:
        db.close()


async def run_queue_background() -> None:
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, process_pending_queue)
