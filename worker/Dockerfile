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

RUN chmod +x /app/app_worker/resize.sh

RUN pip install -r requirements.txt
ENV PYTHONPATH=/app

# CMD ["celery", "-A", "app_worker.celery", "worker", "-l", "error", "--events"]
CMD ["python", "/app/app_worker/subscriber.py"]


