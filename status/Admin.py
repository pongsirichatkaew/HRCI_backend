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
        # sql = "INSERT INTO Admin (employeeid,username,name,permission,createby) VALUES (%s,%s,%s,%s,%s)"
        # cursor.execute(sql,(data_new['employeeid'],data_new['username'],data_new['name'],data_new['permission'],data_new['createby']))
        sql = "INSERT INTO Admin (employeeid,username,name,permission) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql,(data_new['employeeid'],data_new['username'],data_new['name'],data_new['permission']))
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

        sqlUp = "UPDATE Admin SET validstatus=%s WHERE employeeid=%s"
        cursor.execute(sqlUp,('0',data_new['employeeid']))

        # sqlIn = "INSERT INTO Admin (employeeid,username,name,permission,createby,validstatus) VALUES (%s,%s,%s,%s,%s,%s)"
        # cursor.execute(sqlIn,(data_new['employeeid'],data_new['username'],data_new['name'],data_new['permission'],data_new['createby'],'1'))
        sqlIn = "INSERT INTO Admin (employeeid,username,name,permission,validstatus) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn,(data_new['employeeid'],data_new['username'],data_new['name'],data_new['permission'],'1'))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryAdmin', methods=['POST'])
@connect_sql()
def QryAdmin(cursor):
    try:
        sql = "SELECT id,employeeid,username,name,permission FROM Admin WHERE validstatus = 1"
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

        sql_OldTimeAdmin = "UPDATE Admin SET validstatus=0 WHERE employeeid=%s"
        cursor.execute(sql_OldTimeAdmin,(data_new['employeeid']))

        # sql_NewTimeAdmin = "INSERT INTO Admin (employeeid,username,name,permission,createby,validstatus) VALUES (%s,%s,%s,%s,%s,%s)"
        # cursor.execute(sql_NewTimeAdmin,(data_new['employeeid'],data_new['username'],data_new['name'],data_new['permission'],data_new['createby'],0))
        sql_NewTimeAdmin = "INSERT INTO Admin (employeeid,username,name,permission,validstatus) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sql_NewTimeAdmin,(data_new['employeeid'],data_new['username'],data_new['name'],data_new['permission'],0))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
