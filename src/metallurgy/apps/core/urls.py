from django.urls import path
from .views import (
    main
)

app_name = 'core'
urlpatterns = [
    path('', main),
]
