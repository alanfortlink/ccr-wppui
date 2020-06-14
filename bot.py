from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/bot', methods=['POST'])

def bot():
    incoming_msg = request.values.get('Body', '').lower()
    location_lat = request.values.get('Latitude', '').lower()
    location_lon = request.values.get('Longitude', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if location_lat and location_lon:
        msg.body(" *Posto Ipiranga RJ-112* \n 8 Km de distância \n Nota Geral 3.7 \n Preço: $$ (Médio) \n Avaliações: 113 \n - WIFI \n - Estacionamento \n - Banho \n Mais detalhes: www.google.com.br \n \n \n *Posto BR* \n 11.3km Distância \n Nota Geral: 4.1 \n Preço: $ (Baixo) \n Avaliações: 17 \n - WIFI \n - Banho \n - Almoço \n Mais detalhes: www.g1.com.br")
        responded = True
    if 'cat' in incoming_msg:
        # return a cat pic
        msg.media('https://cataas.com/cat')
        responded = True
    if not responded:
        msg.body('Olá! Envie a sua localização para consultar os pontos de parada cadastrados! Envie Ajuda para números de emergência, Para mais informações acesse: http://www.google.com.br')
    return str(resp)



if __name__ == '__main__':
    app.run()
