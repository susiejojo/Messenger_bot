# Also the capabilities

def handle_greeting(recipient_id, new_user):
    message = ""
    if new_user:
        message = "Hi there!"
    else:
        message = "Welcome back!!!"
    message += " Enter /help to view what I can do."
    payload = {
        "recipient": {"id": recipient_id},
        "messaging_type": "RESPONSE",
        "message": {"text": message},
    }
    return payload
