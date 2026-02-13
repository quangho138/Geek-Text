from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    home_address = models.TextField(blank=True, default="TEMP_HOME_ADDRESS")

    def __str__(self):
        return f"TEMP_PROFILE_FOR_{self.user.username}"