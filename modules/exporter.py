"""
Document export service for AI WriteMate.
Generates publication-ready DOCX (via python-docx), PDF (via ReportLab), Markdown, and TXT files.
Returns bytes streams ready for Streamlit's st.download_button and supports direct file saving.
"""

import io
import html
import re
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path

# python-docx for Word document exports
try:
    import docx
    from docx.shared import Inches, Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

# ReportLab for PDF exports
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
    from reportlab.lib.units import inch
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False


class ExporterService:
    """Handles document generation across multiple export formats."""

    # =================================================================
    # DOCX Export (python-docx)
    # =================================================================

    @staticmethod
    def export_to_docx(
        title: str,
        content: str,
        author: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> bytes:
        """
        Creates a styled Microsoft Word (.docx) document in memory.
        Returns bytes suitable for Streamlit download buttons.
        """
        if not HAS_DOCX:
            raise ImportError("python-docx is not installed. Please run: pip install python-docx")

        doc = docx.Document()

        # Set 1-inch standard margins
        for section in doc.sections:
            section.top_margin = Inches(1.0)
            section.bottom_margin = Inches(1.0)
            section.left_margin = Inches(1.0)
            section.right_margin = Inches(1.0)

        # Document Title
        title_para = doc.add_paragraph()
        title_run = title_para.add_run(title)
        title_run.font.name = "Arial"
        title_run.font.size = Pt(22)
        title_run.font.bold = True
        title_run.font.color.rgb = RGBColor(15, 23, 42)  # Slate 900
        title_para.paragraph_format.space_after = Pt(4)

        # Meta subtitle (Date, Author, App)
        meta_parts = [datetime.now().strftime("%B %d, %Y"), "Generated with AI WriteMate"]
        if author:
            meta_parts.insert(0, f"By {author}")
        if metadata:
            for k, v in metadata.items():
                meta_parts.append(f"{k}: {v}")

        meta_para = doc.add_paragraph()
        meta_run = meta_para.add_run(" • ".join(meta_parts))
        meta_run.font.name = "Arial"
        meta_run.font.size = Pt(9.5)
        meta_run.font.italic = True
        meta_run.font.color.rgb = RGBColor(100, 116, 139)  # Slate 500
        meta_para.paragraph_format.space_after = Pt(16)

        # Horizontal rule divider
        divider = doc.add_paragraph()
        divider_run = divider.add_run("—" * 45)
        divider_run.font.color.rgb = RGBColor(226, 232, 240)
        divider.paragraph_format.space_after = Pt(14)

        # Parse content line by line (supports Markdown headers and lists)
        lines = content.split("\n")
        in_code_block = False

        for raw_line in lines:
            line = raw_line.rstrip()

            # Handle code block toggle
            if line.startswith("```"):
                in_code_block = not in_code_block
                continue

            if in_code_block:
                p = doc.add_paragraph()
                r = p.add_run(line)
                r.font.name = "Consolas"
                r.font.size = Pt(9.5)
                r.font.color.rgb = RGBColor(30, 41, 59)
                p.paragraph_format.left_indent = Inches(0.25)
                p.paragraph_format.space_after = Pt(2)
                continue

            # Heading 1 (#)
            if line.startswith("# ") and not line.startswith("## "):
                h = doc.add_heading(level=1)
                r = h.add_run(line.replace("# ", "").strip())
                r.font.name = "Arial"
                r.font.size = Pt(16)
                r.font.color.rgb = RGBColor(30, 41, 59)
                h.paragraph_format.space_before = Pt(14)
                h.paragraph_format.space_after = Pt(6)
            # Heading 2 (##)
            elif line.startswith("## ") and not line.startswith("### "):
                h = doc.add_heading(level=2)
                r = h.add_run(line.replace("## ", "").strip())
                r.font.name = "Arial"
                r.font.size = Pt(13)
                r.font.color.rgb = RGBColor(51, 65, 85)
                h.paragraph_format.space_before = Pt(12)
                h.paragraph_format.space_after = Pt(4)
            # Heading 3 (###)
            elif line.startswith("### "):
                h = doc.add_heading(level=3)
                r = h.add_run(line.replace("### ", "").strip())
                r.font.name = "Arial"
                r.font.size = Pt(11.5)
                r.font.color.rgb = RGBColor(71, 85, 105)
                h.paragraph_format.space_before = Pt(8)
                h.paragraph_format.space_after = Pt(2)
            # Bullet list items
            elif line.startswith("- ") or line.startswith("* "):
                p = doc.add_paragraph(style="List Bullet")
                clean_text = line[2:].strip()
                ExporterService._add_formatted_runs_docx(p, clean_text)
                p.paragraph_format.space_after = Pt(3)
            # Numbered list items
            elif re.match(r"^\d+\.\s", line):
                p = doc.add_paragraph(style="List Number")
                clean_text = re.sub(r"^\d+\.\s", "", line).strip()
                ExporterService._add_formatted_runs_docx(p, clean_text)
                p.paragraph_format.space_after = Pt(3)
            # Empty line
            elif not line:
                spacer = doc.add_paragraph()
                spacer.paragraph_format.space_after = Pt(6)
            # Standard Body Paragraph
            else:
                p = doc.add_paragraph()
                ExporterService._add_formatted_runs_docx(p, line)
                p.paragraph_format.space_after = Pt(6)
                p.paragraph_format.line_spacing = 1.15

        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        return buffer.getvalue()

    @staticmethod
    def _add_formatted_runs_docx(paragraph, text: str) -> None:
        """Parses basic Markdown **bold** and *italic* into Word runs."""
        # Split on markdown bold (**text**)
        parts = re.split(r"(\*\*.*?\*\*)", text)
        for part in parts:
            if part.startswith("**") and part.endswith("**") and len(part) >= 4:
                run = paragraph.add_run(part[2:-2])
                run.font.name = "Arial"
                run.font.size = Pt(10.5)
                run.font.bold = True
            else:
                run = paragraph.add_run(part)
                run.font.name = "Arial"
                run.font.size = Pt(10.5)

    # =================================================================
    # PDF Export (ReportLab)
    # =================================================================

    @staticmethod
    def export_to_pdf(
        title: str,
        content: str,
        author: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> bytes:
        """
        Creates a styled PDF document in memory using ReportLab.
        Returns bytes suitable for Streamlit download buttons.
        """
        if not HAS_REPORTLAB:
            raise ImportError("reportlab is not installed. Please run: pip install reportlab")

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=0.75 * inch,
            leftMargin=0.75 * inch,
            topMargin=0.75 * inch,
            bottomMargin=0.75 * inch,
        )

        story = []
        styles = getSampleStyleSheet()

        # Custom typography styles
        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            textColor=colors.HexColor("#0f172a"),
            spaceAfter=4,
        )

        meta_style = ParagraphStyle(
            "DocMeta",
            parent=styles["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#64748b"),
            spaceAfter=12,
        )

        h1_style = ParagraphStyle(
            "DocH1",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=colors.HexColor("#1e293b"),
            spaceBefore=12,
            spaceAfter=6,
        )

        h2_style = ParagraphStyle(
            "DocH2",
            parent=styles["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=15,
            textColor=colors.HexColor("#334155"),
            spaceBefore=10,
            spaceAfter=4,
        )

        body_style = ParagraphStyle(
            "DocBody",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#1e293b"),
            spaceAfter=8,
        )

        bullet_style = ParagraphStyle(
            "DocBullet",
            parent=body_style,
            leftIndent=15,
            firstLineIndent=-10,
            spaceAfter=4,
        )

        code_style = ParagraphStyle(
            "DocCode",
            parent=body_style,
            fontName="Courier",
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#0f172a"),
            backColor=colors.HexColor("#f1f5f9"),
            leftIndent=15,
            spaceAfter=4,
        )

        # Title
        story.append(Paragraph(html.escape(title), title_style))

        # Metadata subtitle
        meta_parts = [datetime.now().strftime("%B %d, %Y"), "AI WriteMate"]
        if author:
            meta_parts.insert(0, f"Author: {author}")
        if metadata:
            for k, v in metadata.items():
                meta_parts.append(f"{k}: {v}")
        story.append(Paragraph(html.escape(" • ".join(meta_parts)), meta_style))

        # Horizontal rule
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1"), spaceAfter=14))

        # Process lines
        lines = content.split("\n")
        in_code_block = False

        for raw_line in lines:
            line = raw_line.rstrip()

            if line.startswith("```"):
                in_code_block = not in_code_block
                continue

            if in_code_block:
                safe_code = html.escape(line)
                story.append(Paragraph(safe_code, code_style))
                continue

            # Heading 1
            if line.startswith("# ") and not line.startswith("## "):
                h_text = html.escape(line.replace("# ", "").strip())
                story.append(Paragraph(h_text, h1_style))
            # Heading 2
            elif line.startswith("## ") and not line.startswith("### "):
                h_text = html.escape(line.replace("## ", "").strip())
                story.append(Paragraph(h_text, h2_style))
            # Heading 3
            elif line.startswith("### "):
                h_text = html.escape(line.replace("### ", "").strip())
                story.append(Paragraph(h_text, h2_style))
            # Bullet list
            elif line.startswith("- ") or line.startswith("* "):
                bullet_text = ExporterService._markdown_to_reportlab_html(line[2:].strip())
                story.append(Paragraph(f"&bull; {bullet_text}", bullet_style))
            # Numbered list
            elif re.match(r"^\d+\.\s", line):
                clean_num = re.match(r"^(\d+\.)\s", line).group(1)
                text_part = re.sub(r"^\d+\.\s", "", line).strip()
                num_text = ExporterService._markdown_to_reportlab_html(text_part)
                story.append(Paragraph(f"{clean_num} {num_text}", bullet_style))
            # Empty line
            elif not line:
                story.append(Spacer(1, 4))
            # Normal paragraph
            else:
                p_text = ExporterService._markdown_to_reportlab_html(line)
                story.append(Paragraph(p_text, body_style))

        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

    @staticmethod
    def _markdown_to_reportlab_html(text: str) -> str:
        """Converts Markdown **bold** and *italic* into ReportLab-supported XML tags."""
        escaped = html.escape(text)
        # Convert **bold** to <b>bold</b>
        escaped = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", escaped)
        # Convert *italic* to <i>italic</i>
        escaped = re.sub(r"\*(.*?)\*", r"<i>\1</i>", escaped)
        return escaped

    # =================================================================
    # Markdown & Plain Text Exports
    # =================================================================

    @staticmethod
    def export_to_markdown(title: str, content: str) -> str:
        """Formats text as clean markdown with header and timestamp."""
        header = f"# {title}\n\n*Generated with AI WriteMate on {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n---\n\n"
        return header + content

    @staticmethod
    def export_to_txt(title: str, content: str) -> str:
        """Formats text as clean UTF-8 plain text."""
        header = f"{title.upper()}\n{'=' * len(title)}\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        return header + content


# Singleton helper
_exporter_instance: Optional[ExporterService] = None


def get_exporter_service() -> ExporterService:
    global _exporter_instance
    if _exporter_instance is None:
        _exporter_instance = ExporterService()
    return _exporter_instance
