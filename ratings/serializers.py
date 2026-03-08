from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
      
  # make the comment field optional
  comment = serializers.CharField(required=False, allow_blank=True, max_length=255)

  class Meta:
    model = Review
    fields = ['user', 'book', 'rating', 'created_at', 'comment', 'updated_at']
    read_only_fields = ['id', 'book', 'created_at', 'updated_at']

    # read_only means the serializer skips "book", "created_at", and "updated_at" during validation, so the user doesn't need to include it in the POST body. It also includes the book in the serialied output (the Response object)

