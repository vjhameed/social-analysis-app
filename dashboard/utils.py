import requests
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


def getUserPages(accessToken):
    pages = requests.get('https://graph.facebook.com/me/accounts?access_token='+accessToken+'&fields=id,name,category,cover,single_line_address,access_token').json()
    if pages.get('error', False):
        raise Exception('facebook')
    return pages.get('data')


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
