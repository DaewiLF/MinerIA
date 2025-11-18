from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.db.mysql_connection import Base, engine
from app.api import auth, analysis  # nuestros routers

app = FastAPI(title=settings.APP_NAME)

# Crear tablas (solo para desarrollo)
Base.metadata.create_all(bind=engine)

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


app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/reports", StaticFiles(directory="reports"), name="reports")

@app.get("/")
def root():
    return {"message": "Backend MinerIA OK"}

