from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, filters, generics, status, views
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import AccessToken

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from users.models import CustomUser
from reviews.models import Genre, Category, Title, Comment, Review
from .permissions import IsAdminOnly, IsOwnerOrReadOnly
from .mixins import ListCreateDestroyViewSet
from .serializers import (
    AdminSerializer, UserSerializer, UserSignUpSerializer,
    GenreSerializer, CategorySerializer, TitleGETSerializer, TitleSerializer,
    CommentSerializer, ReviewSerializer)


class UserSignupAPI(views.APIView):
    """Класс для регистрации пользователя и отправки кода подтверждения."""

    permission_classes = (AllowAny,)

    def create_code_send_mail(self, request):
        """Метод генерации кода и отсылки сообщения."""
        confirmation_code = default_token_generator.make_token(
            get_object_or_404(
                CustomUser, username=request.data['username']
            ))
        send_mail(
            subject='Регистрация пользователя',
            message=('Для получения токена перейдите по адресу'
                     '/api/v1/auth/token/ и введите код подтверждения'
                     f' confirmation_code: {confirmation_code}'),
            from_email='api_yamdb@example.com',
            recipient_list=[f'{request.data["email"]}'],
            fail_silently=True,
        )

    def post(self, request):
        """Метод для обработки пост запроса на регистрацию."""
        if not request.data:
            raise ValidationError({'email': ['This field is required.'],
                                   'username': ['This field is required.']})
        if request.data.get('username') is None:
            raise ValidationError({'username': ['This field is required.'], })
        if request.data.get('email') is None:
            raise ValidationError({'email': ['This field is required.'], })
        if CustomUser.objects.filter(
                username=request.data.get('username'),
                email=request.data.get('email')
        ).exists():
            self.create_code_send_mail(request=request)
            return Response(
                ['Вам отправлено письмо с кодом подтверждения.'],
                status=status.HTTP_200_OK
            )
        if request.data['username'] == 'me':
            return Response(
                ['Выберите другое имя.'], status=status.HTTP_400_BAD_REQUEST
            )
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            self.create_code_send_mail(request=request)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserObtainTokenAPI(views.APIView):
    """Класс для отправки токена пользователю."""

    permission_classes = (AllowAny,)

    def post(self, request):
        """Метод обработки пост запроса на получение токена."""
        if not request.data or request.data.get('username') is None:
            raise ValidationError(f"{['username']}")
        user = get_object_or_404(
            CustomUser, username=request.data.get('username')
        )
        if default_token_generator.check_token(
                user, request.data['confirmation_code']):
            token = AccessToken.for_user(user)
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
        return Response(
            ['Неверный код подтверждения.'], status=status.HTTP_400_BAD_REQUEST
        )


class UserRetrieveUpdateAPI(views.APIView):
    """Класс для обновления профиля пользователем."""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Метод для получения данных профиля пользователем."""
        user = get_object_or_404(CustomUser, id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        """Метод для обновления данных профиля пользователем."""
        user = get_object_or_404(CustomUser, id=request.user.id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminCreateList(generics.ListCreateAPIView):
    """Класс создания пользователя и получения списка пользователей админом."""

    queryset = CustomUser.objects.all()
    serializer_class = AdminSerializer
    permission_classes = (IsAdminOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = PageNumberPagination


class AdminDetail(generics.RetrieveUpdateDestroyAPIView):
    """Класс получения/обновления/удаления профиля пользователя админом."""

    queryset = CustomUser.objects.all()
    serializer_class = AdminSerializer
    permission_classes = (IsAdminOnly,)
    lookup_field = 'username'
    http_method_names = ('get', 'patch', 'delete',)


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


class CommentViewSet(viewsets.ModelViewSet):
    """Обработчик объектов модели коментариев"""
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id')
        )
        return review.comments.all()
    
    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id')
        )
        serializer.save(
            author=self.request.user,
            review=review
        )


class ReviewViewSet(viewsets.ModelViewSet):
    """Обработчик объектов модели отзывов"""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        serializer.save(
            author=self.request.user,
            title=title
        )

    
