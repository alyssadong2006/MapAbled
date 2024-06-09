from django import forms
from django.db.models import fields
from .models import Accessibility, Location, Comment

types = [('Ramps', 'Ramps'), ('Parking', 'Parking'),
         ('Washrooms', 'Washrooms'), ('Restrooms', 'Restrooms'),
         ('Braille', 'Braille'), ('Elevators', 'Elevators'),
         ('Seating', 'Seating')]


class AccessibilityForm(forms.ModelForm):
    #type of accessibility, used as tags in comments
    class Meta:
        model = Accessibility
        fields = ['feature']


class LocationForm(forms.ModelForm):
    #address of location
    class Meta:
        model = Location
        fields = ['geo_info', 'name']
        labels = {'geo_info':'Address'}


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['description', 'accessibility_rating', 'tags']

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if len(tags) > 1:
            raise forms.ValidationError("You can only select one tag.")
        return tags

class SearchForm(forms.Form):
    query = forms.CharField(max_length=500)