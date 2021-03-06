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
        cursor.execute(sqlQry)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        cost_center_name_id_last=result[0]['cost_center_name_id']+1

        sql = "INSERT INTO cost_center_name (cost_center_name_id,cost_detail,email,createby) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql,(cost_center_name_id_last,data_new['cost_detail'],data_new['email'],data_new['createby']))

        type_action = "ADD"

        sql_log = "INSERT INTO cost_center_name_log (cost_center_name_id,cost_detail,email,createby,type_action) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(cost_center_name_id_last,data_new['cost_detail'],data_new['email'],data_new['createby'],type_action))
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
        sql = "SELECT * FROM cost_center_name WHERE cost_center_name_id=%s"
        cursor.execute(sql,(data_new['cost_center_name_id']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action= "Edit"

        sqlIn_log = "INSERT INTO cost_center_name_log (cost_center_name_id,cost_detail,email,createby,type_action) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_log,(result[0]['cost_center_name_id'],result[0]['cost_detail'],result[0]['email'],data_new['createby'],type_action))

        sqlDe = "DELETE FROM cost_center_name WHERE cost_center_name_id=%s"
        cursor.execute(sqlDe,(data_new['cost_center_name_id']))

        sqlIn = "INSERT INTO cost_center_name (cost_center_name_id,cost_detail,email,createby) VALUES (%s,%s,%s,%s)"
        cursor.execute(sqlIn,(result[0]['cost_center_name_id'],data_new['cost_detail'],data_new['email'],data_new['createby']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryCost_center', methods=['POST'])
@connect_sql()
def QryCost_center(cursor):
    try:
        sql = "SELECT cost_center_name_id,cost_detail,email,id FROM cost_center_name"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/DeleteCost_center', methods=['POST'])
@connect_sql()
def DeleteCost_center(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT * FROM cost_center_name WHERE cost_center_name_id=%s"
        cursor.execute(sql,(data_new['cost_center_name_id']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action= "Delete"

        sqlIn_log = "INSERT INTO cost_center_name_log (cost_center_name_id,cost_detail,email,createby,type_action) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_log,(result[0]['cost_center_name_id'],result[0]['cost_detail'],result[0]['email'],data_new['createby'],type_action))

        sqlDe = "DELETE FROM cost_center_name WHERE cost_center_name_id=%s"
        cursor.execute(sqlDe,(data_new['cost_center_name_id']))
        
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
