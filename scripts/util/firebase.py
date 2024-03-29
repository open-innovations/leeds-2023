import firebase_admin
from firebase_admin import firestore
import pandas as pd


firebase_admin.initialize_app()


def get_db():
    db = firestore.client()
    return db


def pull_collection(collection_name, fields):
    db = get_db()
    ballot_ref = db.collection(collection_name)
    docs = ballot_ref.select(fields).stream()
    return pd.DataFrame([doc.to_dict() for doc in docs])
