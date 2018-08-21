#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/InsertPosition', methods=['POST'])
@connect_sql()
def InsertPosition(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sqlQry = "SELECT position_id FROM position ORDER BY position_id DESC LIMIT 1"
        cursor.execute(sqlQry)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        position_id_last=result[0]['position_id']+1

        sql = "INSERT INTO position (position_id,position_detail,createby) VALUES (%s,%s,%s)"
        cursor.execute(sql,(position_id_last,data_new['position_detail'],data_new['createby']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditPosition', methods=['POST'])
@connect_sql()
def EditPosition(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT position_id FROM position WHERE position_id=%s"
        cursor.execute(sql,(data_new['position_id']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sqlUp = "UPDATE position SET validstatus=0 WHERE position_id=%s"
        cursor.execute(sqlUp,(data_new['position_id']))

        sqlIn = "INSERT INTO position (position_id,position_detail,createby) VALUES (%s,%s,%s)"
        cursor.execute(sqlIn,(result[0]['position_id'],data_new['position_detail'],data_new['createby']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryPosition', methods=['POST'])
@connect_sql()
def QryPosition(cursor):
    try:
        sql = "SELECT position_id,position_detail FROM position WHERE validstatus = 1"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/DeletePosition', methods=['POST'])
@connect_sql()
def DeletePosition(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql_OldTimePosition = "UPDATE position SET validstatus=0,createby=%s WHERE position_id=%s"
        cursor.execute(sql_OldTimePosition,(data_new['createby'],data_new['position_id']))

        sql_NewTimePosition = "INSERT INTO position (position_id,position_detail,validstatus,createby) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql_NewTimePosition,(data_new['position_id'],data_new['position_detail'],0,data_new['createby']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
