from rest_framework.serializers import ModelSerializer, StringRelatedField
from tasker.models import *



class TaskResponseSerializer(ModelSerializer):
    class Meta:
        model = TaskResponse
        fields = ['id', 'title', 'description', 'file', 'staff', 'task', 'last_modified', 'date_added']

class StaffSerializer (ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'user', 'title', 'role']
    
    user = StringRelatedField() 

class TaskAdminSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ['id','title','deadline','status','staff', 'receivers']

    staff = StaffSerializer()
    receivers = StaffSerializer()

class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ['id','title', 'description', 'deadline','file', 'status','staff', 'receivers', 'task_response']
    task_response = TaskResponseSerializer()
    staff = StaffSerializer()
    receivers = StaffSerializer() 

class CreateTaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline','file', 'status', 'receivers']

    def save(self, **kwargs):
        staff_id=self.context['staff_id']
        staff = Staff.objects.get(pk = staff_id)
        task = Task.objects.create(staff=staff, **self.validated_data) 
        return task

class UpdateTaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline','file', 'status', 'receivers']

class CreateTaskResponseSerializer(ModelSerializer):
    class Meta:
        model = TaskResponse
        fields = ['title', 'description', 'file', 'task']
    def save(self, **kwargs):
        staff_id=self.context['staff_id']
        staff = Staff.objects.get(pk = staff_id)
        task = TaskResponse.objects.create(staff=staff, **self.validated_data)
        return task

class UpdateTaskResponseSerializer(ModelSerializer):
    class Meta:
        model = TaskResponse
        fields = ['title', 'description', 'file', 'task']

class LeaveRequestSerializer(ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ['id', 'leave_type', 'start_date', 'end_date', 'created_at']
    def save(self, **kwargs):
        staff=self.context['staff']
        staff = Staff.objects.get(pk = staff.id)
        self.sender_role = staff.role
        self.sender_department = staff.Department
        self.sender_college = staff.college
        self.sender_title = staff.title
        self.sender_name = staff.user
        leave = LeaveRequest.objects.create(sender_id=staff, sender_role = staff.role, sender_name = staff.user, sender_title = staff.title, sender_department = staff.Department, **self.validated_data) 
        return leave
    
class ShowLeavesSerializer(ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ['sender_name', 'sender_title', 'sender_role', 'sender_college', 'status', 'sender_department', 'leave_type', 'start_date', 'end_date', 'num_days', 'created_at']

class UpdateLeaveSerializer(ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ['approve']

class LeaveResponseSerializer(ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ['id', 'sender_name', 'sender_department', 'sender_role', 'leave_type', 'start_date', 'end_date', 'num_days', 'status', 'dean_approved', 'vice_approved', 'head_approved']