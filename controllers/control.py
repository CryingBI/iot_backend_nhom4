import pymysql
import paho.mqtt.client as paho
from app import *
from utils.db import mysql
from flask import jsonify
from flask import flash, request
from flask_jwt_extended import jwt_required
import time, json
from flask_jwt_extended import get_jwt_identity
from mqtt_connect import *

#API dieu khien thiet bi
@app.route('/device/<int:id>/control', methods=['PUT'], endpoint='controlDevice')
@jwt_required()
def controlDevice(id):
    content = None
    conn = None
    cursor = None
    current_user = get_jwt_identity()
    try:
        _json = request.json
        _is_active = _json['is_active']
        _param = _json['param']
        _json['id'] = id
        _json['userID'] = current_user
        sql = "UPDATE device_room SET is_active=%s, param=%s WHERE id=%s"
        data = (_is_active, _param, id)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        client.publish("/iot_project_nhom04", payload=json.dumps(_json))

        res = jsonify(_json)
        return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

