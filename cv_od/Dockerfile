FROM ultralytics/yolov5:v6.2-cpu

WORKDIR /cv_od

#RUN apt-get update
#RUN apt-get install ffmpeg libsm6 libxext6 x264 libx264-dev -y

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["/usr/bin/python3", "track.py"]