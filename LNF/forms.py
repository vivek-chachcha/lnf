from django import forms
from django.db import models
from django.utils import timezone
from django.core.files import File
from django.conf import settings
from .models import Post

class PostForm(forms.ModelForm):
    #picture = forms.ImageField(required=False)
    #date = forms.DateTimeField(required=False)
    
    class Meta:
        model = Post
        fields = ['name', 'state', 'date', 'colour', 'breed', 'sex', 'description', 'picture']
    
    #post = forms.CharField(label='description', max_length=100)
   