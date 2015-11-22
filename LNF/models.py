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
from django.core.exceptions import ValidationError

class Post(models.Model):
    lat = models.FloatField(null=True, default=None)
    lon = models.FloatField(null=True, default=None)
    address = models.CharField(max_length=50, null=True, default=None)

    author = models.CharField(max_length=200, null=True)	
    name = models.CharField(max_length=30, null=True)
    breed = models.CharField(max_length=30, null=True)
    colour = models.CharField(max_length=30, null=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    
    date_created = models.DateTimeField('date posted', null=True)
    def valid_date(value):
        if datetime.date.today() < value:
            raise ValidationError('Date is not valid.')    
    date = models.DateField('date lost/found', null=True, validators=[valid_date])
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
        if self.date_created == None:
            self.date_created = timezone.now()
        self.modified_date = timezone.now()

        if self.address != None:
            address = urllib.parse.quote_plus(self.address)
            maps_api_url = "https://maps.google.com/maps/api/geocode/json?address=%s&key=%s" % (address,"AIzaSyAHjZ8463T8-5IvzglxU4TtWx3tMxsnxnc")
            response = urllib.request.urlopen(maps_api_url)
            data = json.loads(response.read().decode('utf8'))
            self.lat = float(data['results'][0]['geometry']['location']['lat'])
            self.lon = float(data['results'][0]['geometry']['location']['lng'])
        
        super(Post,self).save(*args, **kwargs)


    def image_url(self):
        if self.picture and hasattr(self.picture, 'url'):
            return self.picture.url
        else:
            return os.path.join(settings.STATIC_URL, 'paw.png')
    def description_text(self):
        if self.description:
            return self.description
        else:
            return "No description is available for this pet."

    def __str__(self):              # __unicode__ on Python 2
        return str(self.id)
        
class BookmarkedPost(models.Model):
    post = models.ForeignKey(Post)
    date_bmed = models.DateTimeField()
    bmList = models.ForeignKey('BookmarkedPostList')
    
    def save(self, *args, **kwargs):
        self.date_bmed = timezone.now()
        super(BookmarkedPost,self).save(self, *args, **kwargs)
      
class BookmarkedPostList(models.Model):
    user = models.OneToOneField(User, editable=False)
    bmList = models.ManyToManyField(BookmarkedPost, blank=True)

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

