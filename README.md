### Install

```bash
pip install -r requirements.txt
```

### Run with Docker

To run the app with docker, you can run the following command:

```bash
docker-compose up
```

### Run with flask

Is not recommended to run the app with flask, but if you want to do it, you can run the following commands:

```bash
export FLASK_APP=app/app.py
flask run
```

## Turn off volumes

```bash
docker-compose down --volumes
```
