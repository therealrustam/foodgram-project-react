FROM python:3.7-slim

COPY ./ /app

WORKDIR /app

COPY backend/requirements.txt pwd

RUN pip3 install --upgrade pip && pip3 install -r backend/requirements.txt --no-cache-dir

RUN pip install gunicorn==20.1.0

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"] 
