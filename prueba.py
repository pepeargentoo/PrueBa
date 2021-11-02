import json
import requests
import random 
from flask import Flask

app = Flask(__name__)

api = 'https://rickandmortyapi.com/api'
@app.route("/")
def infochapter():
    info = requests.get(api)
    return info.json()