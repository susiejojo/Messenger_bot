


def handle_happy_person(recipient_id):
    send_request(
        "recipient": {"id": recipient_id},
        "messaging_type": "RESPONSE",
        "message": {"text": "I have something planned for you. Here's a "},
    )