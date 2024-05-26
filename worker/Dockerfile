# worker/Dockerfile
FROM python:latest

WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
    gcc \
    python3-dev \
    ffmpeg && \  
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
COPY . /app/


RUN pip install -r requirements.txt
EXPOSE 8080

CMD ["gunicorn", "-w", "4", "--preload", "--timeout", "0" , "-b", "0.0.0.0:8080", "app:app"]
