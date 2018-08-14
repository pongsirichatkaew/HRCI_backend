#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/InsertSection', methods=['POST'])
@connect_sql()
def InsertSection(cursor):
    try:
        data = request.json
        source = data['source']
        data_new = source
        sect_id = data_new['sect_id']
        sect_detail = data_new['sect_detail']
        validstatus = data_new['validstatus']
        sql = "INSERT INTO section (sect_id,sect_detail,validstatus) VALUES (%s,%s,%s)"
        cursor.execute(sql,(sect_id,sect_detail,validstatus))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditSection', methods=['POST'])
@connect_sql()
def EditSection(cursor):
    try:
        data = request.json
        source = data['source']
        data_new = source
        id = data_new['id']
        sect_id = data_new['sect_id']
        sect_detail = data_new['sect_detail']
        validstatus = data_new['validstatus']
        sqlUp = "UPDATE section SET sect_id = %s, sect_detail = %s, validstatus = %s  WHERE id = %s"
        cursor.execute(sqlUp,(sect_id,sect_detail,validstatus,id))
        # sqlIn = "INSERT INTO section (sect_id,sect_detail) VALUES (%s,%s)"
        # cursor.execute(sqlIn,(sect_id,sect_detail))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QrySection', methods=['POST'])
@connect_sql()
def QrySection(cursor):
    try:
        sql = "SELECT sect_id,sect_detail,id,validstatus FROM section"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
