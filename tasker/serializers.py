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

