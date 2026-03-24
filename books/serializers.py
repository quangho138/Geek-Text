from rest_framework import serializers
from .models import Book
from ratings.models import Rating

class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            "isbn",
            "name",
            "genre",
            "publisher",
            "copies_sold",
            "average_rating",
            "author_name",
        ]

    def get_author_name(self, obj):
        return f"{obj.author.first_name} {obj.author.last_name}"

    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        if ratings.exists():
            total = sum(r.rating for r in ratings)
            return round(total / ratings.count(), 2)
        return None