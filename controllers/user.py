import pymysql
import hashlib
from app import *
from utils.db import mysql
from flask import jsonify
from flask import flash, request
#from datetime import datetime
from flask_jwt_extended import jwt_required
#from flask_jwt_extended import get_jwt_identity

#GET
@app.route('/user', methods=['GET'])
#@cross_origin(supports_credentials=True)
@jwt_required()
def getAllUsers():
    conn = None
    cursor = None
    try:
	    conn = mysql.connect()
	    cursor = conn.cursor(pymysql.cursors.DictCursor)
	    cursor.execute("SELECT * FROM user")
	    rows = cursor.fetchall()
	    res = jsonify(rows)
	    res.status_code = 200
	    return res
    except Exception as e:
	    print(e)
    finally:
	    cursor.close()
	    conn.close()

#POST
@app.route('/user', methods=['POST'], endpoint='createUser')
@jwt_required()
def createUser():
    conn = None
    cursor = None
    try:
        _json = request.json
        _name = _json['name']
        _phone_number = _json['phone_number']
        _email = _json['email']
        _password = _json['password']
        #validate
        if _name!=None and _email!=None and request.method == 'POST':
            #save edited
            _hashed_password = hashlib.sha256(_password.encode('utf-8')).hexdigest()
            sql = "INSERT INTO user (name, phone_number, email, password) VALUES (%s, %s, %s, %s)"
            data = (_name, _phone_number, _email, _hashed_password)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            res = jsonify({"message": "Create user successfully"})
            res.status_code = 200
            return res
        else:
            res = jsonify({"message": "Cannot create user"})
            return res
    except Exception as e:
        print(e)

#Search one
@app.route('/user/<int:id>', endpoint='findUser')
@cross_origin(orgin='*')
@jwt_required()
def findUser(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM user WHERE id = %s", id)
        row = cursor.fetchone()
        res = jsonify(row)
        res.status_code = 200
        return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#PUT
@app.route('/user/<int:id>/update', methods=['PUT', 'POST'], endpoint='updateUser')
@cross_origin(orgin='*')
@jwt_required()
def updateUser(id):
    conn = None
    cursor = None
    try:
        _json = request.json
        _name = _json['name']
        _phone_number = _json['phone_number']
        _email = _json['email']
        _role = _json['role']
        _password = _json['password']
        if _email!=None and _password!=None and request.method == 'PUT' or 'POST':
            #update
            sql = "UPDATE user SET name=%s, phone_number=%s, email=%s, role=%s, password=%s WHERE id=%s"
            data = (_name, _phone_number, _email, _role, _password, id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            res = jsonify({"message": "Update user successfully"})
            res.status_code = 200
            return res
        else:
            res = jsonify({"message": "Update user failed"})
            return res
    except Exception as e:
        print(e)

#DELETE
@app.route('/user/<int:id>/delete', methods=['DELETE','POST'], endpoint='deleteUser')
@cross_origin(orgin='*')
@jwt_required()
def deleteUser(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user WHERE id=%s", id)
        conn.commit()
        res = jsonify({"message": "Delete user successfully"})
        #print(type(res))
        res.status_code = 200
        return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()






