FROM python:3.7-slim-bullseye

WORKDIR /app

RUN apt-get update
RUN apt-get install -y git libffi-dev libsodium-dev libopus-dev ffmpeg

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "main.py" ]