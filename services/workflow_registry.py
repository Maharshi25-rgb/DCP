from typing import Optional


# =========================================
# Canonical workflow registry
# =========================================

WORKFLOW_REGISTRY = {

    "travel_planning": {

        "aliases": [
            "trip_planning",
            "vacation_planning",
            "holiday_planning"
        ],

        "fields": {

            "destination": {
                "field_type": "string",
                "required": True
            },

            "start_date": {
                "field_type": "date",
                "required": True
            },

            "end_date": {
                "field_type": "date",
                "required": False
            },

            "number_of_people": {
                "field_type": "integer",
                "required": True
            },

            "trip_duration_days": {
                "field_type": "integer",
                "required": True
            },

            "budget": {
                "field_type": "integer",
                "required": False
            }
        }
    },


    "image_generation": {

        "aliases": [
            "image_creation",
            "image_generator"
        ],

        "fields": {

            "subject": {
                "field_type": "string",
                "required": True
            },

            "style": {
                "field_type": "string",
                "required": False
            },

            "aspect_ratio": {
                "field_type": "enum",
                "required": False
            }
        }
    },


    "interview_preparation": {

        "aliases": [
            "interview_prep",
            "job_interview_preparation"
        ],

        "fields": {

            "job_role": {
                "field_type": "string",
                "required": True
            },

            "experience_level": {
                "field_type": "string",
                "required": False
            },

            "technology": {
                "field_type": "list",
                "required": False
            }
        }
    }
}


# =========================================
# Resolve workflow type
# =========================================

def resolve_workflow_type(
    workflow_type: str
) -> Optional[str]:

    normalized = workflow_type.strip().lower()

    # Direct canonical match
    if normalized in WORKFLOW_REGISTRY:

        return normalized

    # Alias match
    for canonical_name, definition in WORKFLOW_REGISTRY.items():

        aliases = definition.get("aliases", [])

        if normalized in aliases:

            return canonical_name

    # Unknown workflow
    return None


# =========================================
# Get workflow definition
# =========================================

def get_workflow_definition(
    workflow_type: str
):

    canonical_type = resolve_workflow_type(
        workflow_type
    )

    if canonical_type is None:

        return None

    return WORKFLOW_REGISTRY[
        canonical_type
    ]