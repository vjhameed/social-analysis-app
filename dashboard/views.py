from django.views.generic.edit import FormView
from django.views.generic import TemplateView, View
from django.views.generic.base import RedirectView, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.core import serializers
from datetime import datetime,timedelta
from dateutil.parser import parse
from email.utils import parsedate_tz
import json
import requests
import time
import tweepy #API for twitter
from dashboard.models import Project, Usertoken, Pagetoken, Comment, Usertwittertoken
from .tasks import fetchUserData, fetchTwitterData

CONSUMER_KEY = 'mqjmf3Tp4D8NGNDd5AR9dHKrT'
CONSUMER_SECRET = 'd3uPKttcEBYLPeyyrLIFRi45KzPCKcgeEMYs8kAo00gFk5egDD'


def MainView(request,pid):
    pro = Project.objects.get(id=pid)
    projects = Project.objects.filter(user=request.user)
    comments = Comment.objects.filter(project=pro)  
    nomale = Comment.objects.filter(gender='male').count()
    nofemale = Comment.objects.filter(gender='female').count()
    nopositive = Comment.objects.filter(sentiment='Positive').count()
    nonegative = Comment.objects.filter(sentiment='Negative').count()
    nonuetral = Comment.objects.filter(sentiment='Nuetral').count()
    
    return render(request,'core/main.html',{'comments':comments,'project':pro,'projects':projects,'nomale':nomale,'nofemale':nofemale,'nonegative':nonegative,'nopositive':nopositive,'nonuetral':nonuetral})

def HomePageView(request):
    projects = Project.objects.filter(user=request.user)
    return render(request,'core/index.html',{"projects":projects})

def SentimentView(request,pid):
    pro = Project.objects.get(id=pid)
    projects = Project.objects.filter(user=request.user)
    comments = Comment.objects.filter(project=pro)  
    

    return render(request,'core/sentiment.html',{'comments':comments,'project':pro,'projects':projects})

def CrisisPageView(request,pid):
    projects = Project.objects.filter(user=request.user)

    pro = Project.objects.get(id=pid)
    comments = Comment.objects.filter(project=pro)
    crisiscomments = comments.filter(is_crisis='Problematic')  
    nocrisiscomments = comments.filter(is_crisis='Non Problematic')    
    numnocrisiscomments = comments.filter(is_crisis='Non Problematic').count()  
    numcrisiscomments = comments.filter(is_crisis='Problematic').count()  
    fbcrisiscomments = crisiscomments.filter(source='fb').count()
    twitcrisiscomments = crisiscomments.filter(source='twit').count()

    return render(request,'core/crisis.html',{'project':pro,'projects':projects,'comments':crisiscomments,'noncricom':nocrisiscomments,'numcricomments':numcrisiscomments,'numnocricomments':numnocrisiscomments,'fbtox':fbcrisiscomments,'twittox':twitcrisiscomments})

def IntentPageView(request,pid):
    projects = Project.objects.filter(user=request.user)

    pro = Project.objects.get(id=pid)
    comments = Comment.objects.filter(project=pro)
    intcoms = comments.filter(is_intent='True')  
    nonintcoms = comments.filter(is_intent='False')    
    num_non_int_com = comments.filter(is_intent='False').count()  
    num_int_com = comments.filter(is_intent='True').count()  
    fb_tox_com = intcoms.filter(source='fb').count()
    twit_tox_com = intcoms.filter(source='twit').count()

    return render(request,'core/intent.html',{'project':pro,'projects':projects,'comments':intcoms,'nonintcom':nonintcoms,'numnointcomments':num_non_int_com,'numintcomments':num_int_com,'fbtox':fb_tox_com,'twittox':twit_tox_com})

def GuardPageView(request,pid):
    projects = Project.objects.filter(user=request.user)

    pro = Project.objects.get(id=pid)
    comments = Comment.objects.filter(project=pro)
    toxcoms = comments.filter(is_toxic='True')  
    nontoxcoms = comments.filter(is_toxic='False')    
    num_non_tox_com = comments.filter(is_toxic='False').count()  
    num_tox_com = comments.filter(is_toxic='True').count()  
    fb_tox_com = toxcoms.filter(source='fb').count()
    twit_tox_com = toxcoms.filter(source='twit').count()

    return render(request,'core/guard.html',{'project':pro,'projects':projects,'comments':toxcoms,'nontoxcom':nontoxcoms,'numnotoxcomments':num_non_tox_com,'numtoxcomments':num_tox_com,'fbtox':fb_tox_com,'twittox':twit_tox_com})

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
        fetchTwitterData.delay(request.user.id,proid)
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
    return JsonResponse('success',safe=False)
    
def sentimentAnalysis(request,pid):
    pro = Project.objects.get(id=pid)
    comments = Comment.objects.filter(project=pro)

def FilterView(request):
    params = json.loads(request.body)
    com = {}
    project = Project.objects.get(id=params['pro_id'])    
    comments = Comment.objects.filter(project_id=params['pro_id'])
    if len(params['social']) > 0:
        comments = comments.filter(source__in=params['social'])
    if len(params['lng']) > 0:
        comments = comments.filter(language__in=params['lng'])

    if len(params['gen']) > 0:
        comments = comments.filter(gender__in=params['gen'])

    if params['sent'] != '':
        comments = comments.filter(sentiment=params['sent'])

    if len(params['date']) > 0:
        tempcoms = list()
        for com in comments:
            d1 = to_datetime(com.created_at)
            d2 = datetime.now()
            delta = d2 - d1
            for date in params['date']:
                print(delta.days)
                if delta.days <= int(date):
                    tempcoms.append(com)
        comments = tempcoms

    data = serializers.serialize("json", comments)
    return JsonResponse(data,safe=False)

def to_datetime(datestring):
    time_tuple = parsedate_tz(datestring.strip())
    dt = datetime(*time_tuple[:6])
    return dt - timedelta(seconds=time_tuple[-1])
    
def callback(request):
    verifier = request.GET.get('oauth_verifier')
    oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    token = request.session['request_token']

    request.session.delete('request_token')

    oauth.request_token = token    

    oauth.get_access_token(verifier)    
    try:
        twit = Usertwittertoken.objects.get(user=request.user.id)
        twit.user = request.user
        twit.access_key = oauth.access_token
        twit.access_secret = oauth.access_token_secret
        twit.save()

    except Usertwittertoken.DoesNotExist:
        newtwit = Usertwittertoken()
        newtwit.user = request.user
        newtwit.access_key = oauth.access_token
        newtwit.access_secret = oauth.access_token_secret
        newtwit.save()

    return redirect('/dashboard')


def twitterAuth(request):   
    request.session.delete('request_token')
    # start the OAuth process, set up a handler with our details
    oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    # direct the user to the authentication url
    # if user is logged-in and authorized then transparently goto the callback URL
    auth_url = oauth.get_authorization_url(True)
    response = HttpResponseRedirect(auth_url)

    # store the request token
    request.session['request_token'] = oauth.request_token
    print(request.session['request_token'])
    return response
