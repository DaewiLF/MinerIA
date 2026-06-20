#!/usr/bin/env python3
"""
Script para crear usuarios de prueba en la BD de MinerIA.
Ejecutar dentro del container backend o con acceso a la BD.
"""

import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

# Configurar contexto de hashing igual que en el backend
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Datos de conexión
DB_USER = "root"
DB_PASSWORD = "root_password"
DB_HOST = "db"  # nombre del servicio en docker-compose
DB_PORT = 3306
DB_NAME = "proyecto_integracion"

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Importar modelos (mismo que en el backend)
from app.db.models import Usuario

# Crear engine
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)

def create_users():
    """Crear dos usuarios: admin y analista."""
    db = Session()
    
    try:
        # 1. Admin
        admin_email = "admin2@gmail.com"
        admin_password = "Patito123$$"
        admin_hash = pwd_context.hash(admin_password)
        
        # Verificar si ya existe
        existing_admin = db.query(Usuario).filter(Usuario.email == admin_email).first()
        if existing_admin:
            print(f"⚠️  Usuario {admin_email} ya existe. Omitiendo.")
        else:
            admin = Usuario(
                nombre="Admin User",
                email=admin_email,
                hashed_password=admin_hash,
                cargo="admin"
            )
            db.add(admin)
            print(f"✅ Usuario Admin creado: {admin_email}")
        
        # 2. Analista
        analyst_email = "analista2@gmail.com"
        analyst_password = "Patito123$$"
        analyst_hash = pwd_context.hash(analyst_password)
        
        existing_analyst = db.query(Usuario).filter(Usuario.email == analyst_email).first()
        if existing_analyst:
            print(f"⚠️  Usuario {analyst_email} ya existe. Omitiendo.")
        else:
            analyst = Usuario(
                nombre="Analyst User",
                email=analyst_email,
                hashed_password=analyst_hash,
                cargo="analyst"
            )
            db.add(analyst)
            print(f"✅ Usuario Analista creado: {analyst_email}")
        
        # Commit
        db.commit()
        print("\n✅ Usuarios guardados en la BD correctamente.")
        print(f"\nCredenciales:")
        print(f"  Admin: {admin_email} / Patito123$$")
        print(f"  Analista: {analyst_email} / Patito123$$")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    create_users()
