#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/InsertAdmin', methods=['POST'])
@connect_sql()
def InsertAdmin(cursor):
    try:
        data = request.json
        source = data['source']
        data_new = source
        employeeid = data_new['employeeid']
        username = data_new['username']
        name = data_new['name']
        permission = data_new['permission']
        sql = "INSERT INTO Admin (employeeid,username,name,permission) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql,(employeeid,username,name,permission))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditAdmin', methods=['POST'])
@connect_sql()
def EditAdmin(cursor):
    try:
        data = request.json
        source = data['source']
        data_new = source
        id = data_new['id']
        employeeid = data_new['employeeid']
        username = data_new['username']
        name = data_new['name']
        permission = data_new['permission']
        sqlUp = "UPDATE Admin SET showAdmin=%s WHERE id=%s"
        cursor.execute(sqlUp,('0',id))
        sqlIn = "INSERT INTO Admin (employeeid,username,name,permission,showAdmin) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn,(employeeid,username,name,permission,'1'))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryAdmin', methods=['POST'])
@connect_sql()
def QryAdmin(cursor):
    try:
        sql = "SELECT id,employeeid,username,name,permission FROM Admin WHERE showAdmin = 1"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
