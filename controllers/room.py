import pymysql
from app import *
from utils.db import mysql
from flask import jsonify
from flask import flash, request
from datetime import datetime
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

#Thêm filter house-room
#thêm filler post house-room

#Huan API
#1 GET GET house/:house_id/room
@app.route('/house/<int:house_id>/rooms', methods=['GET'], endpoint='getRoomOfHouse')
@jwt_required()
def getRoomOfHouse(house_id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM room where house_id=%s", house_id)
        rows = cursor.fetchall()
        res = jsonify(rows)
        res.status_code = 200
        return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#2 POST house/:house_id/room
@app.route('/house/<int:house_id>/room', methods=['POST'], endpoint='createRoomOfHouse')
@jwt_required()
def createRoomOfHouse(house_id):
    conn = None
    cursor = None
    try:
        _json = request.json
        _name = _json['name']
        _created = datetime.utcnow()
        _updated = datetime.utcnow()
        # validate
        if  _name != None and request.method == 'POST':
            # save edited
            sql = "INSERT INTO house (house_id, name, created_at, updated_at) VALUES (%s, %s, %s, %s)"
            data = (house_id, _name, _created, _updated)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            res = jsonify({"message": "Create room successfully"})
            res.status_code = 200
            return res
        else:
            res = jsonify({"message": "Cannot create room"})
            return res
    except Exception as e:
        print(e)

#3 PUT house/:house_id/room/:room_id/update
@app.route('/house/<int:house_id>/room/<int:room_id>/update', methods=['POST', 'PUT'], endpoint='updateRoomOfHouse')
@jwt_required()
def updateRoomOfHouse(house_id, room_id):
    conn = None
    cursor = None
    try:
        _json = request.json
        _name = _json['name']
        _updated_at = datetime.utcnow()
        if house_id!=None and room_id!=None and _name!=None and request.method == 'PUT' or 'POST':
            # update
            sql = "UPDATE room SET name=%s, updated_at=%s WHERE house_id=%s AND id=%s"
            data = (_name, _updated_at, house_id, room_id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            res = jsonify({"message": "Update room successfully"})
            res.status_code = 200
            return res
        else:
            res = jsonify({"message": "Update room failed"})
            return res
    except Exception as e:
        print(e)

#4 DELTE house/:house_id/room/:room_id/delete
@app.route('/house/<int:house_id>/room/<int:room_id>/delete', methods=['POST', 'DELETE'], endpoint='deleteRoomOfHouse')
@jwt_required()
def deleteRoomOfHouse(house_id, room_id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM room WHERE house_id=%s AND id=%s", (house_id,room_id))
        conn.commit()
        res = jsonify({"message": "Delete room successfully"})
        # print(type(res))
        res.status_code = 200
        return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

