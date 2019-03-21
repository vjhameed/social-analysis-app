from django.views.generic.edit import FormView
from django.views.generic import TemplateView, View
from django.views.generic.base import RedirectView, HttpResponseRedirect
from django.contrib.auth import authenticate, login
# from dashboard.utils import *
from django.shortcuts import render
import datetime
from dateutil.parser import parse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import json
from django.shortcuts import redirect, render
from django.urls import reverse
from dashboard.models import Project, Usertoken, Pagetoken, Comment
import requests
from .tasks import fetchUserData
import time
from django.core import serializers


def MainView(request,pid):
    pro = Project.objects.get(id=pid)
    projects = Project.objects.all()
    comments = Comment.objects.filter(project=pro)  
    return render(request,'core/main.html',{'comments':comments,'project':pro,'projects':projects})

def HomePageView(request):
    projects = Project.objects.all()
    return render(request,'core/index.html',{"projects":projects})

def SentimentView(request):
    return render(request,'core/sentiment.html')

def CrisisPageView(request):
    return render(request,'core/crisis.html')

def IntentPageView(request):
    return render(request,'core/intent.html')

def GuardPageView(request):
    return render(request,'core/guard.html')

def ReputationView(request):
    return render(request,'core/reputation.html')

def FinanceView(request):
    return render(request,'core/finance.html')

def ArabiziView(request):
    return render(request,'core/arabizi.html')

def EntityView(request):
    return render(request,'core/entity.html')

def TopicView(request):
    return render(request,'core/topic.html')

def DeleteProject(request,pid):
    pro = Project.objects.get(id=pid)    
    pro.delete()
    return redirect('/dashboard')

def CreateProject(request):
    if request.method == 'POST':
        pro = Project()
        pro.title = request.POST['project_name']
        pro.notification_duration = 8
        pro.user = request.user
        pro.save()
        mainurl = '/dashboard/main/{}'.format(pro.id)  
        proid = pro.id
        fetchUserData.delay(request.user.id,proid)
        time.sleep(20)
        return redirect(mainurl)
    return redirect('/')


def UserTokenView(request): 

    tok = json.loads(request.body.decode('utf-8'))
    token = tok['token']
    tokenurl = "https://graph.facebook.com/v3.2/oauth/access_token?grant_type=fb_exchange_token&client_id=250604469198313&client_secret=b08af79b04bffcd4d55671cdabc61b43&fb_exchange_token={}".format(token)
    r = requests.get(tokenurl)
    pk = json.loads(r.content)
    newtoken = pk['access_token']

    
def sentimentAnalysis(request,pid):
    pro = Project.objects.get(id=pid)
    comments = Comment.objects.filter(project=pro)

def FilterView(request):
    params = json.loads(request.body)
    print(params)
    com = {}
    project = Project.objects.get(id=24)    
    comments = Comment.objects.filter(project_id=project.id)
    if len(params['social']) > 0:
        comments = comments.filter(source__in=params['social'])

    if len(params['lng']) > 0:
        comments = comments.filter(language__in=params['lng'])

    if len(params['gen']) > 0:
        comments = comments.filter(gender__in=params['gen'])

    # if len(params['date']) > 0:
    #     comments = comments.filter(source__in=params['lng'])


    data = serializers.serialize("json", comments)
    return JsonResponse(data,safe=False)

