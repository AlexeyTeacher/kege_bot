FROM python:3.9-slim

COPY . /app
WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV TZ=Europe/Moscow

COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh


RUN pip3 install --upgrade pip
RUN pip3 install -r /app/requirements.txt

RUN apt-get update
RUN apt-get install nano

ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]
