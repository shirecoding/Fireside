# User Management

- [django-allauth](https://django-allauth.readthedocs.io/en/latest/installation.html)


## UserProfile

- Created when a user is created (see *profile_settings/signals/handlers.py*)

## UserSession

- Created/Updated when user logs in (see *profile_settings/signals/handlers.py*)
- *last_updated* shows the last datetime of activity of the user (see *profile_settings/middleware/SetUserSessionLastUpdated*)
