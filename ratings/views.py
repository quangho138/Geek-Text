from books.models import Book
from .models import Review
from .serializers import ReviewSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status



@api_view(['POST'])
def create_rating(request, book_id):

  # tries to find the book in the database. If it doesn't exist, a Book.DoesNotExist exception is raised.
  try:
      book = Book.objects.get(pk=book_id)
  except Book.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  
  # checks if user already made a review on the book
  user_id = request.data.get('user')
  existing_review = check_user_ratings(user_id, book)
  if existing_review:
    return existing_review

  serializer = ReviewSerializer(data=request.data)
  if serializer.is_valid():
    
    serializer.save(book=book) # creates a new row in the Review table, injecting the book object that was looked up earlier as the book_id using the serializer's field 'book'

    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
  # if .is_valid() fails, return the error messages
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




def check_user_ratings(user, book):
   if Review.objects.filter(user=user, book=book).exists():
      return Response({"message" : f"User {user} has already made a review on {book}"}, status=status.HTTP_400_BAD_REQUEST)
   return None