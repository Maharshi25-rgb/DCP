from pydantic import BaseModel, Field
from typing import Optional, Literal


class WorkflowField(BaseModel):

    field_name: str

    value: Optional[str] = None

    field_type: Literal[
        "string",
        "integer",
        "boolean",
        "date",
        "list",
        "enum"
    ] = "string"

    required: bool = True

    question: str

    source: Literal[
    "user_confirmed",
    "ai_suggested",
    "assumed",
    "missing"
] = "missing"


class WorkflowSuggestion(BaseModel):

    field_name: str

    value: str

    reason: str

    status: Literal[
        "pending_confirmation",
        "user_confirmed",
        "rejected"
    ] = "pending_confirmation"


class GenericWorkflow(BaseModel):

    workflow_type: str

    user_request: str

    fields: list[WorkflowField]

    suggestions: list[WorkflowSuggestion] = Field(
        default_factory=list
    )

    next_action: str