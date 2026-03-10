from rest_framework import serializers
from .models import Book, Author
from ratings.models import Rating

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = "__all__"

    def get_average_rating(self, obj):
        ratings = Rating.objects.filter(book=obj)
        if ratings.exists():
            total = sum(r.rating for r in ratings)
            return round(total / ratings.count(), 2)
        return None