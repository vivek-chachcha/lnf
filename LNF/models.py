from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files import File
from django.conf import settings
import os
import datetime
from PIL import Image


class Post(models.Model):
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)

    author = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=30, null=True)
    breed = models.CharField(max_length=30, null=True)
    colour = models.CharField(max_length=30, null=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    
    date_created = models.DateTimeField('date posted', null=True)
    date = models.DateField('date lost/found', null=True)
    modified_date = models.DateTimeField('date last modified')

    PET_SEX_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('M/N', 'Male Neutered'),
    ('F/S', 'Female Spayed'),
    ('X', 'Unknown'),
    )
    sex = models.CharField(max_length=3, choices=PET_SEX_CHOICES, default='M')

    picture = models.ImageField(upload_to='posts', null=True, blank=True)
    PET_STATE_CHOICES = (
    ('0', 'Lost'),
    ('1', 'Found'),
    )
    state = models.CharField(max_length=1, choices=PET_STATE_CHOICES, default='0')

    def save(self, *args, **kwargs):
        self.date_created = timezone.now()
        self.modified_date = timezone.now()
        super(Post,self).save(self, *args, **kwargs)
    def image_url(self):
        if self.picture and hasattr(self.picture, 'url'):
            return self.picture.url
        else:
            return os.path.join(settings.MEDIA_URL, 'paw.png')
    def description_text(self):
        if self.description:
            return self.description
        else:
            return "No description is available this pet."

    def __str__(self):              # __unicode__ on Python 2
        return self.name

    class Meta:
        unique_together = ["name", "breed", "colour", "description", "sex", "state", "date"]
		
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    author = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_known_location = models.CharField(max_length=200, null=True, blank=True)
    photo = models.ImageField(upload_to='comments', null=True, blank=True)
    text = models.TextField()

    def __str__(self):              
        return self.text

    def save(self, *args, **kwargs):
        super(Comment,self).save(self, *args, **kwargs)
		
    def image_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
