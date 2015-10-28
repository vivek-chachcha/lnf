from django.db import models
from django.contrib.auth.models import User

class LNF_User(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=100)
    """"firstname = models.CharField(max_length=100)
    lastname  = models.CharField(max_length=100)"""

    def __unicode__(self):
	    return self.user.get_username()

""""class SavedPost
    user = models.OneToManyField(LNF_User)"""


		
			   