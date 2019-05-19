FROM python:3.7-alpine
MAINTAINER Lionell Loh

ENV PYTHONUNBUFFERED 1

#Copy from our directory to our docker image's root director
COPY ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user