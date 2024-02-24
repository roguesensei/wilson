FROM python:3.11-slim-bullseye

WORKDIR /app

RUN apt-get update && \
	# basic deps
	apt-get install -y -qq git mercurial cloc openssl ssh gettext sudo build-essential wget \
	# voice support
	libffi-dev libsodium-dev libopus-dev ffmpeg

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3", "main.py" ]