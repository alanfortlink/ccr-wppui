import requests
import json

base_url = "http://ccr-service.herokuapp.com"
get_places_url = base_url + "/places"

def getIcon(weather):
    cloudiness = float(weather["clouds"]["all"])

    if cloudiness <= 33:
        return "🌤️"
    if cloudiness <= 66:
        return "⛅"

    return "🌥️"

def getCelsius(kelvin):
    return float(kelvin) - 273.15

def get_places(lat, lon, id):
    r = requests.post(get_places_url, {"latitude": lat, "longitude": lon, "driverId": id}, verify=False)
    places = json.loads(r.content)
    return places

def get_weather(lat, lon):
    url = "http://api.openweathermap.org/data/2.5/weather?lat="+str(lat)+"&lon="+str(lon)+"&appid=cb58e3ec07de6c3e5f60e7dc8212cd0d"
    print(url)
    r = requests.get(url, verify=False)
    weather = json.loads(r.content)

    return "Olá, em " + weather["name"] + " a temperatura é " + "%.1f" % getCelsius(weather["main"]["temp"]) + "°C " + getIcon(weather)
