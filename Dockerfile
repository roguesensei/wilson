FROM arm32v7/python:3.11-slim-bullseye

WORKDIR /app

RUN apt-get update
RUN apt-get install -y build-essential libssl-dev libffi-dev libsodium-dev libopus-dev python-dev ffmpeg git

COPY requirements.txt .
RUN pip install --upgrade pip wheel setuptools
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "main.py" ]