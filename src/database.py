import firebase_admin, os

from firebase_admin import credentials

if not os.path.exists("data/firebase.json"):
    exit("firebase.json not found, please run setup.py")

cred = credentials.Certificate("data/firebase.json")
firebase_admin.initialize_app(cred)
