import airtable
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin import auth
import requests
import time
import os
import sys

host = 'http://127.0.0.1:5000/api'
# Abre el fichero altasTSGC y procesa cada línea
# Initialize Firestore
cred = credentials.Certificate('thesecretgolfclub-a47120c46aa1.json')
firebase_admin.initialize_app(cred, {
    'projectId': 'thesecretgolfclub',
})
print("Procesando altasTSGC")   
with open('altasTSGC.csv', 'r') as file:
    for line in file:
        # Divide la línea en columnas usando el delimitador ';'
        nombre, liga, email, licencia = line.strip().split(';')
        
        # Aquí puedes hacer otras cosas con las variables
        print(f"nombre: {nombre}, liga: {liga}, email: {email}, licencia: {licencia}")
        email.split('@')[0]
        try:
            user = auth.create_user(
            email=email,
            email_verified=True,
            password=email.split('@')[0],
            display_name=nombre,
            photo_url='http://www.example.com/12345678/photo.png',
            disabled=False)
            print('Sucessfully created new user: {0}'.format(user.uid)+" "+nombre+"\n")
        except Exception as e:
            print('Error creating new user: '+nombre+" "+e+"\n")
            pass
        time.sleep(2)