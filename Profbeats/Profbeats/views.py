from re import A
from .forms import *
from django.shortcuts import render,get_object_or_404
from django.http import Http404,JsonResponse
from .models import *
from django.views.decorators.http import require_POST, require_GET
import spotipy
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

def Search(name, explicit, tempoMin = None, tempoMax = None, durMin = None, durMax = None ):
    query = Musicdata.objects.filter(name__contains = name)
    print(explicit)
    if tempoMin is not None:
        query = query.filter(tempo__gte = tempoMin)
    if tempoMax is not None:
        query = query.filter(tempo__lte = tempoMax)
    if durMin is not None:
        query = query.filter(duration_ms__gte = durMin * 60000)
    if durMax is not None:
        query = query.filter(duration_ms__lte = durMax * 60000)
    if not explicit:
        query = query.filter(explicit__lte = 0)
    return list(query.order_by('-popularity').values('id','name','year', 'tempo', 'duration_ms'))


def searchForm(request):
      # create a form instance and populate it with data from the request:
    form = SearchForm(request.POST)
    ##sort_form = SortForm(request.POST)
    # check whether it's valid:
    if form.is_valid():
        # process the data in form.cleaned_data as required
        
        sort = form.cleaned_data['sort']
        tempo = form.cleaned_data['tempo']

        if(tempo == 'slow'):
            tempoMin = 20
            tempoMax = 99
        elif(tempo == 'medium'):
            tempoMin = 100
            tempoMax = 149
        elif(tempo == 'fast'):
            tempoMin = 150
            tempoMax = 250
        else:
            tempoMin = 0
            tempoMax = 500
        explicit = form.cleaned_data['explicit']
        
        durMin = form.cleaned_data['durMin'] 
        durMax = form.cleaned_data['durMax']
        albums = Search(
                form.cleaned_data['name'],
                explicit,
                tempoMin,
                tempoMax,
                durMin,
                durMax,
                
                
            )
        
        # Random 3 of top 10 popular albums
        answer = albums
        random.shuffle(answer)
        answer = list(answer)[:7]
        #x = 1/0
        
        if(sort != 'random' and sort != ''):
            answer = sorted(answer, key = lambda i: i[sort])
        return render(request, 'recommender/advanced.html', {'form': form, 'albums': answer })
    else:
        raise Http404('Something went wrong')

def createAccountForm(request):
    pass

def loginForm(request):
    form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    # Redirect to a success page.


    
def createPlaylistForm(request):
    pass

def comments(request,playlistId,userId):
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
