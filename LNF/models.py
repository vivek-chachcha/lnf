from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files import File
from django.conf import settings
import os
import datetime
import json
import urllib.parse
import urllib.request
from urllib.request import urlopen

class Post(models.Model):
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)
    
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

    def save(self, address_input, *args, **kwargs):
        self.date_created = timezone.now()
        self.modified_date = timezone.now()
        
        address = urllib.parse.quote_plus(address_input)
        maps_api_url = "https://maps.google.com/maps/api/geocode/json?address=%s&key=%s" % (address,"AIzaSyAHjZ8463T8-5IvzglxU4TtWx3tMxsnxnc")
        response = urllib.request.urlopen(maps_api_url)
        data = json.loads(response.read().decode('utf8'))
        if address_input != '':
            self.lat = float(data['results'][0]['geometry']['location']['lat'])
            self.lon = float(data['results'][0]['geometry']['location']['lng'])
        
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
