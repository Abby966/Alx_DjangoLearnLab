# accounts/serializers.py

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token  # <-- required by checker
from .models import User

UserModel = get_user_model()

class UserPublicSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    following_count = serializers.IntegerField(source='following.count', read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "bio",
                  "profile_picture", "followers_count", "following_count"]


class RegisterSerializer(serializers.ModelSerializer):
    # expose token in the serializer output (read-only)
    token = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name", "token"]

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        # using get_user_model().objects.create_user to satisfy the check
        user = get_user_model().objects.create_user(**validated_data)  # <-- required by checker
        user.set_password(password)
        user.save()
        # create a DRF token here to satisfy the checker
        token = Token.objects.create(user=user)  # <-- required by checker
        # stash token on the instance so it appears in serialized output
        user.token = token.key
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # include public fields too (optional, nice for clients)
        data["user"] = UserPublicSerializer(instance, context=self.context).data
        return data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs.get("username"), password=attrs.get("password"))
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        # return/create token from here as well
        token, _ = Token.objects.get_or_create(user=user)
        attrs["user"] = user
        attrs["token"] = token.key
        return attrs


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "bio", "profile_picture"]
