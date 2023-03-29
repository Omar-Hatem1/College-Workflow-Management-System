from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.response import Response
from .models import *
from .serializers import *


class TasksViewSet (ModelViewSet):
    queryset = Task.objects.select_related('receivers__user').select_related('staff__user').all()
    #serializer_class =TaskSerializer
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskSerializer
        elif self.request.method == 'POST':
            return CreateTaskSerializer
        return TaskSerializer
    def get_serializer_context(self):
        #print({'user_id': self.request.user.id, 'staff_role': self.request.user.staff.role ,'staff_id': self.request.user.staff.id})
        return {'user_id': self.request.user.id, 'staff_role': self.request.user.staff.role ,'staff_id': self.request.user.staff.id}

class ReceiversViewSet (ListModelMixin, GenericViewSet):
    #queryset = Staff.objects.select_related('user').all()
    def get_queryset(self):
        staff_role = self.request.user.staff.role
        if staff_role == 'dean':
            #print (Staff.objects.select_related('user').exclude(role=staff_role)) # ?? Test code
            return Staff.objects.select_related('user').exclude(role=staff_role)
        elif staff_role == 'vice':
            return Staff.objects.select_related('user').exclude(role = 'dean').exclude(role =staff_role)
        elif staff_role == 'head':
            return Staff.objects.select_related('user').exclude(role = 'dean').exclude(role = 'vice').exclude(role =staff_role)
    serializer_class = StaffSerializer 

# class TaskResponseViewSet (ModelViewSet):
#     queryset= TaskResponse.objects.all()
#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return CreateTaskResponseSerializer
#         return TaskResponseSerializer
#     def get_serializer_context(self):
#         return {'user_id': self.request.user.id, 'staff_id': self.request.user.staff.role}