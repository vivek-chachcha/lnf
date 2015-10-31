from django import forms
from django.forms import Textarea, TextInput
from django.db import models
from django.utils import timezone
from django.core.files import File
from django.conf import settings
from .models import Post

class PostForm(forms.ModelForm):
        
    class Meta:
        model = Post
        fields = ('name', 'state', 'date', 'colour', 'breed', 'sex', 'description', 'picture')
        widgets = {
            'name': TextInput(attrs={'size': 25}),
            'date': TextInput(attrs={'size': 25}),
            'colour': TextInput(attrs={'size': 25}), 
            'breed': TextInput(attrs={'size': 25}),
            'description': Textarea(attrs={'cols': 27, 'rows': 10}),
        }
       