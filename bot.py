import tweepy
import requests
import time
import schedule
from datetime import datetime
from openai import OpenAI
import os

# ====== READ KEYS FROM ENVIRONMENT (SECURE) ======
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

ai = OpenAI(api_key=OPENAI_API_KEY)

client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

def get_trending_topic():
    url = "https://trends.google.com/trends/api/dailytrends?geo=IN"
    r = requests.get(url)
    data = r.text[5:]
    import json
    j = json.loads(data)
    return j["default"]["trendingSearchesDays"][0]["trendingSearches"][0]["title"]["query"]

def generate_tweet(topic):
    prompt = f"Write one viral Hinglish tweet on: {topic}. Add emotion, hook and hashtags. Max 260 chars."
    response = ai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )
    return response.choices[0].message.content.strip()

def post_tweet():
    try:
        topic = get_trending_topic()
        tweet = generate_tweet(topic)
        client.create_tweet(text=tweet)
        print(f"[{datetime.now()}] Posted: {tweet}")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    print("AI Trend Bot (GitHub Actions Mode) Running...")
    post_tweet()
    print("Tweet posted, job finished.")
