from django.db import models
from books.models import Book
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
  user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', null=False)
  book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews', null=False)
  rating = models.IntegerField(
    validators=[
      MinValueValidator(1),
      MaxValueValidator(5)
    ]
  )

  comment = models.CharField(max_length=255, blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True, null=True)

  class Meta:
    constraints = [
        models.CheckConstraint(
            condition=models.Q(rating__gte=1, rating__lte=5),
            name='check_rating_between_1_and_5'
        )
    ]
    unique_together = ('user', 'book')
