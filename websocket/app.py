import time
import json
from threading import Thread
import asyncio

import websockets
import pika

from pymongo import MongoClient

client = MongoClient("mongo")
db = client.test_database

for _ in range(10):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="mq"))
    except pika.exceptions.AMQPConnectionError:
        time.sleep(1)

channel = connection.channel()
channel.queue_declare(queue="cv_to_sockets")
channel.queue_declare(queue="od_to_sockets")

connected = set()


async def watch(websocket):
    connected.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        connected.remove(websocket)


async def receiver():

    while True:
        await asyncio.sleep(0)
        method_frame, header_frame, body = channel.basic_get("cv_to_sockets")
        if method_frame:
            # BUG - this one runs too many times
            channel.basic_ack(method_frame.delivery_tag)
            db.events.insert_one(json.loads(body))
            websockets.broadcast(connected, str(body))

        method_frame, header_frame, body = channel.basic_get("od_to_sockets")
        if method_frame:
            print('broadcasting from od', body, flush=True)
            channel.basic_ack(method_frame.delivery_tag)
            db.events.insert_one(json.loads(body))
            websockets.broadcast(connected, str(body))


async def main():
    async with websockets.serve(watch, "0.0.0.0", 5001):
        await receiver()
        # await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
