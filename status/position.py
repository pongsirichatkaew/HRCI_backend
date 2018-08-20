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
        cursor3.execute(sqlQry)
        columns = [column[0] for column in cursor3.description]
        result = toJson(cursor3.fetchall(),columns)
        position_id_last=result[0]['position_id']+1

        sql = "INSERT INTO position (position_id,position_detail) VALUES (%s,%s)"
        cursor3.execute(sql,(position_id_last,data_new['position_detail']))
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
        cursor3.execute(sql,(data_new['position_id']))
        columns = [column[0] for column in cursor3.description]
        result = toJson(cursor3.fetchall(),columns)

        sqlUp = "UPDATE position SET validstatus=0 WHERE status_id=%s"
        cursor3.execute(sqlUp,(data_new['position_id']))

        sqlIn = "INSERT INTO position (position_id,position_detail) VALUES (%s,%s)"
        cursor3.execute(sqlIn,(result[0]['position_id'],data_new['position_detail']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryPosition', methods=['POST'])
@connect_sql()
def QryPosition(cursor):
    try:
        sql = "SELECT position_id,position_detail FROM position WHERE validstatus = 1"
        cursor3.execute(sql)
        columns = [column[0] for column in cursor3.description]
        result = toJson(cursor3.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
