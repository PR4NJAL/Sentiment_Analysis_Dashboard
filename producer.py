from api_fetch import fetch_subreddit_comments
import pika
import json


#http://localhost:15672

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='reddit')

def send_comments_to_queue(subreddit_name, post_keyword, comment_limit=100):
    
    channel.basic_publish(
        exchange='',
        routing_key='reddit',
        body=json.dumps({'type': 'metadata', 'comment_limit': comment_limit})
    )

    comments = fetch_subreddit_comments(subreddit_name, 
                                        post_keyword, 
                                        comment_limit)

    if comments:
        for comment in comments:
            comment['type'] = 'comment'
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
    
        print(f"\nFetching data from r/{subreddit_name}...")
        success = send_comments_to_queue(subreddit_name, post_keyword, comment_limit)

        if not success:
            print("No comments found. Please try again.")

    connection.close()