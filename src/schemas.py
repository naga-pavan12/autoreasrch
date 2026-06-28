from pydantic import BaseModel, Field
from typing import List, Optional, Any

class PainPoint(BaseModel):
    title: str = Field(description="A summarizeable name for the problem.")
    description: str = Field(description="A deep dive into why this matters.")
    evidence_quotes: List[str] = Field(description="Actual words from the user.")
    severity: str = Field(description="Impact: High, Medium, Low.")

class ExtractionSchema(BaseModel):
    pain_points: List[PainPoint]

class CompetitorProblem(BaseModel):
    competitor_name: str
    feature_gap: str
    user_frustration: str
    evidence_quote: str

class CompetitorSchema(BaseModel):
    problems: List[CompetitorProblem]

class IssueTheme(BaseModel):
    theme_name: str
    issue_count: int
    sample_tickets: List[str]
    root_cause: str

class ThemeSchema(BaseModel):
    themes: List[IssueTheme]

class Opportunity(BaseModel):
    rank: int
    name: str
    impact_score: int
    effort_estimate: str
    strategic_alignment: str

class OpportunitySchema(BaseModel):
    opportunities: List[Opportunity]
