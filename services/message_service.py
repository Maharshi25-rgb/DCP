def process_message(message: str):

    message = message.lower()

    if "travel" in message:
        result = "DCP detected a travel-related request."

    elif "security" in message:
        result = "DCP detected a cybersecurity-related request."

    else:
        result = "DCP could not identify the request category."

    return result