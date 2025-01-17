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

bot_usernames = [
        'AutoModerator',
        'Bot',
        'bot',
        '[deleted]',
        '[removed]'
    ]

def fetch_subreddit_comments(subreddit_name, post_keyword, comment_limit=100, include_replies=False):
    subred = reddit.subreddit(subreddit_name)
    comments_data = []
    try:
        found_posts = False
        for submission in subred.search(post_keyword, limit=10):
            print(f"\nFound post: {submission.title}")
            choice = input("Is this is the post you want to analyze? (y/n): ")
            if choice.lower() == 'y':
                found_posts = True
                submission.comments.replace_more(limit=0)
                valid_comments = []
                if include_replies:
                    all_comments = submission.comments.list()
                else:
                    all_comments = submission.comments
                for comment in all_comments:
                    if(comment.author is not None or str(comment.author) not in bot_usernames or 'bot' not in str(comment.author).lower()):
                        valid_comments.append(comment)
                valid_comments.sort(key=lambda x: x.score, reverse=True)
                for comment in valid_comments[:comment_limit]:
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
                break
        if not found_posts:
            print("No post found with the given keyword. Would you like to:")
            print("1. Retry with a different keyword")
            print("2. Retry with a different subreddit")
            print("3. Exit")
            choice = input("Enter your choice (1/2/3): ")
            if choice == '1':
                new_keyword = input("Enter new keyword: ")
                return fetch_subreddit_comments(subreddit_name, new_keyword, comment_limit, include_replies)
            elif choice == '2':
                new_subreddit = input("Enter new subreddit name: ")
                new_keyword = input("Enter new keyword: ")
                return fetch_subreddit_comments(new_subreddit, new_keyword, comment_limit, include_replies)
            else:
                return []
    except Exception as e:
        print(f"Error fetching subreddit: {e}")
    return comments_data

while True:
    subreddit_name = input("\nEnter subreddit name (or 'quit' to exit): ")
    
    if subreddit_name.lower() == 'quit':
        break

    post_keyword = input("Enter keywords to search for the post: ")
    comment_limit = int(input("How many comments to analyze?: "))
    include_replies = input("Include replies to comments? (y/n):").lower() == 'y'
    
    print(f"\nFetching data from r/{subreddit_name}...")
    comments = fetch_subreddit_comments(subreddit_name, post_keyword, comment_limit, include_replies)
    
    if comments:
        df = pd.DataFrame(comments)
        print("\nSummary Statistics:")
        print(f"Total Comments Analyzed: {len(df)}")
        print(f"Number of Positive Texts: {len(df[df['sentiment'] == 'positive'])}")
        print(f"Number of Negative Texts: {len(df[df['sentiment'] == 'negative'])}")
        print(f"Number of Neutral Texts: {len(df[df['sentiment'] == 'neutral'])}")
        print(f"Most Positive Comment: {df.loc[df['compound'].idxmax()]['text'][:100]}...")
        print(f"Most Negative Comment: {df.loc[df['compound'].idxmin()]['text'][:100]}...")
        print("\nTop 3 Most Upvoted Comments:")
        top_comments = df.nlargest(3, 'score')
        for _, comment in top_comments.iterrows():
            print(f"\nUpvotes: {comment['score']}")
            print(f"Sentiment: {comment['compound']:.3f}")
            print(f"Text: {comment['text'][:100]}...")