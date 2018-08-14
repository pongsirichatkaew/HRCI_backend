#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/InsertPosition', methods=['POST'])
@connect_sql()
def InsertPosition(cursor):
    try:
        data = request.json
        source = data['source']
        data_new = source
        position_id = data_new['position_id']
        position_detail = data_new['position_detail']
        validstatus = data_new['validstatus']
        sql = "INSERT INTO position (position_id,position_detail,validstatus) VALUES (%s,%s,%s)"
        cursor.execute(sql,(position_id,position_detail,validstatus))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditPosition', methods=['POST'])
@connect_sql()
def EditPosition(cursor):
    try:
        data = request.json
        source = data['source']
        data_new = source
        id = data_new['id']
        position_id = data_new['position_id']
        position_detail = data_new['position_detail']
        validstatus = data_new['validstatus']
        sqlUp = "UPDATE position SET position_id = %s, position_detail = %s, validstatus = %s WHERE id = %s"
        cursor.execute(sqlUp,(position_id, position_detail, validstatus, id))
        # sqlIn = "INSERT INTO position (position_id,position_detail) VALUES (%s,%s)"
        # cursor.execute(sqlIn,(position_id,position_detail))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryPosition', methods=['POST'])
@connect_sql()
def QryPosition(cursor):
    try:
        sql = "SELECT position_id,position_detail,id,validstatus FROM position"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
