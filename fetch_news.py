import requests

API_KEY = "d853da22e622496ea090b06a3bd37301"

url = (
    f"https://newsapi.org/v2/top-headlines?"
    f"country=us&apiKey={API_KEY}"
)

response = requests.get(url)

data = response.json()

for article in data["articles"]:
    print(article["title"])