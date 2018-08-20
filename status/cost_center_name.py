#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/InsertCost_center', methods=['POST'])
@connect_sql()
def InsertCost_center(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sqlQry = "SELECT cost_center_name_id FROM cost_center_name ORDER BY cost_center_name_id DESC LIMIT 1"
        cursor3.execute(sqlQry)
        columns = [column[0] for column in cursor3.description]
        result = toJson(cursor3.fetchall(),columns)
        cost_center_name_id_last=result[0]['cost_center_name_id']+1

        sql = "INSERT INTO cost_center_name (cost_center_name_id,cost_detail,email) VALUES (%s,%s,%s)"
        cursor3.execute(sql,(cost_center_name_id_last,data_new['cost_detail'],data_new['email']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditCost_center', methods=['POST'])
@connect_sql()
def EditCost_center(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT cost_center_name_id FROM cost_center_name WHERE cost_center_name_id=%s"
        cursor3.execute(sql,(data_new['cost_center_name_id']))
        columns = [column[0] for column in cursor3.description]
        result = toJson(cursor3.fetchall(),columns)

        sqlUp = "UPDATE cost_center_name SET validstatus=0 WHERE cost_center_name_id=%s"
        cursor3.execute(sqlUp,(data_new['cost_center_name_id']))

        sqlIn = "INSERT INTO cost_center_name (cost_center_name_id,cost_detail,email) VALUES (%s,%s,%s)"
        cursor3.execute(sqlIn,(result[0]['cost_center_name_id'],data_new['cost_detail'],data_new['email']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryCost_center', methods=['POST'])
@connect_sql()
def QryCost_center(cursor):
    try:
        sql = "SELECT cost_center_name_id,cost_detail,email FROM cost_center_name WHERE validstatus=1"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
