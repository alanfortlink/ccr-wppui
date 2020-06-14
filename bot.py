# -*- coding: utf-8 -*-

TypeToService = ["", "Wifi", "Banho", "Comida", "Estacionamento", "Pernoite", "Borracharia", "Atendimento Médico"]
TypeToIcon = ["", "📡", "🚿", "🍲", "🅿️", "🛏️", "🛠️", "🏥"]

from data import get_places, get_weather

from flask import Flask, request
import os
import requests
import random
from twilio.twiml.messaging_response import MessagingResponse

calls = 0

app = Flask(__name__)

place_template_instance = """
**%s**
%.1f Km de distância
Nota Geral %.1f %s
Preço: %s
Avaliações: %d
%s
"""

places_template = """
%s 
Aqui estão algumas opções que conseguimos encontrar:
%s

Para mais detalhes e outras opções, acesse https://www.caminhoneirozap.com.br?id=469827346-ae-28374-121365fe
"""

def getRandomMessage():
    messages = [
        'https://scontent-lhr8-1.xx.fbcdn.net/v/t1.0-9/102919628_3218256124892835_456269927930658816_n.png?_nc_cat=111&_nc_sid=8024bb&_nc_ohc=d0iedhVnvRIAX9NBRub&_nc_ht=scontent-lhr8-1.xx&_nc_rmd=260&_nc_log=1&oh=40f6ef5a5a3df9fc801faea44cfcca0e&oe=5F0D0B34',
        'https://scontent-lht6-1.xx.fbcdn.net/v/t1.0-9/p960x960/91544282_3062610210457428_6616723309369229312_o.png?_nc_cat=106&_nc_sid=2d5d41&_nc_ohc=aaPmf4FnSGUAX_RqEHg&_nc_ht=scontent-lht6-1.xx&_nc_rmd=260&_nc_log=1&oh=e0edcd068732402e3d08a82a5ad0f32a&oe=5F0D46A2',
        'https://www.rm.co.mz/rm.co.mz/media/k2/items/cache/e3547aa5163be1cf0308beec1632f77e_XL.jpg'
    ]

    index = random.randint(0, len(messages) - 1)
    return index == len(messages) - 1, messages[index]

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

    outro = 0

    add_extra = False

    global calls
    calls += 1
    if calls == 3:
        calls = 0

        isLast, media = getRandomMessage()
        add_extra = isLast
        msg.media(media)

    # Received a location
    if location_lat and location_lon:
        places = get_places(location_lat, location_lon, "0")

        items = []

        for place in places:
            services_str = "\n".join([TypeToIcon[int(service["type"])] + " " + TypeToService[int(service["type"])] for service in place['services']])
            place_str = place_template_instance % (place['name'], place['distance'], place['rating'], getRating(place['rating']), getPrice(place['price']), place['numEvaluations'], services_str)
            items.append(place_str)

        body = ""
        body += places_template % (get_weather(location_lat, location_lon, add_extra), '\n'.join(items))
        msg.body(body)
        responded = True

    if not responded:
        msg.body('Oi, Sou o Caminhoneiro Zap. Me envie sua localização que eu vejo os melhores pontos de parada próximos a você.')
        msg.media('https://www.infocompu.com.br/infocom/wp-content/uploads/2018/01/Localizacao-WhatsApp01.jpg')

    return str(resp)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
