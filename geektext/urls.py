from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # Profile / user management routes
    path("users/", include("users.urls")),

    # API routes
    path("api/", include("books.urls")),
    path('api/', include('cart.urls')),
    path('api/', include('ratings.urls'))
]
