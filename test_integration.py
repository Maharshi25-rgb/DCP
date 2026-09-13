import json

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def print_result(test_name, response):
    print(f"\n{test_name}")
    print(f"Status code: {response.status_code}")

    try:
        print(json.dumps(response.json(), indent=2))
    except Exception:
        print(response.text)


def main():
    user_request = (
        "Renew the SSL certificate for api.example.com "
        "before it expires"
    )

    # ========================================================
    # TEST 1 — Generate workflow
    # ========================================================

    response = client.post(
        "/workflow/",
        json={
            "request": user_request
        },
    )

    print_result("TEST 1 — Generate workflow", response)

    assert response.status_code == 200, (
        f"Workflow generation failed: {response.text}"
    )

    workflow_result = response.json()
    workflow = workflow_result.get("workflow")

    assert workflow is not None, (
        "The response does not contain a workflow."
    )

    # ========================================================
    # TEST 2 — Confirm workflow fields
    # ========================================================

    response = client.post(
        "/workflow/confirm",
        json={
            "workflow": workflow,
            "confirmed_fields": {
                "domain_name": "api.example.com",
                "renew_before_expiry": True,
            },
        },
    )

    print_result("TEST 2 — Confirm workflow fields", response)

    assert response.status_code == 200, (
        f"Workflow confirmation failed: {response.text}"
    )

    confirmed_result = response.json()
    confirmed_workflow = confirmed_result.get("workflow")

    assert confirmed_workflow is not None, (
        "The confirmation response does not contain a workflow."
    )

    # ========================================================
    # TEST 3 — Generate prompt
    # ========================================================

    response = client.post(
        "/workflow/generate-prompt",
        json={
            "workflow": confirmed_workflow
        },
    )

    print_result("TEST 3 — Generate prompt", response)

    assert response.status_code == 200, (
        f"Prompt generation failed: {response.text}"
    )

    prompt_result = response.json()
    prompt = prompt_result.get("prompt")

    assert prompt is not None, (
        "The prompt response does not contain a prompt."
    )

    # ========================================================
    # TEST 4 — Generate final AI response
    # ========================================================

    response = client.post(
        "/workflow/generate-response",
        json={
            "workflow": confirmed_workflow,
            "prompt": prompt,
        },
    )

    print_result("TEST 4 — Generate final AI response", response)

    assert response.status_code == 200, (
        f"Final response generation failed: {response.text}"
    )

    final_result = response.json()

    assert final_result is not None, (
        "The final response is empty."
    )

    print("\nALL END-TO-END INTEGRATION TESTS PASSED")


if __name__ == "__main__":
    main()