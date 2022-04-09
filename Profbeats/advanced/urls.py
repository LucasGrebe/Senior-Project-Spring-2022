from django.urls import path
from . import views

#app_name = 'recommender'

urlpatterns = [
    
    path('', views.advanced_get, name='advanced'),
    path('/results/', views.advanced_post, name='results'),

]
 