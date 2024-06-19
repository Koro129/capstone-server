from app.model.node import Node
from app.controller.AccountController import getAccountId

from app import response, app, db
from flask import request

def index():
    try:
        idAccount = getAccountId()
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
        photo = request.form.get('photo')
        desc = request.form.get('desc')
        address = request.form.get('address')
        level = request.form.get('level')

        node = Node(idAccount=idAccount, name=name, photo=photo, desc=desc, address=address, level=level)
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