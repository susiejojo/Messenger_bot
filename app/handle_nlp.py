import wit
from .config import WIT_INTENT, WIT_DEPRESS
from .fb_requests import send_request
from .handle_common import *

client_intent = wit.Wit(WIT_INTENT)
client_depress = wit.Wit(WIT_DEPRESS)

positive_list = ["yup","yeah","yes","that's right","sure","totally","cool","i'm in","thanks","works with me","amazing","great","yup","fine","alright","ok","okay"]
negative_list = ["no","nope","nah","that is insane","are you crazy?","what is wrong with you?","whatever","i don't want this","never","that's not right","that is bad","this makes no sense"]

def firstTrait(nlp, name):
    if nlp.get("traits"):
        return nlp["traits"][name] and nlp["traits"][name][0]

def secondTrait(nlp, name):
    if nlp.get("traits"):
        return nlp and nlp.get("traits") and nlp["traits"][name] and nlp["traits"][name][1]
    else:
        return None

def handle_nlp(db, recipient_id, message):
    greeting = firstTrait(message["nlp"], 'wit$greetings')
    sentiment = firstTrait(message["nlp"], 'wit$sentiment')
    print(sentiment and sentiment["value"],sentiment and sentiment["confidence"])
    last_convo = db.flow_convo.find_one({"user": recipient_id})["tag"]
    state = db.flow_convo.find_one({"user": recipient_id})["state"]
    if (greeting and greeting["confidence"] > 0.8):
        return "Greeting"
    intent_response = client_intent.message(message["text"])
    depress_response = client_depress.message(message["text"])
    depress_text = ''
    if depress_response['entities'].get('Happy:Happy'):
        depress_text = 'Happy'
    elif depress_response['entities'].get('Depressed:Depressed'):
        depress_text = 'Sad'
    elif depress_response['entities'].get('Suicidal:Suicidal'):
        depress_text = 'Suicidal' 
    print(depress_response)
    if intent_response.get('intents') and intent_response["intents"][0]["name"] == 'talk_to_someone' and intent_response["intents"][0]["confidence"]>0.7:
        print(intent_response) 
        return "Talk to someone"
    elif last_convo == "Confused last question" and sentiment["value"] == "positive":
        return "Talk to someone"
    elif intent_response.get('intents') and intent_response["intents"][0]["name"] == 'talk_to_psych' and intent_response["intents"][0]["confidence"]>0.7:
        print(intent_response) 
        return "Book an appointment"
    elif intent_response.get('intents') and intent_response["intents"][0]["name"] == 'get_yoga' and intent_response["intents"][0]["confidence"]>0.7:
        print(intent_response) 
        return "Get yoga"
    elif intent_response.get('intents') and intent_response["intents"][0]["name"] == 'get_quote' and intent_response["intents"][0]["confidence"]>0.7:
        print(intent_response) 
        return "Get a quote"
    elif intent_response.get('intents') and intent_response["intents"][0]["name"] == 'get_music' and intent_response["intents"][0]["confidence"]>0.7:
        print(intent_response) 
        return "Get music"
    elif intent_response.get('intents') and intent_response["intents"][0]["name"] == 'get_meme' and intent_response["intents"][0]["confidence"]>0.7:
        print(intent_response) 
        return "Get memes"
    elif intent_response.get('intents') and intent_response["intents"][0]["name"] == 'get_story' and intent_response["intents"][0]["confidence"]>0.7:
        print(intent_response) 
        return "Get stories"
    elif intent_response.get('intents') and intent_response["intents"][0]["name"] == 'cheer_up' and intent_response["intents"][0]["confidence"]>0.7:
        print(intent_response)
        return cheer_up(recipient_id)
    elif intent_response.get('intents') and intent_response["intents"][0]["name"] == 'bot_help' and intent_response["intents"][0]["confidence"]>0.7:
        print(intent_response)
        return "Bot info"
    elif intent_response.get('intents') and intent_response["intents"][0]["name"] == 'get_joke' and intent_response["intents"][0]["confidence"]>0.7:
        print(intent_response) 
        return "Get a joke"
    elif depress_text == "Happy":
        return "Happy"
    elif depress_text == "Sad":
        return "Sad"
    elif depress_text == "Suicidal":
        return "Suicidal"
    elif (state == "Suicidal" and (sentiment["value"] =="negative" or message["text"].lower() in negative_list)):
        return handle_suicidal_person(recipient_id,"no",db)
    elif state == "Suicidal" and last_convo == "book_appointment":
        return handle_suicidal_person(recipient_id,"book_appointment",db)
    elif ((sentiment["value"] == "positive" or message["text"].lower() in positive_list) and last_convo == "attachment" and state=="Suicidal"):
        return handle_suicidal_person(recipient_id,"nice",db)
    elif state == "Suicidal" and last_convo != "Suicidal":
        return handle_suicidal_person(recipient_id,"others",db)
    elif ((sentiment["value"] == "positive" or message["text"].lower() in positive_list) and last_convo == "attachment"):
        return "Nice"
    elif (last_convo == "Happy" and (sentiment["value"] == "positive" or message["text"].lower() in positive_list)):
        return handle_happy_person(recipient_id)
    elif (last_convo == "Sad" and (sentiment["value"] == "positive" or message["text"].lower() in positive_list)):            # can handle it someway else
        return cheer_up(recipient_id)
    elif (last_convo == "attachment" and (sentiment["value"] == "negative" or message["text"].lower() in negative_list) and state == "Sad"):
        return "Sad negative"
    elif (sentiment["value"] == "negative" or message["text"].lower() in negative_list):
        return "Sorry"
    else:
        if last_convo == "Sad negative":
            return "Confused last question"
        elif last_convo == "Suicidal":
            send_request({
            "recipient": {"id": recipient_id},
            "messaging_type": "RESPONSE",
            "message": {"text": "Let me schedule an appointment with a therapist for you."}
            })
            return "Book an appointment"
        else:
            return "Didn't get"