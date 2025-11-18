import os
from typing import Any, Dict

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


def _wrap_text(text: str, max_chars: int = 90):
    """
    Rompe un texto largo en líneas para que quepa en la página.
    """
    words = text.split()
    lines = []
    current = []
    length = 0

    for w in words:
        if length + len(w) + 1 > max_chars:
            lines.append(" ".join(current))
            current = [w]
            length = len(w)
        else:
            current.append(w)
            length += len(w) + 1

    if current:
        lines.append(" ".join(current))

    return lines


def generate_pdf_report(payload: Dict[str, Any], output_path: str) -> None:
    """
    Genera un PDF simple con la información del análisis.
    payload viene del detalle (AnalysisDetail).
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    x = 2 * cm
    y = height - 2 * cm

    def line(text: str, font="Helvetica", size=10, leading=14):
        nonlocal y
        c.setFont(font, size)
        c.drawString(x, y, str(text))
        y -= leading

    # Encabezado
    line("MinerIA - Reporte de análisis", "Helvetica-Bold", 14, 18)
    line(f"Fecha: {payload.get('date', '')}")
    line(f"Zona: {payload.get('zone', '')}")
    line(f"Categoría: {payload.get('category', '')}")
    line(f"Riesgo: {payload.get('riskLevel', '')}")
    line(f"Ley Cu: {payload.get('copperGrade', '')}")
    line(f"Estado: {payload.get('status', '')}")
    line("")

    # Resumen IA
    line("Resumen IA", "Helvetica-Bold", 12, 16)
    for t in _wrap_text(payload.get("aiSummary", "")):
        line(t)

    line("")
    # Recomendaciones
    line("Recomendaciones", "Helvetica-Bold", 12, 16)
    for rec in payload.get("recommendations", []):
        for t in _wrap_text(f"• {rec}"):
            line(t)

    c.showPage()
    c.save()
