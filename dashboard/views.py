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
from django.utils.encoding import smart_bytes, smart_text, force_text
import sys
from django.conf import settings
import facebooksdk as facebook
import traceback

graph = facebook.GraphAPI(version="2.12")

 
def MainView(request,pid):
    pro = Project.objects.get(id=pid)
    projects = Project.objects.filter(user=request.user)
    comments = Comment.objects.filter(project=pro)  
    filtercounts = dict()
    filtercounts['nomale'] = comments.filter(gender='Male').count()
    filtercounts['nofemale'] = comments.filter(gender='Female').count()

    filtercounts['nofb'] = comments.filter(source='fb').count()
    filtercounts['notwit'] = comments.filter(source='twit').count()
    filtercounts['noyou'] = comments.filter(source='youtube').count()
    filtercounts['noins'] = comments.filter(source='insta').count()

    filtercounts['nopos'] = comments.filter(sentiment='Positive').count()
    filtercounts['noneg'] = comments.filter(sentiment='Negative').count()
    filtercounts['nonue'] = comments.filter(sentiment='Neutral').count()

    filtercounts['encom'] = comments.filter(language='en').count()
    filtercounts['frcom'] = comments.filter(language='fr').count()
    filtercounts['arcom'] = comments.filter(language='ar').count()
    filtercounts['arzcom'] = comments.filter(language='arz').count()

    return render(request,'core/main.html',{'comments':comments,'project':pro,'projects':projects,'filterdata':filtercounts})

def HomePageView(request):
    projects = Project.objects.filter(user=request.user)

    insta_connect_url = None

    if 'fb_access_token' not in request.session or not request.session['fb_access_token']:
        perms = ["instagram_basic", "instagram_manage_comments","manage_pages"]
        insta_connect_url = graph.get_auth_url(settings.FACEBOOK_CONFIG['app_id'], settings.FACEBOOK_CONFIG['redirect_uri'], perms)        
    else:
        graph.access_token = request.session['fb_access_token']
        accounts = graph.request('/me/accounts')
        print(accounts)

    perms = ["instagram_basic", "instagram_manage_comments","manage_pages"]
    insta_connect_url = graph.get_auth_url(settings.FACEBOOK_CONFIG['app_id'], settings.FACEBOOK_CONFIG['redirect_uri'], perms)

    return render(request, 'core/index.html', {"projects": projects, 'insta_connect_url': insta_connect_url})

def SentimentView(request,pid):
    pro = Project.objects.get(id=pid)
    projects = Project.objects.filter(user=request.user)
    comments = Comment.objects.filter(project=pro)  
    filtercounts = dict()
    filtercounts['nomale'] = comments.filter(gender='Male').count()
    filtercounts['nofemale'] = comments.filter(gender='Female').count()

    filtercounts['nofb'] = comments.filter(source='fb').count()
    filtercounts['notwit'] = comments.filter(source='twit').count()
    filtercounts['noyou'] = comments.filter(source='youtube').count()
    filtercounts['noins'] = comments.filter(source='insta').count()

    filtercounts['nopos'] = comments.filter(sentiment='Positive').count()
    filtercounts['noneg'] = comments.filter(sentiment='Negative').count()
    filtercounts['nonue'] = comments.filter(sentiment='Neutral').count()

    filtercounts['encom'] = comments.filter(language='en').count()
    filtercounts['frcom'] = comments.filter(language='fr').count()
    filtercounts['arcom'] = comments.filter(language='ar').count()
    filtercounts['arzcom'] = comments.filter(language='arz').count()


    return render(request,'core/sentiment.html',{'comments':comments,'project':pro,'projects':projects,'filterdata':filtercounts})

def CrisisPageView(request,pid):
    projects = Project.objects.filter(user=request.user)

    pro = Project.objects.get(id=pid)
    comments = Comment.objects.filter(project=pro)
    crisiscomments = comments.filter(is_crisis='Problematic')  
    nocrisiscomments = comments.filter(is_crisis='Non Problematic')    
    numnocrisiscomments = comments.filter(is_crisis='Non Problematic').count()  
    numcrisiscomments = comments.filter(is_crisis='Problematic').count()  
    filtercounts = dict()

    filtercounts['nocrisis'] = numnocrisiscomments
    filtercounts['crisis'] = numcrisiscomments

    filtercounts['nomale'] = comments.filter(gender='Male').count()
    filtercounts['nofemale'] = comments.filter(gender='Female').count()

    filtercounts['nofb'] = comments.filter(source='fb').count()
    filtercounts['notwit'] = comments.filter(source='twit').count()
    filtercounts['noyou'] = comments.filter(source='youtube').count()
    filtercounts['noins'] = comments.filter(source='insta').count()

    filtercounts['nopos'] = comments.filter(sentiment='Positive').count()
    filtercounts['noneg'] = comments.filter(sentiment='Negative').count()
    filtercounts['nonue'] = comments.filter(sentiment='Neutral').count()

    filtercounts['encom'] = comments.filter(language='en').count()
    filtercounts['frcom'] = comments.filter(language='fr').count()
    filtercounts['arcom'] = comments.filter(language='ar').count()
    filtercounts['arzcom'] = comments.filter(language='arz').count()

    return render(request,'core/crisis.html',{'project':pro,'projects':projects,'comments':crisiscomments,'filterdata':filtercounts})

def IntentPageView(request,pid):
    projects = Project.objects.filter(user=request.user)

    pro = Project.objects.get(id=pid)
    comments = Comment.objects.filter(project=pro)
    intcoms = comments.filter(is_intent='True')  
    num_non_int_com = comments.filter(is_intent='False').count()  
    num_int_com = comments.filter(is_intent='True').count()  

    filtercounts = dict()
    filtercounts['nointent'] = num_non_int_com
    filtercounts['intent'] = num_int_com

    filtercounts['nomale'] = comments.filter(gender='Male').count()
    filtercounts['nofemale'] = comments.filter(gender='Female').count()

    filtercounts['nofb'] = comments.filter(source='fb').count()
    filtercounts['notwit'] = comments.filter(source='twit').count()
    filtercounts['noyou'] = comments.filter(source='youtube').count()
    filtercounts['noins'] = comments.filter(source='insta').count()

    filtercounts['nopos'] = comments.filter(sentiment='Positive').count()
    filtercounts['noneg'] = comments.filter(sentiment='Negative').count()
    filtercounts['nonue'] = comments.filter(sentiment='Neutral').count()

    filtercounts['encom'] = comments.filter(language='en').count()
    filtercounts['frcom'] = comments.filter(language='fr').count()
    filtercounts['arcom'] = comments.filter(language='ar').count()
    filtercounts['arzcom'] = comments.filter(language='arz').count()

    return render(request,'core/intent.html',{'project':pro,'projects':projects,'comments':intcoms,'filterdata':filtercounts})

def GuardPageView(request,pid):
    projects = Project.objects.filter(user=request.user)

    pro = Project.objects.get(id=pid)
    comments = Comment.objects.filter(project=pro)
    toxcoms = comments.filter(is_toxic='True')  
    nontoxcoms = comments.filter(is_toxic='False')    
    num_non_tox_com = comments.filter(is_toxic='False').count()  
    num_tox_com = comments.filter(is_toxic='True').count()  

    filtercounts = dict()
    filtercounts['notoxic'] = num_non_tox_com
    filtercounts['toxic'] = num_tox_com

    filtercounts['nomale'] = comments.filter(gender='Male').count()
    filtercounts['nofemale'] = comments.filter(gender='Female').count()

    filtercounts['nofb'] = comments.filter(source='fb').count()
    filtercounts['notwit'] = comments.filter(source='twit').count()
    filtercounts['noyou'] = comments.filter(source='youtube').count()
    filtercounts['noins'] = comments.filter(source='insta').count()

    filtercounts['nopos'] = comments.filter(sentiment='Positive').count()
    filtercounts['noneg'] = comments.filter(sentiment='Negative').count()
    filtercounts['nonue'] = comments.filter(sentiment='Neutral').count()

    filtercounts['encom'] = comments.filter(language='en').count()
    filtercounts['frcom'] = comments.filter(language='fr').count()
    filtercounts['arcom'] = comments.filter(language='ar').count()
    filtercounts['arzcom'] = comments.filter(language='arz').count()

    return render(request,'core/guard.html',{'project':pro,'projects':projects,'comments':toxcoms,'filterdata':filtercounts})

def ReputationView(request):
    return render(request,'core/reputation.html')

def FinanceView(request):
    return render(request,'core/fintech.html')

def HotelView(request):
    return render(request, 'core/hotel.html')

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
    r = requests.get(tokenurl).json()
    pk = r
    newtoken = pk['access_token']

    pages = requests.get('https://graph.facebook.com/me/accounts?access_token='+newtoken).json()
    if pages.get('error', False):
        raise Exception('facebook')
    twits = pages.get('data')
    Pagetoken.objects.filter(user=request.user.id).delete()
    
    for twit in twits:
        newtwit = Pagetoken()
        newtwit.user = request.user
        newtwit.page_id = twit['id']
        newtwit.page_access_token = twit['access_token']
        newtwit.save()

    try:
        twit = Usertoken.objects.get(user=request.user.id)
        twit.user = request.user
        twit.access_token = newtoken
        twit.save()

    except Usertoken.DoesNotExist:
        newtwit = Usertoken()
        newtwit.user = request.user
        newtwit.access_token = newtoken
        newtwit.save()
    return JsonResponse('success',safe=False)
    
def sentimentAnalysis(request,pid):
    pro = Project.objects.get(id=pid)
    comments = Comment.objects.filter(project=pro)

def FilterView(request):
    params = json.loads(request.body.decode('utf-8'))
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

    if params['daterange'] != '':
        strarr = params['daterange'].split('-')
        tempcoms = list()
        for com in comments:
            if(com.source == 'twit'):
                comdate = to_datetime(com.created_at)                
            else:
                comdate = datetime.strptime(com.created_at,'%Y-%m-%d %H:%M:%S')
            startdate = datetime.strptime(strarr[0].strip(),'%m/%d/%Y')
            enddate = datetime.strptime(strarr[1].strip(),'%m/%d/%Y')
            if comdate > startdate and comdate < enddate:
                tempcoms.append(com)
        comments = tempcoms

    if len(params['date']) > 0:
        tempcoms = list()
        for com in comments:
            d1 = to_datetime(com.created_at,'%Y-%m-%d %H:%M:%S')
            d2 = datetime.now()
            delta = d2 - d1
            for date in params['date']:
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
    oauth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
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
    oauth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    # direct the user to the authentication url
    # if user is logged-in and authorized then transparently goto the callback URL
    auth_url = oauth.get_authorization_url(True)
    response = HttpResponseRedirect(auth_url)

    # store the request token
    request.session['request_token'] = oauth.request_token
    return response


def facebook_auth_handler(request):
    code = request.GET.get("code")
    if not code:
        return redirect('/')
    try:
        access_token = graph.get_access_token_from_code(code, settings.FACEBOOK_CONFIG['redirect_uri'],
                                                        settings.FACEBOOK_CONFIG['app_id'],
                                                        settings.FACEBOOK_CONFIG['app_secret'])
        if not access_token:
            return redirect('/')
        graph.access_token = access_token['access_token']
        request.session['fb_access_token'] = access_token['access_token']
    except Exception as e:
        print(e)
        traceback.print_exc()
    return redirect('/')