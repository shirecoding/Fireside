# User Management

- [django-allauth](https://django-allauth.readthedocs.io/en/latest/installation.html)

## UserProfile

- Created when a user is created (see _user_profile/signals/handlers.py_)
- Stores the session which ties django session to a user
- Session is updated on every request via middleware (see _user_profile/middleware/UpdateUserProfileMiddleware_)
