
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('schedule/', views.schedule, name='schedule'),
    path('communication/', views.communication, name='communication'),
    path('management/', views.management, name='management'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signupplayer/', views.signup_player, name='signup_player'),
    path('signupmanager/', views.signup_manager, name='signup_manager'),
    path('performance/', views.performance, name='performance'),
    path('myuser/', views.myuser, name="myuser"),
    path('changepassword/', views.change_password, name="changepassword"),
    path('deleteaccount/', views.delete_account, name="deleteaccount"),
    path('forgotpassword/', views.forgot_password, name="forgotpassword"),
    path('add_team/', views.add_team, name='add_team'),

]