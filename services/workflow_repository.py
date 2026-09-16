import json
from datetime import datetime

from sqlalchemy.orm import Session

from models.workflow_db import WorkflowDB


def save_workflow(
    db: Session,
    workflow_id: str,
    workflow_type: str,
    user_request: str,
    workflow_data: dict,
    status: str = "created",
) -> WorkflowDB:
    workflow = WorkflowDB(
        workflow_id=workflow_id,
        workflow_type=workflow_type,
        user_request=user_request,
        workflow_data=json.dumps(workflow_data),
        status=status,
    )

    db.add(workflow)
    db.commit()
    db.refresh(workflow)

    return workflow


def get_workflow_by_id(
    db: Session,
    workflow_id: str,
) -> WorkflowDB | None:
    return (
        db.query(WorkflowDB)
        .filter(WorkflowDB.workflow_id == workflow_id)
        .first()
    )


def get_all_workflows(
    db: Session,
) -> list[WorkflowDB]:
    return (
        db.query(WorkflowDB)
        .order_by(WorkflowDB.created_at.desc())
        .all()
    )


def update_workflow_status(
    db: Session,
    workflow_id: str,
    status: str,
) -> WorkflowDB | None:
    workflow = get_workflow_by_id(
        db=db,
        workflow_id=workflow_id,
    )

    if workflow is None:
        return None

    workflow.status = status
    workflow.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(workflow)

    return workflow