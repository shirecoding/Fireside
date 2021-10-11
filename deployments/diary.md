
# 10 Oct 2021
--------------------------------------------------------------------------------------------

## Setup

1. Copy over the following folders from *deps/django-soft-ui-dashboard* to *firesideweb/*

    - apps/authentication (rename config.py to apps.py, modify accordingly)
    - apps/home (rename config.py to apps.py, modify accordingly)
    - static
    - templates
    - core/urls.py (fill in other apps as needed)

2. Add *home* and *authentication* to *settings/INSTALLED_APPS*

3. Fix all imports, paths, urls that reference *apps*

