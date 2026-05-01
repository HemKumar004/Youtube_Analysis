import os
import sys
from dotenv import load_dotenv

# Force load the .env file in the exact same directory as this script
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, ".env")
load_dotenv(dotenv_path=env_path, override=True)

print("=== API Connectivity Test ===\n")

# 1. Test Twitter Credentials
print("Testing Twitter/X API...")
twitter_key = os.getenv("TWITTER_API_KEY")
twitter_secret = os.getenv("TWITTER_API_SECRET")
twitter_token = os.getenv("TWITTER_ACCESS_TOKEN")
twitter_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

if not all([twitter_key, twitter_secret, twitter_token, twitter_token_secret]):
    print("❌ FAILED: Missing one or more Twitter API keys in .env file.")
else:
    try:
        import tweepy
        client = tweepy.Client(
            consumer_key=twitter_key,
            consumer_secret=twitter_secret,
            access_token=twitter_token,
            access_token_secret=twitter_token_secret
        )
        # Verify credentials by getting the authenticated user
        me = client.get_me()
        if me and me.data:
            print(f"✅ SUCCESS: Connected to Twitter as @{me.data.username}")
        else:
            print("❌ FAILED: Twitter keys are present but authentication failed. Check if keys are valid.")
    except ImportError:
        print("❌ FAILED: 'tweepy' library is not installed.")
    except Exception as e:
        print(f"❌ FAILED: Twitter API error: {e}")

print("\n---------------------------\n")

# 2. Test Gemini API
print("Testing Google Gemini API...")
gemini_key = os.getenv("GEMINI_API_KEY")
if not gemini_key:
    print("❌ FAILED: Missing GEMINI_API_KEY in .env file.")
else:
    try:
        from google import genai
        from google.genai import types
        
        client = genai.Client(api_key=gemini_key)
        # Simple test to see if the client initializes and can ping the models
        models = client.models.list()
        print("✅ SUCCESS: Successfully authenticated with Gemini API!")
        print("✅ SUCCESS: The google-genai package is installed properly.")
    except ImportError:
        print("❌ FAILED: The 'google-genai' library is NOT installed. You must run: pip install google-genai")
    except Exception as e:
        print(f"❌ FAILED: Gemini API error: {e}")

print("\n===========================\n")
print("Test Complete.")
