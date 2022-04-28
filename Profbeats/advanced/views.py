from Profbeats.forms import PlaylistForm
from advanced.forms import AdvancedForm
from django.shortcuts import render
from django.http import Http404, JsonResponse
from Profbeats.models import *
from .forms import *
from django.views.decorators.http import require_POST, require_GET

from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import random
from spotipy import oauth2
cid = 'e6b4976d09b1435288d2f2f6814ac2c3'
secret = 'b68c3747cf384432886d7781987f34e6'
client_credentials_manager = oauth2.SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

spOAuth = oauth2.SpotifyOAuth(client_id=cid, client_secret=secret, redirect_uri='http://127.0.0.1:8000/')


    
def find_spotipy(artist):
    to_pass = 'artist,album,track,playlist,show,episode'
    results = sp.search(q='artist:' + artist, type=to_pass)
    return results



def advanced_find(owner, title):

    if(len(owner) != 0):
        
        try: 
            results = User.objects.get(email=owner)
            print(type(results.playlists.all()))
            results = results.playlists.all()
        except:
            print(owner, " not found")
            return None

        if(len(title) != 0):
            print(type(results))
            try: 
                results = results.filter(title=title)
                
            except:
                print("Noothing found")
                return None
        return results
    
    else:
        if(len(title) != 0):
        
            try: 
                results = Playlist.objects.filter(title=title)
                
            except:
                print("Noothing found")
                return None
        return results
    return None
@require_POST
def advanced_post(request):
     # create a form instance and populate it with data from the request:
    form = AdvancedForm(request.POST)
    ##sort_form = SortForm(request.POST)
    # check whether it's valid:
   

    if form.is_valid():
        owner = form.cleaned_data['owner']
        title = form.cleaned_data['title']
        answer = advanced_find(
            owner,
            title
    )
        playlists = {}
        if(answer is not None):
            for playlist in answer:
                playlists[playlist] = list(playlist.tracks.all())
        
        
        return render(request, 'advanced/advanced.html', {'form': form, 'playlists': playlists})
    else:
        answer = 3
        raise Http404('Form was invalid')


@require_GET
def advanced_get(request):
    form = AdvancedForm()
    return render(request, 'advanced/advanced.html', {'form': form})

