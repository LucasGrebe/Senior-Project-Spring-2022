from django.contrib import admin
from .models import FriendRequest, PRating, Playlist, TPR_Meta, TRating,Track,Comment, UserProfile

#Register all existing models here so we can do admin debugging and for final usability
admin.site.register(Playlist)
admin.site.register(Track)
admin.site.register(Comment)
admin.site.register(PRating)
admin.site.register(TRating)
admin.site.register(TPR_Meta)
admin.site.register(UserProfile)
admin.site.register(FriendRequest)