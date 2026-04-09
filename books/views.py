from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Book
from .serializers import BookSerializer
from decimal import Decimal


@api_view(['GET'])
def book_list(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def books_by_genre(request):
    genre = request.GET.get('genre')

    if not genre:
        return Response({"error": "Genre parameter is required"}, status=400)

    books = Book.objects.filter(genre__iexact=genre)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def top_sellers(request):
    books = Book.objects.order_by('-copies_sold')[:10]
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


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

    if not publisher or discount is None:
        return Response({"error": "publisher and discount_percent required"}, status=400)

    try:
        discount = float(discount)
    except ValueError:
        return Response({"error": "discount_percent must be a number"}, status=400)

    books = Book.objects.filter(publisher__iexact=publisher)

    if not books.exists():
        return Response({"error": "No books found for this publisher"}, status=404)

    for book in books:
        discount_factor = Decimal(100 - discount) / Decimal(100)
        book.price = book.price * discount_factor
        book.save()

    return Response({"message": "Discount applied successfully"})