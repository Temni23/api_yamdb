from rest_framework import serializers

from users.models import User
from reviews.models import Comment, Review


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, required = True)
    email = serializers.EmailField(max_length=254, required = True)
    class Meta:
        fields = ("username", "email")
        model = User

class MeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("username", "email", "first_name", "last_name", "bio", "role")
        model = User
        read_only_fields = ("role",)

class JWTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ("username", "confirmation_code")

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

