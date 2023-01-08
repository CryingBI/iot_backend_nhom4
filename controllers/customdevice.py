import pymysql
from app import app
from utils.db import mysql
from flask import jsonify
from flask import flash, request


@app.route('/customdevice', methods=['GET'])
def getAllCustomDevices():
    conn = None
    cursor = None
    try:
	    conn = mysql.connect()
	    cursor = conn.cursor(pymysql.cursors.DictCursor)
	    cursor.execute("SELECT * FROM customdevice")
	    rows = cursor.fetchall()
	    res = jsonify(rows)
	    res.status_code = 200
	    return res
    except Exception as e:
	    print(e)
    finally:
	    cursor.close()
	    conn.close()


@app.route('/customdevice', methods=['POST'])
def createCustomDevice():
    conn = None
    cursor = None
    try:
        _json = request.json
        _id = _json['id']
        _roomID = _json['roomID']
        _name = _json['name']
        _param = _json['param']
        _is_active = _json['is_active']
        _created = _json['created_at']
        _updated = _json['updated_at']
        #validate
        if _id and _roomID and _name and _param and _is_active and request.method == 'POST':
            #save edited
            sql = "INSERT INTO customdevice VALUES(%s, %s, %s, %s, %s, %s, %s)"
            data = (_id, _roomID, _name, _param, _is_active, _created, _updated)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            res = jsonify("Customedevice created successfully")
            res.status_code = 200
            return res
        else:
            res = jsonify("Cannot create customed!")
            return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


