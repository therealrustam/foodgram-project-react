FROM python:3.7-slim

COPY ./ /app

WORKDIR /app

COPY backend/requirements.txt pwd

RUN pip3 install --upgrade pip && pip3 install -r /app/backend/requirements.txt --no-cache-dir

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000 
