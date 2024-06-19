from app.model.node import Node

from app import response, app, db
from flask import request

def index():
    try:
        node = Node.query.all()
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
        'description': data.description,
        'address': data.address,
        'level': data.level,
    }
    return data

def detail(id):
    try:
        node = Node.query.filter_by(idNode=id).first()
        if not node:
            return response.badRequest([], 'Node not found')
        data = singleObject(node)
        return response.success(data, 'success')
    except Exception as e:
        print(e)