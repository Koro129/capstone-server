from app.model.noderelation import NodeRelation
from app.model.node import Node
from app.controller.AccountController import getAccountId  # Pastikan Anda mengimpor fungsi getAccountId dari modul yang benar
from app import response, app, db
from flask import request

def index():
    try:
        idAccount = getAccountId()

        # Lakukan join antara NodeRelation dan Node untuk mengakses idAccount dari masing-masing node
        nodeRelations = db.session.query(NodeRelation).join(Node, NodeRelation.idNode1 == Node.idNode).filter(Node.idAccount == idAccount).all()

        data = formatarray(nodeRelations)
        return response.success(data, 'success')
    except Exception as e:
        print(e)

def formatarray(datas):
    data = []
    for i in datas:
        data.append(singleNodeRelation(i))
    return data

def singleNodeRelation(data):
    data = {
        'idNode1': data.idNode1,
        'idNode2': data.idNode2,
        'weight': data.weight
    }
    return data

def addEdge():
    try:
        idAccount = getAccountId()
        idNode1 = request.form.get('idNode1')
        idNode2 = request.form.get('idNode2')
        weight = request.form.get('weight')

        # Pastikan idNode1 dan idNode2 ada di database
        node1 = Node.query.filter_by(idNode=idNode1, idAccount=idAccount).first()
        node2 = Node.query.filter_by(idNode=idNode2, idAccount=idAccount).first()

        if not node1 or not node2:
            return response.badRequest([], 'Node(s) not found')

        # Buat objek Edge baru
        edge = NodeRelation(idNode1=idNode1, idNode2=idNode2, weight=weight)
        db.session.add(edge)
        db.session.commit()

        data = singleEdge(edge)
        return response.success(data, 'success add edge')

    except Exception as e:
        print(e)

def deleteEdge():
    try:
        idAccount = getAccountId()
        idNode1 = request.form.get('idNode1')
        idNode2 = request.form.get('idNode2')

        # Pastikan edge yang akan dihapus ada di database
        edge = NodeRelation.query.filter_by(idNode1=idNode1, idNode2=idNode2).first()
        if not edge:
            return response.badRequest([], 'Edge not found')

        db.session.delete(edge)
        db.session.commit()

        data = singleEdge(edge)
        return response.success(data, 'success delete edge')

    except Exception as e:
        print(e)
