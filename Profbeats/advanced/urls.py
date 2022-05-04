from django.urls import path
from . import views

#app_name = 'advanced'

urlpatterns = [
    
    path('advanced_search/', views.advanced_get, name='advsearch'),
    path('advanced_results/', views.advanced_post, name='results'),
    path('search_results/', views.omni_get, name='omniresults'),
    
]
 