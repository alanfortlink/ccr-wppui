import requests
import json

base_url = "http://ccr-service.herokuapp.com"
base_url = "http://localhost:5100"
get_places_url = base_url + "/places"

def get_places(lat, lon, id):
    r = requests.post(get_places_url, {"latitude": lat, "longitude": lon, "driverId": id})
    places = json.loads(r.content)
    return places
