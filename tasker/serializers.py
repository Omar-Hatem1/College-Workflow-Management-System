from rest_framework import serializers
from .models import *


class TaskResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskResponse
        fields ='__all__' 

class StaffSerializer (serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'user', 'title', 'role']
    
    user = serializers.StringRelatedField() 

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id','title', 'description', 'deadline','file', 'status','staff', 'receivers', 'task_response']
    task_response = TaskResponseSerializer(TaskResponse)
    staff = StaffSerializer(Staff)
    receivers = StaffSerializer(Staff) 

class TaskAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title','deadline','status','staff', 'receivers']

    staff = StaffSerializer(Staff)
    receivers = StaffSerializer(Staff)

class TaskViewSerializer(serializers.ModelSerializer):
    # assigned_by = serializers.PrimaryKeyRelatedField(source='staff', read_only=True)
    # assigned_to = serializers.PrimaryKeyRelatedField(source='receivers',read_only=True)
    class Meta:
        model = Task
        fields = ['id','title', 'description', 'deadline','file', 'status','staff', 'receivers']
    staff = StaffSerializer(Staff)
    receivers = StaffSerializer(Staff)
    #assigned_by = StaffSerializer(Staff) 
    #assigned_to = StaffSerializer(Staff)

class ReceiversSerializer(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        staff_role = self.context['staff_role']
        if staff_role == 'dean':
            #print (Staff.objects.exclude(role=staff_role))
            return Staff.objects.exclude(role=staff_role)
        elif staff_role == 'vice':
            return Staff.objects.exclude(role = 'dean').exclude(role =staff_role)
        elif staff_role == 'head':
            return Staff.objects.exclude(role = 'dean').exclude(role = 'vice').exclude(role =staff_role)

class CreateTaskSerializer(serializers.ModelSerializer):
    receivers = ReceiversSerializer() # List of allowed receivers
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline','file', 'status', 'receivers']

    def save(self, **kwargs):
        staff_id=self.context['staff_id']
        staff = Staff.objects.get(pk = staff_id)
        task = Task.objects.create(staff=staff, **self.validated_data) # Todo update or create methods -> done
        return task

class UpdateTaskSerializer(serializers.ModelSerializer):
    receivers = ReceiversSerializer() # List of allowed receivers
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline','file', 'status', 'receivers']

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.deadline = validated_data.get('deadline', instance.deadline)
        instance.file = validated_data.get('file', instance.file)
        instance.status = validated_data.get('status', instance.status)
        instance.receivers = validated_data.get('receivers', instance.receivers)
        instance.save()
        return instance


# class TaskListSerializer(serializers.PrimaryKeyRelatedField):
#     def get_queryset(self):
#         staff_id = self.context['staff_id']
#         if staff_id == staff_id:
#             return Task.objects.filter(staff_id = self.receivers)

class TaskResponseForeignKeySerializer(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user_id=self.context['user_id']
        if user_id == user_id:
            return Task.objects.select_related('receivers__user').select_related('staff__user').filter(receivers__user_id=user_id)

class CreateTaskResponseSerializer(serializers.ModelSerializer):
    task = TaskResponseForeignKeySerializer()
    class Meta:
        model = TaskResponse
        fields = ['title', 'description', 'file', 'task']
    def save(self, **kwargs):
        # task_pk = self.context['task_pk']
        # task = Task.objects.get(pk = task_pk)
        staff_id=self.context['staff_id']
        staff = Staff.objects.get(pk = staff_id)
        task = TaskResponse.objects.create(staff=staff, **self.validated_data)
        return task

class UpdateTaskResponseSerializer(serializers.ModelSerializer):
    task = TaskResponseForeignKeySerializer()
    class Meta:
        model = TaskResponse
        fields = ['title', 'description', 'file', 'task']
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.file = validated_data.get('file', instance.file)
        instance.task = validated_data.get('task', instance.task)
        instance.save()
        return instance



# class ReceiverListSerlizer (serializers.Serializer):
#     def get_queryset(self):
#         user_id = self.context['user_id']
#         if self.context['staff_id'] == '1':
#             return Staff.objects.exclude(user_id=user_id)
#         elif self.context['staff_id'] == '2':
#             return Staff.objects.exclude(role = '1').exclude(user_id=user_id)
#         elif self.context['staff_id'] == '3':
#             return Staff.objects.exclude(role = '1').exclude(role = '2').exclude(user_id=user_id)
