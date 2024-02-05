from django.db import models
from django.contrib.auth.models import AbstractUser
from timezone_field import TimeZoneField


# Create your models here.

class myUserDB (AbstractUser):
    username = models.CharField(max_length = 32, unique = True, primary_key = True )
    #institution = models.TextField(blank = True, null = True)
    bio = models.TextField(blank=True, null=True)
    # interests = will create interest DB
    timezone = TimeZoneField(default='Asia/Dhaka', null = True) 
    
    def __str__(self):
        return self.username 
    
    
    
class TrackedTimeDB (models.Model):

    user = models.ForeignKey(myUserDB, on_delete=models.CASCADE, related_name='usersTime')
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    duration = models.DurationField()
    

    
    
    

