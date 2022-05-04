from .forms import *
from django.shortcuts import render,redirect
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from .models import *
from django.views.decorators.http import require_POST, require_GET
import spotipy
from django.contrib import messages as djangomessages

from django.contrib.auth import logout
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import random
from spotipy import oauth2
cid = '44dbdabeed3d42eba9abf16a4159c53e'
secret = '139765ae1bb445b2abfb6799e1698072'
client_credentials_manager = oauth2.SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

spOAuth = oauth2.SpotifyOAuth(client_id=cid, client_secret=secret, redirect_uri='http://127.0.0.1:8000/')

def find_artists(artist, song1, song2, song3, song4):
    to_pass = 'artist,album,track,playlist,show,episode'
    results = sp.search(q='artist:' + artist, type=to_pass)
    items = results['artists']['items']
    r_tracks = sp.recommendations(seed_artists=[items[0]['id']], seed_tracks=[song1,song2,song3,song4], seed_genres=['rock'])
    temp = r_tracks.get('tracks')
    tracks = []
    for i in range(len(temp)):
        temp2 = temp[i]
        track = temp2.get('id')
        tracks.append(track)
    return tracks

def find_tracks(songs):
    r_tracks = sp.recommendations(limit=100, seed_tracks=songs)
    temp = r_tracks.get('tracks')
    tracks = []
    for i in range(len(temp)):
        temp2 = temp[i]
        track = temp2.get('id')
        tracks.append(track)
    return tracks

def createAccount(request):
    pass

def loginForm(request):
    form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    # Redirect to a success page.

def createPlaylist(request):
    f_playlist = PlaylistForm(request)
    new_playlist = f_playlist.save(commit=False)
    new_playlist.title="Untitled"
    new_playlist.aggRating=0.0
    new_playlist.image=None
    new_playlist.owner=request.user
    new_playlist.tracks=None
    new_playlist.save()
    return HttpResponseRedirect(request.path_info)

def addToPlaylist(request):
    if request.method == 'POST':
        f_TPR = AddToPlaylistForm(request.POST)
        new_TPR = None
        if f_TPR.is_valid():
            new_TPR=f_TPR.save(commit=False)
            new_TPR.save()
        else:
            raise Http404('Cannot add the same song to a playlist twice')
    return HttpResponseRedirect(request.path_info)

def updatePlaylist(request):
    pass

### Universal Handler Function for the playlistContent.html webpage ###
def updatePlaylistContent(request,playlistId):
    playlist=Playlist.objects.get(pk=playlistId)
    f_comment = CommentForm(None)
    f_prate = PlaylistRatingForm(None)
    f_trate = TrackRatingForm(None)

    if request.method == 'POST':
        if 'post_comment' in request.POST:
            f_comment = CommentForm(request.POST)
            new_comment=None
            if f_comment.is_valid():
                new_comment=f_comment.save(commit=False)
                new_comment.playlist=playlist
                new_comment.save()
            else:
                raise Http404('Comment Failed to Post')
        if 'rate_playlist' in request.POST:
            f_prate = PlaylistRatingForm(request.POST)
            if f_prate.is_valid():
                f_prate.save()
        if 'rate_track' in request.POST:
            f_trate = TrackRatingForm(request.POST)
            if f_trate.is_valid():
                f_trate.save()

    ### REFERENCE KEY FOR FRONTEND VARIABLES ###
    ### You can access ALL FIELDS of playlist using playlist.fieldname in .html! ###
    context = {
        'f_comment':f_comment,
        'f_prate':f_prate,
        'f_trate':f_trate,
        'content':playlist.tracks.all(),
        'comments':playlist.comments.all(),
        'playlist':playlist,
    }
    return render(request,'playlistContent.html',context)


@require_POST
def recommend(request):
    form = ArtistForm(request.POST)
    if form.is_valid():
        song1 = None if form.cleaned_data['song1'] == None else form.cleaned_data['song1']
        song2 = None if form.cleaned_data['song2'] == None else form.cleaned_data['song2']
        song3 = None if form.cleaned_data['song3'] == None else form.cleaned_data['song3']
        song4 = None if form.cleaned_data['song4'] == None else form.cleaned_data['song4']
        tracks = find_artists(form.cleaned_data['artist'], song1, song2, song3, song4)
        return render(request, 'recommender/searchformRecommendations.html', {'form': form, 'tracks':tracks })
    else:
        raise Http404('Something went wrong')

@require_GET
def recommend_get(request):
    form = ArtistForm()
    return render(request, 'recommender/searchformRecommendations.html', {'form': form})

def lander_get(request):
    tracksall = []
    recently_listened_to = ['7CMVo848b9LsUtVavIoiXC', '5tUfJOqyiROxClednTF2FC', '7AYSl3u70hJ402o0u0gry5', '3jgHOTLHVfPI7twjEobWcC']
    tracks = find_tracks(recently_listened_to)
    for i in range(0, 1000, 4):
        tracksall.append(tracks[i:i+4])
    return render(request, 'lander.html', {'tracksall': tracksall, 'recently_listened_to': recently_listened_to})

def profile(request):
    # You need to be logged in to view your profile.
    # Redirect to the login page if the user is not logged in.
    if not request.user.is_authenticated:
        djangomessages.warning(request, ("You need to be logged in to view your profile."))
        return redirect('login')

    context = {}
    form = FriendRequestForm()
    if request.method == 'POST':
        form = FriendRequestForm(request.POST)
        if form.is_valid():
            formrecipient = form.cleaned_data['recipient']
            if User.objects.filter(email=formrecipient).exists():
                if request.user.get_username() != formrecipient:
                    recipient = User.objects.get(email = formrecipient)
                    if recipient not in request.user.profile.friendList.all():
                        if not FriendRequest.objects.filter(sender=request.user, recipient=recipient).exists():
                            fr = FriendRequest(sender=request.user, recipient=recipient)
                            fr.save()
                            djangomessages.success(request, ("Your friend request was sent."))
                        else:
                            djangomessages.warning(request, ("You've already sent a friend request to that user."))
                    else:
                        djangomessages.warning(request, ("You're already friends with that user."))
                else:
                    djangomessages.warning(request, ("You can't send a friend request to yourself."))
            else:
                djangomessages.warning(request, ("Couldn't find that user to send a friend request to."))

        else:
            print(form.errors.as_data())

    context['form'] = form
    context['friend_request_list'] = FriendRequest.objects.filter(recipient=request.user)
    return render(request, 'profile.html', context)

def messageFriend(request, friendId):
    friend = User.objects.get(pk=friendId)
    recipient = friend.get_username()
    return redirect('/messager/writemessage/' + recipient)

def deleteFriend(request, friendId):
    friend = User.objects.get(pk=friendId)
    request.user.profile.friendList.remove(friend)
    friend.profile.friendList.remove(request.user)
    djangomessages.success(request, ('Friend deleted.'))
    return redirect('profile')

def acceptFriendRequest(request, FRId):
    fr = FriendRequest.objects.get(pk=FRId)
    sender = fr.sender
    sender.profile.friendList.add(request.user)
    request.user.profile.friendList.add(sender)
    fr.delete()
    djangomessages.success(request, ('Friend request accepted.'))
    return redirect('profile')

def denyFriendRequest(request, FRId):
    fr = FriendRequest.objects.get(pk=FRId)
    fr.delete()
    djangomessages.success(request, ('Friend request denied.'))
    return redirect('profile')