FROM python:3.7-slim

ENV PYTHONIOENCODING=UTF-8

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "./run.py"] 