# YouTube AI Automation Platform

An end-to-end AI-driven application that extracts YouTube discourse data, processes it via advanced NLP pipelines, visualizes trends, generates AI images and tweets, and automates social media publishing. 

## ✨ Key Features & Updates

- **Massive YouTube Data Extraction**: Leverages the official YouTube Data API to intelligently search for up to **100 videos** based on topics and extract thousands of viewer comments per session.
- **Advanced NLP & Sentiment Analysis**: Uses tools like `spacy` and `vaderSentiment` to analyze text discussions. It categorizes general sentiment (Positive, Neutral, Negative), extracts specific leader and political party mentions, and groups top discussion topics.
- **Automated Social Media Generation**: 
  - Generates highly engaging, human-like summary posts via the **OpenAI API (GPT-4o-mini)** based on the parsed YouTube discussion.
  - Automatically generates a custom AI visualization via **OpenAI Image Generation** to accompany the post.
  - Includes a brand new **Download Image** button in the UI so you can save the AI-generated graphics locally.
- **Direct Twitter (X) Integration**: Allows seamless, 1-click publishing directly to your Twitter account utilizing `tweepy` and OAuth 1.0a User Access Tokens.
- **Interactive Analytics Dashboard**: A sleek, modern React frontend using Vite and Vanilla CSS that visualizes data findings using interactive Recharts (pie and bar charts). 
- **1-Click Execution**: Includes an easy-to-use `run_project.bat` script to instantly boot up both your frontend and backend servers simultaneously on Windows.
- **API Diagnostics**: Includes a standalone `test_apis.py` script to instantly verify your API configurations and network connections.

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Data & APIs**: `google-api-python-client` (YouTube), `tweepy` (Twitter), `openai` (GPT & DALL-E)
- **NLP**: `vaderSentiment`, `spacy`
- **Document & Export Pipeline**: `fpdf2`, `python-docx`, `matplotlib`, `pandas`

### Frontend
- **Framework**: React.js with Vite
- **Styling**: Modern aesthetic built with purely custom Vanilla CSS frameworks and fluid transitions.
- **Data Visualization**: `recharts` for dynamic, responsive front-end charts.
- **API Calls**: Custom lightweight fetch-services explicitly integrated with the FastAPI pipeline.

## 🚀 Setup Instructions

### 1. Environment Configuration (.env)
In the root directory, you must have a `.env` file that contains all your API keys. 
*Note: Make sure your Twitter keys are generated with **OAuth 1.0a (User Access Tokens)** and have Read/Write permissions!*

```env
# Google & YouTube
YOUTUBE_API_KEY=your_key_here

# OpenAI (For Text and Image Generation)
OPENAI_API_KEY=your_key_here

# Twitter/X Publishing
TWITTER_API_KEY=your_key_here
TWITTER_API_SECRET=your_key_here
TWITTER_ACCESS_TOKEN=your_key_here
TWITTER_ACCESS_TOKEN_SECRET=your_key_here
```

*(Optional) Test your API keys at any time by opening a terminal in the root folder and running: `.\backend\venv\Scripts\python test_apis.py`*

### 2. Quick Start (Windows)
If you are on Windows, you can skip the manual setup and simply double-click the **`run_project.bat`** file in your root directory! It will automatically start both the FastAPI server and the React frontend.

### 3. Manual Start (Alternative)
If you prefer running the commands manually:

**Backend Setup:**
1. Open a terminal and navigate to `./backend`.
2. Activate your virtual environment: `.\venv\Scripts\activate`.
3. Install dependencies: `pip install -r requirements.txt`.
4. Start the backend API locally via: `python -m uvicorn app.main:app --reload`.
5. The backend API is successfully running at `http://localhost:8000`.

**Frontend Setup:**
1. Open a secondary terminal to `./frontend`.
2. Install Node dependencies: `npm install`.
3. Launch your web UI engine: `npm run dev`. 
4. Access the web interface at `http://localhost:5173/`.
