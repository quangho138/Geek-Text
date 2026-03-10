from django.db import models
from django.conf import settings
from books.models import Book


class Wishlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wishlists"
    )
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, related_name="wishlists", blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "name"], name="unique_wishlist_name_per_user")
        ]

    def __str__(self):
        return f"{self.name} (ID: {self.id})"