import json
import requests
import random 
from flask import Flask,request,jsonify,Response,send_file
import io
import time
import zipfile


app = Flask(__name__)
api = 'https://rickandmortyapi.com/api'
@app.route("/", methods =['POST'])
def infochapter(**datos):
    datos = request.form
    info = requests.get(api).json()  
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
        return info

@app.route('/<filtro>',methods =['POST'])
def getcharacter(filtro):
    datos = request.form
    if(filtro == "character" or filtro == "location" or filtro == "episode"):
        url = api+'/'+filtro
        character = requests.get(url).json()
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
        return character
    return json.dumps({'code':400,'status':'upss'})


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
