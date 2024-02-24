FROM python:3.11-slim-bullseye

WORKDIR /app

RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y libffi-dev libsodium-dev libopus-dev ffmpeg

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3", "main.py" ]