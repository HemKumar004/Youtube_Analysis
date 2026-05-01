import nbformat as nbf

nb = nbf.v4.new_notebook()

# 1. Introduction
nb.cells.append(nbf.v4.new_markdown_cell("""# Dynamic YouTube Data Analysis

## 1. Introduction
This notebook analyzes YouTube data dynamically based on user queries, without any hardcoded assumptions about the topic. It pulls real-time YouTube metadata and comments, cleans them, and applies Natural Language Processing to extract named entities, sentiment, and core topics."""))

# 2. Dynamic Data Extraction
nb.cells.append(nbf.v4.new_markdown_cell("""## 2. Dynamic Data Extraction
Extracting video data dynamically using the YouTube API v3 based on a generic input query."""))

nb.cells.append(nbf.v4.new_code_cell("""import os
import pandas as pd
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv('../.env')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

def fetch_youtube_data(query, max_videos=10):
    if not YOUTUBE_API_KEY:
        print("Missing YouTube API Key!")
        return [], []
        
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    
    # Search for videos dynamically
    search_response = youtube.search().list(
        q=query,
        part='id,snippet',
        maxResults=max_videos,
        type='video',
        order='relevance'
    ).execute()
    
    videos = []
    comments = []
    
    for item in search_response.get('items', []):
        video_id = item['id']['videoId']
        videos.append({
            'video_id': video_id,
            'title': item['snippet']['title'],
            'channel': item['snippet']['channelTitle']
        })
        
        # Fetch comments for each video
        try:
            comment_response = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=100,
                textFormat='plainText'
            ).execute()
            
            for c_item in comment_response.get('items', []):
                text = c_item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append({
                    'video_id': video_id,
                    'comment': text
                })
        except Exception as e:
            pass # Comments might be disabled
            
    return videos, comments

# Example dynamic extraction
QUERY = "Artificial Intelligence 2026"
videos, comments = fetch_youtube_data(QUERY)
print(f"Fetched {len(videos)} videos and {len(comments)} comments for '{QUERY}'")"""))

# 3. Data Cleaning
nb.cells.append(nbf.v4.new_markdown_cell("""## 3. Data Cleaning
Clean the comments by removing URLs, emojis, special characters, stopwords, and converting to lowercase."""))

nb.cells.append(nbf.v4.new_code_cell("""import re
import nltk
from nltk.corpus import stopwords

# Download stopwords
try:
    stop_words = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = str(text).lower()
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    # Remove special characters and emojis
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Remove stopwords
    words = [word for word in text.split() if word not in stop_words]
    return ' '.join(words)

# Apply cleaning
df_comments = pd.DataFrame(comments)
if not df_comments.empty:
    df_comments['cleaned'] = df_comments['comment'].apply(clean_text)
df_comments.head()"""))

# 4. Exploratory Data Analysis
nb.cells.append(nbf.v4.new_markdown_cell("""## 4. Exploratory Data Analysis
Overview of the collected text data lengths and basic distributions."""))

nb.cells.append(nbf.v4.new_code_cell("""import matplotlib.pyplot as plt
import seaborn as sns

if not df_comments.empty:
    df_comments['word_count'] = df_comments['cleaned'].apply(lambda x: len(x.split()))
    
    plt.figure(figsize=(8, 4))
    sns.histplot(df_comments['word_count'], bins=20, kde=True, color='blue')
    plt.title('Distribution of Comment Word Counts')
    plt.xlabel('Word Count')
    plt.ylabel('Frequency')
    plt.show()"""))

# 5. Topic Analysis
nb.cells.append(nbf.v4.new_markdown_cell("""## 5. Topic Analysis
Perform basic topic modeling / keyword extraction on the cleaned text to see what is being discussed."""))

nb.cells.append(nbf.v4.new_code_cell("""from collections import Counter

if not df_comments.empty:
    all_words = ' '.join(df_comments['cleaned']).split()
    # Filter very short words
    all_words = [w for w in all_words if len(w) > 3]
    
    word_freq = Counter(all_words)
    top_topics = word_freq.most_common(10)
    
    df_topics = pd.DataFrame(top_topics, columns=['Topic', 'Frequency'])
    
    plt.figure(figsize=(8, 4))
    sns.barplot(data=df_topics, x='Topic', y='Frequency', palette='viridis')
    plt.title('Top 10 Extracted Topics/Keywords')
    plt.xticks(rotation=45)
    plt.show()"""))

# 6. Named Entity Extraction
nb.cells.append(nbf.v4.new_markdown_cell("""## 6. Named Entity Extraction
Use Spacy to dynamically extract Named Entities (Persons and Organizations) from the corpus, without hardcoding names."""))

nb.cells.append(nbf.v4.new_code_cell("""import spacy

try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    import spacy.cli
    spacy.cli.download('en_core_web_sm')
    nlp = spacy.load('en_core_web_sm')

def extract_entities(text):
    doc = nlp(str(text))
    orgs = [ent.text.strip().title() for ent in doc.ents if ent.label_ == 'ORG' and len(ent.text) > 2]
    persons = [ent.text.strip().title() for ent in doc.ents if ent.label_ == 'PERSON' and len(ent.text) > 2]
    return orgs, persons

if not df_comments.empty:
    all_orgs = []
    all_persons = []
    
    # We apply Spacy to original text for better capitalization context
    for text in df_comments['comment']:
        orgs, persons = extract_entities(text)
        all_orgs.extend(orgs)
        all_persons.extend(persons)
        
    top_orgs = Counter(all_orgs).most_common(10)
    top_persons = Counter(all_persons).most_common(10)
    
    print("Top Organizations:", top_orgs)
    print("Top Persons:", top_persons)"""))

# 7. Sentiment Analysis
nb.cells.append(nbf.v4.new_markdown_cell("""## 7. Sentiment Analysis
Analyze the sentiment of the comments using the VADER sentiment intensity analyzer."""))

nb.cells.append(nbf.v4.new_code_cell("""from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def apply_sentiment(text):
    score = analyzer.polarity_scores(str(text))['compound']
    if score >= 0.05: return 'positive'
    elif score <= -0.05: return 'negative'
    else: return 'neutral'

if not df_comments.empty:
    df_comments['sentiment'] = df_comments['cleaned'].apply(apply_sentiment)
    sentiment_counts = df_comments['sentiment'].value_counts()
    print("Sentiment Breakdown:\\n", sentiment_counts)"""))

# 8. Visualization
nb.cells.append(nbf.v4.new_markdown_cell("""## 8. Visualization
Visualizing the named entities and the overall sentiment distribution."""))

nb.cells.append(nbf.v4.new_code_cell("""if not df_comments.empty:
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Sentiment Pie Chart
    axes[0].pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', colors=['#10b981', '#9ca3af', '#ef4444'])
    axes[0].set_title('Sentiment Distribution')
    
    # Organizations Bar Chart
    if top_orgs:
        df_orgs = pd.DataFrame(top_orgs, columns=['Organization', 'Count'])
        sns.barplot(data=df_orgs, x='Organization', y='Count', ax=axes[1], palette='Blues_r')
        axes[1].set_title('Top Named Entities (Organizations)')
        axes[1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()"""))

# 9. Key Insights
nb.cells.append(nbf.v4.new_markdown_cell("""## 9. Key Insights
Algorithmically derived conclusions from the dynamic extraction."""))

nb.cells.append(nbf.v4.new_code_cell("""if not df_comments.empty:
    print(f"--- Key Insights for '{QUERY}' ---")
    print(f"1. A total of {len(comments)} comments were analyzed from {len(videos)} top videos.")
    if top_topics:
        print(f"2. The most discussed topic/keyword is '{top_topics[0][0]}' appearing {top_topics[0][1]} times.")
    
    dominant_sentiment = sentiment_counts.index[0]
    print(f"3. The overall discourse is predominantly {dominant_sentiment} ({sentiment_counts.max()} comments).")
    
    if top_orgs:
        print(f"4. The most heavily mentioned organization is '{top_orgs[0][0]}'.")
    if top_persons:
        print(f"5. The most heavily mentioned person is '{top_persons[0][0]}'.")"""))

nbf.write(nb, 'd:/Maxxin/data_analysis/youtube_analysis.ipynb')
print("Notebook successfully updated.")
