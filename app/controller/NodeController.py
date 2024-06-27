import os
from datetime import datetime

from app.model.node import Node
from app.model.noderelation import NodeRelation

# from app.controller.UploadConfig import allowed_file
from app.controller.AccountController import getAccountId
from googleapiclient.discovery import build
from google.oauth2 import service_account

from app import response, app, db, uploadConfig
from flask import request

def index():
    try:
        # data = request.json
        idAccount = getAccountId()
        # level = data.get('level')
        level = request.args.get('level')
        if level:
            node = Node.query.filter_by(idAccount=idAccount, level=level).all()
        else:
            node = Node.query.filter_by(idAccount=idAccount).all()
        data = formatarray(node)
        return response.success(data, 'success')
    except Exception as e:
        print(e)

def indexForUser(id):
    try:
        idAccount = id
        node = Node.query.filter_by(idAccount=idAccount).all()
        data = formatarray(node)
        return response.success(data, 'success')
    except Exception as e:
        print(e)

def detailForUser(id, idNode):
    try:
        idAccount = id
        node = Node.query.filter_by(idNode=idNode, idAccount=idAccount).first()
        if not node:
            return response.badRequest([], 'Node not found')
        data = singleNode(node)
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
        'id': data.idNode,
        'name': data.name,
        'photo': data.photo,
        'description': data.desc,
        'address': data.address,
        'type': data.nodetype,
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
        data = request.json
        idAccount = getAccountId()
        name = data.get('name')
        desc = data.get('description')
        address = data.get('address')
        nodetype = data.get('type')
        level = data.get('level')
        photo = data.get('photo')

        # photo = request.files['photo']
        # photo = uploadPhoto(photo, idAccount, name)

        node = Node(idAccount=idAccount, name=name, photo=photo, desc=desc, address=address, nodetype=nodetype, level=level)
        db.session.add(node)
        db.session.commit()

        data = singleNode(node)
        return response.success(data, 'success add node')

    except Exception as e:
        print(e)

def updateNode(id):
    try:
        data = request.json
        idAccount = getAccountId()
        name = data.get('name')
        desc = data.get('description')
        address = data.get('address')
        nodetype = data.get('type')
        level = data.get('level')
        photo = data.get('photo')

        input = [
            {
                'name': name,
                'photo': photo,
                'desc': desc,
                'address': address,
                'type': nodetype,
                'level': level
            }
        ]

        node = Node.query.filter_by(idNode=id, idAccount=idAccount).first()

        node.name = name
        node.photo = photo
        node.desc = desc
        node.nodetype = nodetype
        node.address = address
        node.level = level

        db.session.commit()

        return response.success(input, 'success update data')

    except Exception as e:
        print(e)

def deleteNode(id):
    try:
        idAccount = getAccountId()
        node = Node.query.filter_by(idNode=id, idAccount=idAccount).first()
        if not node:
            return response.badRequest([], 'node not found')

        # Check if the node is used as a foreign key in NodeRelation
        nodeRelations = NodeRelation.query.filter_by(idNode1=id).all()
        nodeRelations += NodeRelation.query.filter_by(idNode2=id).all()
        if nodeRelations:
            return response.badRequest([], 'Node used on relation')

        db.session.delete(node)
        db.session.commit()

        return response.success('', 'success delete data')
    
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
