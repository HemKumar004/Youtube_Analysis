# import os
# import tweepy
# from dotenv import load_dotenv

# def publish_tweet(text: str) -> dict:
#     # Force reload environment variables inside the function to guarantee fresh keys
#     # and bypass any uvicorn hot-reload caching issues.
#     load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.env")), override=True)
    
#     API_KEY = os.getenv("TWITTER_API_KEY")
#     API_SECRET = os.getenv("TWITTER_API_SECRET")
#     ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
#     ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

#     if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
#         raise ValueError("Missing Twitter/X API credentials in .env file.")
        
#     try:
#         # Twitter API v2 uses tweepy.Client
#         client = tweepy.Client(
#             consumer_key=API_KEY,
#             consumer_secret=API_SECRET,
#             access_token=ACCESS_TOKEN,
#             access_token_secret=ACCESS_TOKEN_SECRET
#         )
        
#         response = client.create_tweet(text=text)
#         return {
#             "success": True,
#             "tweet_id": response.data['id'],
#             "text": text
#         }
#     except Exception as e:
#         return {
#             "success": False,
#             "error": str(e)
#         }
import os
import tweepy
from dotenv import load_dotenv

# Load .env once
load_dotenv()

def publish_tweet(text: str):
    API_KEY = os.getenv("TWITTER_API_KEY")
    API_SECRET = os.getenv("TWITTER_API_SECRET")
    ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

    # Validate credentials
    if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
        raise Exception("Missing Twitter/X API credentials in .env file.")

    try:
        client = tweepy.Client(
            consumer_key=API_KEY,
            consumer_secret=API_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET
        )

        # Validate tweet content
        if not text or len(text.strip()) == 0:
            raise Exception("Tweet content cannot be empty")

        if len(text) > 280:
            raise Exception("Tweet exceeds 280 characters")

        # Create tweet
        response = client.create_tweet(text=text)

        return {
            "tweet_id": response.data["id"],
            "text": text
        }

    except Exception as e:
        print("🔥 TWITTER ERROR:", e)
        raise e   # IMPORTANT: don't return, raise it
        print("LOADED TOKEN:", os.getenv("TWITTER_ACCESS_TOKEN")[:10])