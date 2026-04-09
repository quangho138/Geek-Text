from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Sum, F,QuerySet
from rest_framework.decorators import api_view ,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import CartItem
from .serializers import CartItemSerializer
from books.models import Book

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):
    """
    GET /api/cart/
    
    Retrieve list of books in user's cart.
    
    Query params:
    ?user_id=123
    
    Response:
    {
        "user_id": 123,
        "item_count": 2,
        "books": [...]
    }
    """
    # Get user_id from query params
    user_id = request.query_params.get('user_id')
    
    if not user_id:
        return Response(
            {'error': 'user_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return Response(
            {'error': 'user_id must be a valid number'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if user exists
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Get cart items with book details
    cart_items: QuerySet[CartItem] = CartItem.objects.filter(
        user_id=user_id
    ).select_related('book', 'book__author')
    
    serializer = CartItemSerializer(cart_items, many=True)
    
    return Response({
        'user_id': user_id,
        'item_count': cart_items.count(),
        'books': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_subtotal(request):
    """
    GET /api/cart/subtotal/
    
    Calculate subtotal of all items in user's cart.
    
    Query params:
    ?user_id=123
    
    Response:
    {
        "user_id": 123,
        "subtotal": "149.95"
    }
    """
    user_id = request.query_params.get('user_id')
    
    if not user_id:
        return Response(
            {'error': 'user_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return Response(
            {'error': 'user_id must be a valid number'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if user exists
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Calculate subtotal
    cart_items = CartItem.objects.filter(user_id=user_id)
    subtotal = cart_items.aggregate(
        total=Sum(F('quantity') * F('unit_price'))
    )['total'] or 0
    
    return Response({
        'user_id': user_id,
        'subtotal': f"{subtotal:.2f}"
    }, status=status.HTTP_200_OK)

# NEW: Add to cart endpoint
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    """
    POST /api/cart/items/
    
    Add a book to user's cart or update quantity if already exists.
    
    """
    # Get data from request
    book_id = request.data.get('book_id')
    user_id = request.data.get('user_id')
    quantity = request.data.get('quantity', 1)
    
    # Validate book_id
    if not book_id:
        return Response(
            {'error': 'book_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    # Validate user_id
    if not user_id:
        return Response(
            {'error': 'user_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    # Validate quantity
    try:
        quantity = int(quantity)
        if quantity < 1:
            return Response(
                {'error': 'quantity must be at least 1'},
                status=status.HTTP_400_BAD_REQUEST
            )
    except (ValueError, TypeError):
        return Response(
            {'error': 'quantity must be a valid number'},
            status=status.HTTP_400_BAD_REQUEST
        )
    # Check if user exists
    try:
        book = User.objects.get(id=book_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Check if book exists
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response(
            {'error': 'Book not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Check if item already in user's cart
    cart_item, created = CartItem.objects.get_or_create(
        user_id=user_id,
        book=book,
        defaults={
            'quantity': quantity,
            'unit_price': book.price
        }
    )
    
    if not created:
        # Item already exists, add to quantity
        cart_item.quantity += quantity
        cart_item.save()
        message = 'Cart item quantity updated'
    else:
        message = 'Item added to cart'
    
    # Serialize and return
    serializer = CartItemSerializer(cart_item)
    
    return Response({
        'message': message,
        'item': serializer.data
    }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_cart_item(request, item_id):
    """
    PUT /api/cart/items/{item_id}/
    
    Update quantity of a cart item.
    
    """
    # Check if cart item exists and belongs to user
    try:
        cart_item = CartItem.objects.get(id=item_id, user=request.user)
    except CartItem.DoesNotExist:
        return Response(
            {'error': 'Cart item not found or does not belong to you'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Get new quantity
    quantity = request.data.get('quantity')
    
    if quantity is None:
        return Response(
            {'error': 'quantity is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Validate quantity
    try:
        quantity = int(quantity)
        if quantity < 1:
            return Response(
                {'error': 'quantity must be at least 1'},
                status=status.HTTP_400_BAD_REQUEST
            )
    except (ValueError, TypeError):
        return Response(
            {'error': 'quantity must be a valid number'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Update quantity
    cart_item.quantity = quantity
    cart_item.save()
    
    # Serialize and return
    serializer = CartItemSerializer(cart_item)
    
    return Response({
        'message': 'Cart item updated',
        'item': serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request):
    """
    DELETE /api/cart/items/delete/
    
    Remove a specific book from user's cart.
    
    Request body or query params:
    {
        "book_id": 1,
        "user_id": 123
    }
    
    Response:
    {
        "message": "Book removed from cart"
    }
    """
    # Get parameters from body or query params
    book_id = request.data.get('book_id') or request.query_params.get('book_id')
    user_id = request.data.get('user_id') or request.query_params.get('user_id')
    
    if not book_id:
        return Response(
            {'error': 'book_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not user_id:
        return Response(
            {'error': 'user_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Convert to integers
    try:
        book_id = int(book_id)
        user_id = int(user_id)
    except (ValueError, TypeError):
        return Response(
            {'error': 'book_id and user_id must be valid numbers'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if user exists
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Check if book exists
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response(
            {'error': 'Book not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Find and delete cart item
    try:
        cart_item = CartItem.objects.get(user_id=user_id, book_id=book_id)
        cart_item.delete()
        
        return Response(
            {'message': 'Book removed from cart'},
            status=status.HTTP_200_OK
        )
    except CartItem.DoesNotExist:
        return Response(
            {'error': 'Book is not in the cart'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_cart(request):
    """
    DELETE /api/cart/clear/
    
    Clear all items from user's cart.
    
    Request body or query params:
    {
        "user_id": 123
    }
    
    Response:
    {
        "message": "Cart cleared",
        "items_deleted": 3
    }
    """
    user_id = request.data.get('user_id') or request.query_params.get('user_id')
    
    if not user_id:
        return Response(
            {'error': 'user_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return Response(
            {'error': 'user_id must be a valid number'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if user exists
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Delete all cart items for user
    cart_items = CartItem.objects.filter(user_id=user_id)
    count = cart_items.count()
    cart_items.delete()
    
    return Response({
        'message': 'Cart cleared',
        'items_deleted': count
    }, status=status.HTTP_200_OK)