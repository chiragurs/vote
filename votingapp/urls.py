from django.urls import path
app_name="votingapp"
from votingapp import views
urlpatterns=[
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('vote/',views.vote,name="vote"),
]