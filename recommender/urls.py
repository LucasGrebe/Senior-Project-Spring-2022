from django.urls import path
from . import views

app_name = 'recommender'

urlpatterns = [
    path('best/', views.searchform_get, name='best'),
    path('bestp/', views.searchform_post, name='bestp'),
    path('recommend/', views.recommend, name='recommend'),
    path('recommend_helper/', views.recommend_get, name='recommend_helper'),
]
 