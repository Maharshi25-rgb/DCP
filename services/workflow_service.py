from models.workflow import Workflow


def evaluate_workflow(workflow: Workflow):

    if workflow.missing_information:
        return {
            "status": "incomplete",
            "next_action": "request_user_decision",
            "missing_information": workflow.missing_information,
            "questions": workflow.questions,
            "options": [
                "provide_details",
                "proceed_anyway"
            ]
        }

    return {
        "status": "complete",
        "next_action": "generate_prompt",
        "message": "All required information is available."
    }
def handle_user_decision(workflow: Workflow, decision: str):

    if decision == "provide_details":
        return {
            "status": "waiting_for_details",
            "next_action": "ask_questions",
            "questions": workflow.questions,
            "missing_information": workflow.missing_information
        }

    if decision == "proceed_anyway":
        workflow.next_action = "generate_prompt"

        return {
            "status": "proceeding_with_assumptions",
            "next_action": "generate_prompt",
            "missing_information": workflow.missing_information,
            "message": "Proceeding with available information. Missing information will require assumptions."
        }

    return {
        "status": "error",
        "message": "Invalid decision."
    }