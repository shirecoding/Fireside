## Building Templates

- Apps are located in *react-templates/src/app/*

- Build the react js bundles to the *dist* folder (see *webpack.config.js*)

    ```bash
    # in react-templates
    npm run build
    ```
- Copy static files to django project (see *firesidegames/settings/base.py/STATICFILES_DIRS*)

    ```bash
    # in firesidegames
    ./manage.py collectstatic
    ```