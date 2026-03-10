from django.db import models
from books.models import Book

class Rating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="ratings")
    reviewer_name = models.CharField(max_length=100)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reviewer_name} - {self.book.name}"
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

  # this is set to current time only when object is created
  created_at = models.DateTimeField(auto_now_add=True, null=True)

  # this is set to current time everytime .save() is called
  updated_at = models.DateTimeField(auto_now=True, null=True)

  class Meta:
    constraints = [
        models.CheckConstraint(
            condition=models.Q(rating__gte=1, rating__lte=5),
            name='check_rating_between_1_and_5'
        )
    ]
    unique_together = ('user', 'book')




 
"""
In Django Shell: 

with connection.cursor() as cursor:
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='ratings_review';")

sets the auto_incrementing value of the id back to 0
"""

