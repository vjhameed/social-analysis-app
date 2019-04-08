from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
        # return self.create_user(email, password, is_staff=False, is_superuser=False, is_active=True,
        # **extra_fields)


def create_superuser(self, email, password=None, **extra_fields):
    return self.create_user(email, password, is_staff=True, is_superuser=True, is_active=True,
                            **extra_fields)


def create_business_user(self, email, password=None, **extra_fields):
    return self.create_user(email, password, is_staff=False, is_superuser=False, is_active=True,
                            **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('First name'), max_length=255, blank=True, null=True, )
    last_name = models.CharField(_('Last name'), max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True, verbose_name=_('email'))

    fb_id = models.CharField(max_length=40, blank=True, null=True)
    fb_image_url = models.TextField(verbose_name=_("Facebook Profile Picture"), blank=True, null=True,
                                    default='default_profile_pic.png')
    fb_token = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __unicode__(self):
        if self.full_name:
            return self.full_name
        else:
            return self.email

    @property
    def full_name(self):
        user_full_name = ""
        if self.first_name:
            user_full_name = self.first_name
        if self.last_name:
            user_full_name = user_full_name + ' ' + self.last_name
        return user_full_name.capitalize()


    @property
    def profile_image(self):
        if self.fb_image_url:
            if self.fb_image_url.startswith('http://') or self.fb_image_url.startswith('https://'):
                return self.fb_image_url
            else:
                return settings.SITE_URL + settings.MEDIA_URL + self.fb_image_url

    @property
    def group(self):
        try:
            return self.groups.all()[0].name
        except:
            return None

    def user_data(self, request=None, group=False):
        user_data = {'id': self.id, 'full_name': self.full_name, 'first_name': self.first_name,
                     'last_name': self.last_name, 'email': self.email, 'fb_id': self.fb_id
                     }

        if request and self.fb_image_url:
            if self.fb_image_url.startswith('http://') or self.fb_image_url.startswith('https://'):
                user_data['profile_image'] = self.fb_image_url
            else:
                user_data['profile_image'] = request.scheme + '://' + request.get_host() + settings.MEDIA_URL + self.fb_image_url
        else:
            user_data['profile_image'] = self.fb_image_url

        if group:
            user_data['group'] = self.group

        user_data['fb_image_url'] = user_data['profile_image']
        return user_data

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return self.full_name


class Folder(models.Model):
    user = models.ForeignKey(User, related_name='user_folders', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
