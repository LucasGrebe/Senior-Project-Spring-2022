from django.contrib import admin
from .models import PRating, Playlist, TRating,Track,Comment

#Register all existing models here so we can do admin debugging and for final usability
admin.site.register(Playlist)
admin.site.register(Track)
admin.site.register(Comment)
admin.site.register(PRating)
admin.site.register(TRating)