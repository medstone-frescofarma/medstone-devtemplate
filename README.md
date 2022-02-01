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

- Clone the project to your local machine using ```git clone```
- Copy the ```.env.example``` file to ```.env```
  - Edit ```.env``` file, env variables you probably want to edit are:
    - JWT_SECRET_KEY
    - POSTGRES_PASSWORD
    - SQLALCHEMY_DATABASE_URI

