FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get upgrade
RUN apt-get install -y python3-pip libffi-dev libsodium-dev libopus-dev ffmpeg

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3", "main.py" ]