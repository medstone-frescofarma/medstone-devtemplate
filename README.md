# Medstone template project

## Introduction

This is a template project meant to quickly create a new frontend + backend API for new projects within Medstone. It includes the following modules:

- Vue.js 3.x frontend
  - VueX
  - Vue Router
- FastAPI (Python) backend
  - Celery
  - SQLALchemy
- Postgres database
- Docker, Docker Compose and Docker Swarm files
- .devcontainer folder for development within a docker container (VSCode feature)

## Requirements

Operating System:

- ✅ Linux
  - Development works best on linux
- ✅ Windows
  - Works if you launch the devcontainer from a WSL folder. Otherwise hot-reloading the frontend does not work.
- MacOS ??
  - Not tested

Software:

- Docker & Docker-Compose
- VSCode
- Git

Hardware minimum specs:

- 2 CPU Cores
- 4GB RAM
- ~5GB disk space

## Installation

- The stone/surus environment relies on docker containers. Functioning docker requires the installation of the [docker engine](https://docs.docker.com/engine/install/) and [docker-compose](https://docs.docker.com/compose/install/).
- Development happens in the [VSCode IDE](https://code.visualstudio.com/download/) with the [remote-containers addon](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) enabled.
- Clone the project to your local machine using ```git clone```
- Copy the ```.env.example``` file to ```.env```
  - Edit ```.env``` file, env variables you probably want to edit are:
    - JWT_SECRET_KEY
    - POSTGRES_PASSWORD
    - SQLALCHEMY_DATABASE_URI

To start all development containers click the green '><' icon on the bottom-left of the VSCode IDE and select 'Open in container'
The apt-packages and Python libraries will be installed, this will take a couple of minutes. When completed browse to http://localhost to check if the installation is working.



# FastAPI backend webserver

#### start backend server with automatic reloading
```
uvicorn medstone_backend.main:app --host 0.0.0.0 --port 8000 --reload
```
Visit [http://localhost/docs](http://localhost/docs) to view the OpenAPI/Swagger documentation of our API.


# Database Migrations

#### first change current working directory to the "backend" folder
#### 'Alembic revision' create a new migration, auto diffs the current models in the python files against the current database structure
#### (remove --autogenerate to create a manual migration)
#### 'Alembic upgrade' head upgrades the connected database with the new migrations from backend/migrations/versions/*
```
cd backend
alembic revision --autogenerate
alembic upgrade head
```

# Python libraries

#### New Python libraries required for the backend need to be added to the 'backend/requirements/requirements.in' file.
```
nano backend/requirements/requirements.in
```
#### After adding your version-pinned python package; compile it to a requirements.txt by running
```
pip-compile backend/requirements/requirements.in --upgrade
```


# Celery Task queue

#### start celery queue worker
```
celery -A medstone_backend.main:celery_app worker -l info -Q default_queue
```

#### start celery beat (scheduler)
```
celery -A medstone_backend.main:celery_app beat
```

#### enqueue a task from the cli
```
docker-compose -f prod-new-docker-compose.yml run --rm backend celery -A medstone_backend.main:celery_app call medstone.webserver.main.tasks.pubmed_tasks.pubmed_scrape
```

#### flush redis queue
```
docker exec stone_redis_1 redis-cli flushall
```

#### start celery flower (task monitor interface)
```
celery -A medstone_backend.main:celery_app flower
```

# Live Deployment

#### deploy new version of web frontend and backend
```
docker-compose -f prod-docker-compose.yml config | docker stack deploy -c - --with-registry-auth stone
```


#### deploy new version of AI services
```
docker-compose -f ai-platform-docker-compose.yml config | docker stack deploy -c - --with-registry-auth stone_backend
```


# Code formatting using Black
```
black . --skip-string-normalization --line-length 100 --extend-exclude migrations
```


# Code profiling

## cpu usage with py-spy
```
sudo env "PATH=$PATH" py-spy record -o profile.svg -- python backend/py/medstone-webserver/medstone/webserver/start.py
```
