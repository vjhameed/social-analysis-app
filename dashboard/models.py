from django.db import models
from accounts.models import User

# Create your models here
class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255,db_column='title')    
    created_at = models.DateTimeField(auto_now_add=True)


class Usertoken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)

class Usertwittertoken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_key = models.CharField(max_length=255)
    access_secret = models.CharField(max_length=255)

class Pagetoken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page_access_token = models.CharField(max_length=255)
    page_id = models.CharField(max_length=255)

class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    source = models.CharField(max_length=255)
    message = models.TextField()
    comment_id = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    sentiment = models.CharField(max_length=255)
    created_at = models.CharField(max_length=255)
    user_name =  models.CharField(max_length=255)
    user_image =  models.CharField(max_length=255)
    user_followers =  models.CharField(max_length=255)
    is_toxic =  models.CharField(max_length=255)
    is_intent =  models.CharField(max_length=255)
    is_crisis =  models.CharField(max_length=255)
