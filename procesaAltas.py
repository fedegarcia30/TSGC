import requests
import time
import os
import sys
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin import auth


# Initialize Firestore
cred = credentials.Certificate('thesecretgolfclub-a47120c46aa1.json')
firebase_admin.initialize_app(cred, {
    'projectId': 'thesecretgolfclub',
})

host = 'http://127.0.0.1:5000/api'
# Abre el fichero altasTSGC y procesa cada línea
print("Procesando altasTSGC")   
with open('altasTSGC.csv', 'r') as file:
    for line in file:
        # Divide la línea en columnas usando el delimitador ';'
        nombre, liga, email, licencia = line.strip().split(';')
        
        # Aquí puedes hacer otras cosas con las variables
        print(f"nombre: {nombre}, liga: {liga}, email: {email}, licencia: {licencia}")
        response = requests.get(f'http://127.0.0.1:5000/api/handicap?licencia={licencia}')
        if response.status_code == 200:
            hcp = response.json().get('handicap', None)
            print(f"Handicap de {nombre}: {hcp}")
            response = requests.get(f'http://127.0.0.1:5000/api/NuevoUsuarioHandicap?licencia={licencia}&nombre={nombre}&email={email}') 
            time.sleep(2)
            print(response)
            if response.status_code == 200:
                response = requests.get(f'http://127.0.0.1:5000/api/creaJugadorConfiguracion?email={email}&liga={liga}&nombre={nombre}&licencia={licencia}&hcp={hcp}')
                time.sleep(5)
                print(f"{nombre} Configurado en Jugadores")
                if response.status_code == 200:
                    print(f"Configuración de {nombre} realizada en liga {liga}")
                    response = requests.get(f'http://127.0.0.1:5000/api/creaJugadorEnLiga?email={email}&nombre={nombre}&liga={liga}&hcp={hcp}')
                    if response.status_code == 200:
                        try:
                            user = auth.create_user(
                            email=email,
                            email_verified=True,
                            password=email.split('@')[0],
                            display_name=nombre,
                            photo_url='http://www.example.com/12345678/photo.png',
                            disabled=False)
                            print('Sucessfully created new user:'+" "+nombre+"\n")
                        except Exception as e:
                            print('EError al dar de alta mail: '+nombre+"\n")
                            pass
                    else:
                        print(f"Error al crear jugador en liga: {response}")
                else:
                    print(f"Error al crear usuario de configuracion {liga}: {response}")
            else:
                print(f"Error al crear tarjetas Handicap: {response}")
        else:
            print(f"Error al obtener handicap: {response}")
        time.sleep(1)
print("Proceso de altas TSGC finalizado")
