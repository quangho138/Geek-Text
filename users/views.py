from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import TEMPCreateUserSerializer

TEMP_SUCCESS_MESSAGE = "TEMP_USER_CREATED"

class TEMPCreateUserAPIView(APIView):
    def post(self, request):
        serializer = TEMPCreateUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": TEMP_SUCCESS_MESSAGE, "username": user.username},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)