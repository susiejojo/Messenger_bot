import wit
from .config import WIT_INTENT
client_intent = wit.Wit(WIT_INTENT)

def firstTrait(nlp, name):
    return nlp and nlp["traits"][name] and nlp["traits"][name][0]

def handle_nlp(message):
    greeting = firstTrait(message["nlp"], 'wit$greetings')
    if (greeting and greeting["confidence"] > 0.8):
        return "Greeting"
    intent_response = client_intent.message(message["text"])
    if intent_response.get('intents') and intent_response["intents"][0]["name"] == 'talk_to_someone' and intent_response["intents"][0]["confidence"]>0.7:
        print(intent_response) 
        return "Talk to someone"
    if intent_response.get('intents') and intent_response["intents"][0]["name"] == 'talk_to_psych' and intent_response["intents"][0]["confidence"]>0.7:
        print(intent_response) 
        return "Book an appointment"
    if intent_response.get('intents') and intent_response["intents"][0]["name"] == 'get_yoga' and intent_response["intents"][0]["confidence"]>0.7:
        print(intent_response) 
        return "Get yoga"
    if intent_response.get('intents') and intent_response["intents"][0]["name"] == 'get_quote' and intent_response["intents"][0]["confidence"]>0.7:
        print(intent_response) 
        return "Get a quote"
    if intent_response.get('intents') and intent_response["intents"][0]["name"] == 'get_music' and intent_response["intents"][0]["confidence"]>0.7:
        print(intent_response) 
        return "Get music"
    if intent_response.get('intents') and intent_response["intents"][0]["name"] == 'get_meme' and intent_response["intents"][0]["confidence"]>0.7:
        print(intent_response) 
        return "Get meme"
    if intent_response.get('intents') and intent_response["intents"][0]["name"] == 'get_story' and intent_response["intents"][0]["confidence"]>0.7:
        print(intent_response) 
        return "Get stories"
    if intent_response.get('intents') and intent_response["intents"][0]["name"] == 'get_joke' and intent_response["intents"][0]["confidence"]>0.7:
        print(intent_response) 
        return "Get a joke"
