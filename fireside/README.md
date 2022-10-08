# Setting The Environment

Different settings are loaded depending on the `ENVIRONMENT` variable (development(default), test, production). See

- `core.settings.__init__.py`

# Testing

```bash
# run the following in fireside directory (fish shell)
poetry shell
env ENVIRONMENT=test ./manage.py makemigrations  # make sure fireside_tests models are in the db
env ENVIRONMENT=test ./manage.py migrate
env ENVIRONMENT=test pytest -s
```

These are the relevant pytest config files

- `fireside/pytest.ini`
- `fireside/conftest.py`

During testing the `fireside/core/settings/test.py` django settings will loaded.

- Adds `fireside_tests` app into the django project

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
  SECRET_KEY=lordoftheringsandthematrix
  WEB_PORT=80

  # Postgres
  DB_PASSWORD=lordoftheringsandthematrix
  DB_HOST=127.0.0.1
  DB_PORT=5432

  # Redis
  CACHE_PASSWORD=lordoftheringsandthematrix
  CACHE_HOST=127.0.0.1
  CACHE_PORT=6379

  # M1 Max (+[__NSCFConstantString initialize] may have been in progress in another thread when fork() was called.)
  OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
  ```

The Dockerfile is located at

- `fireside/Fireside.Dockerfile`

# TODOs

- `fireside.tasks.apps.ready` should not reschedule tasks on management commands but only on app start
- ACLs for list view dose not work, blank out fields? for OLP?
- Setup integration test environment with the redis, rq scheduler, rq worker
- move `tasks` into `fireside.tasks`
- Task Definition change of function name should not remove it from the database, but should just update the import path, else just changing a function name will break any tasks which use the definition
- Replace DRF with django ninja
- OLP Change read/write to view/change

- [DONE]Module level ACLs not working with Admin (cant see fields even though set)
