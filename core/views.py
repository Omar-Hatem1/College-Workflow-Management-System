from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from core.models import User
from core.serializers import UserSerializer , TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView as BaseTokenObtainPairView

class UsersViewSet (ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class TokenObtainPairView (BaseTokenObtainPairView):
    serializer_class = TokenObtainPairSerializer