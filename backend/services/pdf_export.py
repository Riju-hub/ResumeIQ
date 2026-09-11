import io
import logging
from typing import Any, Dict

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

logger = logging.getLogger('ats_resume_scorer')


def generate_combined_pdf(analysis_dict: Dict[str, Any]) -> bytes:
    """Generates an ATS report PDF using ReportLab (pure Python, memory safe)."""
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
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1E293B'),
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#4F46E5'),
        spaceAfter=6,
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155'),
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#475569'),
    )

    story = []

    # 1. Header
    story.append(Paragraph('ResumeIQ — ATS Analysis Report', title_style))
    story.append(Paragraph('Comprehensive Evaluation & Optimization Summary', bullet_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width='100%', thickness=1.5, color=colors.HexColor('#E2E8F0'), spaceAfter=12))

    # 2. Overall Score Card
    ats_score = round(float(analysis_dict.get('ats_score') or analysis_dict.get('ATS_score') or 0.0), 1)
    status_text = analysis_dict.get('interpretation') or 'Resume processed against ATS benchmarks.'

    score_data = [
        [
            Paragraph(f'<b>ATS Match Score: {ats_score} / 100</b>', ParagraphStyle('Score', fontName='Helvetica-Bold', fontSize=13, textColor=colors.HexColor('#4F46E5'))),
            Paragraph(f'<b>Status:</b> {status_text}', body_style),
        ]
    ]
    t_score = Table(score_data, colWidths=[270, 270])
    t_score.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t_score)
    story.append(Spacer(1, 12))

    # 3. Component Breakdown
    comp_scores = analysis_dict.get('component_scores') or {}
    if isinstance(comp_scores, dict):
        story.append(Paragraph('Component Breakdown', section_heading))
        breakdown_data = [
            ['Evaluation Category', 'Score'],
            ['Formatting & Structure', f"{comp_scores.get('formatting', 0.0)} / 20"],
            ['Keyword Relevance', f"{comp_scores.get('keywords', 0.0)} / 20"],
            ['Content & Impact', f"{comp_scores.get('content', 0.0)} / 20"],
            ['Skill Validation', f"{comp_scores.get('skill_validation', 0.0)} / 20"],
            ['ATS Compatibility', f"{comp_scores.get('ats_compatibility', 0.0)} / 20"],
        ]
        t_breakdown = Table(breakdown_data, colWidths=[380, 160])
        t_breakdown.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F46E5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
            ('PADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(t_breakdown)
        story.append(Spacer(1, 12))

    # 4. Detailed Feedback / Issues
    feedback_items = analysis_dict.get('detailed_feedback') or analysis_dict.get('issues_summary') or []
    if feedback_items:
        story.append(Paragraph('Identified Issues & Action Items', section_heading))
        for item in feedback_items[:8]:
            if isinstance(item, dict):
                title = item.get('issue_title') or item.get('title') or 'Improvement'
                desc = item.get('how_to_fix') or item.get('explanation') or ''
                story.append(Paragraph(f'<b>• {title}:</b> {desc}', bullet_style))
            else:
                story.append(Paragraph(f'• {item}', bullet_style))
        story.append(Spacer(1, 10))

    # 5. Skills Validation
    svd = analysis_dict.get('skill_validation_details') or {}
    val_skills = svd.get('validated') or []
    unval_skills = svd.get('unvalidated') or []
    if val_skills or unval_skills:
        story.append(Paragraph('Skills Verification Overview', section_heading))
        val_names = [v.get('skill', str(v)) if isinstance(v, dict) else str(v) for v in val_skills]
        unval_names = [u.get('skill', str(u)) if isinstance(u, dict) else str(u) for u in unval_skills]
        
        if val_names:
            story.append(Paragraph(f"<b>Validated in Experience ({len(val_names)}):</b> {', '.join(val_names[:15])}", bullet_style))
            story.append(Spacer(1, 3))
        if unval_names:
            story.append(Paragraph(f"<b>Lacking Context/Projects ({len(unval_names)}):</b> {', '.join(unval_names[:15])}", bullet_style))

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes