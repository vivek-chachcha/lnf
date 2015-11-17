from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.forms import Textarea, TextInput
from django.db import models
from django.utils import timezone
from django.core.files import File
from django.conf import settings
from .models import Post
from django.core.exceptions import ValidationError
import json
import urllib.parse
import urllib.request
from urllib.request import urlopen

class UserCreateForm(UserCreationForm):
    alphabets_only = RegexValidator(r'^[a-zA-Z]*$', 'Only English letters are allowed.')
    firstname = forms.CharField(label=(u'First Name'), required=True, validators=[alphabets_only])
    lastname  = forms.CharField(label=(u'Last Name'), required=True, validators=[alphabets_only])
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

class LoginForm(forms.Form):
    username        = forms.CharField(label=(u'Username'))
    password        = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))

class BookmarkForm(forms.Form):
    bookmark        = forms.BooleanField(label=(u'Bookmark Post'),required=False)

class PostForm(forms.ModelForm):
    
    def valid_address(value):
        address = urllib.parse.quote_plus(value)
        maps_api_url = "https://maps.google.com/maps/api/geocode/json?address=%s&key=%s" % (address,"AIzaSyAHjZ8463T8-5IvzglxU4TtWx3tMxsnxnc")
        response = urllib.request.urlopen(maps_api_url)
        data = json.loads(response.read().decode('utf8'))
        if data['status'] != 'OK':
            raise ValidationError('Address is not valid.')    
        if not ((49.261226-1 <= float(data['results'][0]['geometry']['location']['lat']) <= 49.261226+1) | (-123.1139268-1 <= float(data['results'][0]['geometry']['location']['lng']) <= -123.1139268+1)):
            raise ValidationError('Address is not valid.')    
            
    address = forms.CharField(label=(u'Address'), required=False, validators=[valid_address], widget=TextInput(attrs={'size': 25}))            
    class Meta:
        model = Post
        fields = ('name', 'state', 'date', 'colour', 'breed', 'sex', 'description', 'picture')
        labels = {
            'date': 'Date (mm/dd/yy)'
                 }
        widgets = {
            'name': TextInput(attrs={'size': 25}),
            'date': TextInput(attrs={'size': 25}),
            'colour': TextInput(attrs={'size': 25}), 
            'breed': TextInput(attrs={'size': 25}),
            'description': Textarea(attrs={'cols': 27, 'rows': 10}),
        }
        
