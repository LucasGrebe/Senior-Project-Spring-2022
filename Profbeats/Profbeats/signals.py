from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save

from Profbeats.Profbeats.forms import PlaylistForm
from .models import Playlist, UserProfile
User = get_user_model()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        f_playlist=PlaylistForm(None)
        new_playlist = f_playlist.save(commit=False)
        new_playlist.title="Favorites"
        new_playlist.aggRating=0.0
        new_playlist.image=None
        new_playlist.owner=instance
        new_playlist.tracks=None
        new_playlist.save()
        f2_playlist=PlaylistForm(None)
        new2_playlist = f2_playlist.save(commit=False)
        new2_playlist.title="Recents"
        new2_playlist.aggRating=0.0
        new2_playlist.image=None
        new2_playlist.owner=instance
        new2_playlist.tracks=None
        new2_playlist.save()