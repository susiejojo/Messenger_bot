from .config import ACCTOKEN
import requests

FB_API_URL = "https://graph.facebook.com/v7.0/me/messages"
FB_ATTACH_URL = "https://graph.facebook.com/v7.0/me/message_attachments"
FB_PERSONA_URL = "https://graph.facebook.com/me/personas"
FB_HANDOVER_URL = "https://graph.facebook.com/v7.0/me/pass_thread_control"
FB_TAKE_URL = "https://graph.facebook.com/v7.0/me/take_thread_control"
FB_PROFILE_URL = "https://graph.facebook.com/v7.0/me/messenger_profile"
def send_request(payload):
    auth = {"access_token": ACCTOKEN}
    print("Payload:")
    print(payload)
    response = requests.post(FB_API_URL, params=auth, json=payload)
    print(response, response.json())
    return "success"

def send_persona_request(payload):
    auth = {"access_token": ACCTOKEN}
    response = requests.post(FB_PERSONA_URL, params=auth, json=payload)
    print (response.json())
    persona_id =  response.json()["id"]
    return persona_id
def send_handover_request(payload):
    auth = {"access_token": ACCTOKEN}
    response = requests.post(FB_HANDOVER_URL, params=auth, json=payload)
    return "success"
def take_handover_request(payload,recipient_id):
    auth = {"access_token": ACCTOKEN}
    response = requests.post(FB_TAKE_URL, params=auth, json=payload)
    payload_end = {
        "recipient": {"id": recipient_id},
        "messaging_type": "RESPONSE",
        "message": {"text": "The live chat with the admin ended. Hope we could do justice to your issue!"},
    }
    send_request(payload_end)
    return "success"
def send_url_request(payload):
    auth = {"access_token": ACCTOKEN}
    response = requests.post(FB_ATTACH_URL, params=auth, json=payload)
    return response