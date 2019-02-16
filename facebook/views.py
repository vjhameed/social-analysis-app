from django.shortcuts import redirect, reverse
from django.views.generic import FormView, TemplateView, DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from facebook.forms import FacebookLoginForm
from django.contrib import messages
from django.contrib.auth.signals import user_logged_in
from django.contrib import auth

class FacebookLoginView(FormView):
    form_class = FacebookLoginForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(FacebookLoginView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('dashboard')

    def form_valid(self, form):
        try:
            # form.clean()
            user = form.user
            auth.login(self.request, user)
            messages.success(
                self.request, 'User logged in successfully.')
            return redirect(self.get_success_url())

        except Exception as e:
            if str(e) == "facebook":
                messages.error(
                    self.request, 'Error occurred while authenticating from facebook.'
                )
            messages.error(
                self.request, 'Something went wrong.'
            )
            return self.form_invalid(self.get_form(self.form_class))
