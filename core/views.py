from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from core.models import User
from core.serializers import UserSerializer


class UsersViewSet (ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer