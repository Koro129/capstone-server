from app import app
from app.controller import NodeController, AccountController, NodeRelationController, Dijkstra
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

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
def nodeDetail(id):
    if request.method == 'GET':
        return NodeController.detail(id)
    elif request.method == 'PUT':
        return NodeController.updateNode(id)
    else:
        return NodeController.deleteNode(id)

@app.route('/edge', methods=['GET'])
@jwt_required()
def edge():
    return NodeRelationController.index()

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