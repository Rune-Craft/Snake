import firebase_admin
from firebase_admin import credentials, firestore
import os

# Try to load service account from file or environment variable
service_account_path = os.getenv('FIREBASE_SERVICE_ACCOUNT_PATH', 'snake-game-15694-firebase-adminsdk-fbsvc-1e3fe47bc4.json')

if os.path.exists(service_account_path):
    # Admin access with service account (for you)
    cred = credentials.Certificate(service_account_path)
    firebase_admin.initialize_app(cred)
else:
    # Anonymous/limited access for other users
    # They will need to set up Firestore security rules to allow public read/write
    firebase_admin.initialize_app(options={
        'projectId': 'snake-game-15694'
    })

db = firestore.client()