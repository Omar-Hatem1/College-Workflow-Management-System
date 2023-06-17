from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.mixins import  DestroyModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.filters import SearchFilter, OrderingFilter
from tasker.models import *
from tasker.serializers import *
from tasker.permissions import *
from tasker.pagination import DefaultPagination
from rest_framework.response import Response

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
        if staff_role == 'dean':
            return Staff.objects.select_related('user').exclude(role=staff_role)
        elif staff_role == 'vice':
            return Staff.objects.select_related('user').exclude(role = 'dean').exclude(role =staff_role)
        elif staff_role == 'head':
            return Staff.objects.select_related('user').exclude(role = 'dean').exclude(role = 'vice').exclude(role =staff_role).filter(Department = senderDep)
    

class TaskResponseViewSet (ModelViewSet):
    permission_classes = [CanReceiveTask]
    pagination_class= DefaultPagination
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
        dean = Staff.objects.select_related('user').filter(role = 'dean')
        vice_dean = Staff.objects.select_related('user').filter(role = 'vice')
        hod = Staff.objects.select_related('user').filter(Department = senderDep, role = 'head')
        List = dean.union(vice_dean)
        List = List.union(hod)
        return List

class DeanViceHOD(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = [IsDeanViceDeanHOD]
    def get_queryset(self):
        if(self.request.user.staff.role == 'head'):
            recieverDep = self.request.user.staff.Department
            return LeaveRequest.objects.filter(sender_department = recieverDep)
        return LeaveRequest.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return UpdateLeaveSerializer
        return LeaveResponseSerializer
    def update(self, request, *args, **kwargs):
        leave_id = kwargs['pk']
        leave = LeaveRequest.objects.get(id=leave_id)
        leave.approve = request.data['approve']

        if(self.request.user.staff.role == 'dean'):
            if(leave.approve == 'Accepted'):
                leave.dean_approved = True
            else:
                leave.dean_approved = False

        elif(self.request.user.staff.role == 'vice'):
            if(leave.approve == 'Accepted'):
                leave.vice_approved = True
            else:
                leave.vice_approved = False
        else:
            if(leave.approve == 'Accepted'):
                leave.head_approved = True
            else:
                leave.head_approved = False
        
        if(leave.dean_approved == True or leave.vice_approved == True):
            leave.status = 'Accepted'

        elif(leave.dean_approved == False or leave.vice_approved == False):
            leave.status = 'Refused'
            
        leave.save()
        return Response({'success': 'Leave status updated successfully'})
    
class SecretaryLeavesView(ReadOnlyModelViewSet):
    queryset = LeaveRequest.objects.filter(status = 'Accepted')
    serializer_class = LeaveResponseSerializer
    permission_classes = [IsSecretaryAdmin]