from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
  class Meta:
    model = Review
    fields = ['user', 'book', 'rating', 'created_at']
    read_only_fields = ['book', 'created_at']

    # read_only means the serializer skips "book" during validation, so the user doesn't need to include it in the POST body. It also includes the book inthe serialied output (the Response object)