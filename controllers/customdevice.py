import pymysql
from app import app
from utils.db import mysql
from flask import jsonify
from flask import flash, request

#GET
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


#POST
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
        if _id!=None and _roomID!=None and _name!=None and _param!=None and _is_active!=None and request.method == 'POST':
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
            res = jsonify("Cannot create customedevice!")
            return res
    except Exception as e:
        print(e)

#Search one
@app.route('/customdevice/<int:id>')
def findCustomDevice(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM customdevice WHERE id = %s", id)
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
@app.route('/update_dv/<int:id>', methods=['PUT'])
def updateCustomDevice(id):
    conn = None
    cursor = None
    try:
        _json = request.json
        _roomID = _json['roomID']
        _name = _json['name']
        _param = _json['param']
        _is_active = _json['is_active']

        if id!=None and _roomID!=None and _name!=None and _param!=None and _is_active!=None and request.method == 'PUT':
            #update
            sql = "UPDATE customdevice SET roomID=%s, name=%s, param=%s, is_active=%s WHERE id=%s"
            data = (_roomID, _name, _param, _is_active, id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            res = jsonify("Update customdevice successfully")
            res.status_code = 200
            return res
        else:
            res = jsonify("Update customdevice failed")
            return res
    except Exception as e:
        print(e)

#DELETE
@app.route('/delele_dv/<int:id>', methods=['DELETE'])
def deleteCustomDevices(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM customdevice WHERE id=%s", id)
        conn.commit()
        res = jsonify("Delete customdevice successfully")
        res.status_code = 200
        return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()