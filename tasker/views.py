from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, CreateModelMixin 
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from tasker.models import *
from tasker.serializers import *
from tasker.permissions import CanSendTask
from tasker.pagination import DefaultPagination

class TaskAdminViewSet (ListModelMixin,RetrieveModelMixin,DestroyModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Task.objects.select_related('receivers__user').select_related('staff__user').all()
    serializer_class = TaskAdminSerializer
    pagination_class= DefaultPagination #PageNumberPagination
    filter_backends = [DjangoFilterBackend ,SearchFilter, OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['title']
    ordering_fields = ['last_modified'] 
class SentTasksViewSet (ModelViewSet):
    #queryset = Task.objects.select_related('receivers__user').select_related('staff__user').all()
    serializer_class =TaskViewSerializer
    permission_classes = [IsAuthenticated, CanSendTask ]
    pagination_class= DefaultPagination
    filter_backends = [DjangoFilterBackend ,SearchFilter, OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['title']
    ordering_fields = ['last_modified'] # Todo : Create a serializer for this
    def get_queryset(self):
        user_id = self.request.user.id
        if user_id == self.request.user.id:
            return Task.objects.select_related('receivers__user').select_related('staff__user').select_related('task_response').filter(staff__user_id=user_id)

    #serializer_class =TaskSerializer
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskSerializer
        elif self.request.method == 'POST':
            return CreateTaskSerializer
        elif self.request.method == 'PUT':
            return UpdateTaskSerializer
        return TaskSerializer
    def get_serializer_context(self):
        #print({'user_id': self.request.user.id, 'staff_role': self.request.user.staff.role ,'staff_id': self.request.user.staff.id})
        return {'user_id': self.request.user.id, 'staff_role': self.request.user.staff.role ,'staff_id': self.request.user.staff.id}

class ReceivedTasksViewSet (ListModelMixin,RetrieveModelMixin, GenericViewSet):
    serializer_class =TaskViewSerializer
    pagination_class= DefaultPagination #PageNumberPagination
    filter_backends = [DjangoFilterBackend ,SearchFilter, OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['title']
    ordering_fields = ['last_modified'] # Todo : Create a serializer for this
    def get_queryset(self):
        user_id = self.request.user.id
        if user_id == self.request.user.id:
            return Task.objects.select_related('receivers__user').select_related('staff__user').select_related('task_response').filter(receivers__user_id=user_id)

class ReceiversViewSet (ListModelMixin,RetrieveModelMixin, GenericViewSet):
    #queryset = Staff.objects.select_related('user').all()
    serializer_class = StaffSerializer 
    def get_queryset(self):
        staff_role = self.request.user.staff.role
        if staff_role == 'dean':
            #print (Staff.objects.select_related('user').exclude(role=staff_role)) # ?? Test code
            return Staff.objects.select_related('user').exclude(role=staff_role)
        elif staff_role == 'vice':
            return Staff.objects.select_related('user').exclude(role = 'dean').exclude(role =staff_role)
        elif staff_role == 'head':
            return Staff.objects.select_related('user').exclude(role = 'dean').exclude(role = 'vice').exclude(role =staff_role)
    

class TaskResponseViewSet (ListModelMixin,DestroyModelMixin,UpdateModelMixin,CreateModelMixin,RetrieveModelMixin, GenericViewSet):
    queryset= TaskResponse.objects.all()
    # def get_queryset(self, **kwargs):
    #     task_id = self.kwargs['response_pk']
    #     if task_id == task_id :
    #         return TaskResponse.objects.filter(task = task_id)
        #return TaskResponse.objects.all()
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateTaskResponseSerializer
        elif self.request.method == 'PUT':
            return UpdateTaskResponseSerializer
        return TaskResponseSerializer
    def get_serializer_context(self, **kwargs):
        return {'user_id': self.request.user.id, 'staff_role': self.request.user.staff.role ,'staff_id': self.request.user.staff.id}