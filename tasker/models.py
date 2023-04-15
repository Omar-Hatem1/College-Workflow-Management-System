from django.db import models
from django.conf import settings

class Staff (models.Model):
    # roles
    dean = 'dean'
    vice = 'vice'
    head = 'head'
    Dr = 'dr'
    TA = 'ta'
    role_types =[
        (dean, 'Dean'),
        (vice, 'Vice'),
        (head, 'Head'),
        (Dr, 'Dr'),
        (TA, 'TA') 
    ]
    # titles
    Prof = 'Prof'
    Dr = 'Dr'
    TA = 'Eng'
    titles_types =[
    (Prof, 'Prof'),
    (Dr, 'Dr'),
    (TA, 'TA')
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , related_name='staff')
    role = models.CharField(max_length=4, choices=role_types)
    title = models.CharField(max_length=4, choices=titles_types )

class Task(models.Model):
    title = models.CharField(null=True,blank=True, max_length=150)
    description = models.TextField(null=True,blank=True)
    deadline = models.DateField(null=True, blank=True)
    file = models.FileField(upload_to='tasker/files/tasks', null=True, blank=True)
    status = models.BooleanField(default=False)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE) 
    receivers = models.ForeignKey(Staff,on_delete=models.CASCADE, related_name='receivers')
    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_added']
    def __str__(self) -> str:
        return self.title

class TaskResponse(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    task = models.OneToOneField(Task, on_delete=models.CASCADE , related_name='task_response')
    title = models.CharField(null=True,blank=True, max_length=150)
    description = models.TextField(null=True,blank=True)
    file = models.FileField(upload_to='tasker/files/responses', null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)