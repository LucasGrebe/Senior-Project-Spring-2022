from django.db import models
from django.db.models import *


# Model of a playlist and it's fields. Note this is not final and can be subject to change
# A playlist can either be NATIVE or NON-NATIVE. Native playlists need to have their tracks references stored locally, and
# non-native playlists need to have their Spotify url stored locally.
class Playlist(models.Model):
    playlistId=models.IntegerField(primary_key=True)
    nativeItem=models.BooleanField(default=True)
    title=models.CharField(max_length=30)
    spotify_link=models.URLField()          # this field is NOT REQUIRED, unless .nativeItem is FALSE! We need this so we can maintain comment databases on external playlists


# Model of a user and it's fields. Note this is not final and can be subject to change
class User(models.Model):
    id=models.IntegerField(primary_key=True)
    email=models.EmailField()
    firstName=CharField(max_length=20)      # use MaxLengthValidator(User.firstName) to validate length for account creation purposes
    lastName=CharField(max_length=20)       # as with firstName, use the validator class if validation is needed
    username=CharField(max_length=20)       # same validation method
    phoneNumber=CharField(max_length=10)    # best to use characters here, smaller than storing a 10-digit integer
    activeAccount=BooleanField(default=True)
    profilePicture=ImageField()             # this can have useful key options, whoever is on profiles please do research on how we should implement this
    bio=TextField(max_length=500)
    owned_playlists=models.ForeignKey(Playlist,on_delete=models.CASCADE,related_name='playlists',blank=True)



# Model of the track and it's fields. Note this is not final and can be subject to change
# The track list locally stores all songs that belong to user-generated playlists (necessary if we cannot link accounts directly to spotify)
class Track(models.Model):
    urlId=URLField(primary_key=True)
    playlisted_to=models.ForeignKey(Playlist,on_delete=models.CASCADE,related_name='tracks',blank=True)


# Model of the comment and it's fields. Note this is not final and can be subject to change
# When comments are generated, they are linked to a PLAYLIST. This relationship is necessary for functionality
class Comment(models.Model):
    playlist=models.ForeignKey(Playlist,on_delete=models.CASCADE,related_name='comments',blank=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name='poster',blank=True)
    name=TextField(max_length=30)
    body=TextField(max_length=250)
    created_on=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body,self.created_by.username)