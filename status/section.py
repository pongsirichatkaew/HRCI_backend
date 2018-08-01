#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/InsertSection', methods=['POST'])
@connect_sql()
def InsertSection(cursor):
    try:
        data = request.json
        sect_id = data['sect_id']
        sect_detail = data['sect_detail']
        sql = "INSERT INTO section (sect_id,sect_detail) VALUES (%s,%s)"
        cursor.execute(sql,(sect_id,sect_detail))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditSection', methods=['POST'])
@connect_sql()
def EditSection(cursor):
    try:
        data = request.json
        id = data['id']
        sect_id = data['sect_id']
        sect_detail = data['sect_detail']
        sqlUp = "UPDATE section SET validstatus = '0' WHERE id=%s"
        cursor.execute(sqlUp,(data['id']))
        sqlIn = "INSERT INTO section (sect_id,sect_detail) VALUES (%s,%s)"
        cursor.execute(sqlIn,(sect_id,sect_detail))
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
