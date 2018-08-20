#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/InsertOrg_name', methods=['POST'])
@connect_sql()
def InsertOrg_name(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sqlQry = "SELECT org_name_id FROM org_name ORDER BY org_name_id DESC LIMIT 1"
        cursor.execute(sqlQry)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        org_name_id_last=result[0]['org_name_id']+1

        sql = "INSERT INTO org_name (org_name_id,org_name_detail,email,createby) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql,(org_name_id_last,data_new['org_name_detail'],data_new['email'],data_new['createby']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditOrg_name', methods=['POST'])
@connect_sql()
def EditOrg_name(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT org_name_id FROM org_name WHERE org_name_id=%s"
        cursor.execute(sql,(data_new['org_name_id']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sqlUp = "UPDATE org_name SET validstatus=0 WHERE org_name_id=%s"
        cursor.execute(sqlUp,(data_new['org_name_id']))

        sqlIn = "INSERT INTO org_name (org_name_id,org_name_detail,email,createby) VALUES (%s,%s,%s,%s)"
        cursor.execute(sqlIn,(result[0]['org_name_id'],data_new['org_name_detail'],data_new['email'],data_new['createby']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryOrg_name', methods=['POST'])
@connect_sql()
def QryOrg_name(cursor):
    try:
        sql = "SELECT org_name_id,org_name_detail,email,id FROM org_name WHERE validstatus=1"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/DeleteOrg_name', methods=['POST'])
def DeleteOrg_name():
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sqlUp = "UPDATE org_name SET validstatus=0,createby=%s WHERE org_name_id=%s"
        cursor3.execute(sqlUp,(data_new['createby'],data_new['org_name_id']))
        connection.commit()
        connection.close()
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
