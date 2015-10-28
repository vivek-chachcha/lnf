from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from LNF.models import LNF_User

class SignUpForm(ModelForm):
    username  = forms.CharField(label=(u'Username'))
    email     = forms.EmailField(label=(u'Email Address')) #EmailField will check if the input email is a valid one
    password  = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False)) #hash password
    password_verify = forms.CharField(label=(u'Verify Password'), widget=forms.PasswordInput(render_value=False))
    user_agreement = forms.BooleanField()

    class Meta:
        model = LNF_User
        exclude = ('user',)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username = username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("The Username has already existed.") #raise an error if input userID has already existed

    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['password_verify']:
            raise forms.ValidationError("Password verification failed. Please try again.") #raise an error if passwords did not match
        return self.cleaned_data

class LoginForm(forms.Form):
    username        = forms.CharField(label=(u'Username'))
    password        = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))