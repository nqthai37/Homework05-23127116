#!/usr/bin/env python3
"""Render the HW05 Markdown report and AI audit to polished PDF files."""

from __future__ import annotations

import html
import re
from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf"
OUTPUT.mkdir(parents=True, exist_ok=True)


def register_fonts() -> None:
    fonts = Path(r"C:\Windows\Fonts")
    pdfmetrics.registerFont(TTFont("Arial", str(fonts / "arial.ttf")))
    pdfmetrics.registerFont(TTFont("Arial-Bold", str(fonts / "arialbd.ttf")))
    pdfmetrics.registerFont(TTFont("Consolas", str(fonts / "consola.ttf")))


def inline_markup(text: str) -> str:
    escaped = html.escape(text.strip())
    escaped = re.sub(r"`([^`]+)`", r'<font name="Consolas">\1</font>', escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", escaped)
    return escaped


def make_styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "TitleCustom", parent=base["Title"], fontName="Arial-Bold",
            fontSize=20, leading=24, alignment=TA_CENTER, textColor=colors.HexColor("#17365D"),
            spaceAfter=10 * mm,
        ),
        "h1": ParagraphStyle(
            "H1Custom", parent=base["Heading1"], fontName="Arial-Bold",
            fontSize=14, leading=17, textColor=colors.HexColor("#17365D"),
            spaceBefore=5 * mm, spaceAfter=2.5 * mm, keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "H2Custom", parent=base["Heading2"], fontName="Arial-Bold",
            fontSize=11.5, leading=14, textColor=colors.HexColor("#2F5597"),
            spaceBefore=3.5 * mm, spaceAfter=2 * mm, keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "H3Custom", parent=base["Heading3"], fontName="Arial-Bold",
            fontSize=10.5, leading=13, textColor=colors.HexColor("#4472C4"),
            spaceBefore=3 * mm, spaceAfter=1.5 * mm, keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "BodyCustom", parent=base["BodyText"], fontName="Arial",
            fontSize=9.2, leading=13, alignment=TA_JUSTIFY, spaceAfter=2.2 * mm,
        ),
        "bullet": ParagraphStyle(
            "BulletCustom", parent=base["BodyText"], fontName="Arial",
            fontSize=9.2, leading=12.5, leftIndent=5 * mm, firstLineIndent=-3 * mm,
            bulletIndent=1.5 * mm, spaceAfter=1 * mm,
        ),
        "quote": ParagraphStyle(
            "QuoteCustom", parent=base["BodyText"], fontName="Arial",
            fontSize=9.2, leading=13, leftIndent=7 * mm, rightIndent=4 * mm,
            borderColor=colors.HexColor("#4472C4"), borderWidth=1,
            borderPadding=5, backColor=colors.HexColor("#EAF2F8"), spaceAfter=3 * mm,
        ),
        "code": ParagraphStyle(
            "CodeCustom", parent=base["Code"], fontName="Consolas",
            fontSize=7.4, leading=9.5, leftIndent=3 * mm, rightIndent=3 * mm,
            borderPadding=5, backColor=colors.HexColor("#F2F2F2"), spaceAfter=3 * mm,
        ),
        "table": ParagraphStyle(
            "TableCustom", parent=base["BodyText"], fontName="Arial",
            fontSize=6.8, leading=8.4, alignment=TA_LEFT,
        ),
        "table_header": ParagraphStyle(
            "TableHeader", parent=base["BodyText"], fontName="Arial-Bold",
            fontSize=6.8, leading=8.4, textColor=colors.white, alignment=TA_LEFT,
        ),
    }


def parse_table(lines: list[str], styles: dict, available_width: float):
    rows: list[list[str]] = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells):
            continue
        rows.append(cells)
    if not rows:
        return Spacer(1, 1)
    columns = max(len(row) for row in rows)
    for row in rows:
        row.extend([""] * (columns - len(row)))
    weights = []
    for index in range(columns):
        length = max(len(row[index]) for row in rows)
        weights.append(max(8, min(length, 35)))
    total = sum(weights)
    widths = [available_width * weight / total for weight in weights]
    data = []
    for row_index, row in enumerate(rows):
        style = styles["table_header"] if row_index == 0 else styles["table"]
        data.append([Paragraph(inline_markup(cell), style) for cell in row])
    table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2F5597")),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#B4C6E7")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7F9FC")]),
    ]))
    return table


def markdown_story(path: Path, styles: dict, include_hardware: bool = False):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    story = []
    paragraph: list[str] = []
    in_code = False
    code_lines: list[str] = []
    index = 0

    def flush_paragraph() -> None:
        if paragraph:
            story.append(Paragraph(inline_markup(" ".join(paragraph)), styles["body"]))
            paragraph.clear()

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if stripped.startswith("```"):
            flush_paragraph()
            if in_code:
                story.append(Paragraph("<br/>".join(html.escape(x) or " " for x in code_lines), styles["code"]))
                code_lines.clear()
                in_code = False
            else:
                in_code = True
            index += 1
            continue
        if in_code:
            code_lines.append(line)
            index += 1
            continue
        image_match = re.fullmatch(r"!\[([^]]*)\]\(([^)]+)\)", stripped)
        if image_match:
            flush_paragraph()
            image_path = (path.parent / image_match.group(2)).resolve()
            if image_path.exists():
                with PILImage.open(image_path) as source_image:
                    pixel_width, pixel_height = source_image.size
                max_width = 178 * mm
                max_height = 112 * mm
                scale = min(max_width / pixel_width, max_height / pixel_height)
                story.append(Image(
                    str(image_path),
                    width=pixel_width * scale,
                    height=pixel_height * scale,
                ))
                if image_match.group(1):
                    story.append(Paragraph(inline_markup(image_match.group(1)), styles["body"]))
                story.append(Spacer(1, 2 * mm))
            index += 1
            continue
        if stripped.startswith("|") and index + 1 < len(lines) and lines[index + 1].strip().startswith("|"):
            flush_paragraph()
            table_lines = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                table_lines.append(lines[index])
                index += 1
            story.append(parse_table(table_lines, styles, A4[0] - 32 * mm))
            story.append(Spacer(1, 3 * mm))
            continue
        if stripped.startswith("# "):
            flush_paragraph()
            story.append(Paragraph(inline_markup(stripped[2:]), styles["title"]))
        elif stripped.startswith("## "):
            flush_paragraph()
            story.append(Paragraph(inline_markup(stripped[3:]), styles["h1"]))
        elif stripped.startswith("### "):
            flush_paragraph()
            story.append(Paragraph(inline_markup(stripped[4:]), styles["h2"]))
        elif stripped.startswith("#### "):
            flush_paragraph()
            story.append(Paragraph(inline_markup(stripped[5:]), styles["h3"]))
        elif re.match(r"^[-*] ", stripped):
            flush_paragraph()
            story.append(Paragraph(inline_markup(stripped[2:]), styles["bullet"], bulletText="•"))
        elif re.match(r"^\d+\. ", stripped):
            flush_paragraph()
            number, content = stripped.split(". ", 1)
            story.append(Paragraph(inline_markup(content), styles["bullet"], bulletText=f"{number}."))
        elif stripped.startswith(">"):
            flush_paragraph()
            quote_lines = []
            while index < len(lines) and lines[index].strip().startswith(">"):
                quote_lines.append(lines[index].strip()[1:].strip())
                index += 1
            story.append(Paragraph(inline_markup(" ".join(quote_lines)), styles["quote"]))
            continue
        elif stripped in {"---", "***"}:
            flush_paragraph()
            story.append(Spacer(1, 2 * mm))
        elif not stripped:
            flush_paragraph()
        else:
            paragraph.append(stripped)
        index += 1
    flush_paragraph()

    if include_hardware:
        image_path = ROOT / "evidence" / "hardware" / "dxdiag-20260818.png"
        if image_path.exists():
            story.extend([
                PageBreak(),
                Paragraph("Hardware Evidence", styles["h1"]),
                Paragraph("DxDiag System screenshot captured on the test machine on 2026-08-18.", styles["body"]),
                Image(str(image_path), width=175 * mm, height=98.4 * mm),
            ])
    return story


def footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("Arial", 7.5)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawString(16 * mm, 10 * mm, "HW05 Performance Testing - 23127116")
    canvas.drawRightString(A4[0] - 16 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


def build(source: Path, target: Path, include_hardware: bool = False) -> None:
    styles = make_styles()
    document = SimpleDocTemplate(
        str(target), pagesize=A4, rightMargin=16 * mm, leftMargin=16 * mm,
        topMargin=16 * mm, bottomMargin=17 * mm,
        title=source.stem, author="NGUYEN QUANG THAI - 23127116",
    )
    document.build(
        markdown_story(source, styles, include_hardware=include_hardware),
        onFirstPage=footer,
        onLaterPages=footer,
    )


def main() -> None:
    register_fonts()
    build(
        ROOT / "report" / "main-report.md",
        OUTPUT / "23127116_HW05_Performance_Report.pdf",
        include_hardware=True,
    )
    build(
        ROOT / "ai" / "ai-audit-report-final.md",
        OUTPUT / "23127116_AI_Audit_Report.pdf",
        include_hardware=False,
    )


if __name__ == "__main__":
    main()
