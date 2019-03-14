from django.db import models
from accounts.models import User

# Create your models here
class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)    
    created_at = models.DateTimeField(auto_now_add=True)

class Usertoken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)

class Pagetoken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page_access_token = models.CharField(max_length=255)
    page_id = models.CharField(max_length=255)

class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    message = models.TextField()
    comment_id = models.CharField(max_length=255)
    created_at = models.CharField(max_length=255)