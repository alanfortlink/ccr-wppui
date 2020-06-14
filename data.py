import requests
import json

base_url = "http://ccr-service.herokuapp.com"
get_places_url = base_url + "/places"

def get_places(lat, lon, id):
    r = requests.get(get_places_url)
    places = json.loads(r.content)
    return places
