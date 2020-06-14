#https://ccr-whatsapp.herokuapp.com/ -*- coding: utf-8 -*-

from data import get_places

from flask import Flask, request
import os
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

place_template_instance = """
Place: *%s*\\n
"""

places_template = """
\\n
HEADER\\n
%s\\n
FOOTER\\n
"""

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', request.json.get('Body', '')).lower()
    location_lat = request.values.get('Latitude', request.json.get('Latitude', '')).lower()
    location_lon = request.values.get('Longitude', request.json.get('Longitude', '')).lower()

    resp = MessagingResponse()

    msg = resp.message()

    responded = False

    # Received a location
    if location_lat and location_lon:
        places = get_places(location_lat, location_lon, "0")

        items = []

        for place in places:
            items.append(place_template_instance % (place['name']))

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
