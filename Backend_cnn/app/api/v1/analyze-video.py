import os
import cv2
import uuid
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.ml.cnn_model import copper_model
from app.core.config import settings

router = APIRouter() 

VIDEO_UPLOAD_DIR = "uploads/videos"

@router.post("/analyze-video")
async def analyze_video(file: UploadFile = File(...)):
    """
    Recibe un video MP4 de recorridos subterráneos, extrae frames 
    estratégicamente y los analiza en busca de vetas de cobre.
    """
    # 1. Validar que sea un MP4
    if file.content_type != "video/mp4" and not file.filename.lower().endswith(".mp4"):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos de video MP4")

    # 2. Crear directorios si no existen
    os.makedirs(VIDEO_UPLOAD_DIR, exist_ok=True)
    
    # 3. Guardar el video temporalmente/permanentemente en el servidor (Docker)
    video_id = uuid.uuid4().hex
    video_filename = f"{video_id}.mp4"
    video_path = os.path.join(VIDEO_UPLOAD_DIR, video_filename)

    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 4. Procesar el video con OpenCV
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise Exception("No se pudo abrir el archivo de video con OpenCV")

        fps = int(cap.get(cv2.CAP_PROP_FPS))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duracion_segundos = total_frames / fps if fps > 0 else 0

        # Lista para guardar los hallazgos positivos
        hallazgos = []
        frame_actual = 0
        
        # Procesaremos 1 frame por cada segundo de video para no saturar la CPU/RAM
        frames_por_salto = fps 

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break # Fin del video

            # Solo analizamos si estamos en el "segundo" exacto
            if frame_actual % frames_por_salto == 0:
                segundo_actual = int(frame_actual / fps)
                
                # Guardar el frame temporalmente en disco para que la CNN lo lea
                # (O puedes adaptar tu modelo para que reciba el array numpy directamente)
                temp_frame_path = os.path.join(VIDEO_UPLOAD_DIR, f"temp_{video_id}_{segundo_actual}.jpg")
                cv2.imwrite(temp_frame_path, frame)

                # Ejecutar la IA en este frame
                predicted_class, confidence = copper_model.predict(temp_frame_path)
                conf_pct = round(float(confidence) * 100, 2)

                # Si detecta cobre, guardamos el momento exacto
                if predicted_class == "con_cobre" and conf_pct > 60.0: # Umbral de seguridad opcional
                    hallazgos.append({
                        "segundo_del_video": segundo_actual,
                        "timestamp": f"{segundo_actual // 60:02d}:{segundo_actual % 60:02d}",
                        "confianza": conf_pct,
                        "frame_asociado": f"/uploads/videos/temp_{video_id}_{segundo_actual}.jpg"
                    })
                else:
                    # Limpiamos los frames que no tienen cobre para ahorrar espacio
                    os.remove(temp_frame_path)

            frame_actual += 1

        cap.release()

    except Exception as e:
        # Limpieza en caso de error crítico
        if os.path.exists(video_path):
            os.remove(video_path)
        raise HTTPException(status_code=500, detail=f"Error al procesar el video: {str(e)}")

    # 5. Retornar el resumen del análisis
    return JSONResponse({
        "video_id": video_id,
        "duracion_total_segundos": round(duracion_segundos),
        "total_hallazgos": len(hallazgos),
        "detalle_hallazgos": hallazgos,
        "ruta_video_original": f"/uploads/videos/{video_filename}"
    })