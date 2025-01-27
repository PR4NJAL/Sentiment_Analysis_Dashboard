import pika
import json
from processor import processor
from calculate_statistics import calculate_statistics

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='reddit')

    processed_count = 0
    comment_limit = None
    aggregated_data = []

    def callback(ch, method, properties, body):
        nonlocal processed_count, comment_limit, aggregated_data
        try:
            data = json.loads(body)
            if data.get('type') == 'metadata':
                comment_limit = data['comment_limit']
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return
            if data.get('type') == 'comment':
                processed_count += 1
                comment_data = processor(data)   
                aggregated_data.append(comment_data)
                print(f"Processed {processed_count}/{comment_limit} comments")
                ch.basic_ack(delivery_tag=method.delivery_tag)
            if processed_count == comment_limit:
                print("\nAnalysis Complete:")
                calculate_statistics(aggregated_data)
                aggregated_data = []
                print("Exiting after completing analysis.")
                connection.close()
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON data: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except Exception as e:
            print(f"Error loading comment data: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        
    try:
        channel.basic_consume(queue='reddit',
                          on_message_callback=callback)
        print('Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except KeyboardInterrupt:
        print('Exiting...')
        channel.stop_consuming()
    except Exception as e:
        print(f"Unexpected error : {e}")
        channel.stop_consuming()
    finally:
        if connection.is_open:
            connection.close()

if __name__ == '__main__':
    main()