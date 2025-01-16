import praw
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

analyzer = SentimentIntensityAnalyzer()

with open('credentials.json') as f:
    credentials = json.load(f)

client_id = credentials.get('client_id')
client_secret = credentials.get('client_secret')
user_agent = credentials.get('user_agent')
username = credentials.get('username')  
password = credentials.get('password')

reddit = praw.Reddit(client_id=client_id, 
                     client_secret=client_secret, 
                     user_agent=user_agent, 
                     username=username, 
                     password=password)

def fetch_subreddit_comments(subreddit_name, comment_limit=100):
    subred = reddit.subreddit(subreddit_name)
    comments_data = []
    try:
        for submission in subred.hot(limit=10):     #This is a different limit!!!!!
            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list()[:comment_limit]:
                if comment.body:
                    score = analyzer.polarity_scores(comment.body)

                    if score['compound'] >= 0.05:
                        sentiment = 'positive'
                    elif score['compound'] <= -0.05:
                        sentiment = 'negative'
                    else:
                        sentiment = 'neutral'

                    comments_data.append({
                        'text': comment.body,
                        'score': comment.score,
                        'compound': score['compound'],
                        'pos': score['pos'],
                        'neu': score['neu'],
                        'neg': score['neg'],
                        'sentiment': sentiment
                    })
                if len(comments_data) >= comment_limit:
                    break
    except Exception as e:
        print(f"Error fetching subreddit: {e}")
    return comments_data

while True:
    subreddit_name = input("\nEnter subreddit name (or 'quit' to exit): ")
    
    if subreddit_name.lower() == 'quit':
        break
        
    comment_limit = int(input("How many comments to analyze?: "))
    
    print(f"\nFetching data from r/{subreddit_name}...")
    comments = fetch_subreddit_comments(subreddit_name, comment_limit)
    
    if comments:
        df = pd.DataFrame(comments)
        print("\nSummary Statistics:")
        print(f"Total Comments Analyzed: {len(df)}")
        print(f"Number of Positive Texts: {len(df[df['sentiment'] == 'positive'])}")
        print(f"Number of Negative Texts: {len(df[df['sentiment'] == 'negative'])}")
        print(f"Number of Neutral Texts: {len(df[df['sentiment'] == 'neutral'])}")
        print(f"Most Positive Comment: {df.loc[df['compound'].idxmax()]['text'][:100]}...")
        print(f"Most Negative Comment: {df.loc[df['compound'].idxmin()]['text'][:100]}...")