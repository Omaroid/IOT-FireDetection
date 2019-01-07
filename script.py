# -*- coding: utf-8 -*-

from base64 import b64encode, b64decode
from hashlib import sha256
from urllib import quote_plus, urlencode
from hmac import HMAC
import requests
import json
import os
import time

from bluetooth import *
from twilio.rest import Client

# Azure IoT Hub
URI = '**'
KEY = '**'
IOT_DEVICE_ID = '**'
POLICY = '**'

bd_addr='**'
port=1

account_sid='**'
auth_token='**'

def generate_sas_token():
    expiry=3600
    ttl = time.time() + expiry
    sign_key = "%s\n%d" % ((quote_plus(URI)), int(ttl))
    signature = b64encode(HMAC(b64decode(KEY), sign_key, sha256).digest())

    rawtoken = {
        'sr' :  URI,
        'sig': signature,
        'se' : str(int(ttl))
    }

    rawtoken['skn'] = POLICY

    return 'SharedAccessSignature ' + urlencode(rawtoken)

def send_message(token, message):
    url = 'https://{0}/devices/{1}/messages/events?api-version=2016-11-14'.format(URI, IOT_DEVICE_ID)
    headers = {"Content-Type": "application/json","Authorization": token}
    data = json.dumps(message)
    print data
    response = requests.post(url, data=data, headers=headers)

if __name__ == '__main__':

    sock = BluetoothSocket (RFCOMM)
    sock.connect((bd_addr,port))

    token = generate_sas_token()

    rec=""
    
    fire=0
    alert=0
    delai=60
    t=0

    client=Client(account_sid,auth_token)
    message1= client.messages \
        .create(
            body='Initiation du système !',
            from_='**',
            to='**'
        )
    print(message1.sid)

    while True:
        rec+=sock.recv(1024)
        rec_end=rec.find('\n')

        if rec_end != -1:
            data=rec[:rec_end]
            print(data)
            tab=data.split('#')
            print(tab)
            alert=0
            if tab[2]=='0' and fire==0:
                fire=1
                t=time.time()+delai
                alert=1
                message1 = client.messages \
                    .create(
                        body='Feu à la maison !!! (Alerte niveau 1)',
                        from_='**',
                        to='**'
                    )
                print(message1.sid)
            if tab[2]=='0' and fire==1 and time.time()>=t:
                t=time.time()+delai
                alert=1
                message1 = client.messages \
                    .create(
                        body='Feu à la maison !!! (Alerte niveau 2)',
                        from_='**',
                        to='**'
                )
                print(message1.sid)
            if tab[2]!='0' and fire==1 and time.time>=t:
                alert=0
                fire=0
                message1 = client.messages \
                    .create(                                                                                                    body='Etat du feu stabilisé',
                        from_='**',
                        to='**'
                    )
                print(message1.sid)
            message= {"fire":tab[0], "label":tab[1], "range":tab[2], "temp":tab[3], "humidity":tab[4].replace('\r',''),"alert":alert}
            print(message)
            send_message(token, message)
            rec=rec[rec_end+1:]

    sock.close()
