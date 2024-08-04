from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('', views.landing, name = "landing"),
    path('signup/', views.signup, name = "signup"),
    path('login/', views.loginFunc, name = "login"),
    path('logout/', views.logoutFunc, name = "logout"),
    path('dashboard/', views.dashboard, name = "dashboard"),
    path('startTimerClicked/', views.start_timer, name = "startTimerClicked"),
    path('endTimerClicked/', views.stop_timer, name = "endTimerClicked"),
    path('endTimerClicked/renderEntry/', views.renderEntry, name = "renderEntry"),
    path('add/course/', views.addCourse, name = "addCourse"),
    path('add/topic/', views.addTopic, name = "addTopic"),
    path('get/topics/', views.getTopics, name = "getTopics"),
    path('activeusers/', views.active_users, name = "active_users"),
    path('topic/<int:pk>/edit/', views.edit_topic, name='edit_topic'),
    path('course/<int:pk>/edit/', views.edit_course, name='edit_course'),
    path('edit/trackedtime/<int:pk>/', views.edit_trackedtime, name='edit_trackedtime'),
    path('profile/edit/<str:username>/', views.edit_user, name='edit_user'),
    path('entry/course/<int:pk>/', views.renderEntrybyCourse, name='renderEntrybyCourse'),
    path('entry/topic/<int:pk>/', views.renderEntrybyTopic, name='renderEntrybyTopic'),
    
    path('report/', views.reportView, name='report'),
    path('get-chart-data/', views.get_bar_chart_data, name='get_bar_chart_data'),
    path('hello-webpack/', views.helloWebpack, name='hello-webpack'),
    
    
]  + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
 
 
    #path('get_topics/<int:course_id>/', views.get_topics, name = "get_topics"),    