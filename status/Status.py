#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/InsertStatus', methods=['POST'])
@connect_sql()
def InsertStatus(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sqlQry = "SELECT status_id FROM status ORDER BY status_id DESC LIMIT 1"
        cursor.execute(sqlQry)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        status_id_last=result[0]['status_id']+1

        # sql = "INSERT INTO status (status_id,status_detail,path_color,font_color,createby) VALUES (%s,%s,%s,%s,%s)"
        # cursor3.execute(sql,(status_id_last,data_new['status_detail'],data_new['path_color'],data_new['font_color'],data_new['createby']))
        sql = "INSERT INTO status (status_id,status_detail,path_color,font_color) VALUES (%s,%s,%s,%s)"

        cursor.execute(sql,(status_id_last,data_new['status_detail'],data_new['path_color'],data_new['font_color']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditStatus', methods=['POST'])
@connect_sql()
def EditStatus(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT status_id FROM status WHERE status_id=%s"
        cursor.execute(sql,(data_new['status_id']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        # sqlUp = "UPDATE status SET validstatus=0 WHERE status_id=%s"
        # cursor.execute(sqlUp,(data_new['status_id']))
        # sqlIn = "INSERT INTO status (status_id,status_detail,path_color,font_color,createby) VALUES (%s,%s,%s,%s,%s)"
        # cursor.execute(sqlIn,(result[0]['status_id'],data_new['status_detail'],data_new['path_color'],data_new['font_color'],data_new['createby']))
        sqlUp = "UPDATE status SET validstatus=0 WHERE status_id=%s"
        cursor.execute(sqlUp,(data_new['status_id']))
        sqlIn = "INSERT INTO status (status_id,status_detail,path_color,font_color) VALUES (%s,%s,%s,%s)"
        cursor.execute(sqlIn,(result[0]['status_id'],data_new['status_detail'],data_new['path_color'],data_new['font_color']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryStatus', methods=['POST'])
@connect_sql()
def QryStatus(cursor):
    try:
        sql = "SELECT id,status_id,status_detail,path_color,id,font_color,validstatus FROM status WHERE validstatus = 1"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/DeleteStatus', methods=['POST'])
def DeleteStatus():
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        # sqlUp = "UPDATE status SET validstatus=0,createby=%s WHERE status_id=%s"
        # cursor.execute(sqlUp,(data_new['createby'],data_new['status_id']))

        sqlUp = "UPDATE status SET validstatus=0 WHERE status_id=%s"
        cursor.execute(sqlUp,(data_new['status_id']))

        sqlIn = "INSERT INTO status(status_id,status_detail,path_color,font_color,validstatus) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn,(data_new['status_id'],data_new['status_detail'],data_new['path_color'],data_new['font_color'],0))

        connection.commit()
        connection.close()
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/InsertStatus_Appform', methods=['POST'])
@connect_sql3()
def InsertStatus_Appform(cursor3):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sqlQry = "SELECT status_id FROM status_hrci ORDER BY status_id DESC LIMIT 1"
        cursor3.execute(sqlQry)
        columns = [column[0] for column in cursor3.description]
        result = toJson(cursor3.fetchall(),columns)
        status_id_last=result[0]['status_id']+1

        sql = "INSERT INTO status_hrci (status_id,status_detail,path_color,font_color) VALUES (%s,%s,%s,%s)"
        cursor3.execute(sql,(status_id_last,data_new['status_detail'],data_new['path_color'],data_new['font_color']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditStatus_Appform', methods=['POST'])
@connect_sql3()
def EditStatus_Appform(cursor3):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT status_id FROM status_hrci WHERE status_id=%s"
        cursor3.execute(sql,(data_new['status_id']))
        columns = [column[0] for column in cursor3.description]
        result = toJson(cursor3.fetchall(),columns)

        sqlUp = "UPDATE status_hrci SET validstatus=0 WHERE status_id=%s"
        cursor3.execute(sqlUp,(data_new['status_id']))
        sqlIn = "INSERT INTO status_hrci (status_id,status_detail,path_color,font_color) VALUES (%s,%s,%s,%s)"
        cursor3.execute(sqlIn,(result[0]['status_id'],data_new['status_detail'],data_new['path_color'],data_new['font_color']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryStatus_Appform', methods=['POST'])
@connect_sql3()
def QryStatus_Appform(cursor3):
    try:
        sql = "SELECT id,status_id,status_detail,path_color,font_color,validstatus FROM status_hrci WHERE validstatus = 1"
        cursor3.execute(sql)
        columns = [column[0] for column in cursor3.description]
        result = toJson(cursor3.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/DeleteStatus_Appform', methods=['POST'])
@connect_sql3()
def DeleteStatus_Appform(cursor3):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql_OldTimeStatus = "UPDATE status_hrci SET validstatus=0 WHERE status_id=%s"
        cursor3.execute(sql_OldTimeStatus,(data_new['status_id']))

        sql_NewTimeStatus = "INSERT INTO status_hrci (status_id,status_detail,path_color,font_color,validstatus) VALUES (%s,%s,%s,%s,%s)"
        cursor3.execute(sql_NewTimeStatus,(data_new['status_id'],data_new['status_detail'],data_new['path_color'],data_new['font_color'],0))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
