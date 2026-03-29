from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import WishlistCreateSerializer
from .serializers import AddBookToWishlistSerializer

from django.shortcuts import get_object_or_404
from .models import  Wishlist
from books.models import Book

class WishlistCreateView(generics.CreateAPIView):
    serializer_class = WishlistCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # “Response Data: None” -> empty body
        return Response(status=status.HTTP_201_CREATED)

class AddBookToWishlistView(generics.CreateAPIView):
    serializer_class = AddBookToWishlistSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        book_id = serializer.validated_data["book_id"]
        wishlist_id = serializer.validated_data["wishlist_id"]

        wishlist = get_object_or_404(Wishlist, id=wishlist_id)
        book = get_object_or_404(Book, id=book_id)

        wishlist.books.add(book)

        return Response(status=status.HTTP_204_NO_CONTENT)
    
class RemoveBookFromWishlistView(APIView):
    """
    DELETE /api/wishlists/<int:wishlist_id>/books/<int:book_id>/
    """

    def delete(self, request, wishlist_id, book_id):
        wishlist = get_object_or_404(Wishlist, id=wishlist_id)
        book = get_object_or_404(Book, id=book_id)

        if not wishlist.books.filter(id=book_id).exists():
            return Response(
                {"detail": "Book not found in this wishlist."},
                status=status.HTTP_404_NOT_FOUND
            )

        wishlist.books.remove(book)

        return Response(status=status.HTTP_204_NO_CONTENT)