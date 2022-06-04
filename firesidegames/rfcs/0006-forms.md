# Forms

## Rendering forms

- For styling individual elements, use _ModelForm_ widget attrs
- For styling wrappers, _templates/includes/render_form.html_ is used to properly format certain inputs with the correct html and css

## Rendering settings (JSONField)

- Use _firesidegames/forms/settings.py/create_settings_form_ to create a form using introspection of the settings dictionary

## Prefilling forms dynamically

- Use javascript and _document.getElementById_ to get the form input and set the value
