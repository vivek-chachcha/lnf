from django import forms
from django.forms import Textarea
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
            'description': Textarea(attrs={'cols': 25, 'rows': 20}),
        }   