## Build and Run App module

cd app
docker build --tag 'app_docker' .
docker build --platform=linux/amd64 --tag 'app_docker' .
docker run -v /uploads:/app/uploads -p 5005:5005 'app_docker'
docker run -v /Users/santiagoforeroa/uploads:/app/uploads -p 80:80 'app_docker'
docker run -v /uploads:/app/uploads -p 80:80 'us-east1-docker.pkg.dev/desarrollo-sw-nube/app-repo/app_docker'
docker run -v uploads:/app/uploads -p 80:80 'us-east1-docker.pkg.dev/desarrollo-sw-nube/app-repo/app_docker'

docker tag app_docker:latest us-east1-docker.pkg.dev/desarrollo-sw-nube/app-repo/app_docker:latest
docker push us-east1-docker.pkg.dev/desarrollo-sw-nube/app-repo/app_docker:latest

## Build and Run Worker module

cd worker
docker-compose up --build

docker build -t worker_app .
docker build --platform=linux/amd64 --tag 'worker_app' .
docker tag worker_app:latest us-east1-docker.pkg.dev/desarrollo-sw-nube/worker-repo/worker_app:latest
docker push us-east1-docker.pkg.dev/desarrollo-sw-nube/worker-repo/worker_app:latest

docker run -v /Users/santiagoforeroa/uploads:/app/uploads worker_app

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
