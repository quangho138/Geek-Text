from rest_framework import generics
from .models import Author, Book
from rest_framework.response import Response
from .serializers import AuthorSerializer, BookSerializer


@api_view(['GET'])
def books_by_rating(request):
    rating = request.GET.get('rating')

    if not rating:
        return Response({"error": "Rating parameter is required"}, status=400)

    try:
        rating = float(rating)
    except ValueError:
        return Response({"error": "Rating must be a number"}, status=400)

    books = Book.objects.filter(rating__gte=rating)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
def discount_books(request):
    publisher = request.data.get('publisher')
    discount = request.data.get('discount_percent')

    def get(self, request, *args, **kwargs):
        isbn = kwargs.get("isbn")

        if len(isbn) != 10 and len(isbn) != 13:
            return Response(
                {"message": "Please try again with a 10 or 13 digit ISBN."},
                status = 400
            )

        return super().get(request, *args, **kwargs)


    try:
        discount = float(discount)
    except ValueError:
        return Response({"error": "discount_percent must be a number"}, status=400)

    def get_queryset(self):
        author_id = self.kwargs["author_id"]
        return Book.objects.filter(author_id = author_id).order_by("name")

    if not books.exists():
        return Response({"error": "No books found for this publisher"}, status=404)

    for book in books:
        discount_factor = Decimal(100 - discount) / Decimal(100)
        book.price = book.price * discount_factor
        book.save()

    def get_queryset(self):
        return Book.objects.order_by("-copies_sold")
