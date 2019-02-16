from urllib.parse import urlencode
import requests
from django.conf import settings
from django.contrib.auth import get_user_model


class FacebookBackend(object):
    def __init__(self):
        if hasattr(settings, 'AUTH_USER_MODEL'):
            self.auth_model = get_user_model()
        else:
            from django.contrib.auth.models import User
            self.auth_model = User

    def authenticate(self, access_token=None, **kwargs):
        try:
            if access_token and type(access_token) is str:
                profile = requests.get('https://graph.facebook.com/me?fields=id,first_name,last_name,name,email&%s' % urlencode({'access_token': access_token})).json()
                if profile.get('error', False):
                    raise Exception('facebook')
            else:
                return None
        except Exception as e:
            print('Exception occurred while getting data from facebook, access_token: %s', access_token)
            raise Exception("facebook")
        try:
            facebook_id = profile.get('id')
            fb_user = self.auth_model.objects.get(fb_id=facebook_id)
            fb_user.fb_token = access_token
            fb_user.save()
            user = fb_user
        except self.auth_model.DoesNotExist:
            user = self._create_new_fb_user(profile, access_token)
        except Exception as e:
            return None
        return user

    def _create_new_fb_user(self, profile, token):
        facebook_id = profile.get('id')
        user = self.auth_model()
        user.fb_id = facebook_id
        user.email = profile.get('email')
        user.first_name = profile.get('first_name')
        user.last_name = profile.get('last_name')
        user.fb_image_url = 'https://graph.facebook.com/%s/picture?type=large' % facebook_id
        user.fb_token = token
        user.save()
        return user

    def get_user(self, user_id):
        try:
            return self.auth_model.objects.get(pk=user_id)
        except Exception as e:
            return None
