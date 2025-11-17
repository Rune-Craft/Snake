import firebase_admin
from firebase_admin import credentials, firestore
import os

# Try to load service account from file
service_account_path = 'snake-game-15694-firebase-adminsdk-fbsvc-1e3fe47bc4.json'

if os.path.exists(service_account_path):
    # Admin access with service account (for you)
    cred = credentials.Certificate(service_account_path)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    USE_ADMIN_SDK = True
else:
    # For other users, we'll use REST API instead
    db = None
    USE_ADMIN_SDK = False
    FIREBASE_PROJECT_ID = 'snake-game-15694'