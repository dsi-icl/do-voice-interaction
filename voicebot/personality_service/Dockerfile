FROM python:3.8-slim
LABEL maintainer="ms1518@imperial.ac.uk"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

CMD [ "python", "./run_lstm.py" ]