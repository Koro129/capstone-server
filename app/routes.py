from app import app
from app.controller import NodeController, AccountController
from flask import request

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/node', methods=['GET'])
def node():
    return NodeController.index()

@app.route('/account/register', methods=['POST'])
def addAccount():
    return AccountController.addAccount()

@app.route('/account/login', methods=['POST'])
def login():
    return AccountController.login()