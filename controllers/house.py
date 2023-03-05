import pymysql
from app import *
from utils.db import mysql
from flask import jsonify
from flask import flash, request
from datetime import datetime
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

#Thêm filter user-house
#thêm filler post user-house

#GET
@app.route('/house', methods=['GET'], endpoint='getAllHouses')
@jwt_required()
def getAllHouses():
    conn = None
    cursor = None
    try:
	    conn = mysql.connect()
	    cursor = conn.cursor(pymysql.cursors.DictCursor)
	    cursor.execute("SELECT * FROM house, user WHERE house.user_id = user.id")
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
@app.route('/house', methods=['POST'], endpoint='createHouse')
@jwt_required()
def createHouse():
    conn = None
    cursor = None
    try:
        _json = request.json
        _user_id = _json['user_id']
        _name = _json['name']
        _address = _json['address']
        _created = datetime.utcnow()
        _updated = datetime.utcnow()
        #validate
        if _name!=None and _user_id!=None and _address!=None and request.method == 'POST':
            #save edited
            sql = "INSERT INTO house (user_id, name, address, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)"
            data = (_user_id, _name, _address, _created, _updated)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            res = jsonify({"message": "House successfully"})
            res.status_code = 200
            return res
        else:
            res = jsonify({"message": "Cannot create house"})
            return res
    except Exception as e:
        print(e)

#Search one
@app.route('/house/<int:id>', endpoint='findHouse')
@jwt_required()
def findHouse(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM house WHERE id = %s", id)
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
@app.route('/house/<int:id>/update', methods=['POST', 'PUT'], endpoint='updateHouse')
@jwt_required()
def updateHouse(id):
    conn = None
    cursor = None
    try:
        _json = request.json
        _user_id = _json['user_id']
        _name = _json['name']
        _address = _json['address']
        _updated_at = datetime.utcnow()
        if id!=None and _user_id!= None and request.method == 'PUT' or 'POST':
            #update
            sql = "UPDATE house SET user_id=%s, name=%s, address=%s, updated_at=%s WHERE id=%s"
            data = (_user_id, _name, _address, _updated_at, id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            res = jsonify("Update house successfully")
            res.status_code = 200
            return res
        else:
            res = jsonify("Update house failed")
            return res
    except Exception as e:
        print(e)

#DELETE
@app.route('/house/<int:id>/delete', methods=['DELETE'], endpoint='deleteHouse')
@jwt_required()
def deleteHouse(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM house WHERE id=%s", id)
        conn.commit()
        res = jsonify("Delete device successfully")
        #print(type(res))
        res.status_code = 200
        return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


#Huan API
#1 GET user/id/houses
@app.route('/user/<int:user_id>/houses', methods=['GET'], endpoint='getHouseOfUser')
@jwt_required()
def getHouseOfUser(user_id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM house where user_id=%s", user_id)
        rows = cursor.fetchall()
        res = jsonify(rows)
        res.status_code = 200
        return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#2 POST user/id/houses
@app.route('/user/<int:user_id>/house', methods=['POST'], endpoint='createHouseOfUser')
@jwt_required()
def createHouseOfUser(user_id):
    conn = None
    cursor = None
    try:
        _json = request.json
        _name = _json['name']
        _address = _json['address']
        _created = datetime.utcnow()
        _updated = datetime.utcnow()
        # validate
        if _id != None and _name != None and _address != None and request.method == 'POST':
            # save edited
            sql = "INSERT INTO house (user_id, name, address, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)"
            data = (user_id, _name, _address, _created, _updated)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            res = jsonify({"message": "Create house successfully"})
            res.status_code = 200
            return res
        else:
            res = jsonify({"message": "Create house failed"})
            return res
    except Exception as e:
        print(e)

#3 PUT user/:id/house/:house_id/update
@app.route('/user/<int:user_id>/house/<int:house_id>/update', methods=['PUT', 'POST'], endpoint='updateHouseOfUser')
@jwt_required()
def updateHouseOfUser(user_id, house_id):
    conn = None
    cursor = None
    try:
        _json = request.json
        _name = _json['name']
        _address = _json['address']
        _updated_at = datetime.utcnow()
        if user_id!=None and house_id!=None and _name!=None and _address!= None and request.method == 'PUT' or 'POST':
            # update
            sql = "UPDATE house SET name=%s, address=%s, updated_at=%s WHERE user_id=%s AND id=%s"
            data = (_name, _address, _updated_at, user_id, house_id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            res = jsonify({"message": "Update house successfully"})
            res.status_code = 200
            return res
        else:
            res = jsonify({"message": "Update house failed"})
            return res
    except Exception as e:
        print(e)

#4 DELTE user/:id/house/:house_id/delete
@app.route('/user/<int:user_id>/house/<int:house_id>/delete', methods=['DELETE', 'POST'], endpoint='deleteHouseOfUser')
@jwt_required()
def deleteHouseOfUser(user_id, house_id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM house WHERE user_id=%s AND id=%s", (user_id,house_id))
        conn.commit()
        res = jsonify({"message": "Delete house successfully"})
        # print(type(res))
        res.status_code = 200
        return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()