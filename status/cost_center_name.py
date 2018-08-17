#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/InsertCost_center', methods=['POST'])
@connect_sql()
def InsertCost_center(cursor):
    try:
        data = request.json
        source = data['source']
        data_new = source
        cost_center_name_id = data_new['cost_center_name_id']
        cost_detail = data_new['cost_detail']
        email = data_new['email']
        validstatus = data_new['validstatus']
        sql = "INSERT INTO cost_center_name (cost_center_name_id,cost_detail,email,validstatus) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql,(cost_center_name_id,cost_detail,email,validstatus))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditCost_center', methods=['POST'])
@connect_sql()
def EditCost_center(cursor):
    try:
        data = request.json
        source = data['source']
        data_new = source
        id = data_new['id']
        cost_center_name_id = data_new['cost_center_name_id']
        cost_detail = data_new['cost_detail']
        email = data_new['email']
        validstatus = data_new['validstatus']
        sqlUp = "UPDATE cost_center_name SET cost_center_name_id = %s, cost_detail = %s, email = %s,  validstatus = %s WHERE id = %s"
        cursor.execute(sqlUp,(cost_center_name_id, cost_detail, email, validstatus, id))
        # sqlIn = "INSERT INTO cost_center_name (cost_center_name_id,cost_detail,email) VALUES (%s,%s,%s)"
        # cursor.execute(sqlIn,(cost_center_name_id,cost_detail,email))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryCost_center', methods=['POST'])
@connect_sql()
def QryCost_center(cursor):
    try:
        sql = "SELECT id,cost_center_name_id,cost_detail,email,validstatus FROM cost_center_name"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
