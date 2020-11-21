# Testing Platform Api Server
This is the api server application used for testing platform purposes.

## Stack & technologies
- Modern Python development with Python 3.6+
- Django 3.0+
- Fully dockerized, local development via docker-compose.
- MySQL
- Full test coverage, continuous integration, and continuous deployment.
- Celery tasks

## API Docs

API documentation is automatically generated using Swagger and Redoc. You can view documention by visiting this [link](http://localhost:8000/swagger).

## Prerequisites

The project can be setup either using docker containers or locally. For local setup, you will need Python3 and MySQL installed.

## Local Development with Docker:

Start the dev server for local development:
```bash
cp .env.dist .env
docker-compose up
```

## Local Development without Docker

### Install

```bash
python3 -m venv env && source env/bin/activate                # activate venv
cp .env.dist .env                                             # create .env file and fill-in DB info
pip install -r requirements.txt                               # install py requirements
./manage.py migrate                                           # run migrations
./manage.py collectstatic --noinput                           # collect static files
redis-server                                                  # run redis locally for celery
celery -A src.config worker --beat --loglevel=debug
  --pidfile="./celerybeat.pid"
  --scheduler django_celery_beat.schedulers:DatabaseScheduler # run celery beat and worker
```

### Run dev server

This will run server on [http://localhost:8000](http://localhost:8000)

```bash
./manage.py runserver
```

### Create superuser

If you want, you can create initial super-user with next commad:

```bash
./manage.py createsuperuser
```

### Running Tests

To run all tests with code-coverate report, simple run:

```bash
./manage.py test
```

Authors:
Uroš Ogrizović R2-1/2020
Sava Katić R2-24/2020
