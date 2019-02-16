from django.db import models
from accounts.models import User

# Create your models here
class Project(models.Model):
    title = models.CharField(max_length=255)
    key1 = models.CharField(max_length=255,blank='true')
    key2 = models.CharField(max_length=255,blank='true')
    key3 = models.CharField(max_length=255,blank='true')
    key4 = models.CharField(max_length=255,blank='true')
    key5 = models.CharField(max_length=255,blank='true')
    key6 = models.CharField(max_length=255,blank='true')
    key7 = models.CharField(max_length=255,blank='true')
    key8 = models.CharField(max_length=255,blank='true')
    key9 = models.CharField(max_length=255,blank='true')
    key10 = models.CharField(max_length=255,blank='true')
    exkey1 = models.CharField(max_length=255,blank='true')
    exkey2 = models.CharField(max_length=255,blank='true')
    exkey3 = models.CharField(max_length=255,blank='true')
    exkey4 = models.CharField(max_length=255,blank='true')
    exkey5 = models.CharField(max_length=255,blank='true')
    exkey6 = models.CharField(max_length=255,blank='true')
    exkey7 = models.CharField(max_length=255,blank='true')
    exkey8 = models.CharField(max_length=255,blank='true')
    exkey9 = models.CharField(max_length=255,blank='true')
    exkey10 = models.CharField(max_length=255,blank='true')
    notification_duration = models.IntegerField(blank='true')
    notification_email = models.CharField(blank='true',max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

# Create your models here
class ProjectData(models.Model):
    project_id = models.IntegerField()
    key1 = models.TextField(blank='true')
