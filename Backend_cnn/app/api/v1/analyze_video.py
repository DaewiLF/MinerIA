import os
import uuid
import shutil

import cv2
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from app.ml.models.cnn_model import copper_model

router = APIRouter(prefix="/api/v1", tags=["video"])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
VIDEO_UPLOAD_DIR = os.path.join(BASE_DIR, "uploads", "videos")


@router.post("/analyze-video")
async def analyze_video(file: UploadFile = File(...)):
    """Recibe un video MP4, lo guarda a disco y analiza frames con la CNN."""

    # Validación liviana: aceptamos MP4 y MKV.
    # OJO: que OpenCV pueda leerlo depende del contenedor/codec.
    filename = (file.filename or "")
    ext = os.path.splitext(filename)[1].lower()
    allowed_ext = {".mp4", ".mkv"}
    allowed_content_types = {
        "video/mp4",
        "video/x-matroska",
        "application/octet-stream",  # algunos navegadores lo envían así
    }

    if ext not in allowed_ext and (file.content_type or "") not in allowed_content_types:
        raise HTTPException(
            status_code=400,
            detail="Formato no soportado. Sube un video MP4 o MKV.",
        )

    os.makedirs(VIDEO_UPLOAD_DIR, exist_ok=True)

    video_id = uuid.uuid4().hex
    video_filename = f"{video_id}{ext if ext in allowed_ext else '.mp4'}"
    video_path = os.path.join(VIDEO_UPLOAD_DIR, video_filename)

    # Guardar el video en disco
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Procesar el video con OpenCV
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise Exception("No se pudo abrir el archivo de video con OpenCV")

        fps = int(cap.get(cv2.CAP_PROP_FPS))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duracion_segundos = total_frames / fps if fps > 0 else 0

        hallazgos = []
        frame_actual = 0

        # 1 frame por segundo para no saturar CPU/RAM
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

                predicted_class, confidence = copper_model.predict(temp_frame_path)
                conf_pct = round(float(confidence) * 100, 2)

                if predicted_class == "con_cobre" and conf_pct > 60.0:
                    hallazgos.append(
                        {
                            "segundo_del_video": segundo_actual,
                            "timestamp": f"{segundo_actual // 60:02d}:{segundo_actual % 60:02d}",
                            "confianza": conf_pct,
                            "frame_asociado": f"/uploads/videos/{temp_frame_filename}",
                        }
                    )
                else:
                    os.remove(temp_frame_path)

            frame_actual += 1

        cap.release()

    except Exception as e:
        if os.path.exists(video_path):
            os.remove(video_path)
        raise HTTPException(status_code=500, detail=f"Error al procesar el video: {str(e)}")

    return JSONResponse(
        {
            "video_id": video_id,
            "duracion_total_segundos": round(duracion_segundos),
            "total_hallazgos": len(hallazgos),
            "detalle_hallazgos": hallazgos,
            "ruta_video_original": f"/uploads/videos/{video_filename}",
        }
    )
