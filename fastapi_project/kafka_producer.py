import sys, os, six, json

# https://github.com/dpkp/kafka-python/issues/2412
if sys.version_info >= (3, 12, 0):
    sys.modules['kafka.vendor.six.moves'] = six.moves

from kafka import KafkaProducer
from dotenv import load_dotenv
from bson import ObjectId

load_dotenv()

kafka_broker = os.getenv("KAFKA_BROKER")

producer = KafkaProducer(
    bootstrap_servers = [kafka_broker],
    api_version = (0, 10, 1),
    value_serializer = lambda v: json.dumps(v).encode('utf-8')
)

def convert_objectid(data):
    """
    Convert MongoDB ObjectID instances to string in dictionary
    """
    if isinstance(data, dict):
        return {k: convert_objectid(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_objectid(v) for v in data]
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data

def send_kafka_message(topic: str, message: dict):
    """
    Send a message to the specified Kafka topic.
    """
    try:
        message = convert_objectid(message)
        producer.send(topic, value = message)
        producer.flush()
        print(f"Message sent to topic {topic}: {message}")
    except Exception as e:
        print(f"Failed to send message to Kafka: {e}")
