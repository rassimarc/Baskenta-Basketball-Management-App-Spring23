
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
    path('signupcoach/', views.signup_coach, name='signup_coach'),
    path('signupmanager/', views.signup_manager, name='signup_manager'),
    path('performance/', views.performance, name='performance'),
    path('myuser/', views.myuser, name="myuser"),
    path('changepassword/', views.change_password, name="changepassword"),
    path('deleteaccount/', views.delete_account, name="deleteaccount"),
    path('forgotpassword/', views.forgot_password, name="forgotpassword"),
    path('add_team/', views.add_team, name='add_team'),
   # path('edit_team/<int:pk>/', views.edit_team, name='edit_team'),
   # path('update_team/<int:pk>/', views.update_team, name='update_team'),
    path('delete_team/<str:team_name>/', views.delete_team, name='delete_team'),
    path('update_team/<str:team_name>/', views.update_team, name='update_team'),
]