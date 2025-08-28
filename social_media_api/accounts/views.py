from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializers import (
    RegisterSerializer, LoginSerializer,
    UserPublicSerializer, ProfileUpdateSerializer
)

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        resp = super().create(request, *args, **kwargs)
        user = self.serializer_class.Meta.model.objects.get(username=resp.data["username"])
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"user": UserPublicSerializer(user, context={"request": request}).data,
                         "token": token.key}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"user": UserPublicSerializer(user, context={"request": request}).data,
                         "token": token.key})

class ProfileView(APIView):
    def get(self, request):
        return Response(UserPublicSerializer(request.user, context={"request": request}).data)

    def put(self, request):
        serializer = ProfileUpdateSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserPublicSerializer(request.user, context={"request": request}).data)

    def patch(self, request):
        serializer = ProfileUpdateSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserPublicSerializer(request.user, context={"request": request}).data)

# Create your views here.
