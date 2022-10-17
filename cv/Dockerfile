FROM jjanzic/docker-python3-opencv 

WORKDIR /cv

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 x264 libx264-dev -y

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python", "detect_motion.py"]