# test_usuarios.py
from app.db.mysql_connection import SessionLocal
from app.db import models
from app.core.security import get_password_hash  

def main():
    db = SessionLocal()

    # 1) crear hash de una contraseña de prueba
    password_plano = "123456"
    hashed = get_password_hash(password_plano)
    print("Hash generado:", hashed)

    # 2) crear un usuario nuevo
    nuevo = models.Usuario(
        nombre="Usuario Prueba1",
        email="prueba1@example.com",
        hashed_password=hashed,
        cargo="admin",
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    print("Usuario creado con id:", nuevo.id_usuario)

    db.close()

if __name__ == "__main__":
    main()
