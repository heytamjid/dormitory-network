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
    #If you don't explicitly define a primary key field in your Django model, Django automatically adds an id field. This id field is typically an auto-incrementing integer field, serving as the primary key for your model's database table.
    name = models.CharField(max_length=128)
    isArchived = models.BooleanField(default = False)
    user = models.ForeignKey(myUserDB, on_delete=models.CASCADE, related_name = 'CourseUnderUser')
    
    def __str__(self):
        return self.name

class Topic(models.Model):
    name = models.CharField(max_length=128)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null =  True, related_name = 'TopicUnderCourse')
    user = models.ForeignKey(myUserDB, on_delete=models.CASCADE, related_name = 'TopicUnderUser')

    def __str__(self):
        return self.name

    
    
class TrackedTimeDB(models.Model):
    user = models.ForeignKey(myUserDB, on_delete=models.CASCADE, related_name='trackedTimeUnderUser')
    startTime = models.DateTimeField()
    endTime = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='trackedTimeUnderCourse')
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name='trackedTimeUnderTopic')
    session = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return f"Session for {self.topic.name if self.topic else 'No Topic'} ({self.startTime} to {self.endTime if self.endTime else 'ongoing'})"


    
    
    

