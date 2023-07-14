FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl

RUN pip install poetry

COPY . .

RUN chmod +x entrypoint.sh

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi


ENTRYPOINT ["bash", "entrypoint.sh"]
