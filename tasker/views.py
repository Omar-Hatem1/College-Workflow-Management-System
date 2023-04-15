from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.mixins import  DestroyModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from tasker.models import *
from tasker.serializers import *
from tasker.permissions import CanSendTask, CanReceiveTask
from tasker.pagination import DefaultPagination

class TaskAdminViewSet (DestroyModelMixin,ReadOnlyModelViewSet):
    queryset = Task.objects.select_related('receivers__user').select_related('staff__user').all()
    serializer_class = TaskAdminSerializer
    permission_classes = [IsAdminUser]
    pagination_class= DefaultPagination 
    filter_backends = [SearchFilter,DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['title']
    ordering_fields = ['last_modified'] 

class SentTasksViewSet (ModelViewSet):
    permission_classes = [CanSendTask]
    pagination_class= DefaultPagination
    filter_backends = [SearchFilter,DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['title']
    ordering_fields = ['last_modified'] 
    def get_queryset(self):
        user_id = self.request.user.id
        if user_id:
            return Task.objects.select_related('receivers__user').select_related('staff__user').select_related('task_response').filter(staff__user_id=user_id)
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateTaskSerializer
        elif self.request.method == 'PUT':
            return UpdateTaskSerializer
        return TaskSerializer
    def get_serializer_context(self):
        return {'staff_id': self.request.user.staff.id}

class ReceivedTasksViewSet (ReadOnlyModelViewSet):
    serializer_class =TaskSerializer
    permission_classes = [CanReceiveTask]
    pagination_class= DefaultPagination
    filter_backends = [DjangoFilterBackend ,SearchFilter, OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['title']
    ordering_fields = ['last_modified']
    def get_queryset(self):
        user_id = self.request.user.id
        if user_id:
            return Task.objects.select_related('receivers__user').select_related('staff__user').select_related('task_response').filter(receivers__user_id=user_id)

class ReceiversViewSet (ReadOnlyModelViewSet):
    serializer_class = StaffSerializer 
    def get_queryset(self):
        staff_role = self.request.user.staff.role
        if staff_role == 'dean':
            return Staff.objects.select_related('user').exclude(role=staff_role)
        elif staff_role == 'vice':
            return Staff.objects.select_related('user').exclude(role = 'dean').exclude(role =staff_role)
        elif staff_role == 'head':
            return Staff.objects.select_related('user').exclude(role = 'dean').exclude(role = 'vice').exclude(role =staff_role)
    

class TaskResponseViewSet (ModelViewSet):
    permission_classes = [CanReceiveTask]
    def get_queryset(self):
        staff_id = self.request.user.staff.id
        if staff_id:
            return TaskResponse.objects.filter(staff=staff_id)
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateTaskResponseSerializer
        elif self.request.method == 'PUT':
            return UpdateTaskResponseSerializer
        return TaskResponseSerializer
    def get_serializer_context(self, **kwargs):
        return {'staff_id': self.request.user.staff.id}