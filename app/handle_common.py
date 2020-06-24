# Also the capabilities
import random
from .fb_requests import *

def handle_greeting(recipient_id, new_user):
    message = ""
    if new_user:
        message = (
        "Hi there! I am CheerioBot.\nI can keep you entertained with songs,memes,jokes,quotes and connect you to fellow users\nor therapists if you feel depressed. I can schedule your appointments and put you through live chat with your therapist.\nI also work to detect hatespeech and sensitive information in your chats with others to maintain your privacy.\nWith me around, I promise you will never feel lonely! Anytime u feel like you are feeling upset, just let me know\nand I will do my magic on you!\nIf you are willing to know in details what all I am capable of, just go ahead and ask or type /help."
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

def handle_suicidal(recipient_id):
    lis = [
        "Hey, come on, that isn't a smart choice.",
        "I'm not letting you do that on my watch.",
        "Bad idea. I don't want to lose my friend."
    ]
    lis2 = [
        "Life is beautiful and can sometimes take unexpected turns, but that's not the end.",
        "There are many people who love you and care for you. Don't do this to them!",
        "You are far too precious to go like that."
    ]
    message = (
        lis[random.randint(0, 2)]
        + lis2[random.randint(0, 2)] +" I can book an appointment with a therapist for you or try to cheer you up in my own way! " 
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
        "message": {"text": "I am really sorry. I hope I can help you next time."},
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
        "message": {"text": "Umm.... I didn't get what you meant. Do you want me to connect you to a fellow friend?"}
    }
    return payload

def didnt_get(recipient_id):
    payload = {
        "recipient": {"id": recipient_id},
        "messaging_type": "RESPONSE",
        "message": {"text": "I didn't get what u said. Can you say it again?"}
    }
    return payload


def handle_suicidal_person(recipient_id,trigger,db):
    if (trigger=="no"):
        send_request({
            "recipient": {"id": recipient_id},
            "messaging_type": "RESPONSE",
            "message": {"text": "That's okay, but I'm not giving up on you. Let me put you in touch with people who may be able to help you feel better."}
            })

    elif (trigger=="book_appointment"):
        send_request({
            "recipient": {"id": recipient_id},
            "messaging_type": "RESPONSE",
            "message": {"text": "It may take a while till your appointment slot arrives. In the meanwhile, let me put you in touch with people who may be able to help you feel better."}
            })
    elif (trigger=="nice"):
        send_request(handle_nice(recipient_id))
        send_request({
            "recipient": {"id": recipient_id},
            "messaging_type": "RESPONSE",
            "message": {"text": "Let me put you in touch with people who may be able to help you even better than I can."}
            })
    else:
        send_request({
            "recipient": {"id": recipient_id},
            "messaging_type": "RESPONSE",
            "message": {"text": "I hope that was of help. Let me put you in touch with people who may be able to help you feel better."}
            })
    send_request(call_for_help(recipient_id))
    db.flow_convo.update_one({"user": recipient_id},{"$set":{"state":"Suicidal2"}})
    return "handle_suicide2"

def handle_suicide2(recipient_id):
    payload = {
        "recipient": {"id": recipient_id},
        "messaging_type": "RESPONSE",
        "message": {"text": "Please do call on the above number. It has worked magic on many others in such situations before!"}
    }
    return payload

def handle_hurt(recipient_id):
    payload = {
        "recipient": {"id": recipient_id},
        "messaging_type": "RESPONSE",
        "message": {"text": "Oww! I am hurt. Please be nice to me. I know you are not in the right mood."}
    }
    return payload
    
def handle_bye(recipient_id):
    payload = {
        "recipient": {"id": recipient_id},
        "messaging_type": "RESPONSE",
        "message": {"text": "It was really nice to talk with you. Let me know if you need any other help. See you soon!!!"}
    }
    return payload

def bot_info(recipient_id):
    payload = {
        "recipient": {"id": recipient_id},
        "messaging_type": "RESPONSE",
        "message": {"text": 
            "Hi, I am CheerioBot.\nI am here to help you in case you ever need someone to lift your spirits or just a friend to hang out with,\nand you can talk to me regardless of whether you feel happy or sad!\nI don't like to boast 😛 but here are a couple of things I can do for you:\nFetch jokes and learn which genres you prefer based on your ratings,\nFetch music from a curated Spotify playlist,\nFetch motivational quotes,\nFetch memes,\nFetch videos of yoga techniques,\nFetch motivational videos,\nConnect you to a fellow user if you want some company(I will keep all of your personal info safe, don't u worry!),\nBook an appointment with a therapist and connect you to him/her in your preferred slot.\nPlease refer to our Code of Conduct for expected behavior when you are chatting with another user or your therapist.\nI do take hatespeech seriously, and if you are uncomfortable, feel free to report your partner using /report,\nand I will put you in touch with one of our admins to explain your issue.\nHope I can be of help to you!!"}
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
                        #"payload": "+919474925889"
                        "payload":"+919152987821"
                    }]
                }
            }
        }
    }
    return payload