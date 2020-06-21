from .fb_requests import *
from .random_message import *
from .send_message import *
from .handle_nlp import *
from .handle_common import *

def send_message(db, recipient_id, text, message_rec, new_user):
    # sends user the text message provided via input response parameter
    """Send a response to Facebook"""
    if message_rec.get("quick_reply"):
        payload = handle_quickreply(db, recipient_id, message_rec["quick_reply"]["payload"])
    else:
        intent = handle_nlp(message_rec)
        if intent == "":
            intent = message_rec["text"]
        if intent == "Greeting":
            payload = handle_greeting(recipient_id,new_user)
        elif intent == "Talk to someone":
            payload = talk_to_someone(recipient_id, db)
        elif intent == "Book an appointment":
            payload = book_appointment("", recipient_id, db)
        elif intent == "color":
            payload = {
                "recipient": {"id": recipient_id},
                "messaging_type": "RESPONSE",
                "message": {"text": "Pick a color:", "quick_replies": replies["color"]},
            }
        elif intent == "Get a joke":
            payload = jokes_util(recipient_id,db)
        elif intent == "Get a quote":
            payload = get_quotes(recipient_id)
        elif intent == "Get music":
            payload = get_music(recipient_id)
        elif intent == "Get yoga":
            payload = getYoga_displayed(recipient_id)
        elif intent == "Get stories":
            payload = get_motiv_images(recipient_id)
        else:
            payload = {
                "message": {"text": text},
                "recipient": {"id": recipient_id},
                "notification_type": "regular",
            }
    send_request(payload)

def handle_normal_message(db,recipient_id,message, new_user):
    # Facebook Messenger ID for user so we know where to send response back to
    if (message["message"].get("attachments")):
        print("Attachment not supported")
    if message["message"].get("text"):
        response_sent_text = get_message()
        send_message(
            db, recipient_id, response_sent_text, message["message"], new_user 
        )