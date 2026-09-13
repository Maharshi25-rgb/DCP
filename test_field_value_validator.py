from services.field_value_validator import validate_field_value


def run_test(test_name, value, field_type):

    result = validate_field_value(
        value=value,
        field_type=field_type
    )

    print(f"\n{test_name}")
    print(f"Value: {value}")
    print(f"Type: {field_type}")
    print(f"Result: {result}")


# =========================================
# STRING
# =========================================

run_test(
    "String - Valid",
    "Kerala",
    "string"
)

run_test(
    "String - Invalid",
    "",
    "string"
)


# =========================================
# INTEGER
# =========================================

run_test(
    "Integer - Valid",
    4,
    "integer"
)

run_test(
    "Integer - Valid String",
    "4",
    "integer"
)

run_test(
    "Integer - Invalid",
    "four",
    "integer"
)


# =========================================
# BOOLEAN
# =========================================

run_test(
    "Boolean - Valid",
    True,
    "boolean"
)

run_test(
    "Boolean - Valid String",
    "true",
    "boolean"
)

run_test(
    "Boolean - Invalid",
    "maybe",
    "boolean"
)


# =========================================
# DATE
# =========================================

run_test(
    "Date - Valid",
    "2026-12-20",
    "date"
)

run_test(
    "Date - Invalid",
    "20-12-2026",
    "date"
)


# =========================================
# LIST
# =========================================

run_test(
    "List - Valid",
    ["Munnar", "Kochi"],
    "list"
)

run_test(
    "List - Valid String",
    "Munnar, Kochi",
    "list"
)

run_test(
    "List - Invalid",
    "",
    "list"
)


# =========================================
# ENUM
# =========================================

run_test(
    "Enum - Valid",
    "luxury",
    "enum"
)

run_test(
    "Enum - Invalid",
    "",
    "enum"
)


# =========================================
# UNSUPPORTED TYPE
# =========================================

run_test(
    "Unsupported Type",
    "Kerala",
    "float"
)