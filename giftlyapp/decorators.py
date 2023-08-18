from functools import wraps
from django.shortcuts import redirect


def allow_anonymous(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            next_url = request.get_full_path()  # Get the current URL
            return redirect(f'/accounts/login/?next={next_url}')  # Redirect to the login page
    return _wrapped_view
