import requests
import os
import ast

TOP_HEADLINES_URL = "https://newsapi.org/v2/top-headlines"
EVERYTHING_URL = "https://newsapi.org/v2/everything"
SOURCES_URL = "https://newsapi.org/v2/sources"


api_key = os.environ["NEWS_API_KEY"]
auth = {"Content-Type": "Application/JSON", "Authorization": api_key}

payload = {}
payload["country"] = "US"
payload["apiKey"] = api_key

r = requests.get(TOP_HEADLINES_URL, timeout=30, params=payload)

# Check Status of Request
if r.status_code != requests.codes.ok:
    print(NewsAPIException(r.json()))

text = r.json()
print("There are {} headlines right now.".format(text["totalResults"]))
