from django.urls import path
from . import views

urlpatterns = [
  path('books/<int:book_id>/ratings/', views.create_rating, name="create_rating")
]