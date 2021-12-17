# User Management

- [django-allauth](https://django-allauth.readthedocs.io/en/latest/installation.html)


## UserProfile

- Created when a user is created (see *user_profile/signals/handlers.py*)
- Stores the session which ties django session to a user
- Session is updated on every request via middleware (see *user_profile/middleware/UpdateUserProfileMiddleware*)
