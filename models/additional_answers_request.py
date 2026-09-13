from typing import Any

from pydantic import BaseModel, Field

from models.generic_workflow import GenericWorkflow


class AdditionalAnswersRequest(BaseModel):
    workflow: GenericWorkflow
    answers: dict[str, Any] = Field(default_factory=dict)
