#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/InsertCost_center', methods=['POST'])
@connect_sql()
def InsertCost_center(cursor):
    try:
        data = request.json
        cost_center_name_id = data['cost_center_name_id']
        cost_detail = data['cost_detail']
        email = data['email']
        sql = "INSERT INTO cost_center_name (cost_center_name_id,cost_detail,email) VALUES (%s,%s,%s)"
        cursor.execute(sql,(cost_center_name_id,cost_detail,email))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditCost_center', methods=['POST'])
@connect_sql()
def EditCost_center(cursor):
    try:
        data = request.json
        id = data['id']
        cost_center_name_id = data['cost_center_name_id']
        cost_detail = data['cost_detail']
        email = data['email']
        sqlUp = "UPDATE cost_center_name SET validstatus = '0' WHERE id=%s"
        cursor.execute(sqlUp,(data['id']))
        sqlIn = "INSERT INTO cost_center_name (cost_center_name_id,cost_detail,email) VALUES (%s,%s,%s)"
        cursor.execute(sqlIn,(cost_center_name_id,cost_detail,email))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryCost_center', methods=['POST'])
@connect_sql()
def QryCost_center(cursor):
    try:
        sql = "SELECT cost_center_name_id,cost_detail,id FROM cost_center_name WHERE validstatus=1"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
