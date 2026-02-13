from django.urls import path
from .views import TEMPCreateUserAPIView

TEMP_USERS_ROUTE = "TEMP_USERS"

urlpatterns = [
    path("TEMP_USERS/", TEMPCreateUserAPIView.as_view(), name=TEMP_USERS_ROUTE),
]
