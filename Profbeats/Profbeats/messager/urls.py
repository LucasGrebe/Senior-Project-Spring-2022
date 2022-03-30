from django.urls import path
from . import views

app_name = 'messager'

urlpatterns = [
    path('messages/', views.messages, name='messages'),
    path('deletemessage/<message_id>', views.deletemessage, name='deletemessage'),
    path('writemessage/', views.writemessage, name='writemessage'),
    path('replymessage/<recipient>/<subject>/', views.replymessage, name='replymessage'),
]
 