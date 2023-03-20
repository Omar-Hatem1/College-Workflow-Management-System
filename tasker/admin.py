from django.contrib import admin
from .models import *




@admin.register(Staff)
class StaffAdmin (admin.ModelAdmin):
    list_display = ['user', 'role']
    list_editable = ['role']
    
@admin.register(Task)
class TaskAdmin (admin.ModelAdmin):
    #fields = ['title', 'description', 'deadline', 'file', 'status', 'staff']
    pass

@admin.register(TaskResponse)
class TaskResponse (admin.ModelAdmin):
    pass