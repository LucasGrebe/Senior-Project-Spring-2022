from django.db import models
from django.db.models import *
from users.models import CustomUser as User


# Model of the track and it's fields. Note this is not final and can be subject to change
# The track list locally stores all songs that belong to user-generated playlists (necessary if we cannot link accounts directly to spotify)
class Track(Model):
    id=CharField(max_length=50,primary_key=True)
    aggRating=FloatField()


# Model of a playlist and it's fields. Note this is not final and can be subject to change
# A playlist without a spotify-link is a NATIVE playlist. Many TRACKS can be used by many PLAYLISTS. Many RATINGS can belong to SINGLE playlists
class Playlist(Model):
    title=CharField(max_length=30)
    spotify_link=URLField(blank=True,null=True)
    img=ImageField()
    aggRating=FloatField()
    owner=ForeignKey(User,on_delete=CASCADE,related_name='playlists',blank=True,null=True)
    tracks=ManyToManyField(Track,related_name='tracks',blank=True)


# compute aggRating on save: aggRating = aggRating + (val-aggRating)/count(Obj.XRate)
# The following child ratings have modified save methods, they AUTOMATICALLY UPDATE the aggregated average rating of their parent Track or Playlist when created.

class PRating(Model):
    RATINGS=[(1,'ONE'),(2,'TWO'),(3,'THREE'),(4,'FOUR'),(5,'FIVE')]
    rating=PositiveSmallIntegerField(choices=RATINGS)
    prated_by=ManyToManyField(User,related_name='prater')
    target=ForeignKey(Playlist,on_delete=CASCADE,related_name='pratings',blank=True)

    def save(self, *args, **kwargs):
        super(PRating, self).save(*args, **kwargs)
        agg = self.target.aggRating
        rCount = self.target.pratings.count()
        self.target.aggRating = agg + (self.rating - agg)/rCount
        self.target.save()

class TRating(Model):
    RATINGS=[(1,'ONE'),(2,'TWO'),(3,'THREE'),(4,'FOUR'),(5,'FIVE')]
    rating=PositiveSmallIntegerField(choices=RATINGS)
    trated_by=ManyToManyField(User,related_name='trater')
    target=ForeignKey(Track,on_delete=CASCADE,related_name='tratings',blank=True)

    def save(self, *args, **kwargs):
        super(TRating, self).save(*args, **kwargs)
        agg = self.target.aggRating
        rCount = self.target.tratings.count()
        self.target.aggRating = agg + (self.rating - agg)/rCount
        self.target.save()


# Model of the comment and it's fields. Note this is not final and can be subject to change
# When comments are generated, they are linked to a PLAYLIST. This relationship is necessary for functionality
class Comment(Model):
    playlist=ForeignKey(Playlist,on_delete=CASCADE,related_name='comments',blank=True)
    created_by=ForeignKey(User,on_delete=CASCADE,related_name='poster',blank=True)
    name=TextField(max_length=30)
    body=TextField(max_length=250)
    created_on=DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body,self.created_by.username)