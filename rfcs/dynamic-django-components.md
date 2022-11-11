# Dynamic Django Components

## Stack

- django template for widget template
- htmx to dynamically swap html fragments by querying a REST endpoint
- django ninja to serve the REST endpoint

## How it works

Any widget (eg. `FiresideTextInput`) which requires dynamic HTML inherits from `WebComponent`

```python
from abc import ABC, abstractmethod

class WebComponent(ABC):

    throttle = '500ms'

    @abstractmethod
    def on_change(self):
        pass

    def get_context(self):
        return {
            'fragment_url': '/fireside_dynamic_fragment',
            'path': function_to_import_path(self),
        }
```

`get_context` is used to render the django template for the widget

```html
<!-- Reference from: django/forms/widgets/text.html -->
<div>
  <input type="{{ widget.type }}" name="{{ widget.name }}" {% if widget.value !=
  None %} value="{{ widget.value|stringformat:'s' }}"{% endif %} {% include
  "django/forms/widgets/attrs.html" %} hx-trigger="load, keyup changed
  throttle:500ms" hx-get="{{ fragment_url }}" hx-target="#hints"
  hx-swap="innerHTML" >
  <span id="hints"></span>
</div>
```

Single django ninja REST endpoint for dynamic retrieval of content

```python
class WebComponentEvent(Schema):
    path: str
    args:

@api.post('/fireside_dynamic_fragment', description='Dynamic HTML fragments for WebComponent')
def fireside_dynamic_fragment() -> str:

```
