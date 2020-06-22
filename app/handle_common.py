# Also the capabilities
import random
from .fb_requests import *

def handle_greeting(recipient_id, new_user):
    message = ""
    if new_user:
        message = (
            "Hi there! Enter /help to view what I can do. How can I help you today?"
        )
    else:
        message = "Welcome back!!! How are you feeling today?"
    message += " "
    payload = {
        "recipient": {"id": recipient_id},
        "messaging_type": "RESPONSE",
        "message": {"text": message},
    }
    return payload

def handle_happy(recipient_id):
    lis = [
        "I am glad that you feel that way.",
        "Glad that you are happy.",
        "I like to see you this way.",
        "That is so good to hear!",
        "I am happy you feel good today"
    ]
    message = (
        lis[random.randint(0, 4)]
        + " Do you want to share something else? Or we could do something fun."
    )
    payload = {
        "recipient": {"id": recipient_id},
        "messaging_type": "RESPONSE",
        "message": {"text": message},
    }
    return payload


def handle_sad(recipient_id):
    lis = [
        "I am really sorry.",
        "It's really sad to hear this",
        "That makes me sad too."
    ]
    lis2 = [
        "Do you want me to cheer you up?",
        "I can try to cheer you up",
        "I have something in store to cheer you up"
    ]
    message = (
        lis[random.randint(0, 2)]
        + " Do you want to share what happened? " + lis2[random.randint(0, 2)]
    )
    payload = {
        "recipient": {"id": recipient_id},
        "messaging_type": "RESPONSE",
        "message": {"text": message},
    }
    return payload

def handle_happy_person(recipient_id):
    lis = [("joke", "Get a joke"), ("meme", "Get memes"), ("nice song", "Get music")]
    choice = lis[random.randint(0,2)]
    send_request({
        "recipient": {"id": recipient_id},
        "messaging_type": "RESPONSE",
        "message": {"text": "I have something planned for you. Here's a " + choice[0] + " for you"}
    })
    return choice[1]

def cheer_up(recipient_id):
    lis = [("joke", "Get a joke"), ("meme", "Get memes"), ("nice song", "Get music"), ("yoga video", "Get yoga"), ("motivational story", "Get stories") ]
    choice = lis[random.randint(0,4)]
    send_request({
        "recipient": {"id": recipient_id},
        "messaging_type": "RESPONSE",
        "message": {"text": "I have something planned for you. Here's a " + choice[0] + " for you"}
    })
    return choice[1]

def handle_sorry(recipient_id):
    payload = {
        "recipient": {"id": recipient_id},
        "messaging_type": "RESPONSE",
        "message": {"text": "I am really sorry. I wish I could help you next time."},
    }
    return payload

def handle_nice(recipient_id):
    payload = {
        "recipient": {"id": recipient_id},
        "messaging_type": "RESPONSE",
        "message": {"text": "I am really happy that you liked it"},
    }
    return payload

def handle_sad_negative(recipient_id):
    payload = {
        "recipient": {"id": recipient_id},
        "messaging_type": "RESPONSE",
        "message": {"text": "I am sorry that it didnt help you. I can also help you to talk to a fellow friend or talk with a psychiatrist."}
    }
    return payload

def confused_last_question(recipient_id):
    payload = {
        "recipient": {"id": recipient_id},
        "messaging_type": "RESPONSE",
        "message": {"text": "Umm.... I actually didn't get what you meant. Do you want me to connect you to a fellow friend?"}
    }
    return payload

def didnt_get(recipient_id):
    payload = {
        "recipient": {"id": recipient_id},
        "messaging_type": "RESPONSE",
        "message": {"text": "I actually didn't get what u said. Can you say it again?"}
    }
    return payload
def call_for_help(recipient_id):
    payload = {
        "recipient": {"id": recipient_id},
        "messaging_type":"RESPONSE",
        "message":{
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text":"National Suicide Prevention Helpline",
                    "buttons":[
                    {
                        "type":"phone_number",
                        "title":"Call for help",
                        "payload":"09152987821"
                    }]
                }
            }
        }
    }