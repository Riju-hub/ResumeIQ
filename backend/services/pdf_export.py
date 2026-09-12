import io
import logging
from typing import Any, Dict
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

logger = logging.getLogger("ats_resume_scorer")


def _get_val(data: dict, *keys, default=None):
    """Safely extracts a value from multiple possible key names or nested structures."""
    if not isinstance(data, dict):
        return default
    for k in keys:
        if k in data and data[k] is not None:
            return data[k]
    return default


def generate_combined_pdf(analysis_dict: Dict[str, Any]) -> bytes:
    """Generates a professional ATS analysis report as a PDF using ReportLab.
    
    Extracts all fields with fallback normalizations to guarantee accurate scores.
    """
    if hasattr(analysis_dict, "model_dump"):
        analysis_dict = analysis_dict.model_dump()
    elif not isinstance(analysis_dict, dict):
        analysis_dict = {}

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0F172A"),
    )

    section_heading = ParagraphStyle(
        "SectionHeading",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#4F46E5"),
        spaceAfter=6,
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155"),
    )

    bullet_style = ParagraphStyle(
        "Bullet",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#475569"),
    )

    story = []

    # 1. Header Banner
    story.append(Paragraph("ResumeIQ — ATS Analysis Report", title_style))
    story.append(Paragraph("Comprehensive Evaluation & Optimization Summary", bullet_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#E2E8F0"), spaceAfter=12))

    # 2. Extract and Normalize Overall Score
    raw_ats_score = _get_val(analysis_dict, "ats_score", "ATS_score", "overall_score", default=0.0)
    try:
        ats_score = round(float(raw_ats_score), 1)
    except Exception:
        ats_score = 0.0

    raw_interpretation = _get_val(
        analysis_dict,
        "interpretation",
        default="Resume processed successfully against ATS benchmarks."
    )

    score_color = "#10B981" if ats_score >= 75 else ("#F59E0B" if ats_score >= 50 else "#EF4444")

    score_data = [
        [
            Paragraph(
                f'<font color="{score_color}"><b>ATS Match Score: {ats_score} / 100</b></font>',
                ParagraphStyle("Score", fontName="Helvetica-Bold", fontSize=14, leading=16)
            ),
            Paragraph(f"<b>Status:</b> {raw_interpretation}", body_style),
        ]
    ]
    t_score = Table(score_data, colWidths=[270, 270])
    t_score.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(t_score)
    story.append(Spacer(1, 12))

    # 3. Component Breakdown (Scaled to 100 Total Points)
    raw_comp = _get_val(analysis_dict, "component_scores", default={})
    if hasattr(raw_comp, "model_dump"):
        raw_comp = raw_comp.model_dump()
    elif not isinstance(raw_comp, dict):
        raw_comp = {}

    fmt_score = float(_get_val(raw_comp, "formatting", default=0.0))
    kw_score = float(_get_val(raw_comp, "keywords", default=0.0))
    cnt_score = float(_get_val(raw_comp, "content", default=0.0))
    sk_score = float(_get_val(raw_comp, "skill_validation", default=0.0))
    ats_comp_score = float(_get_val(raw_comp, "ats_compatibility", default=0.0))

    story.append(Paragraph("Component Breakdown", section_heading))
    breakdown_data = [
        ["Evaluation Category", "Weight", "Score"],
        ["Formatting & Structure", "20 pts", f"{fmt_score:.1f} / 20"],
        ["Keyword Relevance", "25 pts", f"{kw_score:.1f} / 25"],
        ["Content Quality & Impact", "25 pts", f"{cnt_score:.1f} / 25"],
        ["Skill Context Validation", "15 pts", f"{sk_score:.1f} / 15"],
        ["ATS Parsing Compatibility", "15 pts", f"{ats_comp_score:.1f} / 15"],
    ]
    t_breakdown = Table(breakdown_data, colWidths=[280, 100, 160])
    t_breakdown.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F46E5")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 4),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ("PADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t_breakdown)
    story.append(Spacer(1, 12))

    # 4. Job Description Alignment (if provided)
    jd_comp = _get_val(analysis_dict, "jd_comparison", "jd_match_analysis", default=None)
    if hasattr(jd_comp, "model_dump"):
        jd_comp = jd_comp.model_dump()

    if isinstance(jd_comp, dict) and jd_comp:
        match_pct = float(_get_val(jd_comp, "match_percentage", default=0.0))
        sem_sim = float(_get_val(jd_comp, "semantic_similarity", default=0.0))
        matched_kw = _get_val(jd_comp, "matched_keywords", default=[])
        missing_kw = _get_val(jd_comp, "missing_keywords", default=[])

        story.append(Paragraph("Job Description Alignment", section_heading))
        jd_summary = (
            f"<b>Keyword Match:</b> {match_pct:.1f}% &nbsp;|&nbsp; "
            f"<b>Semantic Similarity:</b> {sem_sim * 100:.1f}%"
        )
        story.append(Paragraph(jd_summary, body_style))
        story.append(Spacer(1, 4))

        if matched_kw:
            m_text = ", ".join([str(k) for k in matched_kw[:12]])
            story.append(Paragraph(f'<font color="#047857"><b>Matched Keywords:</b> {m_text}</font>', bullet_style))
            story.append(Spacer(1, 3))
        if missing_kw:
            ms_text = ", ".join([str(k) for k in missing_kw[:12]])
            story.append(Paragraph(f'<font color="#BE123C"><b>Missing Target Keywords:</b> {ms_text}</font>', bullet_style))
            story.append(Spacer(1, 6))

    # 5. Key Strengths
    strengths = _get_val(analysis_dict, "strengths", default=[])
    if strengths:
        story.append(Paragraph("Identified Strengths", section_heading))
        for s in strengths[:5]:
            text = s if isinstance(s, str) else str(s)
            story.append(Paragraph(f"• {text}", bullet_style))
        story.append(Spacer(1, 10))

    # 6. Actionable Improvements & Issues
    feedback_items = _get_val(analysis_dict, "detailed_feedback", "issues_summary", default=[])
    if feedback_items:
        story.append(Paragraph("Actionable Recommendations & Fixes", section_heading))
        for item in feedback_items[:6]:
            if isinstance(item, dict):
                title = item.get("issue_title") or item.get("title") or "Improvement Item"
                desc = item.get("how_to_fix") or item.get("explanation") or ""
                story.append(Paragraph(f"<b>• {title}:</b> {desc}", bullet_style))
            else:
                story.append(Paragraph(f"• {item}", bullet_style))
        story.append(Spacer(1, 10))

    # 7. Skills Validation
    svd = _get_val(analysis_dict, "skill_validation_details", default={})
    if hasattr(svd, "model_dump"):
        svd = svd.model_dump()
    if isinstance(svd, dict) and svd:
        val_skills = svd.get("validated") or []
        unval_skills = svd.get("unvalidated") or []

        if val_skills or unval_skills:
            story.append(Paragraph("Skills Validation Audit", section_heading))
            val_names = [v.get("skill", str(v)) if isinstance(v, dict) else str(v) for v in val_skills]
            unval_names = [u.get("skill", str(u)) if isinstance(u, dict) else str(u) for u in unval_skills]

            if val_names:
                story.append(Paragraph(f"<b>Context Validated ({len(val_names)}):</b> {', '.join(val_names[:12])}", bullet_style))
                story.append(Spacer(1, 3))
            if unval_names:
                story.append(Paragraph(f"<b>Missing Context ({len(unval_names)}):</b> {', '.join(unval_names[:12])}", bullet_style))

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes