#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/InsertPosition', methods=['POST'])
@connect_sql()
def InsertPosition(cursor):
    try:
        data = request.json
        position_id = data['position_id']
        position_detail = data['position_detail']
        sql = "INSERT INTO position (position_id,position_detail) VALUES (%s,%s)"
        cursor.execute(sql,(position_id,position_detail))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditPosition', methods=['POST'])
@connect_sql()
def EditPosition(cursor):
    try:
        data = request.json
        id = data['id']
        position_id = data['position_id']
        position_detail = data['position_detail']
        sqlUp = "UPDATE position SET validstatus = '0' WHERE id=%s"
        cursor.execute(sqlUp,(data['id']))
        sqlIn = "INSERT INTO position (position_id,position_detail) VALUES (%s,%s)"
        cursor.execute(sqlIn,(position_id,position_detail))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryPosition', methods=['POST'])
@connect_sql()
def QryPosition(cursor):
    try:
        sql = "SELECT position_id,position_detail,id FROM position WHERE validstatus=1"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
