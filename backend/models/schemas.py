from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


class ComponentScores(BaseModel):
    formatting: float = 0.0
    keywords: float = 0.0
    content: float = 0.0
    skill_validation: float = 0.0
    ats_compatibility: float = 0.0


class JDComparison(BaseModel):
    match_percentage: float = 0.0
    semantic_similarity: float = 0.0
    matched_keywords: List[str] = Field(default_factory=list)
    missing_keywords: List[str] = Field(default_factory=list)
    skills_gap: List[str] = Field(default_factory=list)


class SkillValidationDetails(BaseModel):
    validated: List[Union[Dict[str, Any], str]] = Field(default_factory=list)
    unvalidated: List[str] = Field(default_factory=list)
    total: int = 0
    validated_count: int = 0
    validation_pct: float = 0.0


class IssueDetail(BaseModel):
    issue_title: str = "Improvement"
    severity_level: str = "Medium"
    ats_impact: str = "Noticeable"
    explanation: str = ""
    where_it_appears: str = "General"
    how_to_fix: str = ""
    action_items: List[str] = Field(default_factory=list)
    example_improvement: str = ""


class AnalysisResponse(BaseModel):
    ATS_score: float = 0.0
    component_scores: ComponentScores
    issues_summary: List[str] = Field(default_factory=list)
    detailed_feedback: List[Union[IssueDetail, Dict[str, Any], str]] = Field(default_factory=list)
    jd_match_analysis: Optional[JDComparison] = None
    skill_validation_details: Optional[SkillValidationDetails] = None

    ats_score: float = 0.0
    keyword_match: float = 0.0
    missing_keywords: List[str] = Field(default_factory=list)
    matched_keywords: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    critical_issues: List[str] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    jd_comparison: Optional[JDComparison] = None
    warnings: List[str] = Field(default_factory=list)
    interpretation: str = ""