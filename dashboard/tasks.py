import string

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from dashboard.models import Project, Usertoken, Pagetoken, Comment, Usertwittertoken
from celery import shared_task
import requests
from aylienapiclient import textapi
import json
import datetime
import tweepy
from dashboard.utils import get_api, getLanguage, getSentiment, getUserGender, getIntent,getToxic, getCrisis
import re

@shared_task
def fetchTwitterData(userid,proid):
    #read tweet from home_timeline
    twit = Usertwittertoken.objects.get(user_id=userid)
    api = get_api(twit.access_key,twit.access_secret) #Oauth user
    public_tweets = api.user_timeline() #get homepage tweets
    pro = Project.objects.get(id=proid)

    replies = list()
    for full_tweets in public_tweets:
        for tweet in tweepy.Cursor(api.search,q='to:'+full_tweets.user.screen_name,result_type='recent',timeout=999999).items(1000):
            if hasattr(tweet, 'in_reply_to_status_id_str'):
                if (tweet.in_reply_to_status_id_str==full_tweets.id_str):
                    replies.append(tweet)

    for twit in replies:
        obj = twit._json
        
        if not obj['text']:
            return
        else:
            newcom = Comment()
            newcom._message = obj['text'].encode('utf-8')
            newcom.source = 'twit'
            newcom.gender = getUserGender(obj['user']['name'])
            newcom.comment_id = obj['id']
            newcom.created_at = obj['created_at']                        
            newcom.language = 'en' 
            newcom.sentiment = getSentiment(obj['text'],newcom.language)  
            newcom.project = pro
            newcom._user_name = obj['user']['screen_name'].encode('utf-8')
            newcom.user_image = obj['user']['profile_image_url_https']
            newcom.user_followers = obj['user']['followers_count']
            newcom.is_toxic = getToxic(obj['text'])
            newcom.is_intent = getIntent(obj['text'])
            newcom.is_crisis = getCrisis(obj['text'],newcom.language)

            newcom.save()

    return True
    # print(public_tweets)


@shared_task
def fetchUserData(userid,proid):
    pro = Project.objects.get(id=proid)
    pages = Pagetoken.objects.filter(user_id=userid)
    for page in pages:
        tokenurl = "https://graph.facebook.com/{0}/feed?access_token={1}".format(page.page_id,page.page_access_token)
        r = requests.get(tokenurl).json()
        pk = r        
        for post in pk['data']:
            date = post['created_time'].split('T')
            d1 = datetime.datetime.strptime(date[0],'%Y-%M-%d')
            d2 = datetime.datetime.now()
            delta = d2 - d1
            # if 1 ==1 :
            post_id = post['id']            
            tokenurl = "https://graph.facebook.com/{0}/comments?access_token={1}&fields=from,message,attachment,created_time".format(post['id'],page.page_access_token)
            r = requests.get(tokenurl).json()
            comments = r
            for com in comments['data']:
                if not com['message']:
                    pass
                else:
                    date = com['created_time'].split('T')
                    d1 = datetime.datetime.strptime(date[0],'%Y-%M-%d')
                    d2 = datetime.datetime.now()
                    delta = d2 - d1
                    print(com)
                    newcom = Comment()
                    msg = com['message'].encode('utf-8')
                    newcom._message = msg
                    newcom.source = 'fb'
                    newcom.comment_id = com['id']
                    newcom.created_at = com['created_time']                        
                    newcom.language = 'en'  
                    newcom.sentiment = getSentiment(com['message'] ,newcom.language)  
                    newcom.project = pro
                    newcom._user_name = com['from']['name'].encode('utf-8')
                    newcom.user_image = 'img'
                    newcom.user_followers = '123'
                    newcom.gender = getUserGender(com['from']['name'])
                    newcom.is_toxic = getToxic(com['message'])
                    newcom.is_intent = getIntent(com['message'])
                    newcom.is_crisis = getCrisis(com['message'],newcom.language)

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