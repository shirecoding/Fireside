FROM python:3.11-rc-slim

# setup base packages
RUN apt-get update \
    && apt-get -y install libpq-dev gcc wget zip

RUN pip install --upgrade pip

# install app dependencies
RUN mkdir /app
COPY ../pyproject.toml /app
WORKDIR /app
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
