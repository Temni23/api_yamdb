import datetime as dt
import random

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Title, Review
from users.models import User
from .permissions import IsAuthorOrReadOnly
from .serializers import (UserSerializer, CommentSerializer,
                          ReviewSerializer, JWTokenSerializer, MeSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"

    @action(methods=["get", "patch"], detail=False, url_path="me")
    def me(self, request):
        if request.method == "GET":
            user = get_object_or_404(User, username=self.request.user)
            serializer = MeSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "PATCH":
            user = get_object_or_404(User, username=self.request.user)
            serializer = MeSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    # @action(permission_classes = (IsAdmin, ))
    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        email = serializer.validated_data["email"]
        try:
            user, create = User.objects.get_or_create(
                username=username,
                email=email,
            )
            user.save()
        except Exception as error:
            return Response(f"Ошибка при создании пользователя {error}",
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def sign_up(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    confirmation_code = str(random.randint(1000, 9999))
    username = serializer.validated_data["username"]
    email = serializer.validated_data["email"]
    try:
        user, create = User.objects.get_or_create(
            username=username,
            email=email,
        )
        user.confirmation_code = confirmation_code
        user.save()
    except Exception as error:
        return Response(f"Ошибка при создании пользователя {error}",
                        status=status.HTTP_400_BAD_REQUEST)
    send_mail(
        "Код подтверждения регистрации на yamdb",
        f"Код подтверждения регистрации пользователья {username} \n"
        f"КОД: {confirmation_code}",
        "conform@yamdb.com",
        [email],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def get_jwtoken(request):
    serializer = JWTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=serializer.validated_data["username"])
    confirmation_code = serializer.validated_data["confirmation_code"]
    if confirmation_code == user.confirmation_code:
        jwtoken = str(AccessToken.for_user(user))
        return Response({"token": jwtoken}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user,
                        title=title, pub_date=dt.datetime.now())

    def get_queryset(self):
        new_queryset = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return new_queryset.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user,
                        review=review, pub_date=dt.datetime.now())

    def get_queryset(self):
        new_queryset = get_object_or_404(
            Review, pk=self.kwargs.get('review_id'))
        return new_queryset.comments.all()
