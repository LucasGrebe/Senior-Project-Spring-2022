from django import forms

SORT_CRITERIA = [
        ('name', 'Name'),
        ('year', 'Release Date'),
        ('random', 'Random'),
    ]

TEMPO_CRITERIA = [
        ('select', 'Select'),
        ('slow', 'Slow'),
        ('medium', 'Medium'),
        ('fast', 'Fast'),

    ]
"""

TEMPO_CRITERIA = [
        ((20, 69), 'Slow'),
        ((70, 109), 'Medium'),
        ((110, 180), 'High'),

    ]
Filtering

Find songs by:
	Year
	Artist
	Genre
	
	

Sort by:
	Alphabetical (A to Z)
	Release Year (Newest First)
	Artist (Alphabetical, A to Z)

"""

class SearchForm(forms.Form):
    artist = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    from_year = forms.IntegerField(required=False)
    to_year = forms.IntegerField(required=False)
    sort = forms.CharField(required=False,label='Sort', widget=forms.Select(choices=SORT_CRITERIA))

class AdvancedForm(forms.Form):
    sort = forms.CharField(required=False,label='Sort', widget=forms.Select(choices=SORT_CRITERIA))
    #genre = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    tempo = forms.CharField(required=False,label='Tempo', widget=forms.Select(choices=TEMPO_CRITERIA))
    name = forms.CharField(required=False,widget=forms.TextInput(attrs={'size': '50'}))
    durMin = forms.FloatField(required=False, min_value=0)
    durMax = forms.FloatField(required=False, min_value=1)
    explicit = forms.BooleanField(required=False)