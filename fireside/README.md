# Testing

```bash
# run the following in fireside directory (fish shell)
poetry shell
env ENVIRONMENT=test ./manage.py makemigrations  # make sure fireside_tests models are in the db
env ENVIRONMENT=test ./manage.py migrate
env ENVIRONMENT=test pytest
```

These are the relevant pytest config files

- `fireside/pytest.ini`
- `fireside/conftest.py`

During testing the `fireside/core/settings/test.py` django settings will loaded.

- Adds `fireside_tests` app into the django project

# Development Environment

The entire project will be mounted on `/app` inside the fireside docker container

```bash
# run the following in fireside directory
docker-compose up

# seperate window
poetry shell
./manage.py runserver
```

Environment variables are located at (needs to be created as it is not stored in the repository)

- `fireside/.env`

  ```bash
  ENVIRONMENT=development
  SECRET_KEY=REPLACE_WITH_PASSWORD
  DB_PASSWORD=REPLACE_WITH_PASSWORD
  DB_HOST=localhost
  DB_PORT=5432
  CACHE_PASSWORD=REPLACE_WITH_PASSWORD
  CACHE_HOST=127.0.0.1
  CACHE_PORT=6379
  OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES  # M1 Max (+[__NSCFConstantString initialize] may have been in progress in another thread when fork() was called.)
  ```

- `fireside/.env.docker` (host IPs are repalced with the docker IP)
  ```bash
  ENVIRONMENT=development
  SECRET_KEY=REPLACE_WITH_PASSWORD
  DB_PASSWORD=REPLACE_WITH_PASSWORD
  DB_HOST=db
  DB_PORT=5432
  CACHE_PASSWORD=REPLACE_WITH_PASSWORD
  CACHE_HOST=cache
  CACHE_PORT=6379
  OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES  # M1 Max (+[__NSCFConstantString initialize] may have been in progress in another thread when fork() was called.)
  ```

The Dockerfile is located at

- `fireside/Fireside.Dockerfile`

# TODOs

- `fireside.tasks.apps.ready` should not reschedule tasks on management commands but only on app start
- Module level ACLs not working with Admin (cant see fields even though set)
- Setup integration test environment with the redis, rq scheduler, rq worker
- move `tasks` into `fireside.tasks`
- Task Definition change of function name should not remove it from the database, but should just update the import path, else just changing a function name will break any tasks which use the definition
- Replace DRF with django ninja
- OLP Change read/write to view/change

- [DONE] ACLs for list view dose not work, blank out fields? for OLP?
