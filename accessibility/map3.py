import folium
import googlemaps

api_key = 'AIzaSyBH_eCUrklBvV1755CQ9qJWk8j4tLCIUSw'
Maps = googlemaps.Client(key=api_key)


m = folium.Map(location=[43.473040488968536, -
               80.53953064039003], zoom_start=17)


google_maps_tile = folium.TileLayer(
    tiles=f'https://mt1.google.com/vt/lyrs=r&x={{x}}&y={{y}}&z={{z}}&key={api_key}',
    attr='Google',
    name='Google Maps',
    overlay=True,
    control=True
)

google_maps_tile.add_to(m)

# location = input("name an address ")
# address = Maps.geocode(address=location)
# lat = address[0]['geometry']['location']['lat']
# lng = address[0]['geometry']['location']['lng']

# coordinates = [lat, lng]


# folium.Marker(coordinates, popup="inline implicit popup").add_to(m)

m.save('folium_google_maps.html')



#coordinate forat [#,#]
def add_pin(address,name):

    api_key = 'AIzaSyBH_eCUrklBvV1755CQ9qJWk8j4tLCIUSw'
    Maps = googlemaps.Client(key=api_key)

    location = Maps.geocode(address = address)

    lat = location[0]['geometry']['location']['lat']
    lng = location[0]['geometry']['location']['lng']
    
    coordinates = [lat,lng]
    
    folium.Marker(coordinates, popup=name).add_to(m)

    m.save('folium_google_maps.html')
    #creates a new html file with the pin on the map
    print(coordinates)
    print("ran")
    
    
    
    
    
