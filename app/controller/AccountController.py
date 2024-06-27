from app.model.account import Account

from app import response, app, db
from flask import request
from flask_jwt_extended import *

from datetime import datetime, timedelta

def getAccountId():
    current_user = get_jwt_identity()
    idAccount = current_user.get('idAccount')

    account = Account.query.filter_by(idAccount=idAccount).first()

    if not account:
        return response.badRequest([], 'Account not found')

    return idAccount

def index():
    try:
        account = Account.query.all()
        data = formatarray(account)
        return response.success(data, 'success')
    except Exception as e:
        print(e)

def formatarray(datas):
    data = []
    for i in datas:
        data.append(singleAccount(i))
    return data

def singleAccount(data):
    data = {
        'idAccount': data.idAccount,
        'username': data.username,
    }
    return data

def addAccount():
    try:
        username = request.form.get('username')
        password = request.form.get('password')

        account = Account(username=username)
        account.setPassword(password)
        db.session.add(account)
        db.session.commit()

        data = singleAccount(account)
        return response.success(data, 'success')

    except Exception as e:
        print(e)

def login():
    try:
        data = request.json  # Get JSON data from request body
        username = data.get('username')
        password = data.get('password')
        print(f'username: {username}, password: {password}')

        account = Account.query.filter_by(username=username).first()

        if not account or not account.checkPassword(password):
            return response.badRequest([], 'Account not found')

        data = singleAccount(account)

        expires = timedelta(days=7)
        expires_refresh = timedelta(days=7)

        access_token = create_access_token(data, fresh=True, expires_delta=expires)
        refresh_token = create_refresh_token(data, expires_delta=expires_refresh)

        return response.success({
            "data": data,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }, 'success login')
        
    except Exception as e:
        print(e)
