import bson
import json
from datetime import datetime
import time
import random

import pika

for _ in range(10):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="mq"))
    except pika.exceptions.AMQPConnectionError:
        time.sleep(1)

channel = connection.channel()
channel.queue_declare(queue="cv_events")

while True:
    body = {
        "objectID": str(bson.objectid.ObjectId()),
        "eventID": str(bson.objectid.ObjectId()),
        "timestamp": datetime.now().timestamp(),
        "type": "Face",
        "detail": random.choice(["Luke Skywalker", "Han Solo", "Darth Vader"]),
        "clip_url": "127.0.0.1",
    }

    channel.basic_publish(exchange="", routing_key="cv_events", body=json.dumps(body))

    print(f"cv_mock sent {body}", flush=True)

    time.sleep(random.randint(0, 5))

connection.close()
