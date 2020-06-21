import random
import requests
from .quick_replies import *
def jokes_util(recipient_id,db):
	#category = db.joke_categories.aggregate({"$group" : {"_id": null, max: {"$max" : "$score" }}})
	#category = db.joke_categories.find()
	joke_cats = ["yomama","chuck","programming","dad"]
	joke_c = db.user_status.find_one({"user":recipient_id})
	max_cat = ""
	joke = ""
	if (joke_c["joke_calls"]<4):
		max_cat = joke_cats[joke_c["joke_calls"]]
		db.user_status.update_one({"user":recipient_id},{"$inc":{"joke_calls":int(1)}})
		print (max_cat)
	else:
		category_data = db.joke_categories.find({"user":recipient_id})
		db.user_status.update_one({"user":recipient_id},{"$inc":{"joke_calls":int(1)}})
		sum_scores = 0
		weights = []
		for i in range(category_data.count()):
			score = category_data[i]["score"+str(i)]
			print (score)
			if (score>120):
				cat_tag = "score"+str(i)
				db.joke_categories.update_one({cat_tag:score},{"$set": {cat_tag: float(120)}})
				score = 100
			elif (score<20):
				cat_tag = "score"+str(i)
				print ("score<0 ",cat_tag,score)
				db.joke_categories.update_one({cat_tag:score},{"$set": {cat_tag: float(20)}})
				score = 0
			weights.append(score)
			sum_scores += score
		print (sum_scores)
		for j in range(len(weights)):
			weights[j]/=sum_scores
		cat = random.choices(population=[0,1,2,3],weights=weights,k=1)
		print (cat[0])
		max_cat = joke_cats[cat[0]]
		print ("max cat:",max_cat)
		
	if (max_cat=="chuck"):
		url = "http://api.icndb.com/jokes/random"
		resp = requests.get(url)
		resp.encoding = "utf-8"
		data = resp.json()
		joke = data["value"]["joke"]
	elif (max_cat=="programming"):
		url = "https://jokeapi-v2.p.rapidapi.com/joke/Any"
		querystring = {"format":"json","blacklistFlags":"nsfw","idRange":"0-150","type":"single"}

		headers = {
		    'x-rapidapi-host': "jokeapi-v2.p.rapidapi.com",
		    'x-rapidapi-key': "a6b6e74c76msh2bf08617fc0ad50p18382ajsne3b8b2aa7d59"
		    }

		response = requests.request("GET", url, headers=headers, params=querystring)
		joke = response.json()["joke"]
	elif (max_cat=="yomama"):
		url = "https://api.yomomma.info"
		response = requests.request("GET", url)
		print (response)
		joke = response.json()["joke"]
	elif (max_cat=="dad"):
		headers = {
		    'Accept': 'application/json',
		}
		response = requests.get('https://icanhazdadjoke.com', headers=headers)
		print (response.json())
		joke = response.json()["joke"]
	payload = {
	"message": {"text": joke,"quick_replies":get_joke_like(max_cat)},
    "recipient": {"id": recipient_id},
    "notification_type": "regular",
	}
	return payload