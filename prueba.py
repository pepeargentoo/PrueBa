import json
import requests
import random 
from flask import Flask,request,jsonify,Response,send_file
import io
import time
import zipfile
import hashlib


app = Flask(__name__)
api = 'https://rickandmortyapi.com/api'
@app.route("/", methods =['POST'])
def infochapter(**datos):
    datos = request.form
    info = requests.get(api).json()
    p = json.dumps(info)
    h = hash(p)
  
    if len(datos) > 0:
        if "zip" in datos:
            info = json.dumps(info,indent = 4)
            with open("tmp.json", "w") as outfile:
                outfile.write(info)
            createzip()
            FILEPATH = r"tmp.json"
            fileobj = io.BytesIO()
            with zipfile.ZipFile(fileobj, 'w') as zip_file:
                zip_info = zipfile.ZipInfo(FILEPATH)
                zip_info.date_time = time.localtime(time.time())[:6]
                zip_info.compress_type = zipfile.ZIP_DEFLATED
                with open(FILEPATH, 'rb') as fd:
                    zip_file.writestr(zip_info, fd.read())
            fileobj.seek(0)
            return Response(fileobj.getvalue(),
                    mimetype='application/zip',
                    headers={'Content-Disposition': 'attachment;filename=tmp.zip'}) 
    else:
        return json.dumps({'code':200,'data':info,'hash':h})
        #return info

@app.route('/<filtro>',methods =['POST'])
def getcharacter(filtro):
    datos = request.form
    if(filtro == "character" or filtro == "location" or filtro == "episode"):
        url = api+'/'+filtro
        character = requests.get(url).json()
        p = json.dumps(character)
        h = hash(p)
        if len(datos) > 0:
            if "zip" in datos:
                info = json.dumps(character,indent = 4)
                with open("tmp.json", "w") as outfile:
                    outfile.write(info)
                createzip()
                FILEPATH = r"tmp.json"
                fileobj = io.BytesIO()
                with zipfile.ZipFile(fileobj, 'w') as zip_file:
                    zip_info = zipfile.ZipInfo(FILEPATH)
                    zip_info.date_time = time.localtime(time.time())[:6]
                    zip_info.compress_type = zipfile.ZIP_DEFLATED
                    with open(FILEPATH, 'rb') as fd:
                        zip_file.writestr(zip_info, fd.read())
                fileobj.seek(0)
                return Response(fileobj.getvalue(),
                    mimetype='application/zip',
                    headers={'Content-Disposition': 'attachment;filename=tmp.zip'}) 
        return json.dumps({'code':200,'data':character,'hash':h})
    return json.dumps({'code':400,'status':'upss'})

@app.route('/verifico',methods =['POST'])
def verifico():
    datos = request.form
    if "prevurl" not in datos:
        return json.dumps({'code':400,'status':'la prevurl es requerida'})

    if "hash" not in datos:
        return json.dumps({'code':400,'status':'la hash es requerida'})

    if (datos['prevurl'] == "character" or datos['prevurl'] == "location" or 
        datos['prevurl'] == "episode" or datos['prevurl'] == "/" ):
       
        if(datos['prevurl'] == "/"):
            info = requests.get(api).json()
            p = json.dumps(info)
            h = hash(p)
            if(str(h) == str(datos['hash'])):
                return json.dumps({'code':200,'status':'ok'})
            else:
                return json.dumps({'code':400,'status':'invalid'})
        else:
            url = api+'/'+datos['prevurl']
            character = requests.get(url).json()
            p = json.dumps(character)
            h = hash(p)
            if(str(h) == str(datos['hash'])):
                return json.dumps({'code':200,'status':'ok'})
            else:
                return json.dumps({'code':400,'status':'invalid'})
            #print(0)
    else:
        return json.dumps({'code':400,'status':'la url prev no es valida'})


def createzip():
    import zipfile
    try:
        import zlib
        compression = zipfile.ZIP_DEFLATED
    except:
        compression = zipfile.ZIP_STORED
    zf = zipfile.ZipFile("tmp.zip", mode="w")
    try:
        zf.write("tmp.json", compress_type=compression)
    finally:
        zf.close()
