#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/InsertOrg_name', methods=['POST'])
@connect_sql()
def InsertOrg_name(cursor):
    try:
        data = request.json
        org_name_id = data['org_name_id']
        org_name_detail = data['org_name_detail']
        email = data['email']
        sql = "INSERT INTO org_name (org_name_id,org_name_detail,email) VALUES (%s,%s,%s)"
        cursor.execute(sql,(org_name_id,org_name_detail,email))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditOrg_name', methods=['POST'])
@connect_sql()
def EditOrg_name(cursor):
    try:
        data = request.json
        id = data['id']
        org_name_id = data['org_name_id']
        org_name_detail = data['org_name_detail']
        email = data['email']
        sqlUp = "UPDATE org_name SET validstatus = '0' WHERE id=%s"
        cursor.execute(sqlUp,(data['id']))
        sqlIn = "INSERT INTO org_name (org_name_id,org_name_detail,email) VALUES (%s,%s,%s)"
        cursor.execute(sqlIn,(org_name_id,org_name_detail,email))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryOrg_name', methods=['POST'])
@connect_sql()
def QryOrg_name(cursor):
    try:
        sql = "SELECT org_name_id,org_name_detail,id,email FROM org_name WHERE validstatus=1"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
