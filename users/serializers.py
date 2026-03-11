from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile

DEFAULT_HOME_ADDRESS = "No address provided"

class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=6)

    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    home_address = serializers.CharField(required=False, allow_blank=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def create(self, validated_data):
        home_address_value = validated_data.pop("home_address", DEFAULT_HOME_ADDRESS)
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        Profile.objects.create(
            user=user,
            home_address=home_address_value
        )

        return user

class ProfileSerializer(serializers.ModelSerializer):
    home_address = serializers.CharField(source="profile.home_address")

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "home_address"]
        read_only_fields = ["id", "username"]

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", {})

        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        instance.save()

        if profile_data:
            instance.profile.home_address = profile_data.get(
                "home_address",
                instance.profile.home_address
            )
            instance.profile.save()

        return instance