from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated

from webvirtcloud.views import error_message_response
from .models import User, Token
from .serializers import (
    RegisterSerializer,
    AuthTokenSerializer,
    ResetPasswordSerializer,
    ResetPasswordHashSerializer,
)
from .serializers import (
    ProfileSerilizer,
    ChangePasswordSerializer,
)


class Login(ObtainAuthToken):
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")

        try:
            token = Token.objects.get(user=user, scope=Token.WRITE_SCOPE, is_obtained=True)
        except Token.DoesNotExist:
            token = Token.objects.create(
                user=user, scope=Token.WRITE_SCOPE, is_obtained=True, name="Obtained auth token"
            )

        return Response({"token": token.key})


class Register(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response({"token": data.get("token")}, status=status.HTTP_201_CREATED)


class ResetPassword(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response()


class ResetPasswordHash(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordHashSerializer

    def post(self, request, hash, *args, **kwargs):
        if User.objects.filter(hash=hash, is_active=True).exists():
            user = User.objects.get(hash=hash)
            serializer = self.serializer_class(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return error_message_response("User not found or hash is invalid.")


class VerifyEmail(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, hash, *args, **kwargs):
        if User.objects.filter(hash=hash, is_email_verified=False, is_active=True).exists():
            user = User.objects.get(hash=hash)
            user.is_email_verified = True
            user.update_hash()
            user.save()
            return Response(status=status.HTTP_200_OK)
        return error_message_response("Invalid token or email already verified.")


class ProfileAPI(APIView):
    serializer_class = ProfileSerilizer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response({"profile": serializer.data})

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"profile": serializer.data})


class ChangePasswordAPI(APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)
