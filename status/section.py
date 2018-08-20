#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/InsertSection', methods=['POST'])
@connect_sql()
def InsertSection(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sqlQry = "SELECT sect_id FROM section ORDER BY sect_id DESC LIMIT 1"
        cursor.execute(sqlQry)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        sect_id_last=result[0]['sect_id']+1

        sql = "INSERT INTO section (sect_id,sect_detail) VALUES (%s,%s)"
        cursor.execute(sql,(sect_id_last,data_new['sect_detail']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditSection', methods=['POST'])
@connect_sql()
def EditSection(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT sect_id FROM section WHERE sect_id=%s"
        cursor.execute(sql,(data_new['sect_id']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sqlUp = "UPDATE section SET validstatus=0 WHERE sect_id=%s"
        cursor.execute(sqlUp,(data_new['sect_id']))

        sqlIn = "INSERT INTO section (sect_id,sect_detail) VALUES (%s,%s)"
        cursor.execute(sqlIn,(result[0]['sect_id'],data_new['sect_detail']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QrySection', methods=['POST'])
@connect_sql()
def QrySection(cursor):
    try:
        sql = "SELECT sect_id,sect_detail,id FROM section WHERE validstatus=1"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
