from rest_framework import serializers

from users.models import User
from reviews.models import Comment, Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = User


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        model = Review
        read_only_fields = ('pub_date',)
        exclude = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        model = Comment
        read_only_fields = ('pub_date',)
        exclude = ('review',)
