"""
Generador de Informe Técnico de Análisis Mineral - MinerIA
=============================================================

Estructura basada en las prácticas exigidas en Chile para informes técnicos
geológicos/mineros, considerando:

  - Ley N°20.235 y Reglamento (Código CH 20235 / Comisión Minera): exige
    identificación del profesional responsable ("Persona Competente"),
    su N° de registro/certificado de vigencia, y declaración de
    veracidad de la información.
  - Sernageomin (Asistencia Técnica Geológica / Art. 21 Código de Minería):
    exige trazabilidad de la información, metodología empleada, y una
    declaración jurada de que la información es completa, consistente
    y veraz. Sernageomin actúa como ente revisor, por lo que el informe
    debe poder sostenerse técnicamente por sí solo.
  - Estándares internacionales de reporte (JORC/CRIRSCO, en los que se
    basa el Código chileno): exigen identificación de la muestra,
    ubicación geográfica (coordenadas + datum), método de muestreo,
    método analítico/laboratorio, QA/QC, e incertidumbres/limitaciones.

IMPORTANTE: Un resumen generado por IA NO constituye un dictamen
profesional. Por eso el informe distingue explícitamente entre:
  (a) datos analíticos crudos (trazables al laboratorio/base de datos),
  (b) interpretación asistida por IA (apoyo, no vinculante), y
  (c) la validación final, que debe quedar firmada por un geólogo u otro
      profesional competente antes de tener valor ante terceros
      (Sernageomin, Ministerio de Minería, auditorías, etc.).
"""

import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether,
)

from reportlab.platypus import Image as RLImage

# ---------------------------------------------------------------------------
# Paleta y estilos
# ---------------------------------------------------------------------------

COLOR_PRIMARY = colors.HexColor("#1F3864")     # azul institucional
COLOR_ACCENT = colors.HexColor("#B7791F")      # ocre/cobre, guiño minero
COLOR_GREY = colors.HexColor("#5A5A5A")
COLOR_LIGHT_BG = colors.HexColor("#F2F2F2")
COLOR_WARN_BG = colors.HexColor("#FFF4E5")
COLOR_WARN_BORDER = colors.HexColor("#B7791F")

PAGE_W, PAGE_H = A4
MARGIN = 2 * cm

styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    name="ReportTitle", fontName="Helvetica-Bold", fontSize=16,
    textColor=COLOR_PRIMARY, leading=20, spaceAfter=2,
))
styles.add(ParagraphStyle(
    name="ReportSubtitle", fontName="Helvetica", fontSize=9.5,
    textColor=COLOR_GREY, leading=12,
))
styles.add(ParagraphStyle(
    name="SectionHeader", fontName="Helvetica-Bold", fontSize=11.5,
    textColor=colors.white, leading=14, leftIndent=6, spaceBefore=0, spaceAfter=0,
))
styles.add(ParagraphStyle(
    name="SubHeader", fontName="Helvetica-Bold", fontSize=10,
    textColor=COLOR_PRIMARY, leading=13, spaceBefore=4, spaceAfter=4,
))
styles.add(ParagraphStyle(
    name="BodyJustified", fontName="Helvetica", fontSize=9.5,
    leading=13.5, alignment=TA_JUSTIFY, spaceAfter=4,
))
styles.add(ParagraphStyle(
    name="BodySmall", fontName="Helvetica", fontSize=8.5,
    textColor=COLOR_GREY, leading=11,
))
styles.add(ParagraphStyle(
    name="WarnText", fontName="Helvetica-Oblique", fontSize=8.5,
    textColor=colors.HexColor("#7A4A00"), leading=11.5,
))
styles.add(ParagraphStyle(
    name="FieldLabel", fontName="Helvetica-Bold", fontSize=8.5,
    textColor=COLOR_GREY,
))
styles.add(ParagraphStyle(
    name="FieldValue", fontName="Helvetica", fontSize=9.5,
    textColor=colors.black,
))
styles.add(ParagraphStyle(
    name="TableCell", fontName="Helvetica", fontSize=8.5, leading=11,
))
styles.add(ParagraphStyle(
    name="TableHeaderCell", fontName="Helvetica-Bold", fontSize=8.5,
    textColor=colors.white, leading=11,
))
styles.add(ParagraphStyle(
    name="SignatureLabel", fontName="Helvetica", fontSize=8.5,
    textColor=COLOR_GREY,
))


def _section_header(title: str) -> Table:
    """Barra de encabezado de sección con fondo de color."""
    t = Table([[Paragraph(title, styles["SectionHeader"])]],
               colWidths=[PAGE_W - 2 * MARGIN])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), COLOR_PRIMARY),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def _field_row(pairs: List[tuple]) -> Table:
    """Fila de campos tipo etiqueta/valor distribuidos en columnas."""
    n = len(pairs)
    col_w = (PAGE_W - 2 * MARGIN) / n
    data = [
        [Paragraph(label, styles["FieldLabel"]) for label, _ in pairs],
        [Paragraph(str(value) if value not in (None, "") else "—", styles["FieldValue"]) for _, value in pairs],
    ]
    t = Table(data, colWidths=[col_w] * n)
    t.setStyle(TableStyle([
        ("BOTTOMPADDING", (0, 0), (-1, 0), 1),
        ("TOPPADDING", (0, 1), (-1, 1), 0),
        ("BOTTOMPADDING", (0, 1), (-1, 1), 6),
        ("LINEBELOW", (0, 1), (-1, 1), 0.5, colors.HexColor("#D9D9D9")),
        ("BOTTOMPADDING", (0, 1), (-1, 1), 6),
    ]))
    return t


def _risk_badge_color(risk: str) -> colors.Color:
    risk = (risk or "").strip().lower()
    if risk in ("alto", "alta", "high"):
        return colors.HexColor("#C0392B")
    if risk in ("medio", "media", "moderado", "medium"):
        return colors.HexColor("#B7791F")
    if risk in ("bajo", "baja", "low"):
        return colors.HexColor("#1E7B45")
    return COLOR_GREY


# =============================================================================
# ANEXO FOTOGRÁFICO (SECCIÓN COMENTADA - NO AFECTA LA EJECUCIÓN ACTUAL)
# =============================================================================
#
# Sernageomin, en sus guías de contenidos mínimos (p.ej. informe hidrogeológico,
# estudios de peligros geológicos/remociones en masa), exige de forma constante
# un ANEXO FOTOGRÁFICO como evidencia de terreno. El patrón se repite en todas
# las guías oficiales revisadas, aunque no exista una norma única para
# "informes de análisis mineral asistidos por IA":
#
#   1. Fotografía asociada a un punto/muestra específico (no fotos genéricas):
#      debe poder vincularse a un ID de muestra o sondaje y a coordenadas.
#   2. Metadatos mínimos visibles en el documento (no solo en el EXIF del
#      archivo): fecha de captura, coordenadas del punto, y descripción de
#      lo que se observa (litología, alteración, estructura, etc.).
#   3. Resolución mínima legible: Sernageomin publica su propio material
#      gráfico en JPG a 300 dpi; ese es el estándar razonable a exigir
#      también en informes de terceros para que la imagen sea válida en
#      una impresión o revisión técnica (evitar capturas de pantalla o
#      fotos muy comprimidas).
#   4. Formato de archivo: JPG o PNG. Evitar HEIC/WEBP sin convertir, ya
#      que no siempre son legibles por los revisores.
#   5. Escala o referencia de tamaño en la foto cuando sea relevante
#      (ej. chaqueta, moneda, escalímetro) — práctica estándar en
#      fotografía geológica de afloramientos/testigos, aunque no siempre
#      sea exigida explícitamente por Sernageomin.
#   6. Orientación/encuadre: idealmente con referencia de norte u
#      orientación cuando se fotografía un afloramiento o frente de
#      excavación.
#
# Estos puntos están pensados como CHECKLIST a validar antes de incrustar
# cada imagen, no como un filtro automático obligatorio. El filtro de
# "calidad/resolución mínima" sí se puede automatizar (ver función de
# validación más abajo); lo que NO se puede automatizar completamente es el
# criterio geológico de qué fotografiar (eso lo decide el profesional).
#
# -----------------------------------------------------------------------------
# Estructura de datos esperada en el payload (ejemplo):
#
#   payload["photos"] = [
#       {
#           "path": "/ruta/a/foto_sondaje_456_1.jpg",
#           "caption": "Testigo SND-0456, tramo 12.0-14.5 m. Vetilla de óxidos de Cu.",
#           "sampleId": "SND-0456",
#           "coordinates": "345.210 E / 6.789.430 N",
#           "date": "2026-06-18",
#       },
#       ...
#   ]
#
# -----------------------------------------------------------------------------
#
# def _validate_image_for_report(image_path: str, min_dpi: int = 150,
#                                 min_width_px: int = 800,
#                                 max_size_mb: float = 15.0) -> Optional[str]:
#     """
#     Valida que una imagen cumpla con criterios mínimos razonables antes de
#     incrustarla en el informe. Devuelve None si está OK, o un string con el
#     motivo de rechazo/advertencia si no cumple.
#
#     Criterios (ver justificación en el bloque de comentarios superior):
#       - Formato JPG o PNG (Sernageomin publica su material gráfico en JPG).
#       - Resolución mínima en píxeles (para que no se vea pixelada en A4).
#       - DPI informado en el propio archivo, si está disponible.
#       - Tamaño de archivo razonable (evitar archivos RAW sin comprimir).
#     """
#     ext = os.path.splitext(image_path)[1].lower()
#     if ext not in (".jpg", ".jpeg", ".png"):
#         return f"Formato no admitido ({ext}). Usar JPG o PNG."
#
#     try:
#         with PILImage.open(image_path) as img:
#             width, height = img.size
#             dpi = img.info.get("dpi", (72, 72))[0]
#     except Exception as exc:
#         return f"No se pudo leer la imagen: {exc}"
#
#     if width < min_width_px and height < min_width_px:
#         return (f"Resolución muy baja ({width}x{height}px). "
#                 f"Se recomienda mínimo {min_width_px}px en el lado menor.")
#
#     if dpi and dpi < min_dpi:
#         return f"DPI informado bajo ({dpi}). Se recomienda ≥{min_dpi} dpi."
#
#     size_mb = os.path.getsize(image_path) / (1024 * 1024)
#     if size_mb > max_size_mb:
#         return f"Archivo muy pesado ({size_mb:.1f} MB). Comprimir antes de incrustar."
#
#     return None
#
#
# def _extract_image_gps(image_path: str) -> Optional[str]:
#     """
#     Intenta extraer coordenadas GPS desde el EXIF de la foto (si la cámara o
#     el teléfono las guardó). Sirve para contrastar contra las coordenadas
#     declaradas manualmente en el payload y detectar inconsistencias antes
#     de que el geólogo valide el informe.
#
#     Devuelve un string "lat, lon" o None si no hay datos GPS en el EXIF.
#     """
#     try:
#         with PILImage.open(image_path) as img:
#             exif_raw = img._getexif()
#             if not exif_raw:
#                 return None
#             exif = {ExifTags.TAGS.get(k, k): v for k, v in exif_raw.items()}
#             gps_info = exif.get("GPSInfo")
#             if not gps_info:
#                 return None
#             # Conversión completa de GPSInfo (grados/min/seg -> decimal)
#             # omitida aquí por brevedad; implementar si se necesita
#             # contrastar automáticamente contra las coordenadas declaradas.
#             return None
#     except Exception:
#         return None
#
#
# def _build_photo_annex(photos: List[Dict[str, Any]]) -> list:
#     """
#     Construye los flowables del Anexo Fotográfico, con 1-2 fotos por fila,
#     cada una con su pie de foto (caption) indicando ID de muestra,
#     coordenadas y fecha, conforme al criterio de trazabilidad exigido por
#     Sernageomin.
#     """
#     story = []
#     story.append(_section_header("6. Anexo Fotográfico"))
#     story.append(Spacer(1, 8))
#
#     if not photos:
#         story.append(Paragraph(
#             "No se adjuntaron fotografías de respaldo para este análisis. "
#             "Se recomienda incorporar evidencia fotográfica del punto de "
#             "muestreo antes de la validación profesional del informe.",
#             styles["BodyJustified"],
#         ))
#         return story
#
#     max_img_width = (PAGE_W - 2 * MARGIN - 0.5 * cm) / 2  # 2 columnas
#
#     for photo in photos:
#         path = photo.get("path")
#         if not path or not os.path.exists(path):
#             continue
#
#         warning = _validate_image_for_report(path)
#         if warning:
#             # No se descarta la imagen por una advertencia de calidad; se
#             # incrusta igual pero se anota la observación para que el
#             # profesional que valida el informe decida si es aceptable.
#             pass
#
#         img_flowable = RLImage(path, width=max_img_width,
#                                 height=max_img_width * 0.75)  # ratio 4:3
#
#         caption_parts = [photo.get("caption", "Sin descripción.")]
#         meta_bits = []
#         if photo.get("sampleId"):
#             meta_bits.append(f"Muestra: {photo['sampleId']}")
#         if photo.get("coordinates"):
#             meta_bits.append(f"Coord.: {photo['coordinates']}")
#         if photo.get("date"):
#             meta_bits.append(f"Fecha: {photo['date']}")
#         if meta_bits:
#             caption_parts.append(" | ".join(meta_bits))
#         if warning:
#             caption_parts.append(f"⚠ {warning}")
#
#         caption = Paragraph("<br/>".join(caption_parts), styles["BodySmall"])
#
#         story.append(KeepTogether([img_flowable, Spacer(1, 3), caption, Spacer(1, 10)]))
#
#     return story
#
#
# Uso dentro de _build_story(payload):
#
#     # ---------------- Bloque 6: Anexo fotográfico ----------------
#     # photos = payload.get("photos", [])
#     # story.extend(_build_photo_annex(photos))
#
# =============================================================================
# FIN ANEXO FOTOGRÁFICO (SECCIÓN COMENTADA)
# =============================================================================


# ---------------------------------------------------------------------------
# Documento con header/footer fijos (numeración de página, etc.)
# ---------------------------------------------------------------------------

class _ReportDocTemplate(BaseDocTemplate):
    """DocTemplate que dibuja encabezado y pie de página en cada hoja."""

    def __init__(self, filename, payload: Dict[str, Any], **kwargs):
        super().__init__(filename, pagesize=A4, **kwargs)
        self.payload = payload
        frame = Frame(
            MARGIN, MARGIN + 1.1 * cm,
            PAGE_W - 2 * MARGIN, PAGE_H - 2 * MARGIN - 2.6 * cm,
            id="normal",
        )
        template = PageTemplate(id="main", frames=[frame], onPage=self._draw_static)
        self.addPageTemplates([template])

    def _draw_static(self, canvas_obj, doc):
        canvas_obj.saveState()
        payload = self.payload

        # --- Encabezado fijo ---
        top = PAGE_H - 1.3 * cm
        canvas_obj.setFillColor(COLOR_PRIMARY)
        canvas_obj.rect(0, PAGE_H - 0.25 * cm, PAGE_W, 0.25 * cm, stroke=0, fill=1)

        canvas_obj.setFont("Helvetica-Bold", 13)
        canvas_obj.setFillColor(COLOR_PRIMARY)
        canvas_obj.drawString(MARGIN, top, "MinerIA")

        canvas_obj.setFont("Helvetica", 9)
        canvas_obj.setFillColor(COLOR_GREY)
        canvas_obj.drawString(MARGIN + 2.1 * cm, top, "Informe Técnico de Análisis Mineral")

        report_code = payload.get("reportCode") or payload.get("id") or "S/N"
        canvas_obj.setFont("Helvetica", 8.5)
        canvas_obj.drawRightString(PAGE_W - MARGIN, top, f"Código de informe: {report_code}")

        canvas_obj.setStrokeColor(colors.HexColor("#D9D9D9"))
        canvas_obj.setLineWidth(0.5)
        canvas_obj.line(MARGIN, top - 0.35 * cm, PAGE_W - MARGIN, top - 0.35 * cm)

        # --- Pie de página fijo ---
        footer_y = MARGIN - 0.6 * cm
        canvas_obj.setStrokeColor(colors.HexColor("#D9D9D9"))
        canvas_obj.line(MARGIN, footer_y + 0.4 * cm, PAGE_W - MARGIN, footer_y + 0.4 * cm)

        canvas_obj.setFont("Helvetica", 7.5)
        canvas_obj.setFillColor(COLOR_GREY)
        generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        canvas_obj.drawString(
            MARGIN, footer_y + 0.18 * cm,
            f"Generado automáticamente por MinerIA el {generated_at}.",
        )
        canvas_obj.drawString(
            MARGIN, footer_y - 0.18 * cm,
            "Documento de apoyo técnico: requiere validación y firma de profesional competente.",
        )
        canvas_obj.drawRightString(PAGE_W - MARGIN, footer_y, f"Página {doc.page}")

        canvas_obj.restoreState()


# ---------------------------------------------------------------------------
# Construcción del contenido (story)
# ---------------------------------------------------------------------------

def _build_story(payload: Dict[str, Any]) -> list:
    story = []

    # ---------------- Bloque 1: Identificación general ----------------
    story.append(Paragraph("Identificación General del Análisis", styles["ReportTitle"]))
    story.append(Paragraph(
        "Reporte generado a partir de datos de la plataforma MinerIA. "
        "La trazabilidad de cada campo se referencia a la base de datos de origen.",
        styles["ReportSubtitle"],
    ))
    story.append(Spacer(1, 8))

    meta = payload.get("metadata", {}) or {}
    coordinates_val = payload.get("coordinates") or meta.get("coordinates", "")
    responsible_val = payload.get("responsible") or meta.get("responsible", "")
    personnel_val = payload.get("personnel") or meta.get("personnel", "")

    story.append(_field_row([
        ("FECHA DE ANÁLISIS", payload.get("date", "")),
        ("ZONA / FAENA", payload.get("zone", "")),
        ("CATEGORÍA", payload.get("category", "")),
    ]))
    story.append(_field_row([
        ("ID DE MUESTRA / SONDAJE", payload.get("sampleId", "")),
        ("COORDENADAS (UTM)", coordinates_val),
        ("DATUM / HUSO", payload.get("datum", "WGS84 / Huso 19S")),
    ]))
    story.append(_field_row([
        ("MÉTODO DE MUESTREO", payload.get("samplingMethod", "")),
        ("LABORATORIO / MÉTODO ANALÍTICO", payload.get("analyticalMethod", "")),
        ("ESTADO DEL ANÁLISIS", payload.get("status", "")),
    ]))
    story.append(_field_row([
        ("RESPONSABLE", responsible_val),
        ("PERSONAL INVOLUCRADO", personnel_val),
        ("", ""),
    ]))

    story.append(Spacer(1, 10))

    # ---------------- Bloque 2: Resultados analíticos ----------------
    story.append(_section_header("1. Resultados Analíticos"))
    story.append(Spacer(1, 8))

    risk = payload.get("riskLevel", "")
    risk_color = _risk_badge_color(risk)

    results_data = [
        [Paragraph("Parámetro", styles["TableHeaderCell"]),
         Paragraph("Valor", styles["TableHeaderCell"]),
         Paragraph("Unidad", styles["TableHeaderCell"]),
         Paragraph("Observación", styles["TableHeaderCell"])],
        [Paragraph("Ley de cobre (Cu)", styles["TableCell"]),
         Paragraph(str(payload.get("copperGrade", "—")), styles["TableCell"]),
         Paragraph(payload.get("copperGradeUnit", "%"), styles["TableCell"]),
         Paragraph(payload.get("copperGradeNote", "—"), styles["TableCell"])],
        [Paragraph("Nivel de riesgo geológico", styles["TableCell"]),
         Paragraph(str(risk) or "—", styles["TableCell"]),
         Paragraph("—", styles["TableCell"]),
         Paragraph(payload.get("riskNote", "—"), styles["TableCell"])],
    ]

    # Permite agregar parámetros adicionales si vienen en el payload
    for extra in payload.get("additionalParameters", []):
        results_data.append([
            Paragraph(str(extra.get("name", "—")), styles["TableCell"]),
            Paragraph(str(extra.get("value", "—")), styles["TableCell"]),
            Paragraph(str(extra.get("unit", "—")), styles["TableCell"]),
            Paragraph(str(extra.get("note", "—")), styles["TableCell"]),
        ])

    col_widths = [5.5 * cm, 3.0 * cm, 2.5 * cm, None]
    col_widths[-1] = (PAGE_W - 2 * MARGIN) - sum(w for w in col_widths if w)
    results_table = Table(results_data, colWidths=col_widths, repeatRows=1)
    results_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), COLOR_PRIMARY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, COLOR_LIGHT_BG]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CCCCCC")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("TEXTCOLOR", (1, 2), (1, 2), risk_color),
        ("FONTNAME", (1, 2), (1, 2), "Helvetica-Bold"),
    ]))
    story.append(results_table)
    story.append(Spacer(1, 12))

    # ---------------- Bloque 3: Resumen interpretativo (IA) ----------------
    story.append(_section_header("2. Resumen Interpretativo (Generado por IA)"))
    story.append(Spacer(1, 8))

    ai_warning = Table([[Paragraph(
        "Este resumen fue generado automáticamente por el módulo de inteligencia "
        "artificial de MinerIA a partir de los datos analíticos anteriores. "
        "<b>No constituye un dictamen profesional</b> y no reemplaza la evaluación "
        "de un geólogo u otro profesional competente. Debe ser revisado y validado "
        "antes de ser utilizado como respaldo técnico ante terceros.",
        styles["WarnText"],
    )]], colWidths=[PAGE_W - 2 * MARGIN])
    ai_warning.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), COLOR_WARN_BG),
        ("BOX", (0, 0), (-1, -1), 0.6, COLOR_WARN_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(ai_warning)
    story.append(Spacer(1, 8))

    ai_summary = payload.get("aiSummary", "") or "Sin resumen disponible."
    story.append(Paragraph(ai_summary, styles["BodyJustified"]))
    story.append(Spacer(1, 10))

    # ---------------- Bloque 4: Recomendaciones ----------------
    story.append(_section_header("3. Recomendaciones"))
    story.append(Spacer(1, 8))

    recs = payload.get("recommendations", [])
    if recs:
        rec_items = [
            Paragraph(f"{i+1}. {rec}", styles["BodyJustified"])
            for i, rec in enumerate(recs)
        ]
        story.extend(rec_items)
    else:
        story.append(Paragraph("No se registraron recomendaciones para este análisis.", styles["BodyJustified"]))
    story.append(Spacer(1, 10))

    # ---------------- Bloque 5: QA/QC y limitaciones ----------------
    story.append(_section_header("4. Control de Calidad (QA/QC) y Limitaciones"))
    story.append(Spacer(1, 8))

    qaqc_text = payload.get("qaqcNotes") or (
        "No se registran protocolos de control de calidad (duplicados, blancos, "
        "estándares de referencia) asociados a este análisis. Se recomienda "
        "incorporar dicha información antes de la validación final del informe."
    )
    story.append(Paragraph(qaqc_text, styles["BodyJustified"]))

    limitations_text = payload.get("limitations") or (
        "Los resultados presentados corresponden a una muestra puntual y a un "
        "método analítico específico; no deben extrapolarse a la totalidad del "
        "cuerpo mineralizado sin un muestreo estadísticamente representativo. "
        "La clasificación de recursos/reservas, si corresponde, debe ser "
        "efectuada conforme al Código CH 20235 por una Persona Competente."
    )
    story.append(Paragraph(f"<b>Limitaciones:</b> {limitations_text}", styles["BodyJustified"]))
    story.append(Spacer(1, 14))

    # ---------------- Bloque 6: Mapa de calor Grad-CAM ----------------
    gradcam_url = payload.get("gradcamUrl")
    if gradcam_url:
        gradcam_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            gradcam_url.lstrip("/"),
        )
        if os.path.exists(gradcam_path):
            story.append(_section_header("5. Mapa de Activacion (Grad-CAM)"))
            story.append(Spacer(1, 8))
            story.append(Paragraph(
                "Mapa de calor generado por Grad-CAM que resalta las regiones de la "
                "imagen que mas influyeron en la decision del modelo de IA. "
                "Las areas en rojo/amarillo indican mayor activacion para la clase predicha.",
                styles["BodyJustified"],
            ))
            story.append(Spacer(1, 6))

            max_img_width = PAGE_W - 2 * MARGIN
            try:
                img = RLImage(gradcam_path, width=max_img_width, height=max_img_width * 0.75)
                story.append(img)
            except Exception:
                story.append(Paragraph(
                    "No se pudo incrustar el mapa de calor en el informe.",
                    styles["BodySmall"],
                ))
            story.append(Spacer(1, 14))

    # ---------------- Bloque 7: Declaración y firma profesional ----------------
    story.append(_section_header("6. Declaración y Validación Profesional"))
    story.append(Spacer(1, 8))

    declaration_text = (
        "Declaro que la información técnica contenida en este informe es, según "
        "mi conocimiento, completa, consistente y veraz, y que ha sido revisada "
        "conforme a las prácticas profesionales aplicables en geología y minería "
        "en Chile."
    )
    story.append(Paragraph(declaration_text, styles["BodyJustified"]))
    story.append(Spacer(1, 14))

    signer_name = payload.get("reviewerName", "")
    signer_title = payload.get("reviewerTitle", "Geólogo(a) / Profesional Competente")
    signer_reg = payload.get("reviewerRegistration", "")

    sig_table = Table([
        [Paragraph("_" * 38, styles["SignatureLabel"]),
         Paragraph("_" * 38, styles["SignatureLabel"])],
        [Paragraph(f"<b>Nombre:</b> {signer_name or '____________________'}", styles["SignatureLabel"]),
         Paragraph(f"<b>Fecha de validación:</b> {payload.get('validationDate', '____________________')}", styles["SignatureLabel"])],
        [Paragraph(f"<b>Cargo / Especialidad:</b> {signer_title}", styles["SignatureLabel"]),
         Paragraph(f"<b>N° Registro / Comisión Minera:</b> {signer_reg or '____________________'}", styles["SignatureLabel"])],
    ], colWidths=[(PAGE_W - 2 * MARGIN) / 2] * 2)
    sig_table.setStyle(TableStyle([
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(sig_table)

    return story


def generate_pdf_report(payload: Dict[str, Any], output_path: str) -> None:
    """
    Genera un PDF con estructura profesional para un análisis mineral.

    payload viene del detalle (AnalysisDetail) e idealmente incluye, además
    de los campos originales (date, zone, category, riskLevel, copperGrade,
    status, aiSummary, recommendations), los siguientes campos opcionales
    para reforzar trazabilidad y validez técnica:

        reportCode, sampleId, coordinates, datum, samplingMethod,
        analyticalMethod, copperGradeUnit, copperGradeNote, riskNote,
        additionalParameters (lista de dicts: name, value, unit, note),
        qaqcNotes, limitations,
        reviewerName, reviewerTitle, reviewerRegistration, validationDate

    Todos estos campos son opcionales: si no vienen en el payload, el
    informe se genera igual, mostrando los espacios correspondientes en
    blanco para ser completados en la validación profesional.
    """
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    doc = _ReportDocTemplate(
        output_path,
        payload,
        topMargin=MARGIN + 1.0 * cm,
        bottomMargin=MARGIN + 0.6 * cm,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
    )
    story = _build_story(payload)
    doc.build(story)


# =============================================================================
# Generador de PDF para análisis de video (línea temporal + Grad-CAM)
# =============================================================================


def _build_video_story(payload: Dict[str, Any]) -> list:
    """Construye los flowables del PDF de análisis de video."""
    story = []

    # Título
    story.append(Paragraph("Informe de Análisis de Video - MinerIA", styles["ReportTitle"]))
    story.append(Paragraph(
        "Línea temporal de predicciones generadas por el modelo de IA, "
        "con mapa de activación Grad-CAM para cada hallazgo positivo.",
        styles["ReportSubtitle"],
    ))
    story.append(Spacer(1, 8))

    # Metadatos del video
    story.append(_section_header("1. Identificación del Video"))
    story.append(Spacer(1, 6))
    story.append(_field_row([
        ("ARCHIVO", payload.get("filename", "—")),
        ("DURACIÓN", f"{payload.get('duracion_total_segundos', 0)} s"),
        ("HALLAZGOS POSITIVOS", str(payload.get("total_hallazgos", 0))),
    ]))
    story.append(Spacer(1, 12))

    # Línea temporal
    timeline = payload.get("timeline", [])
    story.append(_section_header("2. Línea Temporal de Predicciones"))
    story.append(Spacer(1, 6))

    if not timeline:
        story.append(Paragraph("No se generaron datos de línea temporal.", styles["BodyJustified"]))
    else:
        header = [
            Paragraph("Segundo", styles["TableHeaderCell"]),
            Paragraph("Tiempo", styles["TableHeaderCell"]),
            Paragraph("Predicción", styles["TableHeaderCell"]),
            Paragraph("Confianza", styles["TableHeaderCell"]),
        ]
        rows = [header]
        for entry in timeline:
            clase = entry.get("prediccion", "—")
            conf = entry.get("confianza", 0)
            badge = "con_cobre"
            if clase == "con_cobre" and conf > 60.0:
                badge = "con_cobre"
            else:
                badge = "sin_cobre"
            rows.append([
                Paragraph(str(entry.get("segundo", "—")), styles["TableCell"]),
                Paragraph(entry.get("timestamp", "—"), styles["TableCell"]),
                Paragraph(clase, styles["TableCell"]),
                Paragraph(f"{conf:.2f}%", styles["TableCell"]),
            ])

        col_widths = [2.5 * cm, 2.5 * cm, None, 3.0 * cm]
        col_widths[2] = (PAGE_W - 2 * MARGIN) - sum(w for w in col_widths if w)
        timeline_table = Table(rows, colWidths=col_widths, repeatRows=1)
        timeline_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), COLOR_PRIMARY),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, COLOR_LIGHT_BG]),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CCCCCC")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(timeline_table)

    story.append(Spacer(1, 14))

    # Grad-CAM gallery: solo para hallazgos positivos (top 20 por confianza)
    hallazgos = sorted(
        payload.get("hallazgos", []),
        key=lambda h: h.get("confianza", 0),
        reverse=True,
    )[:20]
    if hallazgos:
        story.append(_section_header("3. Mapa de Activación (Grad-CAM) — Hallazgos Positivos"))
        story.append(Spacer(1, 6))
        story.append(Paragraph(
            "Mapas de calor generados por Grad-CAM que resaltan las regiones "
            "que más influyeron en la decisión del modelo. Se muestran hasta "
            "los 20 hallazgos con mayor confianza.",
            styles["BodyJustified"],
        ))
        story.append(Spacer(1, 6))

        max_img_w = (PAGE_W - 2 * MARGIN - 0.5 * cm) / 2  # 2 columnas
        for i in range(0, len(hallazgos), 2):
            row_cells = []
            for j in range(2):
                idx = i + j
                if idx >= len(hallazgos):
                    row_cells.append(Paragraph("", styles["BodySmall"]))
                    break
                h = hallazgos[idx]
                gradcam_url = h.get("gradcam_url")
                cell_content = []
                if gradcam_url:
                    gradcam_path = os.path.join(
                        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
                        gradcam_url.lstrip("/"),
                    )
                    if os.path.exists(gradcam_path):
                        try:
                            img = RLImage(gradcam_path, width=max_img_w, height=max_img_w * 0.75)
                            cell_content.append(img)
                        except Exception:
                            pass
                cell_content.append(Spacer(1, 2))
                cell_content.append(Paragraph(
                    f"Seg. {h.get('segundo', '—')} — "
                    f"Confianza: {h.get('confianza', 0):.2f}%",
                    styles["BodySmall"],
                ))
                row_cells.append(KeepTogether(cell_content))

            if len(row_cells) == 1:
                row_cells.append(Paragraph("", styles["BodySmall"]))
            story.append(KeepTogether(row_cells))
            story.append(Spacer(1, 6))

    return story


def generate_video_pdf_report(payload: Dict[str, Any], output_path: str) -> None:
    """Genera un PDF con la línea temporal y mapas Grad-CAM de un video."""
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    doc = _ReportDocTemplate(
        output_path,
        payload,
        topMargin=MARGIN + 1.0 * cm,
        bottomMargin=MARGIN + 0.6 * cm,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
    )
    story = _build_video_story(payload)
    doc.build(story)


if __name__ == "__main__":
    # Ejemplo de uso con datos de prueba
    sample_payload = {
        "reportCode": "MIA-2026-00123",
        "date": "2026-06-18",
        "zone": "Sector Norte - Rajo Las Animas",
        "category": "Pórfido cuprífero",
        "sampleId": "SND-0456 / Tramo 12.0-14.5m",
        "coordinates": "345.210 E / 6.789.430 N",
        "datum": "WGS84 / Huso 19S",
        "samplingMethod": "Testigo de sondaje, cuarteo en bandeja, método Boyle",
        "analyticalMethod": "Espectrometría de absorción atómica (AAS) - Lab. Certificado XYZ",
        "riskLevel": "Medio",
        "riskNote": "Riesgo asociado a variabilidad estructural local",
        "copperGrade": "0.85",
        "copperGradeUnit": "% CuT",
        "copperGradeNote": "Sobre el promedio histórico del sector",
        "status": "Analizado - Pendiente de validación",
        "additionalParameters": [
            {"name": "Ley de oro (Au)", "value": "0.12", "unit": "g/t", "note": "Trazas significativas"},
            {"name": "Humedad", "value": "3.4", "unit": "%", "note": "Dentro de rango esperado"},
        ],
        "aiSummary": (
            "El análisis de la muestra SND-0456 indica una concentración de cobre "
            "consistente con mineralización de tipo pórfido cuprífero, con valores "
            "levemente superiores al promedio histórico registrado para el sector "
            "norte. La presencia de trazas de oro sugiere potencial de subproducto. "
            "Se identifica un nivel de riesgo medio asociado a variabilidad "
            "estructural observada en tramos adyacentes, lo que podría afectar la "
            "continuidad de la mineralización si no se contrasta con sondajes "
            "adicionales."
        ),
        "recommendations": [
            "Ejecutar sondajes de confirmación en un radio de 50 m para validar la continuidad de la ley de Cu.",
            "Incorporar muestras duplicadas y estándares de referencia certificados en el próximo lote analítico.",
            "Revisar la estructura geológica local antes de incorporar este tramo a un modelo de recursos.",
        ],
        "qaqcNotes": (
            "Se incluyó un estándar de referencia certificado cada 20 muestras y un "
            "blanco cada 40 muestras. No se registraron desviaciones fuera de los "
            "límites de control establecidos."
        ),
        "reviewerName": "",
        "reviewerTitle": "Geólogo(a) / Persona Competente (Ley N°20.235)",
        "reviewerRegistration": "",
        "validationDate": "",
    }

    out = "/home/claude/ejemplo_informe.pdf"
    generate_pdf_report(sample_payload, out)
    print(f"PDF generado en: {out}")
