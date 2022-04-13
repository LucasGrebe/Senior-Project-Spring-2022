from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import Textarea

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email',)
        widgets = {
            'email' : Textarea(attrs={'cols' : 80, 'rows': 20})
        }


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)
        widgets = {
            'email' : Textarea(attrs={'cols' : 80, 'rows': 20})
        }