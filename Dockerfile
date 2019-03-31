FROM python:3.6-slim
WORKDIR /app
COPY requirements.txt .
RUN apt-get update &&\
      apt-get install -y gcc &&\
      pip install -r requirements.txt &&\
      apt-get remove --purge -y gcc &&\
      apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
COPY . .

