from django.shortcuts import render
from django.db.models import Sum, F
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import CartItem
from .serializers import CartItemSerializer

@api_view(['GET'])
def get_cart(request):
    """
    GET /api/cart/
    
    
    Response includes:
    - item_count: Number of different books
    - total_items: Total quantity across all books
    - total_price: Grand total of all items
    - items: Array of cart items with details
    """
    # Get all cart items with related book and user data
    cart_items = CartItem.objects.all().select_related('book', 'user')
    
    # Calculate totals using database aggregation
    totals = cart_items.aggregate(
        total_price=Sum(F('quantity') * F('unit_price')),
        total_items=Sum('quantity')
    )
    serializer = CartItemSerializer(cart_items, many=True)
    
    return Response({
        'summary': {
        'item_count': cart_items.count(),
        'total_items': totals['total_items'] or 0,
        'total_price': f"{totals['total_price']:.2f}" if totals['total_price'] else "0.00"
        },
        'items': serializer.data
    }, status=status.HTTP_200_OK)