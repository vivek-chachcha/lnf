from django.db import models

class Post(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=200)
    breed = models.CharField(max_length=200)
    date = models.DateTimeField('date published')
    sex = models.CharField(max_length=200) 
    state = models.CharField(max_length=200)
    date_created = models.DateTimeField('date created')
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)

    def __str__(self):
        return self.name