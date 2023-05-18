from django.db import models
from django.conf import settings

class Staff (models.Model):
    #Departments
    Computer_Science = 'CS',
    Information_System= 'IS',
    Artificial_Intelligence= 'AI',
    Communication_Network= 'NetWork',
    General='Gen',

    Dep_CHOICES= [
    ('Computer_Science', 'CS'),
    ('Artificial_Intelligence', 'AI'),
     ('Information_System', 'IS'),
     ('Communication_Network', 'Network'),
     ('General','Gen')
     ]
    
    #roles
    Dean= 'Dean',
    Vice_Dean= 'v.Dean',
    Head_of_department= 'Head',
    Doctor='Doc',
    Secretary= 'sec',
    Assistant ='Assistant',
    Admin = 'Admin'
    Roles_choices= [
     ('Dean', 'Dean'),
     ('Vice_Dean', 'V.Dean'),
     ('Head_of_department', 'Head'),
     ('Doctor', 'Doctor'),
     ('Secretary','Sec'),
     ('Assistant','Assistant'),
     ('Admin', 'Admin'),
    ]
    #Titles
    Professor='Prof',
    Associate_Professor='Associate.Prof',
    Assistant_Professor='Assistant.Prof',
    Instructor='Instructor',
    General='General',

    Titles_Choices=[
     ('Professor','Prof'),
     ( 'Associate_Professor','Associate.Prof'),
     ('Assistant_Professor','Assistant.Prof'),
     ('Instructor','Instructor'),
     ('General','General'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , related_name='staff')
    role = models.CharField(max_length=40, choices=Roles_choices)
    title = models.CharField(max_length=40, choices=Titles_Choices)
    Department = models.CharField(max_length=40, choices=Dep_CHOICES)
    college = models.CharField(max_length=50, default="CSIS")
    name = models.CharField(max_length=100)

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


class LeaveRequest(models.Model):
    LEAVE_TYPES = (
        ('Ordinary', 'Ordinary'),
        ('Casual', 'Casual'),
        ('Sick', 'Sick'),
        ('Unpaid', 'Unpaid')
    )

    STATUS_CHOICES = (
        (None, 'Pending'),
        ('Accepted', 'Accepted'),
        ('Refused', 'Refused')
    )

    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    receiver = models.CharField(max_length=50)
    sender_id = models.ForeignKey(Staff, on_delete = models.CASCADE)
    sender_name = models.CharField(max_length=100)
    sender_role = models.CharField(max_length=20, blank= True, null=True)
    sender_title = models.CharField(max_length=50, blank= True, null= True)
    sender_department = models.CharField(max_length=50)
    sender_college = models.CharField(max_length=50, default="CSIS")
    start_date = models.DateField()
    end_date = models.DateField()
    num_days = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=True)
    approved_by = models.CharField(max_length=20, null=True)
    dean_approved = models.BooleanField(null=True)
    vice_dean_approved = models.BooleanField(null=True)
    head_of_department_approved = models.BooleanField(null=True)
    
    # def save(self, *args, **kwargs):
    #     if self.start_date > self.end_date:
    #         raise ValueError("Start date cannot be later than end date.")
    #     self.num_days = (self.end_date - self.start_date).days + 1
    #     super(LeaveRequest, self).save(*args, **kwargs)

