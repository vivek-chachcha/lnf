from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['name', 'state', 'colour', 'breed', 'sex', 'state', 'description', 'date', 'picture']
    
    #post = forms.CharField(label='description', max_length=100)
   