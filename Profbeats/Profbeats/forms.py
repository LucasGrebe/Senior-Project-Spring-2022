from socket import fromshare
from xml.etree.ElementTree import Comment
from django import forms
from .models import User
# NOTE: SOME MODELS MAY NEED TO BE IMPORTED DIRECTLY

class CreateAccountForm(forms.Form):
    pass

class LoginForm(forms.Form):
    pass

class PlaylistMakeForm(forms.Form):
    pass

class SearchForm(forms.Form):
    pass

class CommentForm(forms.ModelForm):
    created_by=User
    name=User.username + str(User.id)
    body=forms.CharField(widget=forms.Textarea)
    class Meta:
        model=Comment
        fields=('name','body')

class ArtistForm(forms.Form):
    artist = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    song1 = forms.CharField(required=False, widget=forms.TextInput(attrs={'size': '50'}))
    song2 = forms.CharField(required=False, widget=forms.TextInput(attrs={'size': '50'}))
    song3 = forms.CharField(required=False, widget=forms.TextInput(attrs={'size': '50'}))
    song4 = forms.CharField(required=False, widget=forms.TextInput(attrs={'size': '50'}))