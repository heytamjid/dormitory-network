from django.db import models
from django.contrib.auth.models import AbstractUser
from timezone_field import TimeZoneField



class myUserDB (AbstractUser):
    username = models.CharField(max_length = 32, unique = True, primary_key = True )
    #institution = models.TextField(blank = True, null = True)
    bio = models.TextField(blank=True, null=True)
    # interests = will create interest DB
    timezone = TimeZoneField(default='Asia/Dhaka', null = True) 
    
    def __str__(self):
        return self.username 


class Course(models.Model):
    name = models.CharField(max_length=100)
    isArchived = models.BooleanField(default = False)
    user = models.ForeignKey(myUserDB, on_delete=models.CASCADE, related_name = 'Course2myUserDBRelatedName')

    def __str__(self):
        return self.name

class Topic(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null =  True, related_name = 'Topic2CourseRelatedName')
    user = models.ForeignKey(myUserDB, on_delete=models.CASCADE, related_name = 'Topic2myUserDBRelatedName')

    def __str__(self):
        return self.name

    
    
class TrackedTimeDB (models.Model):

    user = models.ForeignKey(myUserDB, on_delete=models.CASCADE, related_name='usersTime')
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    duration = models.DurationField()
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null = True, default = None, related_name = 'TrackedTimeRelatedName' )
    session = models.CharField(max_length=900, null = True, default = None)
    
    def __str__(self):
        return f"Session for {self.topic.name} ({self.start_time} to {self.end_time})"
    


    
    
    

