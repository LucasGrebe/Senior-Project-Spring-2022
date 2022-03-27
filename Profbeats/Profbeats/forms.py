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
    created_by=User.id
    body=forms.CharField(widget=forms.Textarea)
    class Meta:
        model=Comment
        fields=('created_by','body')