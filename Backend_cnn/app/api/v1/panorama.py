import os
import shutil
from typing import Literal
from uuid import uuid4

import cv2
from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from app.ml.utils.sliding_window import sliding_window_patches

router = APIRouter(prefix="/api/v1", tags=["panorama"])

# Base del proyecto (Backend_cnn/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
PANORAMA_DIR = os.path.join(BASE_DIR, "storage", "panoramas")


class PanoramaUploadResponse(BaseModel):
    status: Literal["ok"]
    saved_path: str
    original_filename: str
    size_bytes: int
    content_type: str
    patch_count: int
    grid: list[tuple[int, int, int, int]]


@router.post("/analyze-panorama", response_model=PanoramaUploadResponse)
async def analyze_panorama(file: UploadFile = File(...)):
    """Recibe una imagen panorámica pesada, la guarda en disco y devuelve metadatos básicos.

    Nota: No se aplica ningún límite artificial de tamaño.
    """

    content_type = (file.content_type or "").strip().lower()
    if not content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Archivo inválido: se esperaba una imagen (content-type image/*).",
        )

    os.makedirs(PANORAMA_DIR, exist_ok=True)

    original_filename = file.filename or ""
    ext = os.path.splitext(original_filename)[1].lower()
    if not ext:
        if content_type == "image/jpeg":
            ext = ".jpg"
        elif content_type == "image/png":
            ext = ".png"
        else:
            ext = ".img"

    unique_name = f"{uuid4().hex}{ext}"
    saved_path = os.path.join(PANORAMA_DIR, unique_name)

    try:
        with open(saved_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception:
        # Si la escritura falla, devolvemos 500
        raise HTTPException(
            status_code=500,
            detail="Error al escribir el archivo en disco.",
        )

    try:
        size_bytes = os.path.getsize(saved_path)
    except OSError:
        size_bytes = 0

    # Leer con OpenCV (entorno docker/headless) y calcular grilla de parches
    img = cv2.imread(saved_path, cv2.IMREAD_COLOR)
    if img is None:
        raise HTTPException(
            status_code=400,
            detail="Archivo inválido: no se pudo leer como imagen.",
        )

    # Sprint 1: solo grid/contador (sin materializar parches en RAM)
    patches = sliding_window_patches(img, return_patches=False)
    grid = [(p.x_min, p.y_min, p.x_max, p.y_max) for p in patches]

    return PanoramaUploadResponse(
        status="ok",
        saved_path=saved_path,
        original_filename=original_filename,
        size_bytes=size_bytes,
        content_type=content_type,
        patch_count=len(grid),
        grid=grid,
    )
