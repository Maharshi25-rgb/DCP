from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

from models.generic_workflow import GenericWorkflow


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# CONFIGURATION
# ============================================================

REPAIR_MODEL = "gpt-4.1-mini"


# ============================================================
# REPAIR SERVICE
# ============================================================

def repair_ai_output(
    ai_response: Any,
    workflow: GenericWorkflow,
    validation_result: dict
):
    """
    Ask the AI model to repair an invalid response.

    SECURITY PRINCIPLE:

        The workflow is authoritative.

        The model may rewrite the response, but must not
        modify workflow facts.

    This service only generates a repaired response.

    The repaired response MUST be validated again by
    output_engine.py.
    """

    # ========================================================
    # INPUT VALIDATION
    # ========================================================

    if not isinstance(ai_response, str):

        return {
            "success": False,
            "response": None,
            "error": "AI response must be a string."
        }

    if not ai_response.strip():

        return {
            "success": False,
            "response": None,
            "error": "AI response cannot be empty."
        }

    if not isinstance(validation_result, dict):

        return {
            "success": False,
            "response": None,
            "error": "Validation result must be a dictionary."
        }

    # ========================================================
    # BUILD AUTHORITATIVE WORKFLOW
    # ========================================================

    authoritative_fields = []

    for field in workflow.fields:

        if field.value is None:
            continue

        authoritative_fields.append({
            "field_name": field.field_name,
            "value": field.value,
            "source": field.source,
            "required": field.required
        })

    # ========================================================
    # CLIENT
    # ========================================================

    client = OpenAI()

    # ========================================================
    # SYSTEM PROMPT
    # ========================================================

    system_prompt = """
You are the DCP AI Output Repair Service.

Your task is to repair an AI-generated response that failed
DCP output validation.

SECURITY RULES:

1. The workflow supplied by DCP is AUTHORITATIVE.
2. User-confirmed values MUST NOT be changed.
3. You MUST NOT invent user-provided values.
4. You MUST NOT change destination, people count, duration,
   budget, dates, or any other authoritative workflow value.
5. Repair the response itself, not the workflow.
6. Remove contradictions.
7. Preserve useful information from the original response
   when it remains consistent.
8. Do not mention internal DCP validation mechanisms.
9. Return only the repaired user-facing response.

The repaired response will be independently validated again.
"""

    # ========================================================
    # REPAIR REQUEST
    # ========================================================

    repair_prompt = f"""
AUTHORITATIVE WORKFLOW:

{authoritative_fields}

WORKFLOW TYPE:

{workflow.workflow_type}

ORIGINAL USER REQUEST:

{workflow.user_request}

ORIGINAL AI RESPONSE:

{ai_response}

VALIDATION FAILURE:

{validation_result}

TASK:

Rewrite the AI response so that it complies with the
authoritative workflow.

Do not change any authoritative workflow values.

Return only the repaired response.
"""

    # ========================================================
    # CALL MODEL
    # ========================================================

    response = client.responses.create(
        model=REPAIR_MODEL,
        input=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": repair_prompt
            }
        ]
    )

    # ========================================================
    # EXTRACT RESPONSE
    # ========================================================

    repaired_response = response.output_text

    if not repaired_response:

        return {
            "success": False,
            "response": None,
            "error": "Model returned an empty response."
        }

    return {
        "success": True,
        "response": repaired_response.strip(),
        "error": None
    }