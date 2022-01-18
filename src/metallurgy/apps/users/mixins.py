from django.shortcuts import redirect


class AuthenticatedMixin:
    """Check authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('users:home')
        return super().dispatch(request, *args, **kwargs)
