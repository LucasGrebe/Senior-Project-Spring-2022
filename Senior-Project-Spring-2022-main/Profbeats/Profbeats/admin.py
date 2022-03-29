from django.contrib import admin
from .models import Playlist,User,Track,Comment

#Register all existing models here so we can do admin debugging and for final usability
admin.site.register(Playlist)
admin.site.register(User)
admin.site.register(Track)
admin.site.register(Comment)