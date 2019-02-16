from django.contrib.auth import authenticate, login, get_user_model
from django.conf import settings
from django.http import HttpResponseRedirect
from django.http.response import Http404

User = get_user_model()


class ManualSignupBackend(object):

    def __init__(self):

        if hasattr(settings, 'AUTH_USER_MODEL'):
            self.auth_model = get_user_model()
        else:
            from django.contrib.auth.models import User
            self.auth_model = User

    def authenticate(self, request, **credentials):

        username = credentials["username"]
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'email': username}
        try:
            user = User.objects.get(**kwargs)
        except (User.DoesNotExist, KeyError):
            return None
        else:
            try:
                if user.check_password(credentials["password"]):
                    return user
            except KeyError:
                return None

    def get_user(self, user_id):

        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def custom_backend(request, backend, uid, *args, **kwargs):

    if backend.name == 'custom':
        try:
            details = kwargs['details']
            authenticated_user = authenticate(userid=request.user.id, uid=uid, details=details)
            login(request, authenticated_user)
            return HttpResponseRedirect('/')
        except Exception as exception:
            print (exception)
            raise exception
    raise Http404