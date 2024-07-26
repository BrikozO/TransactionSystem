FROM python:3.12.0-slim

RUN mkdir "web"
RUN groupadd -r web && useradd -r web -g web

ENV WEB_APP=/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR $WEB_APP
RUN pip install --upgrade pip
COPY ./requirements.txt $WEB_APP
RUN pip install -r requirements.txt

COPY . $WEB_APP

RUN chown -R web:web $WEB_APP
