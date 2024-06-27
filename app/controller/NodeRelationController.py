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
        'ID1': data.idNode1,
        'ID2': data.idNode2,
        'weight': data.weight
    }
    return data

def addEdge():
    try:
        idAccount = getAccountId()
        data = request.get_json()
        idNode1 = data.get('ID1')
        idNode2 = data.get('ID2')
        weight = data.get('weight')

        # Pastikan idNode1 dan idNode2 ada di database
        node1 = Node.query.filter_by(idNode=idNode1, idAccount=idAccount).first()
        node2 = Node.query.filter_by(idNode=idNode2, idAccount=idAccount).first()

        if not node1 or not node2:
            return response.badRequest([], 'Node(s) not found')

        # Pastikan node1 dan node2 memiliki level yang sama
        if node1.level != node2.level:
            return response.badRequest([], 'Nodes have different levels')

        # Buat objek Edge baru
        edge = NodeRelation(idNode1=idNode1, idNode2=idNode2, weight=weight)
        db.session.add(edge)
        db.session.commit()

        edge = NodeRelation(idNode1=idNode2, idNode2=idNode1, weight=weight)
        db.session.add(edge)
        db.session.commit()

        data = singleNodeRelation(edge)
        return response.success(data, 'success add edge')

    except Exception as e:
        print(e)

def deleteEdge(id1, id2):
    try:
        idAccount = getAccountId()

        # Pastikan edge yang akan dihapus ada di database
        edge = NodeRelation.query.filter_by(idNode1=id1, idNode2=id2).first()
        edge2 = NodeRelation.query.filter_by(idNode1=id2, idNode2=id1).first()

        if not edge or not edge2:
            return response.badRequest([], 'Edge not found')

        db.session.delete(edge)
        db.session.delete(edge2)
        db.session.commit()

        # data = formatarray(edge)
        return response.success('', 'success delete edge')

    except Exception as e:
        print(e)
