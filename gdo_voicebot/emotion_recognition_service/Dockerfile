FROM python:3.7-slim
LABEL maintainer="ms1518@imperial.ac.uk"

#RUN apt-get -y update
#RUN apt-get install -y ffmpeg espeak
ENV PYTHONIOENCODING=UTF-8

RUN apt-get update && apt-get install -y \
    ffmpeg espeak libespeak-dev python-dev build-essential\
    festival*


WORKDIR /usr/src/app

RUN pip install numpy==1.18.5 beautifulsoup4==4.9.3 lxml==4.6.3 winregistry 
RUN pip install aeneas==1.7.3.0
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./run.py" ]