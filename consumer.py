import pika
import json
import sys
from processor import processor
from calculate_statistics import calculate_statistics
def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='reddit')

    aggregated_data = []

    def callback(ch, method, properties, body):
        try:
            data = json.loads(body)
            comment_data = processor(data)
            aggregated_data.append(comment_data)
            ch.basic_ack(delivery_tag=method.delivery_tag)
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
    finally:
        connection.close()
        if aggregated_data:  
            calculate_statistics(aggregated_data)
        else:
            print("No comments processed, no statistics to display.")
        sys.exit(0)

if __name__ == '__main__':
    main()