FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \   
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
COPY . /app/

RUN pip install -r requirements.txt



ENV FLASK_APP=app.py

EXPOSE 80

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=80"]
