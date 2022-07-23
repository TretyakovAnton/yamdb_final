from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb import settings
from api.permissions import IsAdmin
from .models import User
from .serializers import (
    SignUpSerializer, UserSerializer, GetTokenSerializer
)


class UsersViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для работы с пользователями.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = (IsAdmin, )
    search_fields = ('username',)

    @action(detail=False, permission_classes=(IsAuthenticated, ),
            methods=['get', 'patch'], url_path='me')
    def get_or_update_self(self, request):
        """
        Редактирования и получение информации профиля.
        """
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        if request.method == 'PATCH':
            serializer = UserSerializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )


class APIGetToken(APIView):
    """
    Вьюсет для получения токена.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data.get('confirmation_code')
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)
        if user.confirmation_code != confirmation_code:
            response = {'Неверный код'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        token = str(RefreshToken.for_user(user).access_token)
        response = {'token': token}

        return Response(response, status=status.HTTP_200_OK)


class APISignup(APIView):
    """
    Вьюсет для получения кода авторизации на почту.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        confirmation_code = get_random_string(12)
        User.objects.create_user(
            username=username,
            email=email,
            confirmation_code=confirmation_code
        )
        send_mail(
            'Код подтверждения',
            f'Код подтверждения: {confirmation_code}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
