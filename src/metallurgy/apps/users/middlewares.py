from .models import User
from django.utils import timezone


class LastActivityMiddleware:
    """
    The middleware set last activity for any user.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        if request.user.is_authenticated:
            online_user = User.objects.filter(pk=request.user.pk).first()
            online_user.last_activity = timezone.now()
            online_user.save()

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
