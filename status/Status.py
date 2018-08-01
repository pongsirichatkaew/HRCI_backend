#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/InsertStatus', methods=['POST'])
@connect_sql()
def InsertStatus(cursor):
    try:
        data = request.json
        source = data['source']
        data_new = source
        status_detail = data_new['status_detail']
        path_color = data_new['path_color']
        font_color = data_new['font_color']
        validstatus = data_new['active']
        sql = "INSERT INTO status (status_detail,path_color,font_color,validstatus) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql,(status_detail,path_color,font_color,validstatus))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditStatus', methods=['POST'])
@connect_sql()
def EditStatus(cursor):
    try:
        data = request.json
        source = data['source']
        data_new = source
        id = data_new['statusId']
        status_detail = data_new['status_detail']
        path_color = data_new['path_color']
        font_color = data_new['font_color']
        validstatus = data_new['active']
        # sqlUp = "UPDATE status SET validstatus = '1' WHERE id=%s"
        # cursor.execute(sqlUp,(data['id']))
        sqlUp = "UPDATE status SET status_detail = %s, path_color = %s, font_color = %s, validstatus = %s WHERE id = %s"
        cursor.execute(sqlUp,(status_detail, path_color, font_color, validstatus, id))
        # sqlIn = "INSERT INTO status (status_detail,path_color,font_color) VALUES (%s,%s,%s)"
        # cursor.execute(sqlIn,(status_detail,path_color,font_color))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryStatus', methods=['POST'])
@connect_sql()
def QryStatus(cursor):
    try:
        sql = "SELECT id,status_detail,path_color,id,font_color,validstatus FROM status"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryStatusAppForm', methods=['POST'])
@connect_sql()
def QryStatusAppForm(cursor):
    try:
        sql = "SELECT id,status_detail,path_color,id,font_color FROM status WHERE validstatus = 1"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
