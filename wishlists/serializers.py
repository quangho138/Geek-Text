from rest_framework import serializers
from django.contrib.auth import get_user_model
from wishlists.models import Wishlist
from books.models import Book

User = get_user_model()

class WishlistCreateSerializer(serializers.ModelSerializer):
    # accept user_id in request body (per assignment)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Wishlist
        fields = ["user_id", "name"]

    def validate_user_id(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User does not exist.")
        return value

    def validate(self, attrs):
        user_id = attrs["user_id"]
        name = attrs["name"].strip()

        # limit to 3 wishlists per user
        if Wishlist.objects.filter(user_id=user_id).count() >= 3:
            raise serializers.ValidationError("User already has 3 wishlists.")

        # unique name per user (nice error before DB constraint triggers)
        if Wishlist.objects.filter(user_id=user_id, name__iexact=name).exists():
            raise serializers.ValidationError("Wishlist name must be unique for this user.")

        attrs["name"] = name
        return attrs

    def create(self, validated_data):
        user_id = validated_data.pop("user_id")
        return Wishlist.objects.create(user_id=user_id, **validated_data)
    


class AddBookToWishlistSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    wishlist_id = serializers.IntegerField()