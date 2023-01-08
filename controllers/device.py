import pymysql
from app import app
from utils.db import mysql
from flask import jsonify
from flask import flash, request

#GET
@app.route('/device', methods=['GET'])
def getAllDevices():
    conn = None
    cursor = None
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
@app.route('/device', methods=['POST'])
def createDevice():
    conn = None
    cursor = None
    try:
        _json = request.json
        _id = _json['id']
        _name = _json['name']
        _created = _json['created_at']
        _updated = _json['updated_at']
        #validate
        if _id!=None and _name!=None and request.method == 'POST':
            #save edited
            sql = "INSERT INTO device VALUES(%s, %s, %s, %s)"
            data = (_id, _name, _created, _updated)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            res = jsonify("Device created successfully")
            res.status_code = 200
            return res
        else:
            res = jsonify("Cannot create device!")
            return res
    except Exception as e:
        print(e)

#Search one
@app.route('/device/<int:id>')
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
@app.route('/update_dv/<int:id>', methods=['PUT'])
def updateDevice(id):
    conn = None
    cursor = None
    try:
        _json = request.json
        _name = _json['name']

        if id!=None and request.method == 'PUT':
            #update
            sql = "UPDATE device SET name=%s WHERE id=%s"
            data = (_name, id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            res = jsonify("Update device successfully")
            res.status_code = 200
            return res
        else:
            res = jsonify("Update device failed")
            return res
    except Exception as e:
        print(e)

#DELETE
@app.route('/delele_dv/<int:id>', methods=['DELETE'])
def deleteDevices(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM device WHERE id=%s", id)
        conn.commit()
        res = jsonify("Delete device successfully")
        res.status_code = 200
        return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()