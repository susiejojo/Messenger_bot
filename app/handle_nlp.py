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
