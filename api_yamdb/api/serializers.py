from django.core import validators
from django.utils import timezone
from rest_framework import serializers

from reviews.models import Category, Genre, Title, Comment, Review
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, required=True,
                                     validators=(
                                         validators.MaxLengthValidator(150),
                                         validators.RegexValidator(
                                             r'^[\w.@+-]+\Z')
                                     ))
    email = serializers.EmailField(max_length=254, required=True)

    class Meta:
        fields = (
            "username", "email", "first_name", "last_name", "bio", "role")
        model = User

    def validate(self, attrs):
        if User.objects.filter(email=attrs.get('email')).exists():
            user = User.objects.get(email=attrs.get('email'))
            if user.username != attrs.get('username'):
                raise serializers.ValidationError(
                    {"Этот email уже используется другим пользователем"}
                )
        if User.objects.filter(username=attrs.get('username')).exists():
            user = User.objects.get(username=attrs.get('username'))
            if user.email != attrs.get('email'):
                raise serializers.ValidationError(
                    {"Это имя пользователя уже используется"}
                )
        return super().validate(attrs)


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "username", "email", "first_name", "last_name", "bio", "role")
        model = User
        read_only_fields = ("role",)


class JWTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ("username", "confirmation_code")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleDetailGetSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='slug', queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(slug_field='slug', queryset=Genre.objects.all(), many=True)

    class Meta:
        model = Title
        fields = '__all__'

    def validate(self, attrs):
        attrs = super().validate(attrs)
        year = attrs.get('year')
        if year is not None:
            current_year = timezone.now().year
            if year > current_year:
                raise serializers.ValidationError(
                    'Год произведения не может быть больше текущего года'
                )
        return attrs


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
