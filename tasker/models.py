from django.db import models
from django.conf import settings

class Staff (models.Model):
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
    Prof = 'Prof'
    Dr = 'Dr'
    TA = 'Eng' 
    titles_types =[
    (Prof, 'Prof'),
    (Dr, 'Dr'),
    (TA, 'TA')
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=4, choices=role_types)
    title = models.CharField(max_length=4, choices=titles_types )
    # def __str__(self) -> str:
    #     return self.title + ' ' + self.user.first_name + ' ' + self.user.last_name   


class Task(models.Model):
    # rejected = 'R'
    # accepted= 'A'
    
    # task_status = [
    #     (rejected, 'Reject'),
    #     (accepted, 'Accepted')
    # ]
    
    title = models.CharField(null=True,blank=True, max_length=150)
    description = models.CharField(null=True,blank=True, max_length=150)
    deadline = models.DateField(null=True, blank=True)
    file = models.FileField(upload_to='tasker/files/tasks', null=True, blank=True)
    status = models.BooleanField(default=False)
    # TODO select the sender by default 
    # TODO staff who will receive the task
    # TODO If the sender in Dean that list should contain all Vice, Heads, Staff, and Secretary 
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE) 
    receivers = models.ForeignKey(Staff,on_delete=models.CASCADE, related_name='receivers')
    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.title

class TaskResponse(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    title = models.CharField(null=True,blank=True, max_length=150)
    description = models.CharField(null=True,blank=True, max_length=150)
    file = models.FileField(upload_to='tasker/files/responses', null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


# class Attachment(models.Model):
#     attach = models.TextField(null=True,blank=True)
#     task = models.OneToOneField(Task,on_delete=models.CASCADE)

# class Re_Attachment(models.Model):
#     re_attach = models.TextField(null=True,blank=True)
#     task = models.OneToOneField(Task,on_delete=models.CASCADE)



