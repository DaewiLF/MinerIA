from fastapi import APIRouter

router = APIRouter(
    prefix="/results",
    tags=["Resultados"]
)

# Ejemplo de historial
fake_db = [
    {"id": 1, "muestra": "A1", "resultado": "con_cobre", "probabilidad": 0.87},
    {"id": 2, "muestra": "B3", "resultado": "sin_cobre", "probabilidad": 0.21},
]

@router.get("/")
def listar_resultados():
    return fake_db
