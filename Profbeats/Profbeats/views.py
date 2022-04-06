from re import A
from .forms import *
from django.shortcuts import render,get_object_or_404
from django.http import Http404,JsonResponse
from .models import *
from .forms import *
from django.views.decorators.http import require_POST, require_GET
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
cid = '44dbdabeed3d42eba9abf16a4159c53e'
secret = '139765ae1bb445b2abfb6799e1698072'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(auth_manager=client_credentials_manager)

def find_artists(artist, song1, song2, song3, song4):
    to_pass = 'artist,album,track,playlist,show,episode'
    results = sp.search(q='artist:' + artist, type=to_pass)
    items = results['artists']['items']
    r_tracks = sp.recommendations(seed_artists=[items[0]['id']], seed_tracks=[song1,song2,song3,song4])
    temp = r_tracks.get('tracks')
    tracks = []
    for i in range(len(temp)):
        temp2 = temp[i]
        track = temp2.get('id')
        tracks.append(track)
    return tracks

def Search(INPUTDATA):
    pass

def searchForm(request):
    pass

def createAccountForm(request):
    pass

def loginForm(request):
    pass

def createPlaylistForm(request):
    pass

def comments(request,playlistId,userId):
    pass

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
