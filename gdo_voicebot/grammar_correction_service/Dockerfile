FROM python:3.7-slim

ENV PYTHONIOENCODING=UTF-8

RUN apt-get update && apt-get install -y \
    ffmpeg espeak libespeak-dev python-dev build-essential\
    festival*


WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

COPY . .

CMD [ "python", "./run.py" ]