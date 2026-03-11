from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    home_address = models.TextField(blank=True, default="No address provided")

    def __str__(self):
        return f"Profile for {self.user.username}"