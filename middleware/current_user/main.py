from .data import set_current_user, remove_current_user
from django.utils.functional import SimpleLazyObject


class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        set_current_user(getattr(request, 'user', None))
        # ^ This will work only during Browsable Api View Actions:
        # ie. POST, PUT
        #
        # Keeps getting Anonymous Lazy Object in API Call! (ie. Axios)
        # Because THIS Middleware gets executed before the
        # Token Auth Middleware gets to execute.
        #
        # FIX:
        # Added "set_current_user" to:
        # "app.accesslayer.authentication.AppTokenAuthentication:

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        # Will remove cached user that was set by:
        # "app.accesslayer.authentication.AppTokenAuthentication:
        remove_current_user()

        return response
