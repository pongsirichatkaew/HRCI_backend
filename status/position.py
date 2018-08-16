#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/InsertPosition', methods=['POST'])
@connect_sql()
def InsertPosition(cursor):
    try:
        data = request.json
        # source = data['source']
        # data_new = source
        # position_detail = data_new['position_detail']
        #Gen position_id________________________________________________________
        sql_last_position_id = "SELECT position_id FROM position WHERE validstatus = 1 ORDER BY position_id DESC LIMIT 1"
        cursor.execute(sql_last_position_id)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        last_position2 = int(result[0]['position_id'])+1
        # if   last_position2<=9:
        #      last_position2=str(last_position2)
        #      last_position2="00"+last_position2
        # elif last_position2<=99:
        #      last_position2=str(last_position2)
        #      last_position2="0"+last_position2
        # else:
        #      last_position2=str(last_position2)
        # sql_insert_position = "INSERT INTO position (position_id,position_detail) VALUES (%s,%s)"
        # cursor.execute(sql_insert_position,(new_position_id,position_detail))
        return jsonify(last_position2)

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
        sql = "SELECT position_id,position_detail,id FROM position WHERE validstatus =1"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
