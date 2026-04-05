from books.models import Book
from .models import Rating
from .serializers import RatingSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Avg
from django.core.exceptions import ObjectDoesNotExist

@api_view(['GET'])
def get_ratings(request):
    ratings = Rating.objects.all()
    serializer = RatingSerializer(ratings, many=True)
    return Response(serializer.data)





@api_view(['GET', 'POST'])
def create_review(request, book_id):

  # tries to find the book in the database. If it doesn't exist, a Book.DoesNotExist exception is raised.
  try:
      book = Book.objects.get(pk=book_id)
  except Book.DoesNotExist:
    return Response({"message" : f"The given book id: {book_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)
  
  if request.method == 'GET':
    reviews = Rating.objects.filter(book_id=book_id)
    if not reviews:
      return Response({"message" : "There are no reviews made for this book."}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = RatingSerializer(reviews, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  if request.method == 'POST':
    # checks if user already made a review on the book
    user_id = request.data.get('user')
    existing_review = check_user_ratings(user_id, book)
    if existing_review:
      return existing_review

    serializer = RatingSerializer(data=request.data)
    if not serializer.is_valid():
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    serializer.save(book=book) # creates a new row in the Review table, injecting the book object that was looked up earlier as the book_id using the serializer's field 'book'
    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET', 'PATCH'])
def get_update_review(request, book_id, review_id):

  try:
     book = Book.objects.get(pk=book_id)
     review = Rating.objects.get(pk=review_id, book=book)
  except ObjectDoesNotExist:
     print("Review object: ", review, "Book object: ", book)
     return Response(status=status.HTTP_404_NOT_FOUND)
  
  if request.method == 'GET':
    serializer = RatingSerializer(review)
    return Response(serializer.data)
  
  if request.method == 'PATCH':
    if review.user.id != request.data.get("user"):
      print(f'review.user: {review.user.id}, request.user: {request.data.get("user")}')
      return Response({"message" : f"The given user id: {request.data.get("user")} does not match the user id that submitted the review."},status=status.HTTP_400_BAD_REQUEST)
    
    # pass in the review object as 1st param to update it. partial = true for PATCH request. 
    serializer = RatingSerializer(review, data=request.data, partial=True)
    if not serializer.is_valid():
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    serializer.save()
    return Response(status=status.HTTP_200_OK)
  


@api_view(['GET'])
def get_avg_rating(request, book_id):

  try:
    book = Book.objects.get(pk=book_id)
  except Book.DoesNotExist:
    return Response({"message" : f"The given book id: {book_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)
  
  # database query to get AVG rating
  avg_rating = Rating.objects.filter(book=book).aggregate(Avg('rating')) # avg_rating = {'rating__avg': ...}
  
  if avg_rating['rating__avg'] is None:
    return Response({'message': 'This book does not have any ratings made yet.'})
  return Response(avg_rating, status=status.HTTP_200_OK)

  



def check_user_ratings(user, book):
   if Rating.objects.filter(user=user, book=book).exists():
      return Response({"message" : f"User {user} has already made a review on {book}"}, status=status.HTTP_400_BAD_REQUEST)
   return None
