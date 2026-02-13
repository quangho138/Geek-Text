from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile

TEMP_DEFAULT_HOME_ADDRESS = "TEMP_HOME_ADDRESS"

class TEMPCreateUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=6)

    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    home_address = serializers.CharField(required=False, allow_blank=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("TEMP_ERROR_USERNAME_ALREADY_EXISTS")
        return value

    def create(self, validated_data):
        TEMP_HOME_ADDRESS_VALUE = validated_data.pop("home_address", TEMP_DEFAULT_HOME_ADDRESS)

        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        Profile.objects.create(
            user=user,
            home_address=TEMP_HOME_ADDRESS_VALUE
        )

        return user
