import praw
import random
import requests
from .quick_replies import *
from .fb_requests import *
from .config import *
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
def get_quotes(recipient_id):
	motiv_api = "https://type.fit/api/quotes"
	response = requests.request("GET", motiv_api)
	#print (response.json())
	quote = response.json()[random.randint(0,1000)]["text"]
	payload = {
	"message": {"text": quote},
	"recipient": {"id": recipient_id},
	"notification_type": "regular",
	}
	return payload

def get_music(recipient_id):
	cid = ""
	secret = ""
	redir_url = "http://localhost:8888"
	payload = {
	"recipient": {"id": recipient_id},
	"notification_type": "regular",
	"message":{
    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"generic",
        "elements":[
           {
           "title":"Top song suggestions for you!",
           "image_url":"https://www.bensound.com/bensound-img/hipjazz.jpg",
           "default_action":{
           "type":"web_url",
           "url": "https://open.spotify.com/playlist/1j6WnMbAhQLZyjOYiWDxVB?si=tNbSXXdqTdeo-Z_hYcc9bw",
           "webview_height_ratio":"tall",
           },
            "buttons":[
              {
                "type":"web_url",
                "url":"https://open.spotify.com/playlist/1j6WnMbAhQLZyjOYiWDxVB?si=tNbSXXdqTdeo-Z_hYcc9bw",
                "title":"Play now!"
              }              
            ]      
          }
        ]
      }
    }
  }
	}
	return payload
def find_related_urls(title,website):
	try:
		from googlesearch import search 
	except ImportError:
		print("No module named 'google' found") 
	#print(title)
	related_urls = []
	query1 = website + title
	#print("Sugesstion")
	for q in search(query1, tld="com", num=10, stop=1, pause=2):
		#print(q)
		related_urls.append(q)
	return related_urls

def suggest_yoga():
	yoga_lst = ["Depression yoga","yoga asana practice for mind relaxation"]
	query = random.choice(yoga_lst)
	return find_related_urls(query,"youtube")
def getYoga_displayed(recipient_id):
	url = suggest_yoga()
	print (url[0])
	payload = {
		"message": {"text": "Here is a link to a yoga technique that may help you."},
		"recipient": {"id": recipient_id},
		"notification_type": "regular",
	}
	send_request(payload)
	payload_yoga = {
		"message": {"text": url[0]},
		"recipient": {"id": recipient_id},
		"notification_type": "regular",
	}
	return payload_yoga
def suggest_motiv():
	yoga_lst = ["Motivational stories","Inspirational stories"]
	query = random.choice(yoga_lst)
	return find_related_urls(query,"google")
def get_motiv_images(recipient_id):
	url = suggest_motiv()
	print (url[0])
	payload = {
		"message": {"text": "Why don't you go through this site I found? It has some interesting stories to keep you occupied."},
		"recipient": {"id": recipient_id},
		"notification_type": "regular",
	}
	send_request(payload)
	payload_motiv = {
		"message": {"text": url[0]},
		"recipient": {"id": recipient_id},
		"notification_type": "regular",
	}
	return payload_motiv
def get_meme(recipient_id):
	reddit = praw.Reddit(client_id=client_id,client_secret=client_secret,user_agent=user_agent)
	subreddit = reddit.subreddit('ProgrammerHumor')
	posts = subreddit.top(limit=20)
	image_urls = []
	for post in posts:
		image_urls.append(post.url)
	img_url = image_urls[random.randint(1, 19)]
	#print (img_url)
	payload = {
	#"recipient":{"id":recipient_id},
	"message":{
	"attachment":{
	  "type":"image", 
	  "payload":{
		"is_reusable": True,
		"url":img_url
	  }
	}
	}
	}
	response = send_url_request(payload)
	# print (response.json())
	payload_meme = {
	"recipient":{"id":recipient_id},
	  "message":{
		"attachment": {
		  "type": "template",
		  "payload": {
			 "template_type": "media",
			 "elements": [
				{
				   "media_type": "image",
				   "attachment_id": (response.json())["attachment_id"]
				}
			 ]
		  }
		}    
	  }
	}
	return payload_meme
