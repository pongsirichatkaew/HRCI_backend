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
        sqlUp = "UPDATE status SET valid = %s WHERE id = %s"
        cursor.execute(sqlUp,('0', id))
        sqlIn = "INSERT INTO status (status_detail,path_color,font_color,validstatus) VALUES (%s,%s,%s,%s)"
        cursor.execute(sqlIn,(status_detail,path_color,font_color,validstatus))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryStatus', methods=['POST'])
@connect_sql()
def QryStatus(cursor):
    try:
        sql = "SELECT id,status_detail,path_color,id,font_color,validstatus FROM status WHERE valid = 1"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/InsertStatus_Appform', methods=['POST'])
@connect_sql3()
def InsertStatus_Appform(cursor3):
    try:
        dataInput = request.json
        sqlQry = "SELECT status_id FROM status_hrci ORDER BY status_id DESC LIMIT 1"
        cursor3.execute(sqlQry)
        columns = [column[0] for column in cursor3.description]
        result = toJson(cursor3.fetchall(),columns)
        status_id_last=result[0]['status_id']+1

        sql = "INSERT INTO status_hrci (status_id,status_detail,path_color,font_color) VALUES (%s,%s,%s,%s)"
        cursor3.execute(sql,(status_id_last,dataInput['status_detail'],dataInput['path_color'],dataInput['font_color']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditStatus_Appform', methods=['POST'])
@connect_sql3()
def EditStatus_Appform(cursor3):
    try:
        dataInput = request.json
        sql = "SELECT status_id FROM status_hrci WHERE status_id=%s"
        cursor3.execute(sql,(dataInput['status_id']))
        columns = [column[0] for column in cursor3.description]
        result = toJson(cursor3.fetchall(),columns)

        sqlUp = "UPDATE status_hrci SET validstatus=0 WHERE status_id=%s"
        cursor3.execute(sqlUp,(dataInput['status_id']))

        sqlIn = "INSERT INTO status_hrci (status_id,status_detail,path_color,font_color) VALUES (%s,%s,%s,%s)"
        cursor3.execute(sqlIn,(result[0]['status_id'],dataInput['status_detail'],dataInput['path_color'],dataInput['font_color']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryStatus_Appform', methods=['POST'])
@connect_sql3()
def QryStatus_Appform(cursor3):
    try:
        sql = "SELECT status_id,status_detail,path_color,font_color FROM status_hrci WHERE validstatus = 1"
        cursor3.execute(sql)
        columns = [column[0] for column in cursor3.description]
        result = toJson(cursor3.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
