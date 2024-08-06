from django.contrib.auth.models import User

from django.db import models

# Create your models here.

class Notes(models.Model):
    # 32:52 par ek extension add kiya hai
    # username-ankit
    # email-ankit123@gmail.com
    # password-ankit123
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    title=models.CharField(max_length=100)
    description=models.TextField()
    def __str__(self):
        return self.title
    

class Homework(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    subject=models.CharField(max_length=20)
    title=models.CharField(max_length=50)
    description=models.TextField()
    due=models.DateTimeField()
    status=models.BooleanField(default=False)
    def __str__(self):
        return self.title
    
    

class Todo(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    status=models.BooleanField(default=False)
    def __str__(self):
        return self.title
    
    