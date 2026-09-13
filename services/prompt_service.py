from models.generic_workflow import GenericWorkflow


def build_prompt(workflow: GenericWorkflow) -> str:
    """
    Build a concise prompt from a validated workflow.
    """

    confirmed_information = []
    optional_missing_information = []

    for field in workflow.fields:
        if field.value is not None:
            confirmed_information.append(
                f"- {field.field_name}: {field.value}"
            )

        elif not field.required:
            optional_missing_information.append(
                f"- {field.field_name}"
            )

    if confirmed_information:
        confirmed_text = "\n".join(confirmed_information)
    else:
        confirmed_text = "None"

    if optional_missing_information:
        optional_text = "\n".join(optional_missing_information)
    else:
        optional_text = "None"

    prompt = f"""
You are an AI assistant generating a response for the following request.

Workflow type:
{workflow.workflow_type}

User request:
{workflow.user_request}

Confirmed information:
{confirmed_text}

Optional information not provided:
{optional_text}

Instructions:
1. Use confirmed information as authoritative.
2. Do not invent user preferences or requirements.
3. Treat optional missing information as unknown.
4. Clearly label any assumptions.
5. Provide a practical and structured response.
6. Do not mention DCP or internal workflow processes.

Generate the final response.
""".strip()

    return prompt