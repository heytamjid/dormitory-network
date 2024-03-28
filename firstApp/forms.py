from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *

class SignUpForm(UserCreationForm):
    class Meta:
        model = myUserDB
        fields = ['username', 'email', 'bio']

class LoginForm(AuthenticationForm):
    class Meta:
        model = myUserDB
        fields = ['username', 'password']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name']

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'course'] 
        
    def __init__(self, *args, **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)
        self.fields['course'].required = False