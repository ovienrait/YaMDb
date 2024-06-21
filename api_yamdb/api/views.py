from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import viewsets, status, generics, filters
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated

from reviews.models import Genre, Category, Title
from users.models import User
from .serializers import (
    SignUpSerializer, TokenObtainSerializer, UserSerializer, AdminSerializer,
    GenreSerializer, CategorySerializer, TitleGETSerializer, TitleSerializer)
from .mixins import ListCreateDestroyViewSet
from .utils import (
    generate_confirmation_code, check_confirmation_code,
    send_email_confirmation_code)
from .permissions import IsAdminOnly


class GenreViewSet(ListCreateDestroyViewSet):
    """Обработчик объектов модели жанров"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(ListCreateDestroyViewSet):
    """Обработчик объектов модели категорий"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Обработчик объектов модели произведений"""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGETSerializer
        return TitleSerializer


class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            if username.lower() == 'me':
                return Response(
                    {"detail": "Username 'me' is not allowed."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                if user.email != email:
                    return Response(
                        {"detail": "Email doesn't match"
                         "the registered username."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    confirmation_code = generate_confirmation_code(user)
                    send_email_confirmation_code(email, confirmation_code)
                    return Response(
                        {"username": username, "email": email},
                        status=status.HTTP_200_OK
                    )
            if User.objects.filter(email=email).exists():
                return Response(
                    {"detail": "Email already exists."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user = User.objects.create_user(username=username, email=email)
            confirmation_code = generate_confirmation_code(user)
            send_email_confirmation_code(email, confirmation_code)
            return Response(
                {"username": username, "email": email},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenObtainView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = TokenObtainSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            confirmation_code = serializer.validated_data['confirmation_code']
            try:
                user = User.objects.get(username=username)
            except ObjectDoesNotExist:
                return Response(
                    {"detail": "User not found."},
                    status=status.HTTP_404_NOT_FOUND
                )
            if not check_confirmation_code(user, confirmation_code):
                return Response(
                    {"detail": "Invalid confirmation code."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRetrieveUpdateAPI(APIView):
    """Класс для обновления профиля пользователем."""
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Метод для получения данных профиля пользователем."""
        user = get_object_or_404(User, id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        """Метод для обновления данных профиля пользователем."""
        user = get_object_or_404(User, id=request.user.id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminCreateList(generics.ListCreateAPIView):
    """Класс создания пользователя и получения списка пользователей админом."""

    queryset = User.objects.all()
    serializer_class = AdminSerializer
    permission_classes = (IsAdminOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = PageNumberPagination


class AdminDetail(generics.RetrieveUpdateDestroyAPIView):
    """Класс получения/обновления/удаления профиля пользователя админом."""

    queryset = User.objects.all()
    serializer_class = AdminSerializer
    permission_classes = (IsAdminOnly,)
    lookup_field = 'username'
    http_method_names = ('get', 'patch', 'delete',)
