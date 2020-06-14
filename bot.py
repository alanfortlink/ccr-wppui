# -*- coding: utf-8 -*-

from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

place_template = """
Place: %s

"""

places_template = """
HEADER
%s
FOOTER
"""

@app.route('/bot', methods=['POST'])
def bot():
    print(request.values)
    incoming_msg = request.values.get('Body', '').lower()
    location_lat = request.values.get('Latitude', '').lower()
    location_lon = request.values.get('Longitude', '').lower()

    print(location_lat, location_lon)

    resp = MessagingResponse()

    msg = resp.message()

    responded = False

    # Received a location
    if location_lat and location_lon:
        place_template_instance = place_template % ("Posto Ipiranga RJ-112")
        msg.body(places_template % place_template_instance)
        # msg.body(" *Posto Ipiranga RJ-112* \n 8 Km de distância \n Nota Geral 3.7 \n Preço: $$ (Médio) \n Avaliações: 113 \n - WIFI \n - Estacionamento \n - Banho \n Mais detalhes: www.google.com.br \n \n \n *Posto BR* \n 11.3km Distância \n Nota Geral: 4.1 \n Preço: $ (Baixo) \n Avaliações: 17 \n - WIFI \n - Banho \n - Almoço \n Mais detalhes: www.g1.com.br")
        responded = True

        # # return a cat pic
        # msg.media('https://cataas.com/cat')
    if not responded:
        msg.body('Olá! Envie a sua localização para consultar os pontos de parada cadastrados! Envie Ajuda para números de emergência, Para mais informações acesse: http://www.google.com.br')

    return str(resp)

if __name__ == '__main__':
    app.run()
