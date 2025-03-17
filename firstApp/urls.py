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
    path('endTimerClicked/', views.stop_timer_old, name = "endTimerClicked"),
    path('endTimerClicked/renderEntry/', views.renderEntry, name = "renderEntry"),
    path('add/course/', views.addCourse, name = "addCourse"),
    path('add/topic/', views.addTopic, name = "addTopic"),
    path('get/topics/', views.getTopics, name = "getTopics"),
    path('activeusers/', views.active_users, name = "active_users"),
    path('topic/<int:pk>/edit/', views.edit_topic, name='edit_topic'),
    path('course/<int:pk>/edit/', views.edit_course, name='edit_course'),
    path('edit/trackedtime/<int:pk>/', views.edit_trackedtime, name='edit_trackedtime'),
    path('profile/<str:user_id>/', views.user_profile, name='user_profile'),

    path('profile/edit/<str:username>/', views.edit_user, name='edit_user'),
    path('entry/course/<int:pk>/', views.renderEntrybyCourse, name='renderEntrybyCourse'),
    path('entry/topic/<int:pk>/', views.renderEntrybyTopic, name='renderEntrybyTopic'),
    
    path('report/', views.reportView, name='report'),
    path('get-chart-data/', views.get_bar_chart_data, name='get_bar_chart_data'),
    path('hello-webpack/', views.helloWebpack, name='hello-webpack'),
    
    #after the integration 
    
    path('api/courses/', views.CourseListView.as_view(), name='course-list'),
    path('api/topics/', views.TopicListView.as_view(), name='topic-list'),
    path('api/courses/<int:course_id>/topics/', views.TopicListView.as_view(), name='course-topics'),
    path('api/create/tracked-time/', views.TrackedTimeDBCreateView.as_view(), name='tracked-time-create'),

    path('api/start-timer/', views.start_timer, name='start_timer'),
    path('api/stop-timer/', views.stop_timer, name='stop_timer'),
    path('api/get-active-timer/', views.get_active_timer, name='get_active_timer'),
    
    #path('api-token-auth/', views.obtain_auth_token),
    
    
]  + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
 
 
    #path('get_topics/<int:course_id>/', views.get_topics, name = "get_topics"),    