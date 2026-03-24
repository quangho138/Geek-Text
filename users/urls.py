from django.urls import path
from .views import CreateUserAPIView, ProfileAPIView

CREATE_USER_ROUTE = "create_user"
PROFILE_ROUTE = "profile"

urlpatterns = [
    path("", CreateUserAPIView.as_view(), name=CREATE_USER_ROUTE),
    path("<int:user_id>/", ProfileAPIView.as_view(), name=PROFILE_ROUTE),
]