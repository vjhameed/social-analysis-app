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
from django.conf import settings
from dashboard.models import Project, Usertoken, Pagetoken, Comment, Usertwittertoken
from .tasks import fetchUserData, fetchTwitterData
from django.utils.encoding import smart_bytes, smart_text, force_text
import sys
import traceback

CONSUMER_KEY = 'mqjmf3Tp4D8NGNDd5AR9dHKrT'
CONSUMER_SECRET = 'd3uPKttcEBYLPeyyrLIFRi45KzPCKcgeEMYs8kAo00gFk5egDD'


def MainView(request,pid):
    pro = Project.objects.get(id=pid)
    projects = Project.objects.filter(user=request.user)
    comments = Comment.objects.filter(project=pro)  
    nomale = comments.filter(gender='male').count()
    nofemale = comments.filter(gender='female').count()
    nopositive = comments.filter(sentiment='Positive').count()
    nonegative = comments.filter(sentiment='Negative').count()
    nonuetral = comments.filter(sentiment='Nuetral').count()
    print(to_datetime('Fri Mar 29 18:14:07 +0000 2019'))

    return render(request,'core/main.html',{'comments':comments,'project':pro,'projects':projects,'nomale':nomale,'nofemale':nofemale,'nonegative':nonegative,'nopositive':nopositive,'nonuetral':nonuetral})


def HomePageView(request):
    projects = Project.objects.filter(user=request.user)

    if 'insta_access_token' not in request.session or not request.session['insta_access_token']:
        url = 'https://api.instagram.com/oauth/authorize/?client_id=%s&redirect_uri=%s&response_type=code' % (settings.INSTAGRAM_CONFIG['client_id'], settings.INSTAGRAM_CONFIG['redirect_uri'])
    else:
        url = None

    url = 'https://api.instagram.com/oauth/authorize/?client_id=%s&redirect_uri=%s&response_type=code' % (settings.INSTAGRAM_CONFIG['client_id'], settings.INSTAGRAM_CONFIG['redirect_uri'])


    return render(request,'core/index.html',{"projects":projects, 'insta_connect_url': url})


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
    tokenurl = "https://graph.facebook.com/v3.2/oauth/access_token?grant_type=fb_exchange_token&client_id=188312881935144&client_secret=57ee2101ea55a4e93b6ce36a6cdee00b&fb_exchange_token={}".format(token)
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

    if params['daterange'] != '':
        strarr = params['daterange'].split('-')
        tempcoms = list()
        for com in comments:
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
    return response


def insta_callback(request):
    code = request.GET.get("code")
    if not code:
        return 'Missing code'
    try:
        get_access_token_url = 'https://api.instagram.com/oauth/access_token'
        params = dict(
            client_id=settings.INSTAGRAM_CONFIG['client_id'],
            client_secret=settings.INSTAGRAM_CONFIG['client_secret'],
            grant_type='authorization_code',
            redirect_uri=settings.INSTAGRAM_CONFIG['redirect_uri'],
            code=code
        )
        resp = requests.post(url=get_access_token_url, data=params)
        data = resp.json()
        access_token = data['access_token']
        if not access_token:
            return redirect('/')
        request.session['insta_access_token'] = access_token
        request.session['instagram'] = {}
        request.session['instagram']['user_id'] = data['user']['id']
        request.session['instagram']['user_id'] = data['user']['id']
        request.session['instagram']['username'] = data['user']['username']
        request.session['instagram']['profile_picture'] = data['user']['profile_picture']
        request.session['instagram']['full_name'] = data['user']['full_name']

        get_recent_media_url = 'https://api.instagram.com/v1/users/self/media/recent/?access_token=%s&count=50' % (request.session['insta_access_token'])
        recent_media = requests.get(url=get_recent_media_url)

        recent_media_dict = recent_media.json()

        for index, media in enumerate(recent_media_dict['data']):
            if not media['comments']['count'] == 0:
                get_media_comments_url = 'https://api.instagram.com/v1/media/%s/comments?access_token=%s' % (media['id'], request.session['insta_access_token'])
                media_comments = requests.get(url=get_media_comments_url)
                print(media_comments.json())
                recent_media_dict['data'][index]['comments']['data'] = media_comments.json()['data']

        with open('tmp.json', 'w') as media_file:
            media_file.write(json.dumps(recent_media_dict))
    except Exception as e:
        print(e)
        traceback.print_exc()
    return redirect('/')
