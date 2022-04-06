from django.shortcuts import render, redirect
from .models import *
from .forms import *

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages as djangomessages

auth_manager = SpotifyClientCredentials(client_id='96652f337059433b8015a2fc3b8922fa', client_secret='bc7324bf495b401abd4018f2a5404054')
sp = spotipy.Spotify(auth='BQBudGJkAEas3zrtctXFBRveiTFae3AIqOC', auth_manager=auth_manager)

def messages(request):
    context = {}

    # temporary
    logout(request)
    if not request.user.is_authenticated:
        user = authenticate(request, username="admin", password="admin")
        login(request, user)
    
    context['inbox'] = Message.objects.filter(recipient = request.user.get_username()).order_by('-created_at')
    if not context['inbox']:
        djangomessages.info(request, ("Your inbox is empty. Send someone a message to strike up a conversation!"))

    return render(request, 'messager/messages.html', context)

def deletemessage(request, message_id):
    message = Message.objects.get(pk=message_id)
    message.delete()
    djangomessages.success(request, ('Message deleted.'))
    return redirect('messager:messages')

def writemessage(request):
    context = {}

    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user.get_username()
            if not msg.subject:
                msg.subject = "(no subject)"
            msg.save()
            djangomessages.success(request, ("Your message was sent."))
            return redirect('messager:messages')

        else:
            print(form.errors.as_data())

    else:
        form = MessageForm()
        context['form'] = form
    return render(request, 'messager/writemessage.html', context)

def replymessage(request, recipient, subject):
    context = {'recipient' : recipient, 'subject' : 'RE: ' + subject}

    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user.get_username()
            if not msg.subject:
                msg.subject = "(no subject)"
            msg.save()
            djangomessages.success(request, ("Your message was sent."))
            return redirect('messager:messages')

        else:
            print(form.errors.as_data())

    else:
        form = MessageForm()
        context['form'] = form
    return render(request, 'messager/writemessage.html', context)
