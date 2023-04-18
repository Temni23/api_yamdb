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
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя выбрать имя me!'
            )
        return value

    def validate(self, attrs):
        user = User.objects.filter(email=attrs.get('email'))
        if user.exists():
            user = user.first()
            if user.username != attrs.get('username'):
                raise serializers.ValidationError(
                    {'Этот email уже используется другим пользователем'}
                )
        user = User.objects.filter(username=attrs.get('username'))
        if user.exists():
            user = user.first()
            if user.email != attrs.get('email'):
                raise serializers.ValidationError(
                    {'Это имя пользователя уже используется'}
                )
        return super().validate(attrs)


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User
        read_only_fields = ('role',)


class JWTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField(read_only=True, default=0)

    class Meta:
        model = Title
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        method = self.context['request'].method
        if method == 'GET':
            self.fields['category'] = CategorySerializer()
            self.fields['genre'] = GenreSerializer(many=True)
        else:
            self.fields['category'] = serializers.SlugRelatedField(
                slug_field='slug', queryset=Category.objects.all())
            self.fields['genre'] = serializers.SlugRelatedField(
                slug_field='slug', queryset=Genre.objects.all(), many=True)

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
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        read_only_fields = ('pub_date', 'author')
        exclude = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        read_only_fields = ('pub_date',)
        exclude = ('review',)
