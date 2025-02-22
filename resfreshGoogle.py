import firebase_admin
from firebase_admin import credentials

cred = credentials.RefreshToken('thesecretgolfclub-firebase-adminsdk-allna-7ff9bc89a9.json')
default_app = firebase_admin.initialize_app(cred, {'projectId': 'tsgc'})
