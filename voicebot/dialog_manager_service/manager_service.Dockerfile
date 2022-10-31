FROM python:3.8-buster

RUN pip install -e git+https://github.com/bk121/rasa_personality.git#egg=rasa

CMD ["rasa","run","-m","/app/models", "--enable-api", "--endpoints","/app/config/endpoints.yml","--credentials","/app/config/credentials.yml"]

