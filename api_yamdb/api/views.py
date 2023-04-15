import datetime as dt

from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.permissions import (IsAuthenticatedOrReadOnly)
from django.db.models import Avg

from users.models import User
from .serializers import (UserSerializer, CommentSerializer,
                          ReviewSerializer)
from reviews.models import Title, Review
from .permissions import IsAuthorOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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
