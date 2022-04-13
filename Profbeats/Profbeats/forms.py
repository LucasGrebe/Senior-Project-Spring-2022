# from socket import fromshare
from django import forms
from users.models import CustomUser as User
from .models import Comment, PRating,Playlist, TRating, Track
# NOTE: SOME MODELS MAY NEED TO BE IMPORTED DIRECTLY

class CreateAccountForm(forms.Form):
    pass

class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)
    

class TrackForm(forms.Form):
    aggRating=forms.FloatField(max_value=5.0,min_value=0.0,initial=0.0)
    class Meta:
        model=Track
        fields=('URLId','aggRating')

class PlaylistForm(forms.ModelForm):
    title="Untitled"
    #img=DEFAULT IMAGE HERE
    aggRating=forms.FloatField(max_value=5.0,min_value=0.0,initial=0.0)
    class Meta:
        model=Playlist
        fields=('title','spotify_link','img','aggRating','owner','tracks')

class PlaylistRatingForm(forms.ModelForm):
    class Meta:
        model=PRating
        fields=('rating','prated_by','target')

class TrackRatingForm(forms.ModelForm):
    class Meta:
        model=TRating
        fields=('rating','trated_by','target')

class SearchForm(forms.Form):
    pass

class CommentForm(forms.ModelForm):
    body=forms.CharField(widget=forms.Textarea)
    class Meta:
        model=Comment
        fields=('created_by','name','body')

class ArtistForm(forms.Form):
    artist = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    song1 = forms.CharField(required=False, widget=forms.TextInput(attrs={'size': '50'}))
    song2 = forms.CharField(required=False, widget=forms.TextInput(attrs={'size': '50'}))
    song3 = forms.CharField(required=False, widget=forms.TextInput(attrs={'size': '50'}))
    song4 = forms.CharField(required=False, widget=forms.TextInput(attrs={'size': '50'}))

