from app import app
from flask_cors import CORS
from app.controller import NodeController, AccountController, NodeRelationController, Dijkstra
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/node', methods=['GET', 'POST'])
@jwt_required()
def node():
    if request.method == 'GET':
        return NodeController.index()
    elif request.method == 'POST':
        return NodeController.addNode()

@app.route('/node/<id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def nodeDetail(id):
    if request.method == 'GET':
        return NodeController.detail(id)
    elif request.method == 'PUT':
        return NodeController.updateNode(id)
    else:
        return NodeController.deleteNode(id)

@app.route('/edge', methods=['GET', 'POST'])
@jwt_required()
def edge():
    if request.method == 'GET':
        return NodeRelationController.index()
    elif request.method == 'POST':
        return NodeRelationController.addEdge()
    
@app.route('/edge/<id1>/<id2>', methods=['DELETE'])
@jwt_required()
def edgeDetail(id1, id2):
    return NodeRelationController.deleteEdge(id1, id2)

# @app.route('/account/register', methods=['POST'])
# def addAccount():
#     return AccountController.addAccount()

@app.route('/account/login', methods=['POST'])
def login():
    return AccountController.login()

@app.route('/user/path', methods=['POST'])
def path():
    return Dijkstra.shortest_path()

@app.route('/user/node/<id>', methods=['GET'])
def userNode(id):
    return NodeController.indexForUser(id)

@app.route('/user/node/<id>/<idNode>', methods=['GET'])
def userDetailNode(id, idNode):
    return NodeController.detailForUser(id, idNode)