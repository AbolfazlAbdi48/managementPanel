from django.urls import path
from .views import zarinpal_send_request, zarinpal_verify

app_name = 'payments'
urlpatterns = [
    path('zarinpal-request/', zarinpal_send_request, name='zarinpal-request'),
    path('zarinpal-verify/', zarinpal_verify, name='zarinpal-verify'),
]
