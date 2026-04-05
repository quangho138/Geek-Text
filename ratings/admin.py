from django.contrib import admin
from .models import Rating

class RatingAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'updated_at']

admin.site.register(Rating, RatingAdmin)

# since auto_now and auto_now_add fields are non-editable, Django admin hides them by default. So use readonly_fields to display them