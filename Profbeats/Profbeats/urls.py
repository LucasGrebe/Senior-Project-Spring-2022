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
from django.contrib import admin
from django.urls import path, include
from . import views

"""Notes from
Vince: We're going to try to run most of our urls directly through this file. Features that have SUB url's can be hashed out in future meetings."""

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recommend/', views.recommend, name='recommend'),
    path('recommend_helper/', views.recommend_get, name='recommend_helper'),
    path('messager/', include('messager.urls')),
    path('', views.lander_get, name='lander_get'),

    #path('home/', INCOMPLETE PATH),
    #path('search/', INCOMPLETE PATH), #this will probably have a subpage for search/advanced, but both of them can redirect to plain old searchresults/
    #path('searchresults/', INCOMPLETE PATH),
]
