# app/db/models.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Enum,
    Text,
    ForeignKey,
    Numeric,
    func,
)
from sqlalchemy.dialects.mysql import INTEGER as MySQLInteger
from sqlalchemy.orm import relationship

from app.db.mysql_connection import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    cargo = Column(String(100), nullable=False)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    imagenes = relationship("Imagen", back_populates="usuario", cascade="all, delete-orphan")
    revisiones = relationship("Revision", back_populates="usuario", cascade="all, delete-orphan")
    cola_analisis = relationship(
        "ColaAnalisis", back_populates="usuario", cascade="all, delete-orphan"
    )
    panoramas = relationship(
        "ImagenPanorama", back_populates="usuario", cascade="all, delete-orphan"
    )
    videos = relationship(
        "AnalisisVideo", back_populates="usuario", cascade="all, delete-orphan"
    )


class Imagen(Base):
    __tablename__ = "imagenes"

    id_imagen = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(
        Integer,
        ForeignKey("usuarios.id_usuario", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    ruta_archivo = Column(String(255), nullable=False)
    tamano = Column(Integer, nullable=False)
    formato = Column(String(50), nullable=False)
    fecha_carga = Column(DateTime(timezone=True), server_default=func.now())
    estado = Column(
        Enum("pendiente", "procesada", "error", name="estado_imagen"),
        nullable=False,
        default="pendiente",
    )

    # Relaciones
    usuario = relationship("Usuario", back_populates="imagenes")
    clasificaciones = relationship(
        "Clasificacion", back_populates="imagen", cascade="all, delete-orphan"
    )
    notificaciones = relationship(
        "Notificacion", back_populates="imagen", cascade="all, delete-orphan"
    )


class Clasificacion(Base):
    __tablename__ = "clasificaciones"

    id_clasificacion = Column(Integer, primary_key=True, autoincrement=True)
    id_imagen = Column(
        Integer,
        ForeignKey("imagenes.id_imagen", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    resultado = Column(String(100), nullable=False)
    confianza = Column(Numeric(5, 4))  # DECIMAL(5,4)
    es_correcto = Column(Boolean)
    fecha_clasificacion = Column(DateTime(timezone=True), server_default=func.now())
    modelo_usado = Column(String(50), nullable=False, default="CNN")

    # Relaciones
    imagen = relationship("Imagen", back_populates="clasificaciones")
    reporte = relationship(
        "Reporte", back_populates="clasificacion", uselist=False, cascade="all, delete-orphan"
    )
    predicciones = relationship(
        "Prediccion", back_populates="clasificacion", cascade="all, delete-orphan"
    )
    notificaciones = relationship(
        "Notificacion", back_populates="clasificacion", cascade="all, delete-orphan"
    )


class Reporte(Base):
    __tablename__ = "reportes"

    id_reporte = Column(Integer, primary_key=True, autoincrement=True)
    id_clasificacion = Column(
        Integer,
        ForeignKey("clasificaciones.id_clasificacion", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        unique=True,
    )
    contenido = Column(Text, nullable=False)
    fecha_generacion = Column(DateTime(timezone=True), server_default=func.now())
    formato_reporte = Column(
        Enum("pdf", "html", "json", name="formato_reporte"),
        nullable=False,
        default="pdf",
    )

    # Relaciones
    clasificacion = relationship("Clasificacion", back_populates="reporte")
    errores = relationship("Error", back_populates="reporte", cascade="all, delete-orphan")
    revisiones = relationship("Revision", back_populates="reporte", cascade="all, delete-orphan")


class Error(Base):
    __tablename__ = "errores"

    id_error = Column(Integer, primary_key=True, autoincrement=True)
    id_reporte = Column(
        Integer,
        ForeignKey("reportes.id_reporte", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    descripcion = Column(Text, nullable=False)
    fecha_reporte = Column(DateTime(timezone=True), server_default=func.now())
    resuelto = Column(Boolean, nullable=False, default=False)

    reporte = relationship("Reporte", back_populates="errores")


class Revision(Base):
    __tablename__ = "revisiones"

    id_revision = Column(Integer, primary_key=True, autoincrement=True)
    id_reporte = Column(
        Integer,
        ForeignKey("reportes.id_reporte", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    id_usuario = Column(
        Integer,
        ForeignKey("usuarios.id_usuario", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    comentario = Column(Text)
    aprobado = Column(Boolean)
    fecha_revision = Column(DateTime(timezone=True), server_default=func.now())

    reporte = relationship("Reporte", back_populates="revisiones")
    usuario = relationship("Usuario", back_populates="revisiones")


class Notificacion(Base):
    __tablename__ = "notificaciones"

    id_notificacion = Column(Integer, primary_key=True, autoincrement=True)
    id_imagen = Column(
        Integer,
        ForeignKey("imagenes.id_imagen", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    id_clasificacion = Column(
        Integer,
        ForeignKey("clasificaciones.id_clasificacion", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
    )
    tipo = Column(
        Enum("formato_invalido", "fallo_clasificacion", "exito", name="tipo_notificacion"),
        nullable=False,
    )
    mensaje = Column(Text, nullable=False)
    fecha_notificacion = Column(DateTime(timezone=True), server_default=func.now())
    enviada = Column(Boolean, nullable=False, default=False)

    imagen = relationship("Imagen", back_populates="notificaciones")
    clasificacion = relationship("Clasificacion", back_populates="notificaciones")


class Prediccion(Base):
    __tablename__ = "predicciones"

    id_prediccion = Column(Integer, primary_key=True, autoincrement=True)
    id_clasificacion = Column(
        Integer,
        ForeignKey("clasificaciones.id_clasificacion", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    resultado_en_base_datos = Column(String(100), nullable=False)
    fecha_almacenamiento = Column(DateTime(timezone=True), server_default=func.now())

    clasificacion = relationship("Clasificacion", back_populates="predicciones")


class ColaAnalisis(Base):
    __tablename__ = "cola_analisis"

    id_cola = Column(MySQLInteger(unsigned=True), primary_key=True, autoincrement=True)
    id_usuario = Column(
        MySQLInteger(unsigned=True),
        ForeignKey("usuarios.id_usuario", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    ruta_archivo = Column(String(255), nullable=False)
    tamano = Column(Integer, nullable=False)
    formato = Column(String(50), nullable=False)
    metadata_json = Column(Text, nullable=False)
    modelo_id = Column(String(50), nullable=False, default="copper")
    estado = Column(
        Enum("pendiente", "procesando", "completado", "error", name="estado_cola"),
        nullable=False,
        default="pendiente",
    )
    error = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_procesamiento = Column(DateTime(timezone=True), nullable=True)

    usuario = relationship("Usuario", back_populates="cola_analisis")


class ImagenPanorama(Base):
    __tablename__ = "imagenes_panorama"

    id_panorama = Column(MySQLInteger(unsigned=True), primary_key=True, autoincrement=True)
    id_usuario = Column(
        MySQLInteger(unsigned=True),
        ForeignKey("usuarios.id_usuario", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    ruta_archivo = Column(String(255), nullable=False)
    ancho_original = Column(Integer, nullable=False)
    alto_original = Column(Integer, nullable=False)
    patch_size = Column(Integer, nullable=False, default=224)
    overlap = Column(Integer, nullable=False, default=32)
    total_patches = Column(Integer, nullable=False, default=0)
    fecha_carga = Column(DateTime(timezone=True), server_default=func.now())

    usuario = relationship("Usuario", back_populates="panoramas")
    parches = relationship(
        "ParchePanorama", back_populates="panorama", cascade="all, delete-orphan"
    )


class ParchePanorama(Base):
    __tablename__ = "parches_panorama"

    id_parche = Column(MySQLInteger(unsigned=True), primary_key=True, autoincrement=True)
    id_panorama = Column(
        MySQLInteger(unsigned=True),
        ForeignKey("imagenes_panorama.id_panorama", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    ruta_parche = Column(String(255), nullable=False)
    x_min = Column(Integer, nullable=False)
    y_min = Column(Integer, nullable=False)
    x_max = Column(Integer, nullable=False)
    y_max = Column(Integer, nullable=False)
    fila = Column(Integer, nullable=False, default=0)
    columna = Column(Integer, nullable=False, default=0)

    panorama = relationship("ImagenPanorama", back_populates="parches")


class AnalisisVideo(Base):
    __tablename__ = "analisis_video"

    id_video = Column(MySQLInteger(unsigned=True), primary_key=True, autoincrement=True)
    id_usuario = Column(
        MySQLInteger(unsigned=True),
        ForeignKey("usuarios.id_usuario", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    nombre_archivo = Column(String(255), nullable=False)
    ruta_video = Column(String(255), nullable=False)
    duracion_segundos = Column(Integer, nullable=False, default=0)
    total_frames_analizados = Column(Integer, nullable=False, default=0)
    total_hallazgos = Column(Integer, nullable=False, default=0)
    reporte_json = Column(Text, nullable=False)
    ruta_pdf = Column(String(255), nullable=True)
    fecha_analisis = Column(DateTime(timezone=True), server_default=func.now())

    usuario = relationship("Usuario", back_populates="videos")
