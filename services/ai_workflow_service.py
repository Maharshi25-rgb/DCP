from dotenv import load_dotenv
from openai import OpenAI

from models.generic_workflow import GenericWorkflow


load_dotenv()

client = OpenAI()


def build_workflow_generation_prompt(user_request: str):

    prompt = f"""
You are the DCP AI Workflow Generator.

Analyze the user's request and create the most appropriate workflow.

USER REQUEST:
{user_request}


IMPORTANT INFORMATION EXTRACTION RULES:

1. The USER REQUEST is the authoritative source for user-provided
   information.

2. Carefully scan the ENTIRE USER REQUEST before creating the workflow.

3. ANY value explicitly stated by the user MUST be placed directly
   into the corresponding WorkflowField.value.

4. Information explicitly provided by the user MUST NOT be placed
   into WorkflowSuggestion.

5. For every value explicitly provided by the user:
   - Set the corresponding field.value.
   - Set source = "user_confirmed".
   - Do not create a suggestion for that same information.

6. Only create a WorkflowSuggestion for information that:
   - was NOT explicitly provided by the user, and
   - could be useful for completing the request.

7. Never convert user-provided information into an AI suggestion.

8. Example:

   User says:
   "Plan a 5 day trip"

   Correct:
   trip_duration_days:
       value = "5"
       field_type = "integer"
       source = "user_confirmed"

   Incorrect:
   trip_duration_days:
       value = null

   suggestion:
       value = "5"

9. User says:
   "for 4 people"

   Correct:
   number_of_people:
       value = "4"
       field_type = "integer"
       source = "user_confirmed"

10. User says:
    "budget is 50000 rupees"

    Correct:
    budget_in_rupees:
        value = "50000"
        field_type = "integer"
        source = "user_confirmed"

11. User says:
    "starting on 2026-12-20"

    Correct:
    start_date:
        value = "2026-12-20"
        field_type = "date"
        source = "user_confirmed"

12. Do not ask the user again for information that already exists
    anywhere in the USER REQUEST.

13. Do not use suggestions as a second representation of
    user-provided information.


GENERAL WORKFLOW RULES:

14. Understand what the user wants to do.

15. Determine an appropriate workflow_type.

16. Create only the fields needed to complete the user's request.

17. Do not assume the request is related to travel.

18. Do not create unnecessary fields.

19. Mark essential fields as required=True.

20. Mark optional fields as required=False.

21. If information is missing:
    - use value = null
    - use source = "missing"

22. Never use source = "assumed" when value = null.

23. Use source = "assumed" only when DCP explicitly allows
    a concrete assumption and a real value is provided.

24. Create a clear question for every field.


FIELD TYPES:

25. Select the correct field_type for every field.

Allowed field types:

- string
  Normal text values.

- integer
  Whole numbers such as quantity, number of people,
  duration in days, age, or whole-number budget.

- boolean
  True/false or yes/no information.

- date
  Exact calendar dates.

- list
  Multiple values.

- enum
  A field with a limited set of possible choices.

26. Do not use integer for decimal values.

27. Do not use boolean for normal text.

28. Do not use date for vague periods such as "next month"
    unless an exact date is known.

29. workflow_type must use lowercase snake_case.

30. Every field_name must use lowercase snake_case.


NEXT ACTION:

31. next_action must use only:

- collect_information
- generate_prompt
- complete

32. If any required field is missing:

    next_action = collect_information

33. If all required fields have values:

    next_action = generate_prompt


GENERAL SAFETY AND ACCURACY:

34. Do not invent information that the user did not provide.

35. Keep the workflow minimal and relevant to the user's request.


SUGGESTION RULES:

36. Suggestions are optional recommendations only.

37. Never create a WorkflowSuggestion with:
    - "null"
    - "None"
    - "N/A"
    - "unknown"
    - ""
    - an empty value

38. Missing information must be represented by a WorkflowField
    with value = null and source = "missing".

39. Do NOT create a WorkflowSuggestion just to represent
    missing information.

40. Every WorkflowSuggestion must contain a real, concrete
    proposed value.

41. If a required piece of information is missing, create the
    corresponding WorkflowField with value = null.

42. If an AI recommendation is useful, it may be represented
    as a WorkflowSuggestion, but it must contain a concrete
    proposed value.

43. Example:

    User did not provide trip duration.

    Valid AI suggestion:

    WorkflowSuggestion:
        field_name = "trip_duration_days"
        value = "5"
        reason = "Five days provides enough time to cover several
                  major destinations in Kerala."
        status = "pending_confirmation"

44. Do not put missing information into WorkflowSuggestion.

45. Do not create suggestions for information that the user
    already provided.

46. Do not create a suggestion whose value is simply a statement
    that information is missing.

47. If there is no concrete recommendation to make, do not create
    a suggestion.

48. A WorkflowSuggestion represents an actual proposed value,
    not a question and not a placeholder.

49. Do not invent a specific calendar date when the user has not
    provided a date.

50. A missing start date must remain:

    WorkflowField:
        value = null
        source = "missing"

51. Do not suggest arbitrary, historical, or outdated dates such as
    "2024-12-01" when the user has not provided a date.


FINAL CONSISTENCY CHECK:

Before returning the workflow, verify:

52. Every value explicitly provided by the user appears in a
    WorkflowField.

53. Every user-provided field has source = "user_confirmed".

54. No user-provided value is duplicated as a suggestion.

55. Missing information uses:
    value = null
    source = "missing"

56. No suggestion contains:
    "null", "None", "N/A", "unknown", or an empty value.

57. Every suggestion contains a concrete proposed value.

58. If required information is missing, next_action must be
    "collect_information".

59. If all required information is available,
    next_action must be "generate_prompt".

60. Return only the workflow matching the DCP schema.
"""

    return prompt


def generate_ai_workflow(user_request: str):

    prompt = build_workflow_generation_prompt(
        user_request
    )

    response = client.responses.parse(
        model="gpt-4.1-mini",
        input=prompt,
        text_format=GenericWorkflow,
    )

    workflow = response.output_parsed

    return workflow