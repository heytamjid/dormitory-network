from rest_framework import serializers
from .models import *

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name']

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name', 'course']

class TrackedTimeDBSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackedTimeDB
        fields = ['startTime', 'endTime', 'course', 'topic']
        extra_kwargs = {
            'startTime': {'required': True},
            'endTime': {'required': True},
            'course': {'required': True},
            'topic': {'required': True}
        }