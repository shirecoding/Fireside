# Setting The Environment

Different settings are loaded depending on the `ENVIRONMENT` variable (development(default), test, production). See

- `core.settings.__init__.py`

# Testing

```bash
# run the following in fireside directory (fish shell)
poetry shell
./manage.py makemigrations
./manage.py migrate
pytest -s
```

These are the relevant pytest config files

- `fireside/pytest.ini`
- `fireside/conftest.py`

During testing the `fireside/core/settings/test.py` django settings will loaded.

# Development Environment

Make sure to run the following on a new database

```bash
./manage.py createsuperuser
./manage.py migrate
```

The entire project will be mounted on `/app` inside the fireside docker container

```bash
# run the following in fireside directory
docker-compose up

# separate window
poetry shell
./manage.py runserver
```

## Updating Permissions

When creating new models which inherit from `fireside.models.model` run the following to create the new field level permissions

```bash
./manage.py update_permissions
./manage.py remove_stale_contenttypes
```

Environment variables are located at (needs to be created as it is not stored in the repository)

- `fireside/.env`

  ```bash
  # Django
  SECRET_KEY=password
  WEB_PORT=8000

  # Postgres
  DB_PASSWORD=password
  DB_HOST=127.0.0.1
  DB_PORT=5432

  # Redis
  CACHE_PASSWORD=password
  CACHE_HOST=127.0.0.1
  CACHE_PORT=6379

  # M1 Max (+[__NSCFConstantString initialize] may have been in progress in another thread when fork() was called.)
  OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

  # Allow print statements for development debugging (degrades performance) - do not set for production
  PYTHONUNBUFFERED=1
  ```

The Dockerfile is located at

- `fireside/Fireside.Dockerfile`
