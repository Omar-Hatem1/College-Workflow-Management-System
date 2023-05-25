from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, ViewSetMixin, GenericViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.mixins import  DestroyModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.filters import SearchFilter, OrderingFilter
from tasker.models import *
from tasker.serializers import *
from tasker.permissions import *
from tasker.pagination import DefaultPagination
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.generics import ListCreateAPIView,ListAPIView
from django.contrib.auth import get_user_model
from django.db.models import CharField, Value
from django.db.models.functions import Concat

CustomUser = get_user_model()

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
        senderDep = self.request.user.staff.Department
        if staff_role == 'Dean':
            return Staff.objects.select_related('user').exclude(role=staff_role)
        elif staff_role == 'Vice_Dean':
            return Staff.objects.select_related('user').exclude(role = 'Dean').exclude(role =staff_role)
        elif staff_role == 'Head_of_department':
            return Staff.objects.select_related('user').exclude(role = 'Dean').exclude(role = 'Vice_Dean').exclude(role =staff_role).filter(Department = senderDep)
    

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
    

    
class DoctorAssistantLeaveAPI(ModelViewSet):
    permission_classes = [IsDoctorOrAssistant]
    def get_queryset(self):
        sender = self.request.user.staff.id
        return LeaveRequest.objects.filter(sender_id=sender)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return LeaveRequestSerializer
        return ShowLeavesSerializer
    
    def get_serializer_context(self, **kwargs):
        return {'staff': self.request.user.staff}
    

class LeavesList (ReadOnlyModelViewSet):
    serializer_class = StaffSerializer
    def get_queryset(self):
        senderDep = self.request.user.staff.Department
        dean = Staff.objects.select_related('user').filter(role = 'Dean')
        vice_dean = Staff.objects.select_related('user').filter(role = 'Vice_Dean')
        hod = Staff.objects.select_related('user').filter(Department = senderDep, role = 'Head_of_department')
        List = dean.union(vice_dean)
        List = List.union(hod)
        return List

class DeanViceHOD(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    def get_queryset(self):
        if(self.request.user.staff.role == 'Head_of_department'):
            senderDep = self.request.user.staff.Department
            return LeaveRequest.objects.filter(Department = senderDep)
        return LeaveRequest.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return UpdateLeaveSerializer
        return LeaveResponseSerializer
    def update(self, request, *args, **kwargs):
        leave_id = kwargs['pk']
        leave = LeaveRequest.objects.get(id=leave_id)
        leave.approve = request.data['approve']

        if(self.request.user.staff.role == 'Dean'):
            if(leave.approve == 'Accepted'):
                leave.dean_approved = True
            else:
                leave.dean_approved = False

        elif(self.request.user.staff.role == 'Vice_Dean'):
            if(leave.approve == 'Accepted'):
                leave.vice_dean_approved = True
            else:
                leave.vice_dean_approved = False
        else:
            if(leave.approve == 'Accepted'):
                leave.head_of_department_approved = True
            else:
                leave.head_of_department_approved = False
        
        if(leave.dean_approved == True or leave.vice_dean_approved == True):
            leave.status = 'Accepted'

        elif(leave.dean_approved == False or leave.vice_dean_approved == False):
            leave.status = 'Refused'
            
        leave.save()
        return Response({'success': 'Leave status updated successfully'})
    
class SecretaryLeavesView(ReadOnlyModelViewSet):
    queryset = LeaveRequest.objects.filter(status = 'Accepted')
    serializer_class = LeaveResponseSerializer
    permission_classes = [IsSecretaryAdmin]