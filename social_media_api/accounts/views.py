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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # ensure token in response:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {"user": UserPublicSerializer(user, context={"request": request}).data,
             "token": token.key},
            status=status.HTTP_201_CREATED
        )

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        s = LoginSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        user = s.validated_data["user"]
        token = s.validated_data["token"]
        return Response(
            {"user": UserPublicSerializer(user, context={"request": request}).data,
             "token": token}
        )

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserPublicSerializer(request.user, context={"request": request}).data)

    def put(self, request):
        s = ProfileUpdateSerializer(request.user, data=request.data)
        s.is_valid(raise_exception=True)
        s.save()
        return Response(UserPublicSerializer(request.user, context={"request": request}).data)

    def patch(self, request):
        s = ProfileUpdateSerializer(request.user, data=request.data, partial=True)
        s.is_valid(raise_exception=True)
        s.save()
        return Response(UserPublicSerializer(request.user, context={"request": request}).data)
