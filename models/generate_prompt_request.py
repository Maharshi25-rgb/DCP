from pydantic import BaseModel

from models.generic_workflow import GenericWorkflow


class GeneratePromptRequest(BaseModel):
    workflow: GenericWorkflow
