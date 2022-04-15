FROM python:3.7-slim

COPY ./ /app

WORKDIR /app

COPY backend/requirements.txt pwd

RUN pip3 install -r requirements.txt --no-cache-dir

CMD ["python3", "manage.py", "runserver", "0:8000"] 