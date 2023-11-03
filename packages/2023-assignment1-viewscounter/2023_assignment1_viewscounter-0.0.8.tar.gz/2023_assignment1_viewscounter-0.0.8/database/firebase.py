import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


def initialize_firebase():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(script_dir, 'config.json')
    cred = credentials.Certificate(config_file_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://stassignment-swdev-default-rtdb.europe-west1.firebasedatabase.app/'
    })


def get_counter(name):
    try:
        username_ref = db.reference('users/' + name)
        return username_ref.child('counter').get()
    except Exception:
        return -1


def increment_counter(name):
    try:
        username_ref = db.reference('users/' + name)
        username_ref.child('counter').transaction(lambda current_value: current_value + 1 if current_value else 1)
        return True
    except Exception:
        return False
