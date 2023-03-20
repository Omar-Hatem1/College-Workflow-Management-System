from rest_framework import serializers
from .models import *

class StaffSerializer (serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'user', 'title', 'role']
    
    user = serializers.StringRelatedField()

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id','title', 'description', 'deadline','file', 'status','staff', 'receivers']
    
    staff = StaffSerializer(Staff)
    receivers = StaffSerializer(Staff) 

class TaskListSerializer(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        staff_id = self.context['staff_id']
        if staff_id == staff_id:
            return Task.objects.filter(staff_id = self.receivers)


class ReceiversSerializer(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        staff_role = self.context['staff_role']
        if staff_role == 'dean':
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
        task = Task.objects.create(staff=staff, **self.validated_data)
        return task



# class TaskResponseForeignKeySerializer(serializers.PrimaryKeyRelatedField):
#     def get_queryset(self):
#         user_id=self.context['user_id']
#         return Task.objects.filter(receivers__user_id=user_id)


# class CreateTaskResponseSerializer(serializers.ModelSerializer):
#     task = TaskResponseForeignKeySerializer()
#     class Meta:
#         model = TaskResponse
#         fields = ['title', 'description', 'file', 'task']
    
#     def save(self, **kwargs):
#         staff = Staff.objects.get(user_id=self.context['user_id'])
#         task = TaskResponse.objects.create(staff=staff, **self.validated_data)
#         return task



# class TaskResponseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TaskResponse
#         fields = ['title', 'description', 'file']
        

# class ReceiverListSerlizer (serializers.Serializer):
#     def get_queryset(self):
#         user_id = self.context['user_id']
#         if self.context['staff_id'] == '1':
#             return Staff.objects.exclude(user_id=user_id)
#         elif self.context['staff_id'] == '2':
#             return Staff.objects.exclude(role = '1').exclude(user_id=user_id)
#         elif self.context['staff_id'] == '3':
#             return Staff.objects.exclude(role = '1').exclude(role = '2').exclude(user_id=user_id)


    
