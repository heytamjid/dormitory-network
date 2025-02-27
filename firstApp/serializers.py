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
        fields = ['startTime', 'endTime', 'course', 'topic'] # DRF Serializer also automatically converts the ISO 8601 date strings into Python datetime objects.
        extra_kwargs = { # extra_kwargs provides a way to enforce field-specific rules like making fields required, thereby enhancing the validation process on the top of the model's validation
            'startTime': {'required': True}, #Even if the underlying model might allow null values or have defaults, now the serializer will require these fields to be provided 
            'endTime': {'required': True},
            'course': {'required': True},
            'topic': {'required': True}
        }