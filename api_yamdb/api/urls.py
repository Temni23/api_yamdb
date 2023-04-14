from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, CommentViewSet, ReviewViewSet


app_name = "api"

v1_router = DefaultRouter()
v1_router.register("users", UserViewSet, basename="users")
v1_router.register(
    r'posts/(?P<post_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')

v1_router.register(
    r'posts/(?P<post_id>\d+)/reviews',
    ReviewViewSet, basename='reviews')
v1_router.register(
    r'posts/(?P<post_id>\d+)/reviews/(?P<review_id>\d+)',
    ReviewViewSet, basename='reviewedit')
v1_router.register(
    r'posts/(?P<post_id>\d+)/reviews/(?P<review_id>\d+)'
    r'/comments/(?P<comment_id>\d+)',
    CommentViewSet, basename='commentsedit')
urlpatterns = [
    path("v1/", include(v1_router.urls)),
]
