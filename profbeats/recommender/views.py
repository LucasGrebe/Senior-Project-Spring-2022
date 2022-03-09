from re import A
from winreg import QueryValue
from recommender.forms import SearchForm
from django.shortcuts import render
from django.http import Http404, JsonResponse
from .models import *
from .forms import *
from django.views.decorators.http import require_POST, require_GET



import random


def find_albums(artist, from_year = None, to_year = None):
    query = Musicdata.objects.filter(artists__contains = artist)
    if from_year is not None:
        query = query.filter(year__gte = from_year)
    if to_year is not None:
        query = query.filter(year__lte = to_year)
    return list(query.order_by('-popularity').values('id','name','year'))
    
def advanced_find(name, explicit, tempoMin = None, tempoMax = None, durMin = None, durMax = None ):
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


@require_POST
def searchform_post(request):
    # create a form instance and populate it with data from the request:
    form = SearchForm(request.POST)
    ##sort_form = SortForm(request.POST)
    # check whether it's valid:
    if form.is_valid():
        # process the data in form.cleaned_data as required
        from_year = None if form.cleaned_data['from_year'] == None else int(form.cleaned_data['from_year'])
        to_year = None if form.cleaned_data['to_year'] == None else int(form.cleaned_data['to_year'])
        sort = form.cleaned_data['sort']
        
        albums = find_albums(
                form.cleaned_data['artist'],
                from_year,
                to_year
            )
        
        # Random 3 of top 10 popular albums
        answer = albums
        random.shuffle(answer)
        answer = list(answer)[:7]
        
        
        if(sort != 'random' and sort != ''):
            answer = sorted(answer, key = lambda i: i[sort])
        return render(request, 'recommender/searchform.html', {'form': form, 'albums': answer })
    else:
        raise Http404('Something went wrong')


@require_GET
def searchform_get(request):
    form = SearchForm()
    return render(request, 'recommender/searchform.html', {'form': form})

@require_POST
def advanced_post(request):
     # create a form instance and populate it with data from the request:
    form = AdvancedForm(request.POST)
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
        albums = advanced_find(
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


@require_GET
def advanced_get(request):
    form = AdvancedForm()
    return render(request, 'recommender/advanced.html', {'form': form})
