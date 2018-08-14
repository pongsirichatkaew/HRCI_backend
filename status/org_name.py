#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/InsertOrg_name', methods=['POST'])
@connect_sql()
def InsertOrg_name(cursor):
    try:
        data = request.json
        source = data['source']
        data_new = source
        org_name_id = data_new['org_name_id']
        org_name_detail = data_new['org_name_detail']
        email = data_new['email']
        validstatus = data_new['validstatus']
        sql = "INSERT INTO org_name (org_name_id,org_name_detail,email,validstatus) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql,(org_name_id,org_name_detail,email,validstatus))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditOrg_name', methods=['POST'])
@connect_sql()
def EditOrg_name(cursor):
    try:
        data = request.json
        source = data['source']
        data_new = source
        id = data_new['id']
        org_name_id = data_new['org_name_id']
        org_name_detail = data_new['org_name_detail']
        email = data_new['email']
        validstatus = data_new['validstatus']
        sqlUp = "UPDATE org_name SET org_name_id=%s,org_name_detail=%s,email=%s,validstatus=%s WHERE id=%s"
        cursor.execute(sqlUp,(org_name_id,org_name_detail,email,validstatus,id))
        # sqlIn = "INSERT INTO org_name (org_name_id,org_name_detail,email) VALUES (%s,%s,%s)"
        # cursor.execute(sqlIn,(org_name_id,org_name_detail,email))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryOrg_name', methods=['POST'])
@connect_sql()
def QryOrg_name(cursor):
    try:
        sql = "SELECT org_name_id,org_name_detail,id,email,validstatus FROM org_name"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
