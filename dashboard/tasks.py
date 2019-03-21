import string

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from dashboard.models import Project, Usertoken, Pagetoken, Comment
from celery import shared_task
import requests
from aylienapiclient import textapi
import json
import datetime


@shared_task
def fetchUserData(userid,proid):
    client = textapi.Client("115463a5", "d47f781359288eb4d29b6a42485247d2")
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
            tokenurl = "https://graph.facebook.com/{0}/comments?access_token={1}".format(post['id'],page.page_access_token)
            r = requests.get(tokenurl)
            comments = json.loads(r.content)
            for com in comments['data']:
                date = com['created_time'].split('T')
                d1 = datetime.datetime.strptime(date[0],'%Y-%M-%d')
                d2 = datetime.datetime.now()
                delta = d2 - d1
                # if 1 == 1 :
                lang = client.Language(com['message'])
                lang = lang['lang']
                sent = client.Sentiment(com['message'])
                sent = sent['polarity']
                newcom = Comment()
                newcom.message = com['message']
                newcom.source = 'fb'
                newcom.gender = 'male'
                newcom.comment_id = com['id']
                newcom.created_at = com['created_time']                        
                newcom.language = lang  
                newcom.sentiment = sent  
                newcom.project = pro
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