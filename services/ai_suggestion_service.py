import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

from models.generic_workflow import GenericWorkflow, WorkflowSuggestion


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


class SuggestionResponse(BaseModel):

    suggestions: list[WorkflowSuggestion]


def build_suggestion_prompt(workflow: GenericWorkflow):

    confirmed_information = []

    for field in workflow.fields:

        if field.value is not None:
            confirmed_information.append(
                f"- {field.field_name}: {field.value}"
            )

    previous_suggestions = []

    for suggestion in workflow.suggestions:

        previous_suggestions.append(
            f"- {suggestion.value} "
            f"(status: {suggestion.status})"
        )

    confirmed_text = (
        "\n".join(confirmed_information)
        if confirmed_information
        else "None"
    )

    previous_text = (
        "\n".join(previous_suggestions)
        if previous_suggestions
        else "None"
    )

    prompt = f"""
You are the DCP AI Suggestion Generator.

Your job is to generate useful suggestions for the user's request.

USER REQUEST:
{workflow.user_request}

WORKFLOW TYPE:
{workflow.workflow_type}

INFORMATION ALREADY PROVIDED BY THE USER:
{confirmed_text}

PREVIOUS SUGGESTIONS:
{previous_text}

RULES:

1. Generate useful suggestions relevant to the user's request.
2. Do not repeat information already provided by the user.
3. Do not repeat previously rejected suggestions.
4. Do not repeat previously confirmed suggestions.
5. Do not treat suggestions as user-confirmed information.
6. Every suggestion must have:
   - field_name
   - value
   - reason
   - status
7. Always use status:
   pending_confirmation
8. Generate multiple suggestions when useful.
9. Do not create unnecessary suggestions.
10. Do not invent user preferences or requirements.
11. Suggestions are recommendations only and require explicit user confirmation.
"""

    return prompt


def generate_ai_suggestions(
    workflow: GenericWorkflow
):

    prompt = build_suggestion_prompt(workflow)

    response = client.responses.parse(
        model="gpt-4.1-mini",
        input=prompt,
        text_format=SuggestionResponse,
    )

    return response.output_parsed.suggestions