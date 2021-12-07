# Forms

## Rendering forms

- For styling individual elements, use *ModelForm* widget attrs
- For styling wrappers, *templates/includes/render_form.html* is used to properly format certain inputs with the correct html and css

## Rendering settings (JSONField)

- Use *firesidegames/forms/settings.py/create_settings_form* to create a form using introspection of the settings dictionary

## Prefilling forms dynamically

- Use javascript and *document.getElementById* to get the form input and set the value
