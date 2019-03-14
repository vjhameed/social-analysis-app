from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.contrib.auth import logout
from accounts.forms import SignupForm, PasswordResetForm, PasswordChangeForm
from accounts.models import User
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.views.generic import FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from dashboard.utils import account_activation_token
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import auth

import os


# Create your views here.
class ManualLoginView(LoginView):
    template_name = "accounts/login.html"

    def __init__(self, **kwargs):
        super(LoginView,self).__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super(ManualLoginView, self).get_context_data(**kwargs)
        context['facebook_app_id'] = os.environ.get('FACEBOOK_APP_ID', '188312881935144')
        return context

    def get_success_url(self, fallback_url=None, **kwargs):
        try:
            fallback_url = reverse('dashboard')
            return fallback_url

        except Exception as e:
            pass


class SignUpView(generic.CreateView):
    template_name = 'accounts/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('login')

    def __init__(self, *args, **kwargs):
        super(SignUpView, self).__init__(*args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True
        user.save()

        current_site = get_current_site(self.request)
        mail_subject = 'Activate your account.'
        message = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode("utf-8"),
            'token': account_activation_token.make_token(user),
        })
        # to_email = form.cleaned_data.get('email')
        # email = EmailMessage(
        #     mail_subject, message, to=[to_email]
        # )
        # email.send()

        messages.success(
            self.request, 'Please confirm your email address to complete the registration')
        return redirect(self.success_url)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, 'Thank you for your email confirmation. Now you can login your account.')
    else:
        messages.error(
            request, 'Activation link is invalid!')
    url = reverse("login")
    return redirect(url, args=(), kwargs={})


class ResetView(FormView):
    template_name = 'accounts/reset.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('login')

    def __init__(self, *args, **kwargs):
        super(ResetView, self).__init__(*args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = User.objects.get(email=email)
        current_site = get_current_site(self.request)
        mail_subject = 'Reset your password.'
        message = render_to_string('reset_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode("utf-8"),
            'token': account_activation_token.make_token(user),
        })
        to_email = email
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        messages.success(
            self.request, 'Please confirm your email address to complete the reset process.')
        return redirect(self.success_url)


class ChangePasswordView(FormView):
    template_name = 'accounts/change_password.html'
    form_class = PasswordChangeForm

    def __init__(self, *args, **kwargs):
        super(ChangePasswordView, self).__init__(*args, **kwargs)

    def form_valid(self, form):
        # implement pass change logic here
        password = form.cleaned_data.get('password1')
        if self.request.user.is_authenticated:
            user = self.request.user
            url = reverse('dashboard')
            user.set_password(password)
            user.save()
            user.backend = 'accounts.backends.ManualSignupBackend'
            auth.login(self.request, user)
        else:
            pk = self.request.session['user_id']
            user = User.objects.get(id=pk)
            url = reverse('login')
            user.set_password(password)
            user.save()

        messages.success(
            self.request, 'Password changed successfully.')
        return redirect(url)


def reset_confirm(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        request.session['user_id'] = user.pk
        url = reverse("change-password")
    else:
        messages.error(
            request, 'Reset link is invalid!')
        url = reverse("login")
    return redirect(url, args=(), kwargs={})


def Logout(request):
    logout(request)
    url = reverse("login")
    return redirect(url, args=(),kwargs={})


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
