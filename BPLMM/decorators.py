from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def encoder_required(function):
    @login_required
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.groups.filter(name='Encoder').exists():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def approver_required(function):
    @login_required
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.groups.filter(name='Approver').exists():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
