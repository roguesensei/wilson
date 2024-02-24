FROM arm32v7/python:3.11-slim-bullseye

WORKDIR /app

RUN apt-get update
RUN apt-get install -y git libffi-dev libsodium-dev libopus-dev ffmpeg

COPY requirements.txt .
RUN pip3 install --upgrade-pip
RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT [ "python3", "main.py" ]