import os
from datetime import datetime

from app.model.node import Node
# from app.controller.UploadConfig import allowed_file
from app.controller.AccountController import getAccountId
from googleapiclient.discovery import build
from google.oauth2 import service_account

from app import response, app, db, uploadConfig
from flask import request

def index():
    try:
        idAccount = getAccountId()
        node = Node.query.filter_by(idAccount=idAccount).all()
        data = formatarray(node)
        return response.success(data, 'success')
    except Exception as e:
        print(e)

def indexForUser(id):
    try:
        idAccount = id
        print(idAccount)
        node = Node.query.filter_by(idAccount=idAccount).all()
        data = formatarray(node)
        return response.success(data, 'success')
    except Exception as e:
        print(e)

def formatarray(datas):
    data = []
    for i in datas:
        data.append(singleNode(i))
    return data

def singleNode(data):
    data = {
        'idNode': data.idNode,
        'name': data.name,
        'photo': data.photo,
        'desc': data.desc,
        'address': data.address,
        'nodetype': data.nodetype,
        'level': data.level,
    }
    return data

def detail(id):
    try:
        idAccount = getAccountId()
        node = Node.query.filter_by(idNode=id, idAccount=idAccount).first()
        if not node:
            return response.badRequest([], 'Node not found')
        data = singleNode(node)
        return response.success(data, 'success')
    except Exception as e:
        print(e)

def addNode():
    try:
        idAccount = getAccountId()
        name = request.form.get('name')
        desc = request.form.get('desc')
        address = request.form.get('address')
        nodetype = request.form.get('type')
        level = request.form.get('level')

        photo = request.files['photo']
        photo = uploadPhoto(photo, idAccount, name)

        node = Node(idAccount=idAccount, name=name, photo=photo, desc=desc, address=address, nodetype=nodetype, level=level)
        db.session.add(node)
        db.session.commit()

        data = singleNode(node)
        return response.success(data, 'success add node')

    except Exception as e:
        print(e)

def updateNode(id):
    try:
        idAccount = getAccountId()
        name = request.form.get('name')
        photo = request.form.get('photo')
        desc = request.form.get('desc')
        address = request.form.get('address')
        level = request.form.get('level')

        input = [
            {
                'name': name,
                'photo': photo,
                'desc': desc,
                'address': address,
                'level': level
            }
        ]

        node = Node.query.filter_by(idNode=id, idAccount=idAccount).first()

        node.name = name
        node.photo = photo
        node.desc = desc
        node.address = address
        node.level = level

        db.session.commit()

        return response.success(input, 'success update data')

    except Exception as e:
        print(e)

def hapusNode(id):
    try:
        node = Node.query.filter_by(idNode=id, idAccount=idAccount).first()
        if not node:
            return response.badRequest([], 'node not found')
        
        db.session.delete(node)
        db.session.commit

        return response.success(input, 'success delete data')
    
    except Exception as e:
        print(e)

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'app/credentials.json'
PARENT_FOLDER_ID = '1s_gi4gTZA9T4ZVftC_sIgrwQMpwxR_H0'

def authenticate():
    try:
        creds = None
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        return creds
    except Exception as e:
        print(e)

def uploadPhoto(photo, idAccount,name):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    if not photo or not uploadConfig.allowed_file(photo.filename):
        return response.badRequest([], 'file not found or file extension not allowed')

    filename = f'{idAccount}_{name}_{datetime.now().strftime("%Y%m%d%H%M%S")}.png'
    localFilePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    photo.save(localFilePath)
    
    file_metadata = {
        'name': filename,
        'parents': [PARENT_FOLDER_ID]
    }

    file = service.files().create(
        body=file_metadata,
        media_body=localFilePath,
        fields='id, webViewLink'
    ).execute()

    return file.get('webViewLink')
