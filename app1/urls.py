
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('schedule/', views.schedule, name='schedule'),
    path('communication/', views.communication, name='communication'),
    path('management/', views.management, name='management'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('performance/', views.performance, name='performance'),
]
