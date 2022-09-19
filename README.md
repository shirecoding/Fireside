# Fireside

## Setup

### Environment

- Python 3.10
- postgressql

```bash
brew upgrade python3
brew install postgresql
```

> :warning: Ensure `pip` command is linked to `pip3`

### Installation

```bash
pip3 install poetry

cd fireside
poerty install

# Copy default env settings
cp .env.example .env

```

> :warning: Ensure settings in `.env` is correct

## Start

```bash
cd fireside
docker-compose up

./manage migrate
./manage.py runserver
```
