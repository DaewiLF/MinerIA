# app/api/auth.py
from datetime import timedelta
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.db.mysql_connection import get_db
from app.db import models as db_models
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_user_by_email,
)
from app.core.config import settings

router = APIRouter(prefix="/api/auth", tags=["auth"])


# --------- Schemas ---------

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    # EXACTAMENTE los dos roles que tienes en el front
    role: Literal["admin", "analyst"]


class UserInfo(BaseModel):
    id: int
    email: EmailStr
    role: str
    name: str

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    token: str
    user: UserInfo


class UserCreate(BaseModel):
    nombre: str
    email: EmailStr
    password: str
    cargo: str   # aquí podrás guardar "admin" o "analyst"


# --------- Endpoints ---------

@router.post("/login", response_model=LoginResponse)
def login(
    body: LoginRequest,
    db: Session = Depends(get_db),
):
    # 1) Buscar usuario por email
    user: db_models.Usuario | None = get_user_by_email(db, body.email)
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Correo o contraseña incorrectos",
        )

    # 2) Normalizar cargo de BD y compararlo con el rol enviado por el front
    #    Asumimos que en usuarios.cargo guardas "admin" o "analyst"
    cargo_normalizado = (user.cargo or "").strip().lower()

    if cargo_normalizado != body.role:
        # credenciales bien, pero el rol no coincide
        raise HTTPException(
            status_code=403,
            detail="Rol incorrecto para este usuario",
        )

    # 3) Crear token de acceso (incluimos el rol en el payload por si lo usas luego)
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    token = create_access_token(
        data={"sub": user.email, "role": body.role},
        expires_delta=access_token_expires,
    )

    # 4) Respuesta en el formato que espera tu front
    return LoginResponse(
        token=token,
        user=UserInfo(
            id=user.id_usuario,
            email=user.email,
            role=cargo_normalizado,  # "admin" o "analyst"
            name=user.nombre,
        ),
    )


@router.post("/register")
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un usuario con ese correo",
        )

    hashed = get_password_hash(user_in.password)

    user = db_models.Usuario(
        nombre=user_in.nombre,
        email=user_in.email,
        hashed_password=hashed,
        cargo=user_in.cargo,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id_usuario, "email": user.email}
