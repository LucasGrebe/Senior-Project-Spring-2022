from django.urls import path
from . import views

#app_name = 'recommender'

urlpatterns = [
    path('best/', views.searchform_get, name='best'),
    path('bestp/', views.searchform_post, name='bestp'),
    path('advanced/', views.advanced_get, name='advanced'),
    path('advancedp/', views.advanced_post, name='advancedp'),

]
 