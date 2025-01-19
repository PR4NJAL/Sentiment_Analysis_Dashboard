from api import fetch_subreddit_comments
import pika
import json


#http://localhost:15672

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='reddit')

def send_comments_to_queue(subreddit_name, post_keyword, comment_limit=100, include_replies=False):
    comments = fetch_subreddit_comments(subreddit_name, 
                                        post_keyword, 
                                        comment_limit, 
                                        include_replies)
    if comments:
        for comment in comments:
            channel.basic_publish(exchange='',
                                 routing_key='reddit',
                                 body=json.dumps(comment))
            print(f"Sent comment to queue: {comment['text']}")
        return True
    return False

if __name__ == '__main__':
    while True:
        subreddit_name = input("\nEnter subreddit name (or 'quit' to exit): ")
    
        if subreddit_name.lower() == 'quit':
            break

        post_keyword = input("Enter keywords to search for the post: ")
        comment_limit = int(input("How many comments to analyze?: "))
        include_replies = input("Include replies to comments? (y/n):").lower() == 'y'
    
        print(f"\nFetching data from r/{subreddit_name}...")
        success = send_comments_to_queue(subreddit_name, post_keyword, comment_limit, include_replies)

        if not success:
            print("No comments found. Please try again.")

    connection.close()