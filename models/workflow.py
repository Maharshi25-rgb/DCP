from pydantic import BaseModel
from typing import Dict, List


class Workflow(BaseModel):
    workflow_type: str
    user_request: str
    known_information: Dict[str, str]
    required_information: List[str]
    missing_information: List[str]
    questions: List[str]
    answers: Dict[str, str]
    next_action: str
    