from django.urls import path, include
from .view import ChatView
from rest_framework.routers import DefaultRouter
from .view import ChatView

v1_router = DefaultRouter()

v1_router.register('chat', ChatView, basename='chat')


urlpatterns = [
    path('v1/', include(v1_router.urls)),
]