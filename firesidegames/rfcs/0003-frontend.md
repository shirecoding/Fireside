# Frontend

## Soft UI

- https://github.com/app-generator/django-soft-ui-dashboard

## React templates

- See templates/react-templates

    ```bash
    npx create-react-app react-templates
    npx sb init
    npm run storybook
    ```

- Create symlink to static folder

    ```bash
    cd react-templates/src
    ln -s ../../../static/ static
    ```

- Link static folder to storybook in *package.json/scripts/storybook*

- Load static assets in *.storybook/preview-head.html* and *.storybook/preview-body.html*
