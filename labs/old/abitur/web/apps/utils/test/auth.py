from functools import wraps

from django.contrib.auth import get_user_model

User = get_user_model()


def logged_in_as(email, password):
    def logged_in_decorator(call):
        @wraps(call)
        def wrapper(self, *args, **kwargs):
            User.objects.create_user(
                email=email,
                password=password,
                is_confirmed=True,
            )
            self.client.login(
                username=email,
                password=password,
            )
            return call(self, *args, **kwargs)

        return wrapper

    return logged_in_decorator
