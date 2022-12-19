FROM python:3.11-rc-slim

# setup base packages
RUN apt-get update \
    && apt-get -y install libpq-dev gcc wget zip \
    && pip install --upgrade pip \
    && pip3 install poetry

# install app packages
RUN mkdir /build
COPY ../pyproject.toml /build
WORKDIR /build
RUN poetry config virtualenvs.create false
RUN poetry install --only main
RUN rm -rf /build

# entry
RUN mkdir /app
WORKDIR /app