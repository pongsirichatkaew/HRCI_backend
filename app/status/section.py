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

        sql = "INSERT INTO section (sect_id,sect_detail,createby) VALUES (%s,%s,%s)"
        cursor.execute(sql,(sect_id_last,data_new['sect_detail'],data_new['createby']))

        type_action = "ADD"

        sql_log = "INSERT INTO section_log (sect_id,sect_detail,createby,type_action) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql_log,(sect_id_last,data_new['sect_detail'],data_new['createby'],type_action))
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

        sql = "SELECT sect_id,sect_detail FROM section WHERE sect_id=%s"
        cursor.execute(sql,(data_new['sect_id']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Edit"

        sql_log = "INSERT INTO section_log (sect_id,sect_detail,createby,type_action) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql_log,(result[0]['sect_id'],result[0]['sect_detail'],data_new['createby'],type_action))

        sqlUp = "DELETE FROM section WHERE sect_id=%s"
        cursor.execute(sqlUp,(data_new['sect_id']))

        sqlIn = "INSERT INTO section (sect_id,sect_detail,createby) VALUES (%s,%s,%s)"
        cursor.execute(sqlIn,(result[0]['sect_id'],data_new['sect_detail'],data_new['createby']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QrySection', methods=['POST'])
@connect_sql()
def QrySection(cursor):
    try:
        sql = "SELECT sect_id,sect_detail,id FROM section"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/DeleteSection', methods=['POST'])
@connect_sql()
def DeleteSection(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT sect_id,sect_detail FROM section WHERE sect_id=%s"
        cursor.execute(sql,(data_new['sect_id']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Delete"

        sql_log = "INSERT INTO section_log (sect_id,sect_detail,createby,type_action) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql_log,(result[0]['sect_id'],result[0]['sect_detail'],data_new['createby'],type_action))

        sqlUp = "DELETE FROM section WHERE sect_id=%s"
        cursor.execute(sqlUp,(data_new['sect_id']))

        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
