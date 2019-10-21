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
        sql = "INSERT INTO Admin (employeeid,username,name,permission,position,createby) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(data_new['employeeid'],data_new['username'],data_new['name'],data_new['permission'],data_new['position'],data_new['createby']))

        type_action = "ADD"

        sql_log = "INSERT INTO Admin_log (employeeid,username,name,permission,position,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(data_new['employeeid'],data_new['username'],data_new['name'],data_new['permission'],data_new['position'],data_new['createby'],type_action))
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

        sql = "SELECT * FROM Admin WHERE employeeid=%s"
        cursor.execute(sql,(data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action= "Edit"
    
        sqlIn_log = "INSERT INTO Admin_log (employeeid,username,name,permission,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_log,(result[0]['employeeid'],result[0]['username'],result[0]['name'],result[0]['permission'],data_new['createby'],type_action))

        sqlDe = "DELETE FROM Admin WHERE employeeid=%s"
        cursor.execute(sqlDe,(data_new['employeeid']))

        sqlIn = "INSERT INTO Admin (employeeid,username,name,permission,createby) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn,(data_new['employeeid'],data_new['username'],data_new['name'],data_new['permission'],data_new['createby']))

        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryAdmin', methods=['POST'])
@connect_sql()
def QryAdmin(cursor):
    try:
        sql = "SELECT id,employeeid,username,name,position,permission FROM Admin"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryPermission', methods=['POST'])
@connect_sql()
def QryPermission(cursor):
    try:
        sql = "SELECT permission FROM Permission_Detail"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/DeleteAdmin', methods=['POST'])
@connect_sql()
def DeleteAdmin(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT * FROM Admin WHERE employeeid=%s AND permission=%s"
        cursor.execute(sql,(data_new['employeeid'],data_new['permission']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action= "Delete"

        sqlIn_log = "INSERT INTO Admin_log (employeeid,username,name,permission,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_log,(result[0]['employeeid'],result[0]['username'],result[0]['name'],result[0]['permission'],data_new['createby'],type_action))


        sqlDe = "DELETE FROM Admin WHERE employeeid=%s"
        cursor.execute(sqlDe,(data_new['employeeid']))

        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
