from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Rating
from .serializers import RatingSerializer

@api_view(['GET'])
def get_ratings(request):
    ratings = Rating.objects.all()
    serializer = RatingSerializer(ratings, many=True)
    return Response(serializer.data)