import bson
from datetime import datetime
import time
import json

from flask import Flask, request

app = Flask(__name__)

from flask_cors import CORS

CORS(app)

from pymongo import MongoClient

client = MongoClient("mongo")
db = client.test_database


from werkzeug.routing import BaseConverter


class ObjectIDConverter(BaseConverter):
    def to_python(self, value):
        return bson.objectid.ObjectId(value)

    def to_url(self, value):
        return str(value)


app.url_map.converters["objectID"] = ObjectIDConverter


@app.get("/streams")
def get_streams():

    return {
        "streams": [
            {
                "_id": "0" * 23 + '0',
                "name": "Isengard",
                "url": "http://127.0.0.1:3000/cam.m3u8",
            },

            {
                "_id": "0" * 23 + '1',
                "name": "Alderaan",
                "url": "http://127.0.0.1:3000/second_cam.m3u8",
            },
            # {
            #     "_id": "0" * 23 + '2',
            #     "name": "Jita IV-Moon 4",
            #     "url": "http://127.0.0.1:3000/cam.m3u8",
            # },

            # {
            #     "_id": "0" * 23 + '3',
            #     "name": "Runeterra",
            #     "url": "http://127.0.0.1:3000/cam.m3u8",
            # }
        ]
    }

    # result = list(db.streams.find({}, {"name": 1, "url": 1, "_id": 1}))
    # for record in result:
    #     record["_id"] = str(record["_id"])
    # return {"streams": result}


@app.put("/streams/add")
def add_stream():
    json = request.get_json()
    name = json["name"]
    url = json["url"]

    stream = db.streams.insert_one({"name": name, "url": url})
    stream[_id] = str(stream["id"])
    return {"stream": result}


@app.delete("/stream/<objectID:_id>/delete")
def delete_stream(_id):
    db.streams.delete_one({"_id": _id})

    return {"success": True}


@app.get("/events")
@app.get("/stream/<objectID:stream_id>/events")
def get_events(stream_id=None):
    result = list(db.events.find())
    for record in result:
        record["_id"] = str(record["_id"])
    return {"events": result}


if __name__ == "__main__":
    app.run(host="0.0.0.0")
