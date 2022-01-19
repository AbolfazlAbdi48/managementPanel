from django.http import Http404


class IsSuperUserMixin:
    """Check is superuser."""

    def dispatch(self, request, *args, **kwargs):
        if request.user and request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        raise Http404
