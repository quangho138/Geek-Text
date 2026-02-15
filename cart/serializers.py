from rest_framework import serializers
from .models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for CartItem"""
    
    book_title = serializers.CharField(source='book.name', read_only=True)
    book_author = serializers.CharField(source='book.author', read_only=True)
    book_price = serializers.DecimalField(
        source='book.price',
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    subtotal = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    
    class Meta:
        model = CartItem
        fields = [
            'id',
            'book_title',
            'book_author',
            'book_price',
            'quantity',
            'unit_price',
            'subtotal'
        ]