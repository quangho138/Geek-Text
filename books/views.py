from rest_framework import generics
from .models import Author, Book
from rest_framework.response import Response
from .serializers import AuthorSerializer, BookSerializer


class AuthorCreateView(generics.CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookByISBNView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "isbn"

    def get(self, request, *args, **kwargs):
        isbn = kwargs.get("isbn")

        if len(isbn) != 10 and len(isbn) != 13:
            return Response(
                {"message": "Please try again with a 10 or 13 digit ISBN."},
                status=400
            )

        return super().get(request, *args, **kwargs)


class BooksByAuthorView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        author_id = self.kwargs["author_id"]
        return Book.objects.filter(author_id=author_id).order_by("name")


class TopSellersView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.order_by("-copies_sold")
