from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, ViewSetMixin
from rest_framework.mixins import  DestroyModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from tasker.models import *
from tasker.serializers import *
from tasker.permissions import *
from tasker.pagination import DefaultPagination
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.generics import ListCreateAPIView,ListAPIView

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
    permission_classes = []
    def get_queryset(self):
        sender = self.request.user.staff.id
        return LeaveRequest.objects.filter(sender_id=sender)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def perform_create(self, serializer):
        serializer.save()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return LeaveRequestSerializer
        return ShowLeavesSerializer
    
    def get_serializer_context(self, **kwargs):
        return {'staff': self.request.user.staff}

# class DeanViceDeanHODLeaveAPI(ModelViewSet):
#     permission_classes = [IsAuthenticated, IsDeanViceDeanHOD]
#     def get(self, request):
#         # Get the user making the request
#         user_role = request.user.role
#         if user_role == 'Head of Department':
#             # If the user is a head of department, filter the leave requests by department
#             leave_requests = LeaveRequest.objects.filter(sender__department=request.user.department)
#         else:
#             # If the user is a dean or vice dean, show all leave requests
#             leave_requests = LeaveRequest.objects.all()
#         # Serialize the leave requests and return them
#         serializer = LeaveRequestSerializer(leave_requests, many=True)
#         return Response(serializer.data)

#     def patch(self, request, pk):
#         # Get the data from the request
#         data = request.data
#         # Get the leave request object
#         leave_request = LeaveRequest.objects.get(id=pk)
        
#         # Check if the user making the request is authorized to respond to this leave request
#         user_role = request.user.role
#         if user_role == 'Dean':
#             leave_request.dean_approved = True
#         elif user_role == 'Vice_Dean':
#             leave_request.dean_approved = True
#         elif user_role == 'Head_of_department':
#             # If the user is a head of department, they can only respond to leave requests from their own department
#             if leave_request.sender.department == request.user.department:
#                 leave_request.head_of_department_approved = True
        
#         # Check if the leave request can be marked as accepted (only if it's not already accepted)
#         if leave_request.status == 'Pending' and (leave_request.dean_approved == True or leave_request.vice_dean_approved == True) or (leave_request.head_of_department_approved == True and (leave_request.dean_approved == True or leave_request.vice_dean_approved == True)):
#             leave_request.status = 'Accepted'
#         elif leave_request.status == 'Pending' and (leave_request.dean_approved == False or leave_request.vice_dean_approved == False):
#             leave_request.status = 'Refused'
#         # Save the updated leave request object
#         leave_request.save()
#         # Serialize the updated leave request and return it
#         serializer = LeaveRequestSerializer(leave_request)
#         return Response(serializer.data)
