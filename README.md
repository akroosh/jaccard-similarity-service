## Overview
This project aims to create a Similarity Search Service. The service allows users to find similar items based on an input query by computing the Jaccard similarity score. Additionally, it enables users to add new items to the database for efficient similarity searching.

## Table of Contents  
- [Technologies](#technologies)  
- [Installation](#installation)  
- [Running app](#running)  
- [Migrations](#migrations)  
- [Tests](#tests)  

<a id="technologies"/>

## Using

- [Python3.9](https://docs.python.org/3.9/)
- [gRPC](https://grpc.io/)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/index.html)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)
- [Poetry](https://python-poetry.org/)

<a id="installation"/>

## Installation

To get started, create an `.env` file and fill it using the example provided:
```bash
cp .env-example .env
```

### Poetry
We use `poetry` to manage package dependencies. Follow this [link](https://python-poetry.org/docs/cli/) for more info.

1. Install all dependencies in the root folder by running the following command:
```bash
poetry install
```
This will generate a `poetry.lock` file, which stores all package versions.
2. To add a new package, use the command:
```bash
poetry add <package_name>
```
3. If you encounter an error during the above step, try clearing the poetry cache with:
```bash
poetry cache clear pypi --all
```
4. If the step above doesn't resolve the issue, consider removing `poetry.lock` and regenerating it:
```bash
poetry install
```
5. Activate the virtual environment with:
```bash
poetry shell
```
6. To lock `poetry.lock` and fix the current version before creating a pull request, run%
```bash
poetry lock
```
<a id="running"/>

## Running
### Running for development

You can run app locally with the following command:

```bash
python main.py
```

### Running using Docker

To run the Jaccard Similarity Service using docker-compose, follow these steps:

1. Fill in the required values in the `.env` file. Set `POSTGRES_HOST` to `pgdatabase`.
To run server, set `TARGER` to `app`.


2. Run using following command:
```bash
docker-compose up
```
<a id="migrations"/>

## Database Migrations

> **_NOTE:_** Make sure to activate `.env` first


#### Generate migration
```bash
alembic revision --autogenerate -m "<insert migration description here>"
```

#### Migrate
```bash
alembic upgrade head
```
<a id="tests"/>

## Running Unit Tests
The Jaccard Similarity Service includes a comprehensive suite of unit tests to ensure the functionality and reliability of its components. You can run these unit tests locally or with docker-compose based on your preference.

### Locally using Python
To run the unit tests locally, follow these steps:

1. Ensure you have activated the virtual environment (if you are using one).

2. In the root directory of the project, run the following command:

```bash
python -m unittest
```
The command will execute all the unit tests, and you will see the test results on the console.

### Using Docker Compose
To run the unit tests using docker-compose, follow these steps:

1. Set the `TARGET` environment variable in the `.env` file to `test`.

2. Start the Jaccard Similarity Service with docker-compose:
```bash
docker-compose up
```
The service will run the unit tests automatically due to the `TARGET` being set to `test`. The test results will be displayed in the console output.
