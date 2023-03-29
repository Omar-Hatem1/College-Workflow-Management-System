from rest_framework import serializers
from core.models import User
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken, SlidingToken, UntypedToken

class TokenObtainPairSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh_token'] = str(refresh)
        data['access_token'] = str(refresh.access_token)
        data['user_id'] = self.user.id
        data['user_role'] = self.user.staff.role
        data['user_name'] = (self.user.first_name + ' ' + self.user.last_name)
        return data

class UserSerializer (serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = '__all__'

