from functools import cached_property
from django.db import models
from django.db.models import *
from users.models import CustomUser as User


# Model of the track and it's fields. Note this is not final and can be subject to change
# The track list locally stores all songs that belong to user-generated playlists (necessary if we cannot link accounts directly to spotify)
class Track(models.Model):
    id=CharField(max_length=50,primary_key=True)
    aggRating=FloatField()


# Model of a playlist and it's fields. Note this is not final and can be subject to change
# A playlist without a spotify-link is a NATIVE playlist. Many TRACKS can be used by many PLAYLISTS. Many RATINGS can belong to SINGLE playlists
class Playlist(models.Model):
    title=CharField(max_length=30)
    spotify_link=URLField(blank=True,null=True)
    img=ImageField()
    aggRating=FloatField()
    owner=ForeignKey(User,on_delete=CASCADE,related_name='playlists',blank=True,null=True)
    tracks=ManyToManyField(Track,through='TPR_Meta',related_name='tracks',blank=True)


# compute aggRating on save: aggRating = aggRating + (val-aggRating)/count(Obj.XRate)
# The following child ratings have modified save methods, they AUTOMATICALLY UPDATE the aggregated average rating of their parent Track or Playlist when created.

class PRating(Model):
    RATINGS=[(1,'ONE'),(2,'TWO'),(3,'THREE'),(4,'FOUR'),(5,'FIVE')]
    rating=PositiveSmallIntegerField(choices=RATINGS)
    prated_by=ForeignKey(User,on_delete=PROTECT,related_name='prater',blank=True)
    target=ForeignKey(Playlist,on_delete=CASCADE,related_name='pratings',blank=True)

    class Meta:
        unique_together=[['prated_by','target']]

    def save(self, *args, **kwargs):
        super(PRating, self).save(*args, **kwargs)
        agg = self.target.aggRating
        rCount = self.target.pratings.count()
        self.target.aggRating = agg + (self.rating - agg)/rCount
        self.target.save()

class TRating(Model):
    RATINGS=[(1,'ONE'),(2,'TWO'),(3,'THREE'),(4,'FOUR'),(5,'FIVE')]
    rating=PositiveSmallIntegerField(choices=RATINGS)
    trated_by=ForeignKey(User,on_delete=PROTECT,related_name='trater',blank=True)
    target=ForeignKey(Track,on_delete=CASCADE,related_name='tratings',blank=True)

    class Meta:
        unique_together=[['trated_by','target']]

    def save(self, *args, **kwargs):
        super(TRating, self).save(*args, **kwargs)
        agg = self.target.aggRating
        rCount = self.target.tratings.count()
        self.target.aggRating = agg + (self.rating - agg)/rCount
        self.target.save()


# Models the advanced user profile settings and features, holds a list of all previous ratings through the rating relational classes
class UserProfile(Model):
    user=OneToOneField(User,on_delete=CASCADE,related_name='profile')

    THEMES=[('light','LIGHT'),('dark','DARK')]
    themeChoice=CharField(max_length=10,choices=THEMES,blank=True,null=True)
    friendList=ManyToManyField(User,related_name='friends',blank=True)
    favorites=OneToOneField(Playlist,on_delete=CASCADE,related_name='favorites',blank=True)
    recents=OneToOneField(Playlist,on_delete=CASCADE,related_name='recents',blank=True)


# Meta class representing the relationship between tracks and playlists. (T)rack-(P)laylist-(R)elationship Meta class
# Each TPR_Meta represents the relationship between a track and a playlist, and features the time it was added to the list.
class TPR_Meta(Model):
    track=ForeignKey(Track,on_delete=CASCADE,related_name='relatedPlaylists')
    playlist=ForeignKey(Playlist,on_delete=CASCADE,related_name='relatedTracks')
    added_on=DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=[['track','playlist']]


# Model of the comment and it's fields. Note this is not final and can be subject to change
# When comments are generated, they are linked to a PLAYLIST. This relationship is necessary for functionality
class Comment(Model):
    playlist=ForeignKey(Playlist,on_delete=CASCADE,related_name='comments',blank=True)
    created_by=ForeignKey(User,on_delete=CASCADE,related_name='poster',blank=True)
    name=TextField(max_length=30,blank=True)
    body=TextField(max_length=250)
    created_on=DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body,self.created_by.username)

class FriendRequest(models.Model):
    sender=ForeignKey(User,related_name='sender',on_delete=CASCADE)
    recipient=ForeignKey(User,related_name='recipient',on_delete=CASCADE)

# class Musicdata(models.Model):
#     acousticness = models.FloatField()
#     artists = models.TextField()
#     danceability = models.FloatField()
#     duration_ms = models.FloatField()
#     energy = models.FloatField()
#     explicit = models.FloatField()
#     id = models.TextField(primary_key=True)
#     instrumentalness = models.FloatField()
#     key = models.FloatField()
#     liveness = models.FloatField()
#     loudness = models.FloatField()
#     mode = models.FloatField()
#     name = models.TextField()
#     popularity = models.FloatField()
#     release_date = models.IntegerField()
#     speechiness = models.FloatField()
#     tempo = models.FloatField()
#     valence = models.FloatField()
#     year = models.IntegerField()
