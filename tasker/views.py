from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from .models import *
from .serializers import *




class TasksViewSet (ModelViewSet):
    queryset = Task.objects.all()
    #serializer_class =TaskSerializer
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskSerializer
        elif self.request.method == 'POST':
            return CreateTaskSerializer
        return TaskSerializer
    def get_serializer_context(self):
        return {'user_id': self.request.user.id, 'staff_role': self.request.user.staff.role ,'staff_id': self.request.user.staff.id}



# class TaskResponseViewSet (ModelViewSet):
#     queryset= TaskResponse.objects.all()
#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return CreateTaskResponseSerializer
#         return TaskResponseSerializer
#     def get_serializer_context(self):
#         return {'user_id': self.request.user.id, 'staff_id': self.request.user.staff.role}