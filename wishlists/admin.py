from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Wishlist

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "user"]
    filter_horizontal = ["books"]