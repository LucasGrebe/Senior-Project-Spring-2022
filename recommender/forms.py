from django import forms

class SearchForm(forms.Form):
    artist = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    from_year = forms.IntegerField(required=False)
    to_year = forms.IntegerField(required=False)

class ArtistForm(forms.Form):
    artist = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    song1 = forms.CharField(required=False, widget=forms.TextInput(attrs={'size': '50'}))
    song2 = forms.CharField(required=False, widget=forms.TextInput(attrs={'size': '50'}))
    song3 = forms.CharField(required=False, widget=forms.TextInput(attrs={'size': '50'}))
    song4 = forms.CharField(required=False, widget=forms.TextInput(attrs={'size': '50'}))