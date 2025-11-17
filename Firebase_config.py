import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("snake-game-15694-firebase-adminsdk-fbsvc-1e3fe47bc4.json")
firebase_admin.initialize_app(cred)

db = firestore.client()