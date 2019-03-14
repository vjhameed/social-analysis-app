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


def MainView(request,pid):
    pro = Project.objects.get(id=pid)
    comments = Comment.objects.filter(project=pro)
    return render(request,'core/main.html',{'comments':comments,'project':pro})

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
        pages = Pagetoken.objects.filter(user_id=request.user.id)
        for page in pages:
            tokenurl = "https://graph.facebook.com/{0}/feed?access_token={1}".format(page.page_id,page.page_access_token)
            r = requests.get(tokenurl)
            pk = json.loads(r.content)
            for post in pk['data']:
                post_id = post['id']            
                tokenurl = "https://graph.facebook.com/{0}/comments?access_token={1}".format(post['id'],page.page_access_token)
                r = requests.get(tokenurl)
                comments = json.loads(r.content)
                for com in comments['data']:
                    date = com['created_time'].split('T')
                    d1 = datetime.datetime.strptime(date[0],'%Y-%M-%d')
                    d2 = datetime.datetime.now()
                    delta = d2 - d1
                    if delta.days <= 2:
                        newcom = Comment()
                        newcom.message = com['message']
                        newcom.comment_id = com['id']
                        newcom.created_at = com['created_time']
                        newcom.project = pro
                        newcom.save()

        return redirect(mainurl)
    return redirect('/')


def UserTokenView(request): 

    tok = json.loads(request.body.decode('utf-8'))
    token = tok['token']
    tokenurl = "https://graph.facebook.com/v3.2/oauth/access_token?grant_type=fb_exchange_token&client_id=250604469198313&client_secret=b08af79b04bffcd4d55671cdabc61b43&fb_exchange_token={}".format(token)
    r = requests.get(tokenurl)
    pk = json.loads(r.content)
    newtoken = pk['access_token']
    pageurl = "https://graph.facebook.com/v3.2/me/accounts?access_token={0}".format(newtoken)
    r = requests.get(pageurl)
    pk = json.loads(r.content)
    Pagetoken.objects.filter(user_id=request.user.id).delete()
    for item in pk['data']:
        usertoken = Pagetoken()
        usertoken.page_access_token = item['access_token']
        usertoken.page_id = item['id']
        usertoken.user = request.user
        usertoken.save()
    try:
        fbuser = Usertoken.objects.get(user_id=request.user.id)
        fbuser.access_token = newtoken
        fbuser.save()
        return JsonResponse({'status':newtoken})
    except Usertoken.DoesNotExist:
        usertoken = Usertoken()
        usertoken.access_token = newtoken
        usertoken.user = request.user
        usertoken.save()
        return JsonResponse({'status':newtoken})
    
def sentimentAnalysis(request,pid):
    pro = Project.objects.get(id=pid)
    comments = Comment.objects.filter(project=pro)



