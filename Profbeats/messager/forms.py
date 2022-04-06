from django import forms
from .models import Message

# Create your forms here.

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'text', 'track_id']