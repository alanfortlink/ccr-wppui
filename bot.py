#https://ccr-whatsapp.herokuapp.com/ -*- coding: utf-8 -*-

TypeToService = ["WIFI", "COMIDA", "ESTACIONAMENTO", "OUTRO1", "OUTRO1", "OUTRO1", "OUTRO1"]

from data import get_places

from flask import Flask, request
import os
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

place_template_instance = """
*%s*
%.1f Km de distância
Nota Geral %.1f %s
Preço: %s
Avaliações: %d
%s
"""

places_template = """

HEADER
%s

FOOTER

"""

def getRating(rating):
    return '⭐️' * int(rating)

def getPriceText(price):
    if price <= 2:
        return "Baixo"
    if price <= 4:
        return "Médio"
    return "Alto"

def getPrice(price):
    return '💰' * int(price) + "(" + getPriceText(price) + ")"

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    location_lat = request.values.get('Latitude', '').lower()
    location_lon = request.values.get('Longitude', '').lower()

    if incoming_msg == '' and request.json:
        incoming_msg = request.json.get('Body')
        location_lat = request.json.get('Latitude')
        location_lon = request.json.get('Longitude')

    resp = MessagingResponse()

    msg = resp.message()

    responded = False

    # Received a location
    if location_lat and location_lon:
        places = get_places(location_lat, location_lon, "0")

        items = []

        for place in places:
            services_str = "\n".join(["- " + TypeToService[int(service["type"])] for service in place['services']])
            place_str = place_template_instance % (place['name'], place['distance'], place['rating'], getRating(place['rating']), getPrice(place['price']), place['numEvaluations'], services_str)
            items.append(place_str)

        msg.body(places_template % '\n'.join(items))
        responded = True

        # return a cat pic
        # msg.media('https://cataas.com/cat')
    if not responded:
        msg.body('Olá! Envie a sua localização para consultar os pontos de parada cadastrados! Envie Ajuda para números de emergência, Para mais informações acesse: http://www.google.com.br')

    return str(resp)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
