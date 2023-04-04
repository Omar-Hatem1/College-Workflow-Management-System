from rest_framework import serializers
from core.models import User
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from djoser.serializers import UserCreateSerializer, UserSerializer as BaseUserSerializer
from tasker.serializers import StaffSerializer

class UserSerializer (BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username','first_name', 'last_name','staff')
    staff = StaffSerializer(read_only=True)
    # def update(self, instance, validated_data): 
    # # update() method updates the dictionary with the elements from the another dictionary object or from an iterable of key/value pairs. 
    # # self is the instance of the serializer class.
    # # instance is the object instance that needs to be updated. 
    # # instance is the database query object of the user.
    # # self is the request object that was sent to the server.
    # # validated_data is the dictionary of the validated data that was sent in the request.
    #     staff_data = validated_data.pop('staff')
    #     p = staff_data 
    #     # staff_data is the dictionary of the validated data that was sent in the request.
    #     # pop method removes the key and returns the corresponding value.
    #     staff = instance.staff
    #     i = staff
    #     # staff is the object instance that needs to be updated.
    #     instance = super().update(instance, validated_data)
    #     ins = instance
    #     v = validated_data
    #     #super method returns a proxy object (temporary object of the superclass) that allows us to access methods of the base class.
    #     # update() method updates the dictionary with the elements from the another dictionary object or from an iterable of key/value pairs.
    #     staff_serializer = StaffSerializer(staff, data=staff_data)
    #     staff_serializer.is_valid(raise_exception=True)
    #     staff_serializer.save()
    #     return instance


class TokenObtainPairSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh_token'] = str(refresh)
        data['access_token'] = str(refresh.access_token)
        # data['user_id'] = self.user.id
        # data['user_role'] = self.user.staff.role
        # data['user_name'] = (self.user.first_name + ' ' + self.user.last_name)
        return data

# class UserSerializer (serializers.ModelSerializer):
#     class Meta: 
#         model = User
#         fields = '__all__'

