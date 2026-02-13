from django.contrib import admin
from django.urls import path, include  # <-- add include

urlpatterns = [
    path("admin/", admin.site.urls),

    # Profile / user management routes
    path("users/", include("users.urls")),
]
