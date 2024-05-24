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

RUN chmod +x /app/resize.sh

RUN pip install -r requirements.txt
EXPOSE 8080


CMD ["python", "/app/subscriber.py"]


