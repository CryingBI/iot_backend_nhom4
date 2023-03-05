import pymysql
import hashlib
from app import *
from utils.db import mysql
from flask import jsonify
from flask import flash, request
#from datetime import datetime
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

#GET
@app.route('/user', methods=['GET', 'OPTIONS'])
@cross_origin(supports_credentials=True)
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
@cross_origin(orgin='*')
@jwt_required()
def createUser():
    conn = None
    cursor = None
    try:
        _json = request.json
        _id = _json['id']
        _name = _json['name']
        _phone_number = _json['phone_number']
        _email = _json['email']
        _role = _json['role']
        _password = _json['password']
        #validate
        if _id!=None and _name!=None and _email!=None and request.method == 'POST':
            #save edited
            _hashed_password = hashlib.sha256(_password.encode('utf-8')).hexdigest()
            sql = "INSERT INTO user VALUES(%s, %s, %s, %s, %s, %s)"
            data = (_id, _name, _phone_number, _email, _role, _hashed_password)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            res = jsonify("User created successfully")
            res.status_code = 200
            return res
        else:
            res = jsonify("Cannot create User!")
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
@app.route('/update_us/<int:id>', methods=['PUT'], endpoint='updateUser')
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
        if id!=None and _email!=None and _password!=None and request.method == 'PUT':
            #update
            sql = "UPDATE user SET name=%s, phone_number=%s, email=%s, role=%s, password=%s WHERE id=%s"
            data = (_name, _phone_number, _email, _role, _password, id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            res = jsonify("Update user successfully")
            res.status_code = 200
            return res
        else:
            res = jsonify("Update user failed")
            return res
    except Exception as e:
        print(e)

#DELETE
@app.route('/delele_us/<int:id>', methods=['DELETE'], endpoint='deleteUser')
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
        res = jsonify("Delete user successfully")
        #print(type(res))
        res.status_code = 200
        return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()






