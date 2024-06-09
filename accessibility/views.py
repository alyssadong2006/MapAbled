from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from . import models
from django.db.models import F
import json
from . import forms
import accessibility
import folium
import os
from . import map3
import googlemaps
import pyperclip
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

#from django.contrib.gis.utils import GeoIP

###original map3
api_key = 'AIzaSyBH_eCUrklBvV1755CQ9qJWk8j4tLCIUSw'
Maps = googlemaps.Client(key=api_key)

m = folium.Map(location=[43.473040488968536, -80.53953064039003],
               zoom_start=17)

google_maps_tile = folium.TileLayer(
    tiles=
    f'https://mt1.google.com/vt/lyrs=r&x={{x}}&y={{y}}&z={{z}}&key={api_key}',
    attr='Google',
    name='Google Maps',
    overlay=True,
    control=True)

google_maps_tile.add_to(m)

folium.Map().add_child(
    folium.ClickForLatLng(format_str='"[" + lat + "," + lng + "]"', alert=True)
)

file_path = os.path.join("accessibility/templates/accessibility",
                         "folium_google_maps.html")

m.save(file_path)

list_of_markers = []


#coordinate forat [#,#]
def add_pin(address, name):

  api_key = 'AIzaSyBH_eCUrklBvV1755CQ9qJWk8j4tLCIUSw'
  Maps = googlemaps.Client(key=api_key)

  location = Maps.geocode(address=address)

  lat = location[0]['geometry']['location']['lat']
  lng = location[0]['geometry']['location']['lng']

  coordinates = [lat, lng]

  folium.Marker(coordinates, popup=name).add_to(m)

  file_path = os.path.join("accessibility/templates/accessibility",
                           "folium_google_maps.html")

  m.save(file_path)
  #creates a new html file with the pin on the map
  print(coordinates)
  print("ran")


#from django.contrib.gis.geoip import GeoIP
# Create your views here.
class HomeView(TemplateView):
  template_name = 'accessibility/home.html'
  model = models.Location

class MapView(TemplateView):
  # template_name = 'accessibility/folium_google_maps.html'
  template_name = 'accessibility/maps.html'
  model = models.Location


def add_facility(request):
  if request.method == 'POST':

    locationForm = forms.LocationForm(request.POST)
    commentForm = forms.CommentForm(request.POST)

    #adding pin to the google maps
    location = request.POST.get('geo_info')
    name = request.POST.get('name')
    description = request.POST.get('description')
    accessibility_rating = request.POST.get('accessibility_ratings')
    tags = request.POST.get('tags')

    formatText = ""
    counter = 0
    for letters in str(description):
      counter += 1
      if counter == 100:
        formatText += '\n'
        formatText += letters
        counter = 0
      else:
        formatText += letters
    string = str(location) + '\n'+ str(name) + '\n' + '\n'+ str(formatText)
    add_pin(location, string)
    #add_pin(location, name)

    # locations = models.Location.objects.all()
    # for location in locations:
    #   map3.add_pin(location.geo_info, location.name)

    #adding instance to database
    if locationForm.is_valid() and commentForm.is_valid():
      locationForm.save()
      commentForm.save()
      return redirect('home')
  else:
    locationForm = forms.LocationForm()
    commentForm = forms.CommentForm()
  return render(request,
                'accessibility/locationForm.html',
                context={
                    'locationForm': locationForm,
                    'commentForm': commentForm
                })


#like/dislike
def like_comment(request):
  data = json.loads(request.body)
  print(data)
  id = data["id"]
  comment = models.Comment.objects.get(id=id)
  comment.likes = F('likes') + 1
  comment.save()
  return render(request, 'WHEREEVER THE ICON/BUTTON IS')


def dislike_comment(request):
  data = json.loads(request.body)
  print(data)
  id = data["id"]
  comment = models.Comment.objects.get(id=id)
  comment.dislikes = F('dislikes') + 1
  comment.save()
  return render(request, 'blog/post_detail.html')


def search(request):
  locations = models.Location.objects.all()
  return render(request, 'accessibility/search.html', {"locations": locations})

def sendData(request):
  data = json.load(request.body)
  print(data)

from django.http import JsonResponse


from django.shortcuts import render, redirect
from django.http import HttpResponseNotAllowed
from . import models  # Make sure to import your models properly

from django.shortcuts import render, redirect
from django.http import HttpResponseNotAllowed
from . import models  # Ensure correct import of your models

def receive_location(request):
    if request.method == 'GET':
        print("GET request received")
        location_name = request.GET.get('location')
        print("Location Name:", location_name)
        if location_name:
            try:
                # Query the database for the location
                location = models.Location.objects.get(name=location_name)
                print("Location found:", location)
                # Get related comments or any other data associated with the location
                comments = models.Comment.objects.filter(location=location)  # Assuming there's a ForeignKey from Comment to Location
                print("Comments found:", comments)
                # Render the search results template with the location and related data
                return render(request, 'accessibility/search_results.html', {'location': location, 'comments': comments})
            except models.Location.DoesNotExist:
                print("Location not found in database")
                # Handle the case where the location does not exist in the database
                return render(request, 'accessibility/search_results.html', {'error': 'Location not found'})
        else:
            print("No location provided in the query parameters")
            return render(request, 'accessibility/search_results.html', {'error': 'No location provided'})
    else:
        print("Non-GET request received")
        # Handle non-GET requests
        return HttpResponseNotAllowed(['GET'])
