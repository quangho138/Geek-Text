from django.urls import path
from .views import CreateUserAPIView, ProfileAPIView, LoginView, CurrentUserView

urlpatterns = [
    path("", CreateUserAPIView.as_view()),
    path("login/", LoginView.as_view()),
    path("me/", CurrentUserView.as_view()),
    path("<int:user_id>/", ProfileAPIView.as_view()),
]