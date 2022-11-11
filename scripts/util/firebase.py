import firebase_admin
from firebase_admin import firestore


def get_db():
    firebase_admin.initialize_app()

    db = firestore.client()
    return db
