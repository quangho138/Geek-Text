from django.urls import path
from .views import get_ratings

urlpatterns = [
    path('ratings/', get_ratings, name='get_ratings'),
from . import views

urlpatterns = [
  path('books/<int:book_id>/reviews/', views.create_review, name="create_review"),
  path('books/<int:book_id>/reviews/<int:review_id>', views.update_review, name="update_review")
]