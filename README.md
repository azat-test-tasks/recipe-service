# Recipe service

This is an API service for creating, editing, deleting, retrieving list and getting information about a particular recipe. The service supports basic and advanced functions, such as filtering by ingredient list, cooking step times and sorting the list by total cooking time, user authentication and authorization, the ability to add a score, upload images and more.


## Installation
1. Clone the repository
2. Create a virtual environment
3. Install the requirements


## Local deployment
```bash
python3 -m venv env
source env/bin/activate
pip install poetry
poetry install
```

Create .env file, extract the virtual environment variables into the .env file (you can find an example in env.example)

```bash
alembic upgrade head
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Run linting and formatting
```bash
flake8 . --count --statistics --show-source &&
black . && 
isort --check .
```

### Docker deployment

* Watch commands in the Makefile

```bash
make help
```

* Build docker image

```bash
make build
```

* Run docker container

```bash
make up
```

* Run tests

```bash
make test
```

* Stop docker container

```bash
make down
```

* Clean all docker containers

```bash
make prune
```

## Technologies
* FastAPI 0.95.1
* Alembic 1.10.3
* SQLAlchemy 2.0.9
* PostgreSQL 14.6
* Poetry 1.1.11
* Docker 20.10.17