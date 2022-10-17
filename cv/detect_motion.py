# This was created by Colt C and Tom M for hackathon event Sep 22, this file reads in video stream from RPi and records a 60s video
# whenever motion is detected, saving as a .mp4 file for future use

# Import the neccessary libraries
import cv2
import numpy as np
import time
from datetime import datetime
from skimage.metrics import structural_similarity as compare_ssim
import json
import os
import bson
import pika
import contextlib

for _ in range(10):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="mq"))
    except pika.exceptions.AMQPConnectionError:
        time.sleep(1)

try:
    os.mkdir(f"/output/{os.environ['STREAM_ID']}")
except:
    pass

channel = connection.channel()
channel.queue_declare(queue="cv_to_od")
channel.queue_declare(queue="cv_to_sockets")

url = os.environ['STREAM_URL']
Folderpath = f"/output/{os.environ['STREAM_ID']}"
cap = cv2.VideoCapture(url)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(
    *"VP90"
)  # this is the codec type used to write your output file, x264, h264 or this

# init our loop by faking the previous iteration
ret, prev_frame = cap.read()
recording = False

while True:  # run the loop continuously

    ret, current_frame = cap.read()

    diff = np.sum(cv2.absdiff(prev_frame, current_frame))
    grayA = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    (score, diff) = compare_ssim(grayA, grayB, full=True)

    # we have a difference between frames...
    if score < 0.93:

        # not already recording? start recording
        if not recording:
            recording = True

            # this sets up the file to be written to using opencv
            start_time = datetime.now()
            path = start_time.strftime("%Y%m%d-%H%M%SZ")
            eventID = str(bson.objectid.ObjectId())

            videoWriter = cv2.VideoWriter(
                f"/output/{os.environ['STREAM_ID']}/{path}.webm", fourcc, 10.0, (int(cap.get(3)), int(cap.get(4)))
            )

            body = {
                "streamID": os.environ['STREAM_ID'],
                "eventID": eventID,
                "timestamp": start_time.timestamp(),
                "type": "movement-start",
                "detail": "",
                "clip_url": "",
            }

            channel.basic_publish(
                exchange="", routing_key="cv_to_od", body=json.dumps(body)
            )

            channel.basic_publish(
                exchange="", routing_key="cv_to_sockets", body=json.dumps(body)
            )

        # we're recording already - do nothing
        else:
            pass

        # reset spare frames
        end_frames = 5

    # we don't have a difference between frames...
    else:

        # but we are recording (ie we are recording motion that has now stopped)
        if recording:
            # no more dead frames left? stop recording
            if end_frames == 0:
                videoWriter.release()
                recording = False

                body = {
                    "streamID": os.environ['STREAM_ID'],
                    "eventID": eventID,
                    "timestamp": datetime.now().timestamp(),
                    "type": "movement-stop",
                    "detail": "",
                    "clip_url": f"/{os.environ['STREAM_ID']}/{path}.webm",
                }

            channel.basic_publish(
                exchange="", routing_key="cv_to_od", body=json.dumps(body)
            )

            channel.basic_publish(
                exchange="", routing_key="cv_to_sockets", body=json.dumps(body)
            )

            end_frames -= 1

        # no motion and not recording - do nothing
        else:
            pass

    if recording:
        videoWriter.write(current_frame)

    # finally, current frame is now previous frame
    prev_frame = current_frame

cap.release()
connection.close()
