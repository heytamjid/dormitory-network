from django.urls import path
from . import views



urlpatterns = [
    path('', views.landing, name = "landing"),
    path('signup/', views.signup, name = "signup"),
    path('login/', views.loginFunc, name = "login"),
    path('logout/', views.logoutFunc, name = "logout"),
    path('dashboard/', views.dashboard, name = "dashboard"),
    path('startTimerClicked/', views.start_timer, name = "startTimerClicked"),
    path('endTimerClicked/', views.stop_timer, name = "endTimerClicked"),

    
]
