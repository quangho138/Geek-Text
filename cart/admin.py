from django.contrib import admin
from .models import CartItem


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Admin interface for CartItem."""
    list_display = ['id','user','book','quantity','unit_price','subtotal_display']
    list_filter = ['user']
    search_fields = ['book__title', 'user__username']
    raw_id_fields = ['book']
     # Make unit_price optional in admin
    fields = ['user', 'book', 'quantity', 'unit_price']
    
    def subtotal_display(self, obj):
        return f"${obj.subtotal:.2f}"
    subtotal_display.short_description = 'Subtotal'

    def save_model(self, request, obj, form, change):
        """Auto-fill unit_price if not provided."""
        if not obj.unit_price and obj.book:
            obj.unit_price = obj.book.price
        super().save_model(request, obj, form, change)