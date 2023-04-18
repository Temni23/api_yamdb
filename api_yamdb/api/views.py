from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import BadRequest
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import DOMAIN_NAME
from reviews.models import Category, Genre, Title, Review
from users.models import User
from .permissions import (IsAuthorStaffOrReadOnly, IsAdminOrSuperuser,
                          IsAdminOrSuperuserOrReadOnly)
from .serializers import (UserSerializer, CategorySerializer,
                          GenreSerializer, TitleSerializer,
                          CommentSerializer, ReviewSerializer,
                          JWTokenSerializer, MeSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdminOrSuperuser,)
    filter_backends = (SearchFilter, OrderingFilter)
    ordering_fields = ('username', 'email')
    search_fields = ('username',)
    ordering = ('username',)
    http_method_names = [
        'get', 'post', 'patch', 'delete',
    ]

    @action(methods=['get', 'patch'], detail=False, url_path='me',
            permission_classes=(IsAuthenticated, IsAuthorStaffOrReadOnly,))
    def me(self, request):
        if request.method == 'GET':
            user = get_object_or_404(User, username=self.request.user)
            serializer = MeSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            user = get_object_or_404(User, username=self.request.user)
            serializer = MeSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        try:
            user, _ = User.objects.get_or_create(
                username=username,
                email=email,
            )
            user.save()
        except Exception as error:
            return Response(f'Ошибка при создании пользователя {error}',
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def sign_up(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    try:
        user, _ = User.objects.get_or_create(
            username=username,
            email=email,
        )
        confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = confirmation_code
        user.save()
    except Exception as error:
        return Response(f'Ошибка при создании пользователя {error}',
                        status=status.HTTP_400_BAD_REQUEST)
    send_mail(
        'Код подтверждения регистрации на yamdb',
        f'Код подтверждения регистрации пользователья {username} \n'
        f'КОД: {confirmation_code}',
        recipient_list=[email],
        from_email=DOMAIN_NAME,
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_jwtoken(request):
    serializer = JWTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User,
                             username=serializer.validated_data['username'])
    confirmation_code = serializer.validated_data['confirmation_code']
    if not user or not confirmation_code:
        return Response('Пропущены имя пользователя и (или) код '
                        'потдтвержедния!', status=status.HTTP_400_BAD_REQUEST)
    if confirmation_code == user.confirmation_code:
        jwtoken = str(AccessToken.for_user(user))
        return Response({'token': jwtoken}, status=status.HTTP_200_OK)
    return Response('Неверный код подтверждения!',
                    status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (IsAdminOrSuperuserOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)

    # ordering = ('name',)

    def retrieve(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)


class GenreViewSet(CategoryViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrSuperuserOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)

    def filter_queryset(self, queryset):
        genre_slug = self.request.query_params.get('genre')
        category_slug = self.request.query_params.get('category')
        year = self.request.query_params.get('year')
        name = self.request.query_params.get('name')

        if genre_slug:
            genre = get_object_or_404(Genre, slug=genre_slug)
            queryset = queryset.filter(genre=genre)
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
        if year:
            queryset = queryset.filter(year=year)
        if name:
            queryset = queryset.filter(name=name)
        return queryset.order_by('name')


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorStaffOrReadOnly, IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        try:
            title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
            serializer.save(title=title)
        except IntegrityError:
            raise BadRequest('На одно произведение можно оставить'
                             'только один отзыв!')

    def get_queryset(self):
        new_queryset = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return new_queryset.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorStaffOrReadOnly, IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        id_comment = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        review = get_object_or_404(Review, pk=id_comment, title__id=title_id)
        serializer.save(review=review)

    def get_queryset(self):
        id_comment = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        new_queryset = get_object_or_404(Review, pk=id_comment,
                                         title__id=title_id)
        return new_queryset.comments.all()
