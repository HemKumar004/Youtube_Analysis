# Agentic AI Social Media Automation

This document explains the technical implementation of the Agentic AI Social Media generator and publisher.

## 1. System Overview

The system takes a user-provided topic (e.g., "Agentic AI workflows"), generates an engaging, emoji-rich tweet that strictly adheres to Twitter's length constraints, creates an accompanying AI image prompt with DALL-E, and publishes it via the Twitter/X API.

The project is structured with a React frontend that interacts with a FastAPI backend to perform these actions. Additionally, the standalone script `agentic_workflow.py` provides the exact same functionality via CLI.

## 2. OpenAI API Integration

### Text Generation & Validation Loop
The system utilizes OpenAI's `gpt-3.5-turbo` model in an agentic feedback loop to generate the tweet text.
- **Initial Prompt**: The system prompts the LLM with strict rules: max 200 characters, must include emojis, fun/catchy tone.
- **Validation**: After receiving the generation, the Python backend checks `len(text) <= 200` and `has_emojis(text)`.
- **Agentic Correction**: If the rules fail, the backend generates a new prompt to the LLM: *"Your previous attempt failed these rules... Please try again and fix these issues."* This loops until the constraints are met or maximum retries are reached.
- **Image Prompts**: Another LLM call creates a cinematic, detailed image prompt based on the user's topic.
- **Image Generation**: DALL-E 3 generates the final image visual based on the image prompt.

## 3. Twitter/X API Authentication

The posting automation uses the `tweepy` library to communicate with the Twitter API v2.
Authentication requires the following credentials stored in `.env`:
- `TWITTER_API_KEY` & `TWITTER_API_SECRET`
- `TWITTER_ACCESS_TOKEN` & `TWITTER_ACCESS_TOKEN_SECRET`

These keys initialize the `tweepy.Client`, which invokes `create_tweet(text=post_content)`. The API responds with the new `tweet_id`, which is returned to the frontend to generate a direct URL to the published post.

## 4. Error Management

Errors and edge cases are handled defensively across the application:
1. **Invalid Input**: Empty topics are blocked at the frontend and backend layer.
2. **OpenAI Quota Exceedance (`429` / `insufficient_quota`)**: If the OpenAI API returns a billing or rate limit error, the application seamlessly falls back to mock generated content and a free placeholder image generator (`pollinations.ai`) so the UI workflow remains unblocked.
3. **Twitter Authentication Errors**: The backend catches Tweepy `Unauthorized` (401) or `TooManyRequests` (429) errors and gracefully returns `{ "success": False, "error": str(e) }`. The React frontend displays this error in a styled alert box rather than crashing.

## 5. Execution & Usage

You can test the system either via the standalone script or the full-stack web application:

**CLI:**
```bash
python agentic_workflow.py "Artificial Intelligence in daily life"
```

**Web App:**
Run the React frontend and FastAPI backend, and access the UI to perform the workflow visually.
