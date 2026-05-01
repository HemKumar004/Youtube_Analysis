# import os
# import base64
# from openai import OpenAI
# from dotenv import load_dotenv

# try:
#     from google import genai
#     from google.genai import types
#     GENAI_AVAILABLE = True
# except ImportError:
#     GENAI_AVAILABLE = False

# load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.env")), override=True)

# openai_api_key = os.getenv("OPENAI_API_KEY")
# client = OpenAI(api_key=openai_api_key)

# try:
#     import emoji
#     EMOJI_AVAILABLE = True
# except ImportError:
#     EMOJI_AVAILABLE = False

# def has_emojis(text: str) -> bool:
#     if EMOJI_AVAILABLE:
#         for char in text:
#             if char in emoji.EMOJI_DATA:
#                 return True
#         return False
#     else:
#         # Basic fallback: check if there are any characters in common emoji unicode ranges
#         for char in text:
#             if ord(char) > 0x2600:
#                 return True
#         return False

# def generate_social_media_content(topic: str, max_retries: int = 3) -> dict:
#     if not openai_api_key:
#         raise ValueError("Missing OpenAI API Key")
        
#     system_prompt = (
#         "You are an expert social media manager. Generate a highly creative, engaging, "
#         "and conversational social media post about the requested topic. "
#         "RULES:\n"
#         "1. Maximum length is strictly 200 characters.\n"
#         "2. MUST include at least one fun emoji (e.g., 🔥😂🎯🚀).\n"
#         "3. Tone must be fun, slightly dramatic, or catchy. Never robotic."
#     )
    
#     current_prompt = f"Create a short, fun tweet about: {topic}"
#     post_text = ""
    
#     # Agentic Validation Loop
#     for attempt in range(1, max_retries + 1):
#         try:
#             post_completion = client.chat.completions.create(
#                 model="gpt-3.5-turbo",
#                 messages=[
#                     {"role": "system", "content": system_prompt},
#                     {"role": "user", "content": current_prompt}
#                 ],
#                 max_tokens=60,
#                 temperature=0.8
#             )
#             post_text = post_completion.choices[0].message.content.strip()
#         except Exception as e:
#             if "insufficient_quota" in str(e) or "429" in str(e):
#                 post_text = f"Exploring {topic} has never been more exciting! 🚀 The future is here and it's amazing. 🔥 What are your thoughts? 👇 #Tech"
#                 break
#             else:
#                 raise e
        
#         errors = []
#         if len(post_text) > 200:
#             errors.append(f"Length is {len(post_text)} chars, exceeding 200.")
#         if not has_emojis(post_text):
#             errors.append("Missing emojis. MUST include emojis.")
            
#         if not errors:
#             break
            
#         if attempt < max_retries:
#             current_prompt = (
#                 f"Your previous attempt ('{post_text}') failed these rules: {', '.join(errors)}. "
#                 f"Please try again for the topic '{topic}' and fix these issues."
#             )

#     # Generate Image Prompt
#     try:
#         prompt_completion = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a creative director. Generate a Midjourney/DALL-E image prompt that perfectly visualizes the given topic for a social media post. Focus on visual description, lighting, and style."},
#                 {"role": "user", "content": f"Create a short image prompt for the topic: {topic}"}
#             ],
#             max_tokens=80,
#             temperature=0.7
#         )
#         image_prompt = prompt_completion.choices[0].message.content.strip()
#     except Exception as e:
#         if "insufficient_quota" in str(e) or "429" in str(e):
#             image_prompt = f"A futuristic and cinematic visualization of {topic}, vibrant colors, neon lights, highly detailed, photorealistic, 8k resolution, unreal engine 5 render, dramatic lighting, cyberpunk aesthetic."
#         else:
#             raise e

#     # Generate Actual Image
#     image_url = None
#     try:
#         if not GENAI_AVAILABLE:
#             raise ImportError("google-genai package is missing or failed to load. Using fallback image.")
            
#         gemini_api_key = os.getenv("GEMINI_API_KEY")
#         if not gemini_api_key:
#             raise ValueError("GEMINI_API_KEY is missing")
            
#         gemini_client = genai.Client(api_key=gemini_api_key)
#         image_response = gemini_client.models.generate_images(
#             model='imagen-3.0-generate-002',
#             prompt=image_prompt[:1000],
#             config=types.GenerateImagesConfig(
#                 number_of_images=1,
#                 aspect_ratio="1:1",
#                 output_mime_type="image/jpeg"
#             )
#         )
        
#         # Convert raw bytes to base64 data URI
#         img_bytes = image_response.generated_images[0].image.image_bytes
#         b64_str = base64.b64encode(img_bytes).decode("utf-8")
#         image_url = f"data:image/jpeg;base64,{b64_str}"
        
#     except Exception as e:
#         print(f"Error generating image with Gemini: {e}")
#         if "insufficient_quota" in str(e) or "429" in str(e) or "billing" in str(e) or "GEMINI_API_KEY" in str(e):
#             # Fallback placeholder image for UI demonstration
#             image_url = f"https://placehold.co/1024x1024/1e1e2f/00d4ff?text=AI+Generated+Image+For%5Cn{topic.replace(' ', '+')}"
#         else:
#             image_url = f"https://placehold.co/1024x1024/1e1e2f/00d4ff?text=AI+Generated+Image+For%5Cn{topic.replace(' ', '+')}"

#     return {
#         "post_content": post_text,
#         "image_prompt": image_prompt,
#         "image_url": image_url
#     }
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# OpenAI setup
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# Emoji detection
try:
    import emoji
    EMOJI_AVAILABLE = True
except ImportError:
    EMOJI_AVAILABLE = False


def has_emojis(text: str) -> bool:
    if EMOJI_AVAILABLE:
        return any(char in emoji.EMOJI_DATA for char in text)
    return any(ord(char) > 0x2600 for char in text)


# ✅ OPENAI IMAGE GENERATION (FINAL)
def generate_ai_image(prompt: str):
    try:
        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="512x512"
        )

        image_base64 = result.data[0].b64_json
        return f"data:image/png;base64,{image_base64}"

    except Exception as e:
        print("⚠️ OpenAI Image Error:", e)

        # ✅ FINAL SAFE FALLBACK (always works)
        return "https://picsum.photos/512/512"


def generate_social_media_content(topic: str, max_retries: int = 3) -> dict:
    if not openai_api_key:
        raise ValueError("Missing OpenAI API Key")

    system_prompt = (
        "You are an expert social media manager. Generate a highly engaging and creative post.\n"
        "RULES:\n"
        "1. The post must be between 150 to 200 words.\n"
        "2. MUST include emojis (🔥😂🎯🚀).\n"
        "3. Tone should be exciting and engaging.\n"
        "4. Make it feel natural and human-like."
    )

    current_prompt = f"Write a detailed, engaging social media post (150–200 words) about: {topic}"
    post_text = ""

    # 🔁 Retry loop (improved)
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": current_prompt}
                ],
                max_tokens=400,   # ✅ increased
                temperature=0.8
            )

            post_text = response.choices[0].message.content.strip()

        except Exception as e:
            print("⚠️ OpenAI text error:", e)
            post_text = f"🔥 {topic} is trending right now! What do you think? 👇 #AI"
            break

        # ✅ Validation
        word_count = len(post_text.split())
        has_emoji = has_emojis(post_text)

        if word_count >= 150 and has_emoji:
            break

        # 🔥 Strong retry prompt
        current_prompt = (
            f"Rewrite this post correctly:\n\n{post_text}\n\n"
            f"Requirements:\n"
            f"- 150 to 200 words\n"
            f"- Must include emojis\n"
            f"- More engaging and human tone\n"
            f"- Topic: {topic}"
        )

    # 🖼️ Generate image prompt
    try:
        image_prompt_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Generate a cinematic, detailed AI image prompt."},
                {"role": "user", "content": f"Create a visual for: {topic}"}
            ],
            max_tokens=80,
            temperature=0.7
        )

        image_prompt = image_prompt_response.choices[0].message.content.strip()

    except Exception as e:
        print("⚠️ Image prompt error:", e)
        image_prompt = f"Futuristic {topic}, neon lights, cinematic, 8k"

    # 🖼️ Generate AI image
    image_url = generate_ai_image(image_prompt)

    return {
        "post_content": post_text,
        "image_prompt": image_prompt,
        "image_url": image_url
    }