import requests
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from aylienapiclient import textapi
import json
import tweepy
import xmltodict



CONSUMER_KEY = 'mqjmf3Tp4D8NGNDd5AR9dHKrT'
CONSUMER_SECRET = 'd3uPKttcEBYLPeyyrLIFRi45KzPCKcgeEMYs8kAo00gFk5egDD'


def get_api(access_token,access_secret):
	# set up and return a twitter api object
	oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	access_key = access_token
	access_secret = access_secret
	oauth.set_access_token(access_key, access_secret)
	api = tweepy.API(oauth)
	return api

def getLanguage(text):
    requrl = "http://95.216.2.224:5033/detect-language?text={}".format(text)
    resp = requests.get(requrl).json()
    return  resp['output']

def getToxic(text):
    requrl = "http://95.216.2.224:5033/toxic?comment={}".format(text)
    resp = requests.get(requrl).json()
    return resp['is_toxic'] 

def getIntent(text):
    requrl = "http://95.216.2.224:5033/intent?comment={}".format(text)
    resp = requests.get(requrl).json()
    return resp['is_intent'] 

def getCrisis(text,lang):
    if lang == 'ar' or lang=='arz' or lang=='fr':
        requrl = "http://95.216.2.224:5033/crisis?text={}&language={}".format(text,lang)
        resp = requests.get(requrl).json()
        return resp['output'] 
    else:
        return 'Not Available'


def getSentiment(text,lang):
    requrl = "http://95.216.2.224:9000/sentiment/?comment={}&format=json&lan={}".format(text,lang)
    resp = requests.get(requrl).json()    
    if lang == 'en' or lang == 'arz':
        sent = float(resp['Comment:Class'])
        if sent < 0:
            return 'Negative'
        elif sent > 0:
            return 'Positive'
        else:
            return 'Nuetral'
    else:
        return resp['Comment:Class']
    

def getUserPages(accessToken):
    pages = requests.get('https://graph.facebook.com/me/accounts?access_token='+accessToken).json()
    if pages.get('error', False):
        raise Exception('facebook')
    return pages.get('data')

def getUserGender(user_name):
    appurl = 'http://95.216.2.224:5033/gender?name={}'.format(user_name)
    pages = requests.get(appurl).json()
    if pages.get('error', False):
        raise Exception('facebook')
    return pages['gender']


def getPageDetail(id, token):
    page = requests.get(
        'https://graph.facebook.com/'+id+'?access_token=' + token+'&fields=name,access_token,category,about,bio,contact_address,description,location,website,single_line_address').json()
    if page.get('error', False):
        raise Exception('facebook')
    return page


def getPagePosts(id, token):
    page = requests.get(
        'https://graph.facebook.com/'+id+'/posts?access_token=' + token+'&fields=name,description,picture,caption').json()
    if page.get('error', False):
        raise Exception('facebook')
    return page.get('data')


def getPostComments(id, token):
    page = requests.get(
        'https://graph.facebook.com/'+id+'/comments?access_token=' + token+'&fields=from,message,attachment,created_time').json()
    if page.get('error', False):
        raise Exception('facebook')
    return page.get('data')


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )

account_activation_token = TokenGenerator()
