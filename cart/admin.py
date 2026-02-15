from django.contrib import admin
from .models import CartItem


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Admin interface for CartItem."""
    list_display = ['id','user','book','quantity','unit_price','subtotal_display']
    list_filter = ['user']
    search_fields = ['book__title', 'user__username']
    raw_id_fields = ['book']
    
    def subtotal_display(self, obj):
        return f"${obj.subtotal:.2f}"
    subtotal_display.short_description = 'Subtotal'
