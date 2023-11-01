# django_early_return

## Installation

- `pip install django_early_return`
- add `'django_early_return.EarlyReturnMiddleware'` to `MIDDLEWARE` in your settings
- optionally, add `'django_early_return'` to `INSTALLED_APPS`, if you want to run our tests when executing `python manage.py test`

## Usage

Any view code (or middleware code, if that middleware is installed after EarlyReturnMiddleware) can now instantiate EarlyReturn with any HttpResponse, and that response will be returned to the user:
```python
    if not request.user.has_perm('my_app.some_permission'):
        raise django_early_return.EarlyReturn(http.HttpResponseForbidden())
```

For code in helper functions/middleware/etc., this is often more convenient than passing a response back to the actual view code.