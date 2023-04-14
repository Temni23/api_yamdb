from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from rest_framework import permissions

from .views import UserViewSet, sign_up, get_jwtoken


app_name = "api"

v1_router = DefaultRouter()
v1_router.register("users", UserViewSet)

urlpatterns = [
    path("v1/", include(v1_router.urls)),
    path("v1/auth/signup/", sign_up),
    path("v1/auth/token/", get_jwtoken),
]
