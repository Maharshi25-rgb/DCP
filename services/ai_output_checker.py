from typing import Any

from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv

from models.generic_workflow import GenericWorkflow


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# AI OUTPUT CHECK RESULT
# ============================================================

class AIOutputCheckResult(BaseModel):

    valid: bool

    confidence: float = Field(
        ge=0.0,
        le=1.0
    )

    issues: list[str] = Field(
        default_factory=list
    )

    contradictions: list[str] = Field(
        default_factory=list
    )

    unsupported_claims: list[str] = Field(
        default_factory=list
    )

    reasoning: str


# ============================================================
# AI OUTPUT CHECKER
# ============================================================

def check_ai_output(
    ai_response: Any,
    workflow: GenericWorkflow
):
    """
    Semantically evaluate an AI response against a workflow.

    The AI checker is a secondary semantic validation layer.

    Deterministic validation remains authoritative.
    """

    # ========================================================
    # BASIC RESPONSE VALIDATION
    # ========================================================

    if not isinstance(ai_response, str):

        return {
            "valid": False,
            "confidence": 0.0,
            "issues": [
                "AI response must be a string."
            ],
            "contradictions": [],
            "unsupported_claims": [],
            "reasoning": "Invalid response type."
        }

    if not ai_response.strip():

        return {
            "valid": False,
            "confidence": 0.0,
            "issues": [
                "AI response cannot be empty."
            ],
            "contradictions": [],
            "unsupported_claims": [],
            "reasoning": "Empty response."
        }

    # ========================================================
    # BUILD TRUSTED WORKFLOW CONTEXT
    # ========================================================

    workflow_context = []

    for field in workflow.fields:

        if field.value is not None:

            workflow_context.append({
                "field_name": field.field_name,
                "value": field.value,
                "source": field.source,
                "required": field.required
            })

    # ========================================================
    # OPENAI CLIENT
    # ========================================================

    client = OpenAI()

    # ========================================================
    # SYSTEM PROMPT
    # ========================================================

    system_prompt = """
You are the DCP AI Output Checker.

Your responsibility is to semantically evaluate an AI-generated
response against the trusted workflow supplied by DCP.

You are a secondary validation layer.

You must:

1. Check whether the response respects user-confirmed values.
2. Detect semantic contradictions.
3. Identify unsupported claims about user-provided information.
4. Evaluate whether the response is consistent with the workflow.
5. Return structured output only.

SECURITY RULES:

- User-confirmed values are authoritative.
- Never change or reinterpret user-confirmed values.
- If the response contradicts a user-confirmed value,
  report the contradiction.
- AI suggestions are not user-confirmed facts.
- Missing information must not be treated as user-provided.
- Do not invent facts to justify the response.
- If uncertain, report the uncertainty as an issue.
- Do not mark a response valid simply because it sounds reasonable.

IMPORTANT:

The deterministic DCP output validator is authoritative for
hard validation failures.

Your role is semantic verification.
"""

    # ========================================================
    # USER PROMPT
    # ========================================================

    user_prompt = f"""
TRUSTED WORKFLOW:

{workflow_context}

WORKFLOW TYPE:

{workflow.workflow_type}

ORIGINAL USER REQUEST:

{workflow.user_request}

AI RESPONSE:

{ai_response}

Evaluate the AI response against the trusted workflow.
"""

    # ========================================================
    # STRUCTURED OPENAI RESPONSE
    # ========================================================

    response = client.responses.parse(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        text_format=AIOutputCheckResult
    )

    result = response.output_parsed

    return result.model_dump()