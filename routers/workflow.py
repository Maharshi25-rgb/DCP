import json
import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db

from models.workflow_request import WorkflowRequest
from models.workflow_confirmation_request import WorkflowConfirmationRequest
from models.additional_answers_request import AdditionalAnswersRequest
from models.generate_prompt_request import GeneratePromptRequest
from models.generate_response_request import GenerateResponseRequest

from services.ai_workflow_service import generate_ai_workflow
from services.ai_response_service import generate_ai_response
from services.input_security_service import check_input_security
from services.workflow_engine import process_workflow
from services.trusted_user_context import build_trusted_user_context
from services.prompt_service import build_prompt
from services.output_engine import process_ai_output
from services.workflow_repository import (
    save_workflow,
    get_workflow_by_id,
)


router = APIRouter(
    prefix="/workflow",
    tags=["Workflow"],
)


def normalize_field_value(field_type: str, value: Any):
    """
    Convert incoming values into a consistent string format.
    """

    if value is None:
        return None

    if field_type == "integer":
        return str(int(value))

    if field_type == "boolean":
        return str(bool(value)).lower()

    if field_type == "list":
        if isinstance(value, list):
            return ", ".join(str(item) for item in value)

        return str(value)

    return str(value)


def merge_answers_into_workflow(
    workflow,
    answers: dict[str, Any],
):
    """
    Update workflow fields using user-provided answers.
    """

    for field in workflow.fields:
        if field.field_name in answers:
            field.value = normalize_field_value(
                field.field_type,
                answers[field.field_name],
            )

            field.source = "user_confirmed"

    return workflow


def build_context_from_workflow(workflow):
    """
    Preserve all previously confirmed values as trusted context.
    """

    confirmed_fields = {}

    for field in workflow.fields:
        if (
            field.source == "user_confirmed"
            and field.value is not None
        ):
            confirmed_fields[field.field_name] = field.value

    return build_trusted_user_context(confirmed_fields)


def synchronize_next_action(workflow_result: dict):
    """
    Synchronize workflow.next_action with evaluation.next_action.
    """

    workflow = workflow_result.get("workflow")
    evaluation = workflow_result.get("evaluation", {})

    if workflow is None or not evaluation:
        return workflow_result

    next_action = evaluation.get("next_action")

    if next_action:
        workflow.next_action = next_action

    return workflow_result


@router.post("")
def create_workflow(
    data: WorkflowRequest,
    db: Session = Depends(get_db),
):
    """
    Generate a workflow from the user's request
    and save it in the SQLite database.
    """

    security_result = check_input_security(data.request)

    if not security_result["secure"]:
        return {
            "status": "blocked",
            "security": security_result,
        }

    workflow = generate_ai_workflow(data.request)

    workflow_id = str(uuid.uuid4())

    saved_workflow = save_workflow(
        db=db,
        workflow_id=workflow_id,
        workflow_type=workflow.workflow_type,
        user_request=workflow.user_request,
        workflow_data=workflow.model_dump(),
        status="awaiting_confirmation",
    )

    return {
        "status": "awaiting_confirmation",
        "security": security_result,
        "workflow_id": saved_workflow.workflow_id,
        "workflow": workflow,
    }


@router.get("/{workflow_id}")
def get_saved_workflow(
    workflow_id: str,
    db: Session = Depends(get_db),
):
    """
    Retrieve a saved workflow from SQLite by workflow ID.
    """

    workflow = get_workflow_by_id(
        db=db,
        workflow_id=workflow_id,
    )

    if workflow is None:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found",
        )

    try:
        workflow_data = json.loads(workflow.workflow_data)
    except json.JSONDecodeError:
        workflow_data = workflow.workflow_data

    return {
        "id": workflow.id,
        "workflow_id": workflow.workflow_id,
        "workflow_type": workflow.workflow_type,
        "user_request": workflow.user_request,
        "status": workflow.status,
        "workflow_data": workflow_data,
        "created_at": workflow.created_at,
        "updated_at": workflow.updated_at,
    }


@router.post("/confirm")
def confirm_workflow(
    data: WorkflowConfirmationRequest,
):
    """
    Confirm workflow fields using user answers.
    """

    workflow = merge_answers_into_workflow(
        data.workflow,
        data.answers,
    )

    trusted_context = build_context_from_workflow(workflow)

    workflow_result = process_workflow(
        workflow,
        trusted_user_context=trusted_context,
    )

    workflow_result = synchronize_next_action(
        workflow_result,
    )

    return workflow_result


@router.post("/missing-information")
def get_missing_information(
    data: WorkflowConfirmationRequest,
):
    """
    Return missing required and optional fields.
    """

    workflow = merge_answers_into_workflow(
        data.workflow,
        data.answers,
    )

    trusted_context = build_context_from_workflow(workflow)

    workflow_result = process_workflow(
        workflow,
        trusted_user_context=trusted_context,
    )

    workflow_result = synchronize_next_action(
        workflow_result,
    )

    if workflow_result["status"] != "valid":
        return workflow_result

    evaluation = workflow_result.get("evaluation", {})

    return {
        "status": "valid",
        "workflow": workflow_result["workflow"],
        "missing_required_fields": evaluation.get(
            "missing_required_fields",
            [],
        ),
        "optional_missing_fields": evaluation.get(
            "optional_missing_fields",
            [],
        ),
        "next_action": evaluation.get("next_action"),
    }


@router.post("/additional-answers")
def submit_additional_answers(
    data: AdditionalAnswersRequest,
):
    """
    Add additional answers to an existing workflow.
    """

    workflow = merge_answers_into_workflow(
        data.workflow,
        data.answers,
    )

    trusted_context = build_context_from_workflow(workflow)

    workflow_result = process_workflow(
        workflow,
        trusted_user_context=trusted_context,
    )

    workflow_result = synchronize_next_action(
        workflow_result,
    )

    return workflow_result


@router.post("/generate-prompt")
def generate_workflow_prompt(
    data: GeneratePromptRequest,
):
    """
    Generate the final prompt for an AI model.
    """

    workflow = data.workflow

    trusted_context = build_context_from_workflow(workflow)

    workflow_result = process_workflow(
        workflow,
        trusted_user_context=trusted_context,
    )

    workflow_result = synchronize_next_action(
        workflow_result,
    )

    if workflow_result["status"] != "valid":
        return workflow_result

    evaluation = workflow_result.get("evaluation", {})

    if evaluation.get("status") != "complete":
        return {
            "status": "incomplete",
            "message": (
                "Complete all required fields "
                "before generating a prompt."
            ),
            "workflow": workflow_result["workflow"],
            "missing_required_fields": evaluation.get(
                "missing_required_fields",
                [],
            ),
        }

    prompt = build_prompt(
        workflow_result["workflow"],
    )

    return {
        "status": "prompt_generated",
        "workflow": workflow_result["workflow"],
        "prompt": prompt,
    }


@router.post("/generate-response")
def generate_workflow_response(
    data: GenerateResponseRequest,
):
    """
    Generate and validate the final AI response.
    """

    workflow = data.workflow

    trusted_context = build_context_from_workflow(workflow)

    workflow_result = process_workflow(
        workflow,
        trusted_user_context=trusted_context,
    )

    workflow_result = synchronize_next_action(
        workflow_result,
    )

    if workflow_result["status"] != "valid":
        return workflow_result

    evaluation = workflow_result.get("evaluation", {})

    if evaluation.get("status") != "complete":
        return {
            "status": "incomplete",
            "message": (
                "Complete all required fields "
                "before generating a response."
            ),
            "workflow": workflow_result["workflow"],
            "missing_required_fields": evaluation.get(
                "missing_required_fields",
                [],
            ),
        }

    prompt = build_prompt(
        workflow_result["workflow"],
    )

    ai_response = generate_ai_response(prompt)

    output_result = process_ai_output(
        ai_response,
        workflow_result["workflow"],
    )

    return {
        "status": output_result.get("status"),
        "workflow": workflow_result["workflow"],
        "prompt": prompt,
        "output": output_result,
    }