from django.urls import path
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', auth_views.login, name='login'),
    path('logout', auth_views.logout, name='logout'),
    url(r'readArticle/$', views.readArticle, name='readArticle'),
    path('sendComment', views.sendComment, name='sendComment'),
    path('submit_article', views.submitArticle, name='submit_article'),
    path('editProfile', views.editProfile, name='editProfile'),
]