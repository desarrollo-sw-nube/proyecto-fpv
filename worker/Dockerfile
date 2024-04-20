FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/
COPY . /app/

RUN pip install -r requirements.txt

EXPOSE 5001

CMD ["python" , "-m" , "flask", "run", "--host=0.0.0.0", "--port=5001"]
