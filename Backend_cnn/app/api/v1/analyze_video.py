import json
import os
import uuid
import shutil
from typing import Any, Dict, List

import cv2
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.ml.models.cnn_model import copper_model
from app.ml.utils.report_generator import generate_video_pdf_report
from app.db.mysql_connection import get_db
from app.db import models as db_models
from app.core.security import get_current_user

router = APIRouter(prefix="/api/v1", tags=["video"])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
VIDEO_UPLOAD_DIR = os.path.join(BASE_DIR, "uploads", "videos")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")


@router.post("/analyze-video")
async def analyze_video(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: db_models.Usuario = Depends(get_current_user),
):
    """Recibe un video MP4, lo guarda a disco y analiza frames con la CNN.
    Genera Grad-CAM para todos los frames y produce un PDF con la línea temporal.
    """

    filename = (file.filename or "")
    ext = os.path.splitext(filename)[1].lower()
    allowed_ext = {".mp4", ".mkv"}
    allowed_content_types = {
        "video/mp4",
        "video/x-matroska",
        "application/octet-stream",
    }

    if ext not in allowed_ext and (file.content_type or "") not in allowed_content_types:
        raise HTTPException(
            status_code=400,
            detail="Formato no soportado. Sube un video MP4 o MKV.",
        )

    os.makedirs(VIDEO_UPLOAD_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    video_id = uuid.uuid4().hex
    video_filename = f"{video_id}{ext if ext in allowed_ext else '.mp4'}"
    video_path = os.path.join(VIDEO_UPLOAD_DIR, video_filename)

    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise Exception("No se pudo abrir el archivo de video con OpenCV")

        fps = int(cap.get(cv2.CAP_PROP_FPS))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duracion_segundos = total_frames / fps if fps > 0 else 0

        timeline: List[Dict[str, Any]] = []
        hallazgos: List[Dict[str, Any]] = []
        frame_actual = 0
        frames_por_salto = fps if fps > 0 else 1

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_actual % frames_por_salto == 0:
                segundo_actual = int(frame_actual / fps) if fps > 0 else frame_actual

                temp_frame_filename = f"temp_{video_id}_{segundo_actual}.jpg"
                temp_frame_path = os.path.join(VIDEO_UPLOAD_DIR, temp_frame_filename)
                cv2.imwrite(temp_frame_path, frame)

                prediction = copper_model.analyze(temp_frame_path)
                if prediction is None:
                    continue
                predicted_class = prediction.result
                confidence = prediction.confidence
                conf_pct = round(float(confidence) * 100, 2)
                gradcam_rel = copper_model.generate_heatmap(temp_frame_path, prediction)

                entry = {
                    "segundo": segundo_actual,
                    "timestamp": f"{segundo_actual // 60:02d}:{segundo_actual % 60:02d}",
                    "prediccion": predicted_class,
                    "confianza": conf_pct,
                    "frame_url": f"/uploads/videos/{temp_frame_filename}",
                    "gradcam_url": gradcam_rel,
                }
                timeline.append(entry)

                if predicted_class == "con_cobre" and conf_pct > 60.0:
                    hallazgos.append(entry)

            frame_actual += 1

        cap.release()

    except Exception as e:
        if os.path.exists(video_path):
            os.remove(video_path)
        raise HTTPException(status_code=500, detail=f"Error al procesar el video: {str(e)}")

    pdf_filename = f"reporte_video_{video_id}.pdf"
    pdf_path = os.path.join(REPORTS_DIR, pdf_filename)
    try:
        generate_video_pdf_report(
            {
                "video_id": video_id,
                "filename": filename,
                "duracion_total_segundos": round(duracion_segundos),
                "total_hallazgos": len(hallazgos),
                "timeline": timeline,
                "hallazgos": hallazgos,
                "ruta_video_original": f"/uploads/videos/{video_filename}",
            },
            pdf_path,
        )
    except Exception as e:
        pdf_path = None

    reporte_payload = json.dumps(
        {
            "video_id": video_id,
            "filename": filename,
            "duracion_total_segundos": round(duracion_segundos),
            "total_frames_analizados": len(timeline),
            "total_hallazgos": len(hallazgos),
            "linea_temporal": timeline,
            "detalle_hallazgos": hallazgos,
            "ruta_video_original": f"/uploads/videos/{video_filename}",
            "reporte_pdf": f"/reports/{pdf_filename}" if pdf_path else None,
        },
        ensure_ascii=False,
    )

    analisis_video = db_models.AnalisisVideo(
        id_usuario=current_user.id_usuario,
        nombre_archivo=filename,
        ruta_video=f"/uploads/videos/{video_filename}",
        duracion_segundos=round(duracion_segundos),
        total_frames_analizados=len(timeline),
        total_hallazgos=len(hallazgos),
        reporte_json=reporte_payload,
        ruta_pdf=pdf_path,
    )
    db.add(analisis_video)
    db.commit()
    db.refresh(analisis_video)

    return JSONResponse(
        {
            "id_video": analisis_video.id_video,
            "video_id": video_id,
            "duracion_total_segundos": round(duracion_segundos),
            "total_frames_analizados": len(timeline),
            "total_hallazgos": len(hallazgos),
            "linea_temporal": timeline,
            "detalle_hallazgos": hallazgos,
            "ruta_video_original": f"/uploads/videos/{video_filename}",
            "reporte_pdf": f"/reports/{pdf_filename}" if pdf_path else None,
        }
    )


# --------- SCHEMAS DE HISTORIAL DE VIDEOS ---------

class VideoHistorySummary(BaseModel):
    id_video: int
    nombre_archivo: str
    duracion_segundos: int
    total_frames_analizados: int
    total_hallazgos: int
    fecha_analisis: str
    reporte_pdf: str | None = None


class VideoHistoryDetail(BaseModel):
    id_video: int
    nombre_archivo: str
    ruta_video: str
    duracion_segundos: int
    total_frames_analizados: int
    total_hallazgos: int
    linea_temporal: list
    detalle_hallazgos: list
    fecha_analisis: str
    reporte_pdf: str | None = None


# --------- ENDPOINTS DE HISTORIAL ---------


@router.get("/video-history", response_model=List[VideoHistorySummary])
def get_video_history(
    db: Session = Depends(get_db),
    current_user: db_models.Usuario = Depends(get_current_user),
):
    items = (
        db.query(db_models.AnalisisVideo)
        .filter(db_models.AnalisisVideo.id_usuario == current_user.id_usuario)
        .order_by(db_models.AnalisisVideo.fecha_analisis.desc())
        .limit(200)
        .all()
    )

    result: List[VideoHistorySummary] = []
    for item in items:
        payload = {}
        if item.reporte_json:
            try:
                payload = json.loads(item.reporte_json)
            except Exception:
                payload = {}

        result.append(
            VideoHistorySummary(
                id_video=item.id_video,
                nombre_archivo=item.nombre_archivo,
                duracion_segundos=item.duracion_segundos,
                total_frames_analizados=item.total_frames_analizados,
                total_hallazgos=item.total_hallazgos,
                fecha_analisis=item.fecha_analisis.isoformat()
                if item.fecha_analisis else "",
                reporte_pdf=payload.get("reporte_pdf"),
            )
        )
    return result


@router.get("/video-history/{id_video}", response_model=VideoHistoryDetail)
def get_video_detail(
    id_video: int,
    db: Session = Depends(get_db),
    current_user: db_models.Usuario = Depends(get_current_user),
):
    item = (
        db.query(db_models.AnalisisVideo)
        .filter(
            db_models.AnalisisVideo.id_video == id_video,
            db_models.AnalisisVideo.id_usuario == current_user.id_usuario,
        )
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Análisis de video no encontrado")

    payload = {}
    if item.reporte_json:
        try:
            payload = json.loads(item.reporte_json)
        except Exception:
            payload = {}

    return VideoHistoryDetail(
        id_video=item.id_video,
        nombre_archivo=item.nombre_archivo,
        ruta_video=item.ruta_video,
        duracion_segundos=item.duracion_segundos,
        total_frames_analizados=item.total_frames_analizados,
        total_hallazgos=item.total_hallazgos,
        linea_temporal=payload.get("linea_temporal", []),
        detalle_hallazgos=payload.get("detalle_hallazgos", []),
        fecha_analisis=item.fecha_analisis.isoformat()
        if item.fecha_analisis else "",
        reporte_pdf=payload.get("reporte_pdf"),
    )


@router.get("/video-history/{id_video}/pdf")
def download_video_pdf(
    id_video: int,
    db: Session = Depends(get_db),
    current_user: db_models.Usuario = Depends(get_current_user),
):
    item = (
        db.query(db_models.AnalisisVideo)
        .filter(
            db_models.AnalisisVideo.id_video == id_video,
            db_models.AnalisisVideo.id_usuario == current_user.id_usuario,
        )
        .first()
    )
    if not item or not item.ruta_pdf or not os.path.exists(item.ruta_pdf):
        raise HTTPException(status_code=404, detail="PDF no encontrado")

    return FileResponse(
        item.ruta_pdf,
        media_type="application/pdf",
        filename=f"reporte_video_{item.nombre_archivo}.pdf",
    )
