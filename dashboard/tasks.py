import string

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from dashboard.models import Project, Usertoken, Pagetoken, Comment, Usertwittertoken
from celery import shared_task
import requests
from aylienapiclient import textapi
import json
import datetime
from dashboard.utils import get_api, getLanguage, getSentiment, getUserGender
import re

@shared_task
def fetchTwitterData(userid,proid):
    #read tweet from home_timeline
    twit = Usertwittertoken.objects.get(user_id=userid)
    api = get_api(twit.access_key,twit.access_secret) #Oauth user
    public_tweets = api.home_timeline() #get homepage tweets
    pro = Project.objects.get(id=proid)
    for twit in public_tweets:
        obj = twit._json


        
        newcom = Comment()
        newcom.message = re.sub('[^a-zA-Z0-9 \n\.]', '', obj['text'])
        newcom.source = 'twit'
        newcom.gender = getUserGender(obj['user']['name'])
        newcom.comment_id = obj['id']
        newcom.created_at = obj['created_at']                        
        newcom.language = getLanguage(newcom.message) 
        newcom.sentiment = getSentiment(newcom.message,newcom.language)  
        newcom.project = pro
        newcom.user_name = obj['user']['screen_name']
        newcom.user_image = obj['user']['profile_image_url_https']
        newcom.user_followers = obj['user']['followers_count']
        newcom.save()

    return True
    # print(public_tweets)


@shared_task
def fetchUserData(userid,proid):
    pro = Project.objects.get(id=proid)
    pages = Pagetoken.objects.filter(user_id=userid)
    for page in pages:
        tokenurl = "https://graph.facebook.com/{0}/feed?access_token={1}".format(page.page_id,page.page_access_token)
        r = requests.get(tokenurl)
        pk = json.loads(r.content)        
        for post in pk['data']:
            date = post['created_time'].split('T')
            d1 = datetime.datetime.strptime(date[0],'%Y-%M-%d')
            d2 = datetime.datetime.now()
            delta = d2 - d1
            # if 1 ==1 :
            post_id = post['id']            
            tokenurl = "https://graph.facebook.com/{0}/comments?access_token={1}&fields=from,message,attachment,created_time".format(post['id'],page.page_access_token)
            r = requests.get(tokenurl)
            comments = json.loads(r.content)
            for com in comments['data']:
                date = com['created_time'].split('T')
                d1 = datetime.datetime.strptime(date[0],'%Y-%M-%d')
                d2 = datetime.datetime.now()
                delta = d2 - d1
                # if 1 == 1 :
                newcom = Comment()
                newcom.message = re.sub('[^a-zA-Z0-9 \n\.]', '', com['message'])
                newcom.source = 'fb'
                newcom.gender = 'male'
                newcom.comment_id = com['id']
                newcom.created_at = com['created_time']                        
                newcom.language = getLanguage(newcom.message)  
                newcom.sentiment = getSentiment(newcom.message ,newcom.language)  
                newcom.project = pro
                newcom.user_name = 'name'
                newcom.user_image = 'img'
                newcom.user_followers = '123'

                newcom.save()
                           
    return 'fetched all data for a page'

@shared_task
def create_random_user_accounts(total):
    for i in range(total):
        username = 'user_{}'.format(get_random_string(10, string.ascii_letters))
        email = '{}@example.com'.format(username)
        password = get_random_string(50)
        User.objects.create_user(username=username, email=email, password=password)
    return '{} random users created with success!'.format(total)