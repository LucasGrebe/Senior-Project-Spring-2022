"""Profbeats URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from re import template
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
"""Notes from
Vince: We're going to try to run most of our urls directly through this file. Features that have SUB url's can be hashed out in future meetings."""

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recommend/', views.recommend, name='recommend'),
    path('recommend_helper/', views.recommend_get, name='recommend_helper'),
    path('messager/', include('messager.urls')),
    path('search/', include('advanced.urls')),
    path('', views.lander_get, name='lander_get'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='lander.html'), name='logout'),
    path('playlistContent/<playlistId>',views.updatePlaylistContent,name='content_display'),
    path('playlist/createPlaylist/',views.createPlaylist,name='create_playlist'),
    path('recent/<track>/',views.recent,name='recent'),
    path('profile/', views.profile, name='profile'),
    path('profile/messagefriend/<friendId>', views.messageFriend,name='message_friend'),
    path('profile/deletefriend/<friendId>', views.deleteFriend,name='delete_friend'),
    path('profile/accept/<FRId>', views.acceptFriendRequest,name='accept_friend_request'),
    path('profile/deny/<FRId>', views.denyFriendRequest,name='deny_friend_request'),

    #path('home/', INCOMPLETE PATH),
    #path('search/', INCOMPLETE PATH), #this will probably have a subpage for search/advanced, but both of them can redirect to plain old searchresults/
    #path('searchresults/', INCOMPLETE PATH),
]
