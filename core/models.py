from django.db import models
from django.contrib.auth.models import AbstractUser

class User (AbstractUser):
    email=models.EmailField(max_length=255, unique=True) 

    def __str__(self) -> str:
        return self.first_name +" "+ self.last_name