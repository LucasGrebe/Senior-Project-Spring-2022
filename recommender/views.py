from re import A
from recommender.forms import SearchForm
from django.shortcuts import render
from django.http import Http404, JsonResponse
from .models import *
from .forms import *
from django.views.decorators.http import require_POST, require_GET
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
cid = '44dbdabeed3d42eba9abf16a4159c53e'
secret = '139765ae1bb445b2abfb6799e1698072'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(auth_manager=client_credentials_manager)

def find_albums(artist, from_year = None, to_year = None):
    query = Musicdata.objects.filter(artists__contains = artist)
    if from_year is not None:
        query = query.filter(year__gte = from_year)
    if to_year is not None:
        query = query.filter(year__lte = to_year)
    return list(query.order_by('-popularity').values('id','name','year'))


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
    


    

@require_POST
def searchform_post(request):
    # create a form instance and populate it with data from the request:
    form = SearchForm(request.POST)
    # check whether it's valid:
    if form.is_valid():
        # process the data in form.cleaned_data as required
        from_year = None if form.cleaned_data['from_year'] == None else int(form.cleaned_data['from_year'])
        to_year = None if form.cleaned_data['to_year'] == None else int(form.cleaned_data['to_year'])
        albums = find_albums(
                form.cleaned_data['artist'],
                from_year,
                to_year
            )
        
        # Random 3 of top 10 popular albums
        answer = albums[:10]
        random.shuffle(answer)
        answer = list(answer)[:3] 
        return render(request, 'recommender/searchform.html', {'form': form, 'albums': answer })
    else:
        raise Http404('Something went wrong')



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


@require_GET
def searchform_get(request):
    form = SearchForm()
    return render(request, 'recommender/searchform.html', {'form': form})

