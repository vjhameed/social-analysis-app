from django import forms
from accounts.models import User
class SignupForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    password1 = forms.CharField(label="Password",
        widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation",
        widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email","first_name","last_name")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        staff = super(SignupForm, self).save(commit=False)
        staff.set_password(self.cleaned_data["password1"])
        staff.is_active = True
        if commit:
            staff.save()

        return staff


class PasswordChangeForm(forms.Form):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation",
                                widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

class PasswordResetForm(forms.Form):
    email = forms.EmailField(max_length=254)

    error_messages = {
        'email_mismatch': "The user with this email does not exist",
    }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            User.objects.get(email = email)

        except User.DoesNotExist:
            raise forms.ValidationError(
                self.error_messages['email_mismatch'],
                code='email_mismatch',
            )
        return email
