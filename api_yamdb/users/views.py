"""Класс представлений проиложения Users."""
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, status, views
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .models import CustomUser
from .serializers import AdminSerializer, UserSerializer, UserSignUpSerializer


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
        serializer = UserSignUpSerializer(data=request.data)
        print(request.data)
        if not request.data:
            return Response(
                ["'username', 'email' is required."],
                status=status.HTTP_400_BAD_REQUEST
            )
        if CustomUser.objects.filter(username=request.data['username'],
                                     email=request.data['email']).exists():
            self.create_code_send_mail(request=request)
            return Response(
                ['Вам отправлено письмо с кодом подтверждения.'],
                status=status.HTTP_200_OK
            )
        if request.data['username'] == 'me':
            return Response(
                ['Выберите другое имя.'], status=status.HTTP_400_BAD_REQUEST
            )
        if serializer.is_valid():
            serializer.save()
            self.create_code_send_mail(request=request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserObtainTokenAPI(views.APIView):
    """Класс для отправки токена пользователю."""

    permission_classes = (AllowAny,)

    def post(self, request):
        """Метод обработки пост запроса на получение токена."""
        user = get_object_or_404(CustomUser, username=request.data['username'])
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminCreateList(generics.ListCreateAPIView):
    """Класс создания пользователя и получения списка пользователей админом."""

    queryset = CustomUser.objects.all()
    serializer_class = AdminSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = (filters.SearchFilter)
    search_fields = ('username',)


class AdminDetail(generics.RetrieveUpdateDestroyAPIView):
    """Класс получения/обновления/удаления профиля пользователя админом."""

    queryset = CustomUser.objects.all()
    serializer_class = AdminSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = 'username'
