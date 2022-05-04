from email.policy import default
from django import forms
from Profbeats.models import Comment, PRating,Playlist, TRating, Track
from users.models import CustomUser as User

SORT_CRITERIA = [
        ('name', 'Name'),
        ('year', 'Release Date'),
        ('random', 'Random'),
    ]

TEMPO_CRITERIA = [
        ('select', 'Select'),
        ('slow', 'Slow'),
        ('medium', 'Medium'),
        ('fast', 'Fast'),

    ]
"""

TEMPO_CRITERIA = [
        ((20, 69), 'Slow'),
        ((70, 109), 'Medium'),
        ((110, 180), 'High'),

    ]
Filtering

Find songs by:
	Year
	Artist
	Genre
	
	

Sort by:
	Alphabetical (A to Z)
	Release Year (Newest First)
	Artist (Alphabetical, A to Z)

"""

class AdvancedForm(forms.Form):
    owner=forms.EmailField(required=False,widget=forms.TextInput(attrs={'size': '50'}))
    title=forms.CharField(required=False,widget=forms.TextInput(attrs={'size': '50'}))
    #img=DEFAULT IMAGE HERE
    aggRating=forms.FloatField(required=False, max_value=5.0,min_value=0.0,initial=0.0)
    class Meta:
        model=Playlist
        fields=('title','spotify_link','img','aggRating','owner','tracks')

class OmniSearchForm(forms.Form):
    searchfield=forms.CharField(required=True,widget=forms.TextInput(attrs={'size': '50'}))
    
class AdvancedSongForm(forms.Form):
    sort = forms.CharField(required=False,label='Sort', widget=forms.Select(choices=SORT_CRITERIA))
    #genre = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    tempo = forms.CharField(required=False,label='Tempo', widget=forms.Select(choices=TEMPO_CRITERIA))
    name = forms.CharField(required=False,widget=forms.TextInput(attrs={'size': '50'}))
    durMin = forms.FloatField(required=False, min_value=0)
    durMax = forms.FloatField(required=False, min_value=1)
    explicit = forms.BooleanField(required=False)

    artist = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    from_year = forms.IntegerField(required=False)
    to_year = forms.IntegerField(required=False)