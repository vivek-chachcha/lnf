from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserCreateForm(UserCreationForm):
    firstname = forms.CharField(label=(u'First Name'), required=True)
    lastname  = forms.CharField(label=(u'Last Name'), required=True)
    email     = forms.EmailField(label=(u'Email Address'), required=True) #EmailField will check if the input email is a valid one
    user_agreement = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')  

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["firstname"]
        user.last_name = self.cleaned_data["lastname"]
        if commit:
            user.save()
        return user

    """
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username = username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("The Username has already existed.") #raise an error if input userID has already existed

    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['password_verify']:
            raise forms.ValidationError("Passwords do not match. Please try again.") #raise an error if passwords did not match
        return self.cleaned_data
    """

class LoginForm(forms.Form):
    username        = forms.CharField(label=(u'Username'))
    password        = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))
