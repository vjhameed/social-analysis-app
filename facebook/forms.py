from django import forms
from django.contrib import auth
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class FacebookLoginForm(forms.Form):
    access_token = forms.CharField(required=True)

    def clean(self):
        try:
            access_token = self.cleaned_data.get('access_token')

            if not access_token:
                raise ValidationError(_('Invalid Access Token.'))

            user = auth.authenticate(access_token)

            if user is not None:
                if not user.is_active:
                    raise ValidationError('Your account is inactive, please contact support.')
            else:
                raise ValidationError('Invalid token.')
            if user and user.id:
                self.user = user
        except ValidationError as e:
            raise ValidationError(e)
        except Exception as e:
            raise Exception(e)

        return super(FacebookLoginForm, self).clean()