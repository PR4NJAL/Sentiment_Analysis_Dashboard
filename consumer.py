import pika
import json
import pandas as pd
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='reddit')

def callback(ch, method, properties, body):
    try:
        comment_data = json.loads(body)

        print("\nProcessed Comment:")
        df = pd.DataFrame(comment_data, index=range(len(comment_data)))
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
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error loading comment data: {e}")
        
try:
    channel.basic_consume(queue='reddit',
                          on_message_callback=callback,
                          auto_ack=True)
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
except KeyboardInterrupt:
    print('Exiting...')
    sys.exit(0)
    channel.stop_consuming()
except Exception as e:
    print(f"Unexpected error : {e}")
finally:
    connection.close()