from models.generic_workflow import (
    GenericWorkflow,
    WorkflowField,
)

from services.workflow_registry import (
    resolve_workflow_type,
    get_workflow_definition,
)


def normalize_workflow(
    workflow: GenericWorkflow
):
    """
    Normalize an AI-generated workflow against the
    canonical workflow registry.

    Known workflows:
        - Resolve aliases
        - Apply canonical field metadata
        - Add missing canonical fields

    Unknown workflows:
        - Preserve the dynamically generated workflow
    """

    # -----------------------------------------
    # 1. Resolve workflow type
    # -----------------------------------------

    canonical_type = resolve_workflow_type(
        workflow.workflow_type
    )

    # -----------------------------------------
    # 2. Unknown workflow
    # -----------------------------------------

    if canonical_type is None:

        return workflow

    # -----------------------------------------
    # 3. Normalize workflow type
    # -----------------------------------------

    workflow.workflow_type = canonical_type

    # -----------------------------------------
    # 4. Get canonical definition
    # -----------------------------------------

    definition = get_workflow_definition(
        canonical_type
    )

    if definition is None:

        return workflow

    canonical_fields = definition["fields"]

    # -----------------------------------------
    # 5. Index existing fields
    # -----------------------------------------

    existing_fields = {
        field.field_name: field
        for field in workflow.fields
    }

    # -----------------------------------------
    # 6. Apply canonical metadata
    # -----------------------------------------

    for field in workflow.fields:

        canonical_definition = canonical_fields.get(
            field.field_name
        )

        if canonical_definition is None:

            # Unknown field inside a known workflow.
            # Preserve it because DCP remains dynamic.
            continue

        field.field_type = canonical_definition[
            "field_type"
        ]

        field.required = canonical_definition[
            "required"
        ]

    # -----------------------------------------
    # 7. Add missing canonical fields
    # -----------------------------------------

    for field_name, canonical_definition in canonical_fields.items():

        if field_name in existing_fields:

            continue

        new_field = WorkflowField(

            field_name=field_name,

            value=None,

            field_type=canonical_definition[
                "field_type"
            ],

            required=canonical_definition[
                "required"
            ],

            question=(
                f"What is the {field_name.replace('_', ' ')}?"
            ),

            source="missing"
        )

        workflow.fields.append(new_field)

    return workflow