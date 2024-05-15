from google.cloud import pubsub_v1
import json
from env import TOPIC_NAME

# credentials_path = "../../credentials.json"


def publish_message(data):
    # if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") is None:
    #     os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
    data = json.dumps(data)
    print(data)
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path("cloud-dev-421516", TOPIC_NAME)
    data = data.encode("utf-8")
    print(data)
    future = publisher.publish(topic_path, data)
    return future.result()
