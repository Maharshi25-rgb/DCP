from typing import Any

from pydantic import BaseModel

from models.generic_workflow import GenericWorkflow


class WorkflowConfirmationRequest(BaseModel):
    workflow_id: str | None = None
    workflow: GenericWorkflow
    answers: dict[str, Any] = {}