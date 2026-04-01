from pydantic import BaseModel, Field
from typing import List, Optional, Union, Dict, Any

class TraceStep(BaseModel):
    step: int
    type: str = Field(..., description="E.g., planning, tool_use, reasoning")
    thought: Optional[str] = None
    decision_rationale: Optional[str] = None
    tool: Optional[str] = None
    input: Optional[str] = None
    output: Optional[str] = None
    observation: Optional[str] = None
    alternatives_considered: Optional[List[str]] = None
    chosen_approach: Optional[str] = None

class TraceMetadata(BaseModel):
    total_steps: int = 0
    tools_used: List[str] = Field(default_factory=list)
    reasoning_steps: int = 0
    planning_steps: int = 0
    tool_use_steps: int = 0
    success: bool = False
    quality_score: float = 0.0

class ReasoningTrace(BaseModel):
    task_id: str
    task_description: str
    trace: List[TraceStep] = Field(default_factory=list)
    metadata: TraceMetadata = Field(default_factory=TraceMetadata)

    def to_json(self) -> str:
        return self.model_dump_json(indent=2, exclude_none=True)
