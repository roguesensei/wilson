FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get upgrade
RUN apt-get install -y libffi-dev libsodium-dev libopus-dev ffmpeg

RUN pip install -r requirements.txt

ENTRYPOINT [ "python3", "main.py" ]