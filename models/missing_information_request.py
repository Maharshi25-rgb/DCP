from models.generic_workflow import GenericWorkflow

from pydantic import BaseModel


class MissingInformationRequest(BaseModel):
    workflow: GenericWorkflow
