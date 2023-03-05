import pymysql
from app import *
from utils.db import mysql
from flask import jsonify
from flask import flash, request
from datetime import datetime
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

#GET
@app.route('/device', methods=['GET'], endpoint='getAllDevices')
@jwt_required()
def getAllDevices():
    conn = None
    cursor = None
    current_user = get_jwt_identity()
    print(current_user)
    try:
	    conn = mysql.connect()
	    cursor = conn.cursor(pymysql.cursors.DictCursor)
	    cursor.execute("SELECT * FROM device")
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
@app.route('/device', methods=['POST'], endpoint='createDevice')
@jwt_required()
def createDevice():
    conn = None
    cursor = None
    try:
        _json = request.json
        _name = _json['name']
        _created = datetime.utcnow()
        _updated = datetime.utcnow()
        #validate
        if  _name!=None and request.method == 'POST':
            #save edited
            sql = "INSERT INTO device (name, created_at, updated_at) VALUES(%s, %s, %s)"
            data = (_name, _created, _updated)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            res = jsonify({"message": "Create device successfully"})
            res.status_code = 200
            return res
        else:
            res = jsonify({"message": "Cannot create device"})
            return res
    except Exception as e:
        print(e)

#Search one
@app.route('/device/<int:id>', endpoint='findDevice')
@jwt_required()
def findDevice(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM device WHERE id = %s", id)
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
@app.route('/device/<int:id>/update', methods=['POST', 'PUT'], endpoint='updateDevice')
@jwt_required()
def updateDevice(id):
    conn = None
    cursor = None
    try:
        _json = request.json
        _name = _json['name']
        _updated_at = datetime.utcnow()
        if id!=None and request.method == 'POST' or 'PUT':
            #update
            sql = "UPDATE device SET name=%s, updated_at=%s WHERE id=%s"
            data = (_name, _updated_at, id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            res = jsonify({"message": "Update device successfully"})
            res.status_code = 200
            return res
        else:
            res = jsonify({"message": "Update device failed"})
            return res
    except Exception as e:
        print(e)

#DELETE
@app.route('/device/<int:id>/delete', methods=['POST', 'DELETE'], endpoint='deleteDevices')
@jwt_required()
def deleteDevices(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM device WHERE id=%s", id)
        conn.commit()
        res = jsonify({"message": "Delete device successfully"})
        res.status_code = 200
        return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


#Huan API
#1 GET room/:room_id/device
@app.route('/room/<int:room_id>/devices', methods=['GET'], endpoint='getDeviceOfRoom')
@jwt_required()
def getDeviceOfRoom(room_id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM device_room where room_id=%s", room_id)
        rows = cursor.fetchall()
        res = jsonify(rows)
        res.status_code = 200
        return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

# #2 POST house/:house_id/room
# @app.route('/room/<int:room_id>/device', methods=['POST'], endpoint='createDeviceOfRoom')
# @jwt_required()
# def createDeviceOfRoom(room_id):
#     conn = None
#     cursor = None
#     try:
#         _json = request.json
#         _code = _json['code']
#         _created = datetime.utcnow()
#         _updated = datetime.utcnow()
#         # validate
#         if  _name != None and request.method == 'POST':
#             # save edited
#             sql = "INSERT INTO house (house_id, name, created_at, updated_at) VALUES (%s, %s, %s, %s)"
#             data = (house_id, _name, _created, _updated)
#             conn = mysql.connect()
#             cursor = conn.cursor()
#             cursor.execute(sql, data)
#             conn.commit()
#             res = jsonify({"message": "Create room successfully"})
#             res.status_code = 200
#             return res
#         else:
#             res = jsonify({"message": "Cannot create room"})
#             return res
#     except Exception as e:
#         print(e)