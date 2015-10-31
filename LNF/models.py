from django.db import models
from django.utils import timezone
from django.core.files import File
from django.conf import settings
import os
import datetime

class Post(models.Model):
    lat = models.FloatField(null=True)
    long = models.FloatField(null=True)
    
    name = models.CharField(max_length=30)
    breed = models.CharField(max_length=30)
    colour = models.CharField(max_length=30)
    description = models.CharField(max_length=200, null=True, blank=True)
    
    date_created = models.DateTimeField('date posted')
    date = models.DateTimeField('date lost/found',)
    modified_date = models.DateTimeField('date last modified')

    PET_SEX_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    )
    sex = models.CharField(max_length=1, choices=PET_SEX_CHOICES, default='M')

    picture = models.ImageField(upload_to='posts', null=True, blank=True)
    PET_STATE_CHOICES = (
    ('0', 'Lost'),
    ('1', 'Found'),
    )
    state = models.CharField(max_length=1, choices=PET_STATE_CHOICES, default='0')

        # ...
    def __str__(self):              # __unicode__ on Python 2
        return self.description_text
    
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