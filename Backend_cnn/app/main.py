from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.formparsers import MultiPartParser

from app.core.config import settings
from app.db.mysql_connection import Base, engine
from app.api import auth, analysis  # nuestros routers
from app.api.analysis import UPLOAD_DIR, REPORTS_DIR
from app.api.v1 import analyze_video
from app.api.v1 import panorama


"""FastAPI entrypoint.

Notas de uploads grandes (4K / video):
- Starlette limita el tamaño máximo de cada parte multipart (max_part_size).
- Subimos ese umbral a un valor muy alto para evitar errores por archivos grandes.

El límite real pasa a ser el disco/OS (y el reverse proxy si se agrega uno).
"""

# Permite uploads grandes ("ilimitado" práctico). Ajusta si quieres un techo.
MultiPartParser.max_part_size = 1024 * 1024 * 1024 * 20  # 20 GB

app = FastAPI(title=settings.APP_NAME)

@app.on_event("startup")
def _create_tables_on_startup() -> None:
    # Crear tablas (solo para desarrollo). En Docker funciona con MYSQL_HOST=db.
    # Fuera de Docker, si la BD no está disponible, no bloqueamos el arranque.
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as exc:
        print(f"[WARN] No se pudo conectar a la BD en startup: {exc}")

# CORS para que el frontend (Vite) pueda llamar al backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # URL de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas
app.include_router(auth.router)
app.include_router(analysis.router)
app.include_router(analyze_video.router)
app.include_router(panorama.router)


app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
app.mount("/reports", StaticFiles(directory=REPORTS_DIR), name="reports")

@app.get("/")
def root():
    return {"message": "Backend MinerIA OK"}

