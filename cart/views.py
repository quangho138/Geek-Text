from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import CartItem
from .serializers import CartItemSerializer


@api_view(['GET'])
def get_cart(request):
    """
    Basic GET endpoint to retrieve cart data.
    """
    cart_items = CartItem.objects.all().select_related('book', 'user')
    serializer = CartItemSerializer(cart_items, many=True)
    
    return Response({
        'count': cart_items.count(),
        'items': serializer.data
    }, status=status.HTTP_200_OK)
