import os
import time
import emoji
from openai import OpenAI
import tweepy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize API clients
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    print("Error: OPENAI_API_KEY is not set.")
    exit(1)
client = OpenAI(api_key=openai_api_key)

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

if not all([TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET]):
    print("Error: Twitter/X API credentials are not set.")
    exit(1)

twitter_client = tweepy.Client(
    consumer_key=TWITTER_API_KEY,
    consumer_secret=TWITTER_API_SECRET,
    access_token=TWITTER_ACCESS_TOKEN,
    access_token_secret=TWITTER_ACCESS_TOKEN_SECRET
)

def has_emojis(text: str) -> bool:
    """Check if the text contains at least one emoji."""
    for char in text:
        if char in emoji.EMOJI_DATA:
            return True
    return False

def generate_validated_post(topic: str, max_retries: int = 3) -> str:
    """
    Agentic Workflow step:
    Generates a social media post and validates it against rules.
    If it fails validation, feeds the feedback back to the LLM to correct.
    """
    print(f"\n[Agent] Starting post generation for topic: '{topic}'")
    system_prompt = (
        "You are an expert social media manager. Generate a highly creative, engaging, "
        "and conversational social media post about the requested topic. "
        "RULES:\n"
        "1. Maximum length is strictly 200 characters.\n"
        "2. MUST include at least one fun emoji (e.g., 🔥😂🎯🚀).\n"
        "3. Tone must be fun, slightly dramatic, or catchy. Never robotic."
    )
    
    current_prompt = f"Create a short, fun tweet about: {topic}"
    
    for attempt in range(1, max_retries + 1):
        print(f"[Agent] Attempt {attempt} to generate post...")
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": current_prompt}
                ],
                max_tokens=60,
                temperature=0.8
            )
            post_text = response.choices[0].message.content.strip()
        except Exception as e:
            if "insufficient_quota" in str(e) or "429" in str(e):
                print("[Agent] WARNING: OpenAI Quota Exceeded. Using fallback mock post.")
                post_text = f"Exploring {topic} has never been more exciting! 🚀 The future is here and it's amazing. 🔥 What are your thoughts? 👇 #Tech"
            else:
                raise e

        print(f"[Agent] Generated Draft: '{post_text}' (Length: {len(post_text)})")
        
        # Validation
        errors = []
        if len(post_text) > 200:
            errors.append(f"Length is {len(post_text)} characters, which exceeds the 200 character limit.")
        if not has_emojis(post_text):
            errors.append("Missing emojis. You MUST include emojis.")
            
        if not errors:
            print("[Agent] Validation PASSED. ✅")
            return post_text
        
        # Feedback loop
        print(f"[Agent] Validation FAILED: {', '.join(errors)} ❌")
        if attempt < max_retries:
            print("[Agent] Feeding back errors to LLM for correction...")
            current_prompt = (
                f"Your previous attempt ('{post_text}') failed these rules: {', '.join(errors)}. "
                f"Please try again for the topic '{topic}' and fix these issues."
            )
        else:
            print("[Agent] Max retries reached. Returning best effort.")
            return post_text

def generate_image_prompt(topic: str, post_content: str) -> str:
    """Generate a visual concept (Midjourney/DALL-E prompt) based on the post."""
    print("\n[Agent] Generating image prompt concept...")
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a creative director. Given a social media post, generate a highly detailed and creative text prompt for an AI image generator (like Midjourney). Focus on mood, colors, and scene composition."},
                {"role": "user", "content": f"Topic: {topic}\nPost: {post_content}\nGenerate a matching image prompt."}
            ],
            max_tokens=100,
            temperature=0.7
        )
        image_prompt = response.choices[0].message.content.strip()
    except Exception as e:
        if "insufficient_quota" in str(e) or "429" in str(e):
            print("[Agent] WARNING: OpenAI Quota Exceeded. Using fallback mock image prompt.")
            image_prompt = f"A futuristic and cinematic visualization of {topic}, vibrant colors, neon lights, highly detailed, photorealistic, 8k resolution, unreal engine 5 render, dramatic lighting, cyberpunk aesthetic."
        else:
            raise e
            
    print("[Agent] Image prompt generated. ✅")
    return image_prompt

def publish_to_twitter(post_content: str):
    """Publish the validated post to Twitter/X."""
    print("\n[Agent] Publishing to Twitter/X...")
    try:
        response = twitter_client.create_tweet(text=post_content)
        tweet_id = response.data['id']
        print(f"[Agent] Published successfully! ✅ Tweet ID: {tweet_id}")
        print(f"[Agent] View post at: https://twitter.com/user/status/{tweet_id}")
        return True
    except tweepy.errors.TooManyRequests as e:
        print("[Agent] ERROR: Rate limit exceeded. ❌")
        print(e)
        return False
    except tweepy.errors.Unauthorized as e:
        print("[Agent] ERROR: Authentication failed. Please check your API keys. ❌")
        print(e)
        return False
    except Exception as e:
        print(f"[Agent] ERROR: Failed to publish. ❌\nDetails: {e}")
        return False

def main():
    print("="*50)
    print("🤖 Agentic AI Social Media Publisher")
    print("="*50)
    
    import sys
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = input("Enter a topic to generate a post for: ")
        
    if not topic.strip():
        print("Error: Topic cannot be empty.")
        exit(1)
        
    try:
        # Step 1 & 2: Generate and Validate
        validated_post = generate_validated_post(topic)
        
        # Step 3: Generate Image Concept
        image_concept = generate_image_prompt(topic, validated_post)
        
        print("\n" + "="*50)
        print("📝 FINAL CONTENT")
        print("="*50)
        print(f"POST:\n{validated_post}")
        print("-" * 50)
        print(f"IMAGE PROMPT:\n{image_concept}")
        print("="*50)
        
        # Step 4: Publish
        publish_to_twitter(validated_post)
        
    except Exception as e:
        print(f"\n[Agent] Critical Workflow Error: {e}")

if __name__ == "__main__":
    main()
