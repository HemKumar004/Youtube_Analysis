# 🚀 YouTube AI Automation Platform

An end-to-end AI-driven application that extracts YouTube discourse data, processes it using advanced NLP pipelines, visualizes insights, generates AI-powered content (text + images), and automates social media publishing.

---

# ✨ Key Features

### 📊 Massive YouTube Data Extraction

* Uses YouTube Data API to fetch up to **100 videos**
* Extracts **thousands of comments** per session
* Topic-based intelligent search

---

### 🧠 Advanced NLP & Sentiment Analysis

* Built with **spaCy + VADER Sentiment**
* Classifies:

  * Positive 😊
  * Neutral 😐
  * Negative 😡
* Extracts:

  * People names
  * Organizations
  * Trending discussion topics

---

### 🤖 AI Content Generation

* Uses **OpenAI GPT-4o-mini**
* Generates:

  * Engaging social media posts (150–200 words)
  * Human-like summaries from YouTube discussions
* Includes emojis, tone, and engagement hooks

---

### 🎨 AI Image Generation

* Uses **OpenAI Image API (gpt-image-1)**
* Generates custom visuals based on topic
* Includes:

  * 🎯 Real-time image preview
  * 📥 Download Image button

---

### 🐦 Twitter (X) Automation

* One-click publishing using **Tweepy**
* OAuth 1.0a authentication
* Supports **Read + Write permissions**

---

### 📈 Interactive Dashboard

* Built with **React + Vite**
* Uses **Recharts** for:

  * Pie charts
  * Bar charts
* Fully responsive modern UI

---

### ⚡ 1-Click Execution

* Run everything using:

```bash
run_project.bat
```

---

### 🧪 API Diagnostics Tool

* Includes:

```bash
test_apis.py
```

* Verifies all API connections instantly

---

# 🛠️ Tech Stack

## 🔹 Backend

* FastAPI (Python)
* OpenAI API (Text + Image)
* YouTube Data API
* Tweepy (Twitter API)
* spaCy + vaderSentiment

---

## 🔹 Frontend

* React.js (Vite)
* Vanilla CSS (custom styling)
* Recharts (data visualization)

---

# 🔑 API Setup Guide (Step-by-Step)

---

## 🔴 1. YouTube API Key

👉 Visit: https://console.cloud.google.com/

### Steps:

1. Create a new project
2. Go to **APIs & Services → Library**
3. Enable **YouTube Data API v3**
4. Go to **Credentials → Create API Key**
5. Copy the key

---

## 🟢 2. OpenAI API Key

👉 Visit: https://platform.openai.com/

### Steps:

1. Login / Signup
2. Go to **API Keys**
3. Click **Create new secret key**
4. Copy the key
5. ⚠️ Add billing (required)

---

### ⚠️ Important

Without billing, you will get:

```
429 insufficient_quota
billing_hard_limit_reached
```

---

## 🔵 3. Twitter (X) API Setup

👉 Visit: https://developer.twitter.com/

---

### Steps:

#### Step 1: Create Developer Account

* Apply and create an app

---

#### Step 2: Set Permissions

Go to:

```
App Settings → User Authentication Settings
```

Select:

```
Read and Write
```

---

#### Step 3: Generate Tokens

Copy these:

```env
TWITTER_API_KEY=
TWITTER_API_SECRET=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_TOKEN_SECRET=
```

---

## 🟡 4. Verify API Keys

Run:

```bash
.\backend\venv\Scripts\python test_apis.py
```

Expected:

```
✅ OpenAI connected
✅ Twitter connected
```

---

# ⚙️ Environment Configuration

Create `.env` file in root:

```env
YOUTUBE_API_KEY=your_key
OPENAI_API_KEY=your_key
TWITTER_API_KEY=your_key
TWITTER_API_SECRET=your_key
TWITTER_ACCESS_TOKEN=your_key
TWITTER_ACCESS_TOKEN_SECRET=your_key
```

---

# 🚀 Running the Project

---

## 🟢 Option 1: Quick Start (Windows)

Double-click:

```
run_project.bat
```

---

## 🔵 Option 2: Manual Setup

### Backend

```bash
cd backend
.\venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

---

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

# 🌐 Access URLs

| Service  | URL                   |
| -------- | --------------------- |
| Frontend | http://localhost:5173 |
| Backend  | http://localhost:8000 |

---

# 🧪 Example Workflow

1. Enter topic
2. Fetch YouTube data
3. Analyze comments
4. Generate AI post
5. Generate AI image
6. Publish to Twitter

---

# ⚠️ Troubleshooting

---

## ❌ OpenAI Error (429)

👉 Cause:

* No credits

👉 Fix:

* Add billing

---

## ❌ Random Image / No Image

👉 Cause:

* Image API failed

👉 Fix:

* Check OpenAI key
* Ensure billing is active

---

## ❌ Twitter Post Failed

👉 Check:

* Permissions = Read + Write
* Regenerate tokens after changes

---

## ❌ Backend Not Starting

```bash
pip install -r requirements.txt
```

---

# 📌 Future Improvements

* Instagram API integration
* Local image generation (Stable Diffusion)
* Post scheduling
* Multi-language support
* AI recommendation engine

---

# 🎯 Conclusion

This project demonstrates:

* Full-stack development
* AI integration
* API orchestration
* Real-world automation

Perfect for:

* 💼 Placements
* 🧠 Learning AI systems
* 🚀 Portfolio projects

---

# ⭐ If you like this project

Give it a ⭐ on GitHub!
