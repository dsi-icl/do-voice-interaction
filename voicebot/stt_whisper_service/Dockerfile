FROM python:3.8-slim

WORKDIR /usr/src/app

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN apt update && apt install -y ffmpeg

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update  && apt-get install -y git
RUN pip install git+https://github.com/openai/whisper.git 

CMD [ "python", "run_whisper.py" ]

