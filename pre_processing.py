import re
from nltk.corpus import stopwords
import emoji

def remove_urls(text):
    return re.sub(r'http[s]?://\S+', '', text)

def remove_reddit_mentions(text):
    return re.sub(r'u/[A-Za-z0-9_-]+|r/[A-Za-9_-]+', '', text)

def clean_text(text):
    text = re.sub(r'[^a-zA-Z0-9\s!?.]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

stop_words = set(stopwords.words('english'))

def remove_stopwords(text):
    return ' '.join([word for word in text.split() if word.lower() not in stop_words])

def convert_emojis(text):
    return emoji.demojize(text)

def normalize_text(text):
    text = text.encode('ascii', 'ignore').decode()  # Remove non-ASCII characters
    text = text.replace('\n', ' ').replace('\r', ' ')
    return text

def preprocess_reddit_comment(text):
    text = remove_urls(text)
    text = remove_reddit_mentions(text)
    text = convert_emojis(text)
    text = normalize_text(text)
    text = clean_text(text)
    text = remove_stopwords
    return text