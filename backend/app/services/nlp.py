import re
import nltk
from nltk.corpus import stopwords
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import Counter

# Download stopwords if not present
try:
    stop_words = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

analyzer = SentimentIntensityAnalyzer()

import spacy
from collections import Counter
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    # Remove special characters and emojis
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Remove stopwords
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text

def extract_entities(text: str) -> dict:
    if not isinstance(text, str):
        return {'organizations': [], 'persons': []}
    
    doc = nlp(text)
    organizations = []
    persons = []
    
    for ent in doc.ents:
        clean_text = ent.text.strip().title()
        if len(clean_text) > 2:
            if ent.label_ == "ORG":
                organizations.append(clean_text)
            elif ent.label_ == "PERSON":
                persons.append(clean_text)
            
    return {
        'organizations': organizations,
        'persons': persons
    }

def analyze_sentiment(text: str) -> str:
    if not isinstance(text, str) or not text.strip():
        return 'neutral'
    
    score = analyzer.polarity_scores(text)['compound']
    if score >= 0.05:
        return 'positive'
    elif score <= -0.05:
        return 'negative'
    else:
        return 'neutral'

def extract_top_topics(cleaned_comments: list, top_n: int = 10) -> list:
    """Extract top frequent words/topics as a simple keyword extraction"""
    all_words = ' '.join(cleaned_comments).split()
    # Filter short words
    all_words = [w for w in all_words if len(w) > 3]
    word_freq = Counter(all_words)
    return [{"topic": k, "count": v} for k, v in word_freq.most_common(top_n)]
