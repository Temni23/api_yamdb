from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from rest_framework import permissions


from .views import UserViewSet, sign_up, get_jwtoken, CommentViewSet, ReviewViewSet


app_name = "api"

v1_router = DefaultRouter()
v1_router.register(r"users", UserViewSet, basename="users")
v1_router.register(
    r'posts/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')


v1_router.register(
    r'posts/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews')
v1_router.register(
    r'posts/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)',
    ReviewViewSet, basename='reviewedit')
v1_router.register(
    r'posts/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
    r'/comments/(?P<comment_id>\d+)',
    CommentViewSet, basename='commentsedit')
urlpatterns = [
    path("v1/", include(v1_router.urls)),
    path("v1/auth/signup/", sign_up),
    path("v1/auth/token/", get_jwtoken),
]
