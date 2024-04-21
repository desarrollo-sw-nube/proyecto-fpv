FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/
COPY . /app/

RUN pip install -r requirements.txt

EXPOSE 80 5000 5002

# CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=${PORT:-5000}"]
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
