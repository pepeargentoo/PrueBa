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

@app.route('/<filtro>')
def getcharacter(filtro):
    print(filtro)
    if(filtro == "character" or filtro == "location" or filtro == "episodes"):
        url = api+'/'+filtro
        character = requests.get(url)
        return character.json()
    return json.dumps({'code':400,'status':'upss'})

