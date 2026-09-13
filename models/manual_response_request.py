from pydantic import BaseModel, Field

from models.generic_workflow import GenericWorkflow


class ManualResponseRequest(BaseModel):
    workflow: GenericWorkflow
    ai_response: str = Field(
        min_length=1,
        max_length=100000
    )
