#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/InsertStatus', methods=['POST'])
@connect_sql()
def InsertStatus(cursor):
    try:
        data = request.json
        status_detail = data['status_detail']
        path_color = data['path_color']
        sql = "INSERT INTO status (status_detail,path_color) VALUES (%s,%s)"
        cursor.execute(sql,(status_detail,path_color))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditStatus', methods=['POST'])
@connect_sql()
def EditStatus(cursor):
    try:
        data = request.json
        id = data['id']
        status_detail = data['status_detail']
        path_color = data['path_color']
        sqlUp = "UPDATE status SET validstatus = '0' WHERE id=%s"
        cursor.execute(sqlUp,(data['id']))
        sqlIn = "INSERT INTO status (status_detail,path_color) VALUES (%s,%s)"
        cursor.execute(sqlIn,(status_detail,path_color))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryStatus', methods=['POST'])
@connect_sql()
def QryStatus(cursor):
    try:
        sql = "SELECT status_detail,path_color,id FROM status WHERE validstatus=1"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
