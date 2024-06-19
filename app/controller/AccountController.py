from app.model.account import Account

from app import response, app, db
from flask import request
from flask_jwt_extended import *

from datetime import datetime, timedelta


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
        'username': data.username,
        'password': data.password,
    }
    return data

def addAccount():
    try:
        username = request.form.get('username')
        password = request.form.get('password')

        accounts = Account(username=username)
        accounts.setPassword(password)
        db.session.add(accounts)
        db.session.commit()

        # data = singleAccount(accounts)
        return response.success({
            "username": username,
            "password": password,
        
        }, 'success')

    except Exception as e:
        print(e)

def login():
    try:
        username = request.form.get('username')
        password = request.form.get('password')

        accounts = Account.query.filter_by(username=username).first()

        if not accounts:
            return response.badRequest([], 'Account not found')
        
        data = singleAccount(accounts)
        
        if not accounts.checkPassword(password):
            return response.badRequest({
                'data': data,
                'username': username,
                'password': password
            
            }, 'Password not match')

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