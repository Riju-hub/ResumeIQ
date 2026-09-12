# import io
# import logging
# from typing import Any, Dict
# from reportlab.lib import colors
# from reportlab.lib.pagesizes import letter
# from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
# from reportlab.platypus import (
#     HRFlowable,
#     PageBreak,
#     Paragraph,
#     SimpleDocTemplate,
#     Spacer,
#     Table,
#     TableStyle,
# )

# logger = logging.getLogger("ats_resume_scorer")


# def _get_val(data: dict, *keys, default=None):
#     if not isinstance(data, dict):
#         return default
#     for k in keys:
#         if k in data and data[k] is not None:
#             return data[k]
#     lower_data = {str(k).lower(): v for k, v in data.items()}
#     for k in keys:
#         lk = str(k).lower()
#         if lk in lower_data and lower_data[lk] is not None:
#             return lower_data[lk]
#     return default


# def generate_combined_pdf(analysis_dict: Dict[str, Any]) -> bytes:
#     """Generates a complete, multi-page (4-6 page) ATS evaluation report using ReportLab."""
#     if hasattr(analysis_dict, "model_dump"):
#         analysis_dict = analysis_dict.model_dump()
#     elif not isinstance(analysis_dict, dict):
#         analysis_dict = {}

#     if "analysis_result" in analysis_dict and isinstance(analysis_dict["analysis_result"], dict):
#         analysis_dict = analysis_dict["analysis_result"]
#     elif "data" in analysis_dict and isinstance(analysis_dict["data"], dict):
#         analysis_dict = analysis_dict["data"]

#     buffer = io.BytesIO()
#     doc = SimpleDocTemplate(
#         buffer,
#         pagesize=letter,
#         rightMargin=40,
#         leftMargin=40,
#         topMargin=40,
#         bottomMargin=40,
#     )

#     styles = getSampleStyleSheet()

#     # Style Definitions
#     h1_style = ParagraphStyle(
#         "ReportH1",
#         parent=styles["Normal"],
#         fontName="Helvetica-Bold",
#         fontSize=20,
#         leading=24,
#         textColor=colors.HexColor("#0F172A"),
#         spaceAfter=4,
#     )

#     h2_style = ParagraphStyle(
#         "ReportH2",
#         parent=styles["Normal"],
#         fontName="Helvetica-Bold",
#         fontSize=13,
#         leading=17,
#         textColor=colors.HexColor("#4F46E5"),
#         spaceBefore=12,
#         spaceAfter=6,
#     )

#     subtitle_style = ParagraphStyle(
#         "Subtitle",
#         parent=styles["Normal"],
#         fontName="Helvetica",
#         fontSize=10,
#         leading=14,
#         textColor=colors.HexColor("#64748B"),
#         spaceAfter=10,
#     )

#     body_style = ParagraphStyle(
#         "Body",
#         parent=styles["Normal"],
#         fontName="Helvetica",
#         fontSize=9.5,
#         leading=14,
#         textColor=colors.HexColor("#334155"),
#     )

#     bullet_style = ParagraphStyle(
#         "BulletItem",
#         parent=styles["Normal"],
#         fontName="Helvetica",
#         fontSize=9,
#         leading=13,
#         textColor=colors.HexColor("#334155"),
#     )

#     fix_box_style = ParagraphStyle(
#         "FixBox",
#         parent=styles["Normal"],
#         fontName="Helvetica",
#         fontSize=8.5,
#         leading=12,
#         textColor=colors.HexColor("#065F46"),
#     )

#     code_style = ParagraphStyle(
#         "CodeExample",
#         parent=styles["Normal"],
#         fontName="Courier",
#         fontSize=8,
#         leading=11,
#         textColor=colors.HexColor("#0284C7"),
#     )

#     story = []

#     def _page_header(section_num: int, total_sections: int, title: str):
#         header_table = Table([
#             [
#                 Paragraph("<b>⚡ RESUMEIQ ATS ANALYTICS</b>", ParagraphStyle("Hdr", fontName="Helvetica-Bold", fontSize=9, textColor=colors.HexColor("#4F46E5"))),
#                 Paragraph(f"Section {section_num} of {total_sections}", ParagraphStyle("HdrR", fontName="Helvetica", fontSize=9, textColor=colors.HexColor("#94A3B8"), alignment=2))
#             ]
#         ], colWidths=[300, 232])
#         header_table.setStyle(TableStyle([
#             ("PADDING", (0, 0), (-1, -1), 0),
#             ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
#         ]))
#         story.append(header_table)
#         story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#E2E8F0"), spaceAfter=14))
#         story.append(Paragraph(title, h1_style))

#     # =========================================================================
#     # PAGE 1: EXECUTIVE SUMMARY & SCORE BREAKDOWN
#     # =========================================================================
#     _page_header(1, 4, "Executive ATS Match Summary")
#     story.append(Paragraph("High-level algorithmic evaluation across ATS parsing, keyword distribution, and content quality.", subtitle_style))

#     raw_ats_score = _get_val(analysis_dict, "ats_score", "ATS_score", "overall_score", default=0.0)
#     try:
#         ats_score = round(float(raw_ats_score), 1)
#     except Exception:
#         ats_score = 0.0

#     interpretation = _get_val(analysis_dict, "interpretation", default="Resume evaluated against core ATS benchmarks.")
#     score_color = "#10B981" if ats_score >= 75 else ("#F59E0B" if ats_score >= 50 else "#EF4444")

#     score_card = [
#         [
#             Paragraph(f'<font color="{score_color}" size="26"><b>{ats_score}</b></font><font size="14" color="#94A3B8"> / 100</font><br/><font size="9" color="#64748B"><b>OVERALL ATS SCORE</b></font>', ParagraphStyle("ScoreDisp", alignment=1, leading=20)),
#             Paragraph(f"<b>Assessment Verdict:</b><br/>{interpretation}<br/><br/><i>Evaluates layout durability, keyword frequency matching, and context verification.</i>", body_style),
#         ]
#     ]
#     t_score = Table(score_card, colWidths=[180, 352])
#     t_score.setStyle(TableStyle([
#         ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
#         ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
#         ("PADDING", (0, 0), (-1, -1), 12),
#         ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
#     ]))
#     story.append(t_score)
#     story.append(Spacer(1, 14))

#     # Component Scores Table
#     raw_comp = _get_val(analysis_dict, "component_scores", default={})
#     if hasattr(raw_comp, "model_dump"):
#         raw_comp = raw_comp.model_dump()
#     elif not isinstance(raw_comp, dict):
#         raw_comp = {}

#     story.append(Paragraph("Dimensional Scoring Breakdown", h2_style))
#     breakdown_rows = [
#         ["Evaluation Dimension", "Weight", "Score", "Performance Status"],
#         ["Formatting & Layout Structure", "20 pts", f"{float(_get_val(raw_comp, 'formatting', default=0.0)):.1f} / 20", "Optimal" if float(_get_val(raw_comp, 'formatting', default=0.0)) >= 15 else "Needs Review"],
#         ["Keyword Density & Relevance", "25 pts", f"{float(_get_val(raw_comp, 'keywords', default=0.0)):.1f} / 25", "Strong" if float(_get_val(raw_comp, 'keywords', default=0.0)) >= 18 else "Deficient"],
#         ["Content Quality & Impact Metrics", "25 pts", f"{float(_get_val(raw_comp, 'content', default=0.0)):.1f} / 25", "Measurable" if float(_get_val(raw_comp, 'content', default=0.0)) >= 18 else "Weak Metrics"],
#         ["Skill Context Validation", "15 pts", f"{float(_get_val(raw_comp, 'skill_validation', default=0.0)):.1f} / 15", "Substantiated" if float(_get_val(raw_comp, 'skill_validation', default=0.0)) >= 11 else "Unsubstantiated"],
#         ["ATS Parsing Architecture", "15 pts", f"{float(_get_val(raw_comp, 'ats_compatibility', default=0.0)):.1f} / 15", "Compatible" if float(_get_val(raw_comp, 'ats_compatibility', default=0.0)) >= 12 else "Blockers Found"],
#     ]
#     t_breakdown = Table(breakdown_rows, colWidths=[200, 70, 90, 172])
#     t_breakdown.setStyle(TableStyle([
#         ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F46E5")),
#         ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
#         ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
#         ("FONTSIZE", (0, 0), (-1, 0), 8.5),
#         ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
#         ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
#         ("PADDING", (0, 0), (-1, -1), 6),
#     ]))
#     story.append(t_breakdown)
#     story.append(Spacer(1, 14))

#     # Strengths
#     strengths = _get_val(analysis_dict, "strengths", default=[])
#     if strengths:
#         story.append(Paragraph("Identified Document Strengths", h2_style))
#         for s in strengths:
#             story.append(Paragraph(f"✓ &nbsp; {s}", bullet_style))
#             story.append(Spacer(1, 3))

#     # =========================================================================
#     # PAGE 2: SKILL VALIDATION & CONTEXT AUDIT
#     # =========================================================================
#     story.append(PageBreak())
#     _page_header(2, 4, "Skill Context & Demonstration Audit")
#     story.append(Paragraph("Cross-referencing declared technical proficiencies against work experience context and project bullets.", subtitle_style))

#     svd = _get_val(analysis_dict, "skill_validation_details", default={})
#     if hasattr(svd, "model_dump"):
#         svd = svd.model_dump()
#     if not isinstance(svd, dict):
#         svd = {}

#     total_sk = svd.get("total", 0)
#     val_sk = svd.get("validated") or []
#     unval_sk = svd.get("unvalidated") or []
#     val_pct = svd.get("validation_pct", 0.0)

#     sk_stats = [
#         [
#             Paragraph(f"<b>{total_sk}</b><br/><font size='7.5' color='#64748B'>TOTAL SKILLS</font>", ParagraphStyle("ST1", alignment=1)),
#             Paragraph(f"<font color='#10B981'><b>{len(val_sk)}</b></font><br/><font size='7.5' color='#64748B'>EVIDENCE BACKED</font>", ParagraphStyle("ST2", alignment=1)),
#             Paragraph(f"<font color='#EF4444'><b>{len(unval_sk)}</b></font><br/><font size='7.5' color='#64748B'>MISSING CONTEXT</font>", ParagraphStyle("ST3", alignment=1)),
#             Paragraph(f"<b>{val_pct:.0f}%</b><br/><font size='7.5' color='#64748B'>VALIDATION RATE</font>", ParagraphStyle("ST4", alignment=1)),
#         ]
#     ]
#     t_sk_stats = Table(sk_stats, colWidths=[133, 133, 133, 133])
#     t_sk_stats.setStyle(TableStyle([
#         ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
#         ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
#         ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
#         ("PADDING", (0, 0), (-1, -1), 8),
#     ]))
#     story.append(t_sk_stats)
#     story.append(Spacer(1, 14))

#     # Evidence-backed skills
#     story.append(Paragraph("Validated Skills (Demonstrated in Experience/Projects)", h2_style))
#     if val_sk:
#         for item in val_sk:
#             skill_name = item.get("skill", str(item)) if isinstance(item, dict) else str(item)
#             projects = item.get("projects", []) if isinstance(item, dict) else []
#             proj_str = f" &nbsp;→&nbsp; <i>Demonstrated in: {', '.join(projects)}</i>" if projects else ""
#             story.append(Paragraph(f"• <b>{skill_name}</b>{proj_str}", bullet_style))
#             story.append(Spacer(1, 3))
#     else:
#         story.append(Paragraph("No skills were strongly tied to measurable work experience bullets.", body_style))

#     story.append(Spacer(1, 10))

#     # Unvalidated skills (Full list without truncation)
#     story.append(Paragraph("Unsubstantiated Skills (Listed in Skills section but missing proof)", h2_style))
#     if unval_sk:
#         unval_names = [u.get("skill", str(u)) if isinstance(u, dict) else str(u) for u in unval_sk]
#         story.append(Paragraph(f'<font color="#991B1B">{", ".join(unval_names)}</font>', body_style))
#         story.append(Spacer(1, 8))

#         fix_unval = [
#             [Paragraph("<b>💡 Remediation Guide:</b> For each unsubstantiated skill above, add at least one bullet point in your Experience or Projects section showing how you used the technology with measurable impact.", fix_box_style)]
#         ]
#         t_fix = Table(fix_unval, colWidths=[532])
#         t_fix.setStyle(TableStyle([
#             ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#ECFDF5")),
#             ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#A7F3D0")),
#             ("PADDING", (0, 0), (-1, -1), 8),
#         ]))
#         story.append(t_fix)

#     # =========================================================================
#     # PAGE 3: JOB DESCRIPTION ALIGNMENT & KEYWORD MATRIX
#     # =========================================================================
#     story.append(PageBreak())
#     _page_header(3, 4, "Job Description Match & Keyword Gap")
#     story.append(Paragraph("Detailed analysis of keyword coverage, semantic embedding similarity, and missing qualifications.", subtitle_style))

#     jd_comp = _get_val(analysis_dict, "jd_comparison", "jd_match_analysis", default=None)
#     if hasattr(jd_comp, "model_dump"):
#         jd_comp = jd_comp.model_dump()

#     if isinstance(jd_comp, dict) and jd_comp:
#         kw_match = float(_get_val(jd_comp, "match_percentage", default=0.0))
#         sem_sim = float(_get_val(jd_comp, "semantic_similarity", default=0.0))

#         jd_metric_card = [
#             [
#                 Paragraph(f"<font color='#4F46E5' size='18'><b>{kw_match:.1f}%</b></font><br/><font size='8' color='#64748B'>EXACT KEYWORD MATCH</font>", ParagraphStyle("JM1", alignment=1)),
#                 Paragraph(f"<font color='#7C3AED' size='18'><b>{sem_sim * 100:.1f}%</b></font><br/><font size='8' color='#64748B'>SEMANTIC SIMILARITY</font>", ParagraphStyle("JM2", alignment=1)),
#             ]
#         ]
#         t_jd = Table(jd_metric_card, colWidths=[266, 266])
#         t_jd.setStyle(TableStyle([
#             ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
#             ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
#             ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
#             ("PADDING", (0, 0), (-1, -1), 10),
#         ]))
#         story.append(t_jd)
#         story.append(Spacer(1, 14))

#         matched_kw = _get_val(jd_comp, "matched_keywords", default=[])
#         missing_kw = _get_val(jd_comp, "missing_keywords", default=[])
#         skills_gap = _get_val(jd_comp, "skills_gap", default=[])

#         if matched_kw:
#             story.append(Paragraph(f"Matched Target Keywords ({len(matched_kw)})", h2_style))
#             story.append(Paragraph(f'<font color="#047857">{", ".join(str(k) for k in matched_kw)}</font>', body_style))
#             story.append(Spacer(1, 8))

#         if missing_kw:
#             story.append(Paragraph(f"Missing Job Description Keywords ({len(missing_kw)})", h2_style))
#             story.append(Paragraph(f'<font color="#BE123C">{", ".join(str(k) for k in missing_kw)}</font>', body_style))
#             story.append(Spacer(1, 8))

#         if skills_gap:
#             story.append(Paragraph(f"Core Competency Gaps ({len(skills_gap)})", h2_style))
#             for gap in skills_gap:
#                 story.append(Paragraph(f"• <b>Priority addition candidate:</b> {gap}", bullet_style))
#                 story.append(Spacer(1, 2))
#     else:
#         story.append(Paragraph("No job description was provided during this scan. Add a job description to unlock role-specific keyword matching and semantic gap benchmarking.", body_style))

#     # =========================================================================
#     # PAGES 4+: GRANULAR FEEDBACK & ACTIONABLE CHECKLIST
#     # =========================================================================
#     story.append(PageBreak())
#     _page_header(4, 4, "Actionable Roadmap & Checklist")
#     story.append(Paragraph("Prioritized remediation steps to eliminate ATS filtering bottlenecks and elevate your composite score.", subtitle_style))

#     feedback_items = _get_val(analysis_dict, "detailed_feedback", "issues_summary", default=[])
#     if feedback_items and isinstance(feedback_items, list):
#         story.append(Paragraph("Detailed Findings & Code/Bullet Fixes", h2_style))
#         for idx, item in enumerate(feedback_items, 1):
#             if isinstance(item, dict):
#                 title = item.get("issue_title") or item.get("title") or f"Issue #{idx}"
#                 sev = item.get("severity_level") or "Moderate"
#                 exp = item.get("explanation") or ""
#                 fix = item.get("how_to_fix") or ""
#                 ex = item.get("example_improvement") or ""

#                 sev_color = "#991B1B" if str(sev).lower() == "high" else ("#92400E" if str(sev).lower() == "moderate" else "#3730A3")
#                 story.append(Paragraph(f"<b>{idx}. {title}</b> &nbsp;[<font color='{sev_color}'><b>{sev} Priority</b></font>]", ParagraphStyle("IssTitle", fontName="Helvetica-Bold", fontSize=10, textColor=colors.HexColor("#0F172A"))))
#                 if exp:
#                     story.append(Paragraph(f"<b>Why it matters:</b> {exp}", body_style))
#                 if fix:
#                     story.append(Paragraph(f"<b>How to fix:</b> {fix}", body_style))
#                 if ex:
#                     story.append(Spacer(1, 2))
#                     ex_table = Table([[Paragraph(f"<b>Example Pattern:</b><br/>{ex}", code_style)]], colWidths=[532])
#                     ex_table.setStyle(TableStyle([
#                         ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#0F172A")),
#                         ("PADDING", (0, 0), (-1, -1), 6),
#                     ]))
#                     story.append(ex_table)
#                 story.append(Spacer(1, 8))
#             else:
#                 story.append(Paragraph(f"• {item}", bullet_style))

#     # Final Action Items Checklist
#     story.append(Spacer(1, 8))
#     story.append(Paragraph("Printable Action Items Checklist", h2_style))
#     action_items = _get_val(analysis_dict, "action_items", default=[])

#     checklist_entries = []
#     if action_items:
#         checklist_entries.extend(action_items)
#     elif feedback_items:
#         for f in feedback_items:
#             if isinstance(f, dict) and f.get("how_to_fix"):
#                 checklist_entries.append(f"[{f.get('issue_title', 'Action')}] {f.get('how_to_fix')}")

#     if unval_sk:
#         for u in unval_sk[:6]:
#             u_name = u.get("skill", str(u)) if isinstance(u, dict) else str(u)
#             checklist_entries.append(f"Integrate '{u_name}' into a project bullet point with measurable results.")

#     if checklist_entries:
#         for item in checklist_entries:
#             chk_table = Table([
#                 [Paragraph("<b>[  ]</b>", ParagraphStyle("Box", fontName="Helvetica", fontSize=9, textColor=colors.HexColor("#94A3B8"))),
#                  Paragraph(item, bullet_style)]
#             ], colWidths=[24, 508])
#             chk_table.setStyle(TableStyle([
#                 ("PADDING", (0, 0), (-1, -1), 2),
#                 ("VALIGN", (0, 0), (-1, -1), "TOP"),
#             ]))
#             story.append(chk_table)
#     else:
#         story.append(Paragraph("✓ No pending checklist tasks found. Your resume is in optimal condition.", body_style))

#     doc.build(story)
#     pdf_bytes = buffer.getvalue()
#     buffer.close()
#     return pdf_bytes










import io
import logging
from typing import Any, Dict
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    HRFlowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

logger = logging.getLogger("ats_resume_scorer")


def _get_val(data: dict, *keys, default=None):
    if not isinstance(data, dict):
        return default
    for k in keys:
        if k in data and data[k] is not None:
            return data[k]
    lower_data = {str(k).lower(): v for k, v in data.items()}
    for k in keys:
        lk = str(k).lower()
        if lk in lower_data and lower_data[lk] is not None:
            return lower_data[lk]
    return default


def _draw_cyber_background(canvas, doc):
    """Draws a dark canvas, neon gradient orbs, and angled 'ResumeIQ' watermarks."""
    canvas.saveState()
    width, height = letter

    # 1. Base Dark Cyber Canvas
    canvas.setFillColor(colors.HexColor("#0B0F19"))
    canvas.rect(0, 0, width, height, fill=True, stroke=False)

    # 2. Ambient Multi-Color Neon Mesh Orbs
    # Top-Left Indigo Orb
    canvas.setFillColor(colors.HexColor("#6366F1"), alpha=0.12)
    canvas.circle(50, height - 50, 180, fill=True, stroke=False)

    # Top-Right Pink Orb
    canvas.setFillColor(colors.HexColor("#F43F5E"), alpha=0.10)
    canvas.circle(width - 40, height - 60, 160, fill=True, stroke=False)

    # Bottom-Left Violet Orb
    canvas.setFillColor(colors.HexColor("#A855F7"), alpha=0.10)
    canvas.circle(60, 60, 160, fill=True, stroke=False)

    # Bottom-Right Cyan Orb
    canvas.setFillColor(colors.HexColor("#06B6D4"), alpha=0.10)
    canvas.circle(width - 50, 50, 170, fill=True, stroke=False)

    # Center Emerald Ambient Tint
    canvas.setFillColor(colors.HexColor("#10B981"), alpha=0.06)
    canvas.circle(width / 2, height / 2, 200, fill=True, stroke=False)

    # 3. Watermarked 'ResumeIQ' Typography Pattern
    canvas.setFillColor(colors.white, alpha=0.035)
    canvas.setFont("Helvetica-Bold", 82)
    canvas.rotate(-22)
    
    canvas.drawString(-120, height * 0.95, "RESUMEIQ")
    canvas.drawString(-60, height * 0.65, "RESUMEIQ")
    canvas.drawString(0, height * 0.35, "RESUMEIQ")
    canvas.drawString(60, height * 0.05, "RESUMEIQ")

    canvas.restoreState()


def generate_combined_pdf(analysis_dict: Dict[str, Any]) -> bytes:
    """Generates a multi-page ATS report using ReportLab with dark cyberpunk styling."""
    if hasattr(analysis_dict, "model_dump"):
        analysis_dict = analysis_dict.model_dump()
    elif not isinstance(analysis_dict, dict):
        analysis_dict = {}

    if "analysis_result" in analysis_dict and isinstance(analysis_dict["analysis_result"], dict):
        analysis_dict = analysis_dict["analysis_result"]
    elif "data" in analysis_dict and isinstance(analysis_dict["data"], dict):
        analysis_dict = analysis_dict["data"]

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

    # Typography & Styles
    h1_style = ParagraphStyle(
        "ReportH1",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.white,
        spaceAfter=3,
    )

    h2_cyan = ParagraphStyle(
        "H2Cyan",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#38BDF8"),
        spaceBefore=10,
        spaceAfter=5,
    )

    h2_pink = ParagraphStyle(
        "H2Pink",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#FB7185"),
        spaceBefore=10,
        spaceAfter=5,
    )

    h2_green = ParagraphStyle(
        "H2Green",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#34D399"),
        spaceBefore=10,
        spaceAfter=5,
    )

    h2_amber = ParagraphStyle(
        "H2Amber",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#FBBF24"),
        spaceBefore=10,
        spaceAfter=5,
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#94A3B8"),
        spaceAfter=8,
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#CBD5E1"),
    )

    bullet_style = ParagraphStyle(
        "BulletItem",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#CBD5E1"),
    )

    fix_box_style = ParagraphStyle(
        "FixBox",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor("#A7F3D0"),
    )

    code_style = ParagraphStyle(
        "CodeExample",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=7.5,
        leading=10.5,
        textColor=colors.HexColor("#38BDF8"),
    )

    story = []

    def _page_header(section_num: int, total_sections: int, title: str):
        header_table = Table([
            [
                Paragraph("<b>⚡ RESUMEIQ ATS ANALYTICS</b>", ParagraphStyle("Hdr", fontName="Helvetica-Bold", fontSize=9, textColor=colors.HexColor("#818CF8"))),
                Paragraph(f"Section {section_num} of {total_sections}", ParagraphStyle("HdrR", fontName="Helvetica-Bold", fontSize=8.5, textColor=colors.HexColor("#38BDF8"), alignment=2))
            ]
        ], colWidths=[310, 230])
        header_table.setStyle(TableStyle([
            ("PADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))
        story.append(header_table)
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E293B"), spaceAfter=10))
        story.append(Paragraph(title, h1_style))

    # =========================================================================
    # PAGE 1: EXECUTIVE SUMMARY & SCORE BREAKDOWN
    # =========================================================================
    _page_header(1, 4, "Executive Match Intelligence Summary")
    story.append(Paragraph("Algorithmic diagnostic evaluation across ATS formatting rules, keyword density, and bullet impact.", subtitle_style))

    raw_ats_score = _get_val(analysis_dict, "ats_score", "ATS_score", "overall_score", default=0.0)
    try:
        ats_score = round(float(raw_ats_score), 1)
    except Exception:
        ats_score = 0.0

    interpretation = _get_val(analysis_dict, "interpretation", default="Resume evaluated against core ATS benchmarks.")
    score_color = "#34D399" if ats_score >= 75 else ("#FBBF24" if ats_score >= 50 else "#FB7185")

    score_card = [
        [
            Paragraph(f'<font color="{score_color}" size="24"><b>{ats_score}</b></font><font size="13" color="#64748B"> / 100</font><br/><font size="8" color="#818CF8"><b>OVERALL ATS SCORE</b></font>', ParagraphStyle("ScoreDisp", alignment=1, leading=18)),
            Paragraph(f"<b>Assessment Verdict:</b><br/>{interpretation}<br/><br/><i>Evaluates layout durability, keyword frequency matching, and context verification.</i>", body_style),
        ]
    ]
    t_score = Table(score_card, colWidths=[180, 360])
    t_score.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#0F172A")),
        ("BOX", (0, 0), (-1, -1), 1.2, colors.HexColor("#334155")),
        ("PADDING", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(t_score)
    story.append(Spacer(1, 10))

    # Component Scores Table
    raw_comp = _get_val(analysis_dict, "component_scores", default={})
    if hasattr(raw_comp, "model_dump"):
        raw_comp = raw_comp.model_dump()
    elif not isinstance(raw_comp, dict):
        raw_comp = {}

    story.append(Paragraph("📊 Dimensional Scoring Breakdown", h2_cyan))
    breakdown_rows = [
        ["Evaluation Dimension", "Weight", "Score", "Performance Status"],
        ["Formatting & Layout Structure", "20 pts", f"{float(_get_val(raw_comp, 'formatting', default=0.0)):.1f} / 20", "Optimal" if float(_get_val(raw_comp, 'formatting', default=0.0)) >= 15 else "Needs Review"],
        ["Keyword Density & Relevance", "25 pts", f"{float(_get_val(raw_comp, 'keywords', default=0.0)):.1f} / 25", "Strong" if float(_get_val(raw_comp, 'keywords', default=0.0)) >= 18 else "Deficient"],
        ["Content Quality & Impact Metrics", "25 pts", f"{float(_get_val(raw_comp, 'content', default=0.0)):.1f} / 25", "Measurable" if float(_get_val(raw_comp, 'content', default=0.0)) >= 18 else "Weak Metrics"],
        ["Skill Context Validation", "15 pts", f"{float(_get_val(raw_comp, 'skill_validation', default=0.0)):.1f} / 15", "Substantiated" if float(_get_val(raw_comp, 'skill_validation', default=0.0)) >= 11 else "Unsubstantiated"],
        ["ATS Parsing Architecture", "15 pts", f"{float(_get_val(raw_comp, 'ats_compatibility', default=0.0)):.1f} / 15", "Compatible" if float(_get_val(raw_comp, 'ats_compatibility', default=0.0)) >= 12 else "Blockers Found"],
    ]
    t_breakdown = Table(breakdown_rows, colWidths=[200, 70, 90, 180])
    t_breakdown.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E1B4B")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#C7D2FE")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#1E293B")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#0F172A"), colors.HexColor("#090D16")]),
        ("TEXTCOLOR", (0, 1), (-1, -1), colors.HexColor("#CBD5E1")),
        ("PADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t_breakdown)
    story.append(Spacer(1, 10))

    # Strengths
    strengths = _get_val(analysis_dict, "strengths", default=[])
    if strengths:
        story.append(Paragraph("✨ Identified Strengths", h2_green))
        for s in strengths:
            story.append(Paragraph(f'<font color="#34D399">✦</font> &nbsp; {s}', bullet_style))
            story.append(Spacer(1, 2))

    # =========================================================================
    # PAGE 2: SKILL VALIDATION & CONTEXT AUDIT
    # =========================================================================
    story.append(PageBreak())
    _page_header(2, 4, "Skill Context & Demonstration Audit")
    story.append(Paragraph("Cross-referencing technical proficiencies against work history context and accomplishments.", subtitle_style))

    svd = _get_val(analysis_dict, "skill_validation_details", default={})
    if hasattr(svd, "model_dump"):
        svd = svd.model_dump()
    if not isinstance(svd, dict):
        svd = {}

    total_sk = svd.get("total", 0)
    val_sk = svd.get("validated") or []
    unval_sk = svd.get("unvalidated") or []
    val_pct = svd.get("validation_pct", 0.0)

    sk_stats = [
        [
            Paragraph(f"<font color='#FFFFFF' size='14'><b>{total_sk}</b></font><br/><font size='7' color='#64748B'>TOTAL SKILLS</font>", ParagraphStyle("ST1", alignment=1)),
            Paragraph(f"<font color='#34D399' size='14'><b>{len(val_sk)}</b></font><br/><font size='7' color='#64748B'>EVIDENCE BACKED</font>", ParagraphStyle("ST2", alignment=1)),
            Paragraph(f"<font color='#FB7185' size='14'><b>{len(unval_sk)}</b></font><br/><font size='7' color='#64748B'>MISSING CONTEXT</font>", ParagraphStyle("ST3", alignment=1)),
            Paragraph(f"<font color='#38BDF8' size='14'><b>{val_pct:.0f}%</b></font><br/><font size='7' color='#64748B'>VALIDATION RATE</font>", ParagraphStyle("ST4", alignment=1)),
        ]
    ]
    t_sk_stats = Table(sk_stats, colWidths=[135, 135, 135, 135])
    t_sk_stats.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#0F172A")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#334155")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#1E293B")),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t_sk_stats)
    story.append(Spacer(1, 10))

    # Evidence-backed skills
    story.append(Paragraph("Validated Skills (Demonstrated in Experience/Projects)", h2_green))
    if val_sk:
        for item in val_sk:
            skill_name = item.get("skill", str(item)) if isinstance(item, dict) else str(item)
            projects = item.get("projects", []) if isinstance(item, dict) else []
            proj_str = f" &nbsp;→&nbsp; <font color='#94A3B8'><i>Demonstrated in: {', '.join(projects)}</i></font>" if projects else ""
            story.append(Paragraph(f'<font color="#34D399">✓</font> <b><font color="#A7F3D0">{skill_name}</font></b>{proj_str}', bullet_style))
            story.append(Spacer(1, 2))
    else:
        story.append(Paragraph("No skills were strongly tied to measurable work experience bullets.", body_style))

    story.append(Spacer(1, 8))

    # Unvalidated skills
    story.append(Paragraph("Unsubstantiated Skills (Missing Context in Experience)", h2_pink))
    if unval_sk:
        unval_names = [u.get("skill", str(u)) if isinstance(u, dict) else str(u) for u in unval_sk]
        story.append(Paragraph(f'<font color="#FCA5A5">{", ".join(unval_names)}</font>', body_style))
        story.append(Spacer(1, 6))

        fix_unval = [
            [Paragraph("<b>💡 Remediation Guide:</b> For each unsubstantiated skill above, add at least one bullet point in your Experience or Projects section showing how you used the technology with measurable results.", fix_box_style)]
        ]
        t_fix = Table(fix_unval, colWidths=[540])
        t_fix.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#062419")),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#065F46")),
            ("PADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(t_fix)

    # =========================================================================
    # PAGE 3: JOB DESCRIPTION ALIGNMENT & KEYWORD MATRIX
    # =========================================================================
    story.append(PageBreak())
    _page_header(3, 4, "Job Description Match & Keyword Gap")
    story.append(Paragraph("Evaluating exact keyword overlap, vector embedding semantic similarity, and core qualifications.", subtitle_style))

    jd_comp = _get_val(analysis_dict, "jd_comparison", "jd_match_analysis", default=None)
    if hasattr(jd_comp, "model_dump"):
        jd_comp = jd_comp.model_dump()

    if isinstance(jd_comp, dict) and jd_comp:
        kw_match = float(_get_val(jd_comp, "match_percentage", default=0.0))
        sem_sim = float(_get_val(jd_comp, "semantic_similarity", default=0.0))

        jd_metric_card = [
            [
                Paragraph(f"<font color='#38BDF8' size='16'><b>{kw_match:.1f}%</b></font><br/><font size='7' color='#64748B'>EXACT KEYWORD MATCH</font>", ParagraphStyle("JM1", alignment=1)),
                Paragraph(f"<font color='#FB7185' size='16'><b>{sem_sim * 100:.1f}%</b></font><br/><font size='7' color='#64748B'>SEMANTIC SIMILARITY</font>", ParagraphStyle("JM2", alignment=1)),
            ]
        ]
        t_jd = Table(jd_metric_card, colWidths=[270, 270])
        t_jd.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#0F172A")),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#334155")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#1E293B")),
            ("PADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(t_jd)
        story.append(Spacer(1, 10))

        matched_kw = _get_val(jd_comp, "matched_keywords", default=[])
        missing_kw = _get_val(jd_comp, "missing_keywords", default=[])
        skills_gap = _get_val(jd_comp, "skills_gap", default=[])

        if matched_kw:
            story.append(Paragraph(f"Matched Target Keywords ({len(matched_kw)})", h2_green))
            story.append(Paragraph(f'<font color="#A7F3D0">{", ".join(str(k) for k in matched_kw)}</font>', body_style))
            story.append(Spacer(1, 6))

        if missing_kw:
            story.append(Paragraph(f"Missing Job Description Keywords ({len(missing_kw)})", h2_pink))
            story.append(Paragraph(f'<font color="#FCA5A5">{", ".join(str(k) for k in missing_kw)}</font>', body_style))
            story.append(Spacer(1, 6))

        if skills_gap:
            story.append(Paragraph(f"Core Competency Gaps ({len(skills_gap)})", h2_amber))
            for gap in skills_gap:
                story.append(Paragraph(f'<font color="#FBBF24">✦</font> <b>Candidate for addition:</b> <font color="#FDE68A">{gap}</font>', bullet_style))
                story.append(Spacer(1, 2))
    else:
        story.append(Paragraph("No target job description was provided during this analysis. Upload or paste a job description in the Analyzer interface to unlock comparative match analytics.", body_style))

    # =========================================================================
    # PAGES 4+: GRANULAR FEEDBACK & ACTIONABLE CHECKLIST
    # =========================================================================
    story.append(PageBreak())
    _page_header(4, 4, "Actionable Roadmap & Checklist")
    story.append(Paragraph("Prioritized remediation steps to eliminate ATS filtering bottlenecks and elevate your composite score.", subtitle_style))

    feedback_items = _get_val(analysis_dict, "detailed_feedback", "issues_summary", default=[])
    if feedback_items and isinstance(feedback_items, list):
        story.append(Paragraph("Detailed Action Items & Code/Bullet Fixes", h2_cyan))
        for idx, item in enumerate(feedback_items, 1):
            if isinstance(item, dict):
                title = item.get("issue_title") or item.get("title") or f"Issue #{idx}"
                sev = item.get("severity_level") or "Moderate"
                exp = item.get("explanation") or ""
                fix = item.get("how_to_fix") or ""
                ex = item.get("example_improvement") or ""

                sev_color = "#FB7185" if str(sev).lower() == "high" else ("#FBBF24" if str(sev).lower() == "moderate" else "#818CF8")
                story.append(Paragraph(f"<b><font color='#FFFFFF'>{idx}. {title}</font></b> &nbsp;[<font color='{sev_color}'><b>{sev} Priority</b></font>]", ParagraphStyle("IssTitle", fontName="Helvetica-Bold", fontSize=9.5, textColor=colors.white)))
                if exp:
                    story.append(Paragraph(f"<b>Why it matters:</b> {exp}", body_style))
                if fix:
                    story.append(Paragraph(f"<b>Recommended fix:</b> <font color='#A7F3D0'>{fix}</font>", body_style))
                if ex:
                    story.append(Spacer(1, 2))
                    ex_table = Table([[Paragraph(f"<b>Optimized Pattern Example:</b><br/>{ex}", code_style)]], colWidths=[540])
                    ex_table.setStyle(TableStyle([
                        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#050811")),
                        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#1E293B")),
                        ("PADDING", (0, 0), (-1, -1), 5),
                    ]))
                    story.append(ex_table)
                story.append(Spacer(1, 6))
            else:
                story.append(Paragraph(f"• {item}", bullet_style))

    # Final Action Items Checklist
    story.append(Spacer(1, 6))
    story.append(Paragraph("Action Items Checklist", h2_green))
    action_items = _get_val(analysis_dict, "action_items", default=[])

    checklist_entries = []
    if action_items:
        checklist_entries.extend(action_items)
    elif feedback_items:
        for f in feedback_items:
            if isinstance(f, dict) and f.get("how_to_fix"):
                checklist_entries.append(f"[{f.get('issue_title', 'Action')}] {f.get('how_to_fix')}")

    if unval_sk:
        for u in unval_sk[:6]:
            u_name = u.get("skill", str(u)) if isinstance(u, dict) else str(u)
            checklist_entries.append(f"Integrate '{u_name}' into a project bullet point with measurable results.")

    if checklist_entries:
        for item in checklist_entries:
            chk_table = Table([
                [Paragraph("<b>[  ]</b>", ParagraphStyle("Box", fontName="Helvetica", fontSize=8.5, textColor=colors.HexColor("#38BDF8"))),
                 Paragraph(f"<font color='#CBD5E1'>{item}</font>", bullet_style)]
            ], colWidths=[24, 516])
            chk_table.setStyle(TableStyle([
                ("PADDING", (0, 0), (-1, -1), 2),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]))
            story.append(chk_table)
    else:
        story.append(Paragraph("✓ No pending checklist tasks found. Your resume is in optimal condition.", body_style))

    # Build document with background canvas hooks
    doc.build(story, onFirstPage=_draw_cyber_background, onLaterPages=_draw_cyber_background)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes