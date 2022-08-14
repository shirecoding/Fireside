This app is used only during testing.

When creating new models for testing make sure to `makemigrations` for the test models

```bash
# fish shell
env ENVIRONMENT=test ./manage.py makemigrations
```

Related files and modules: - `core.settings.test` - `pytest.ini`
