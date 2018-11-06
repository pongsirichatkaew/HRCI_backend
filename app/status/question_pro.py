#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/InsertQuestion_pro', methods=['POST'])
@connect_sql()
def InsertQuestion_pro(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sqlQry = "SELECT question_pro_id FROM question_pro ORDER BY question_pro_id DESC LIMIT 1"
        cursor.execute(sqlQry)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        question_pro_id_last=result[0]['question_pro_id']+1

        sql = "INSERT INTO question_pro (question_pro_id,question_pro_detail,type_question_pro,createby) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql,(question_pro_id_last,data_new['question_pro_detail'],data_new['type_question_pro'],data_new['createby']))

        type_action = "ADD"

        sql_log = "INSERT INTO question_pro_log (question_pro_id,question_pro_detail,type_question_pro,createby,type_action) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(question_pro_id_last,data_new['question_pro_detail'],data_new['type_question_pro'],data_new['createby'],type_action))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditQuestion_pro', methods=['POST'])
@connect_sql()
def EditQuestion_pro(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT * FROM question_pro WHERE question_pro_id=%s"
        cursor.execute(sql,(data_new['question_pro_id']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Edit"

        sql_log = "INSERT INTO question_pro_log (question_pro_id,question_pro_detail,type_question_pro,createby,type_action) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(result[0]['question_pro_id'],result[0]['question_pro_detail'],result[0]['type_question_pro'],data_new['createby'],type_action))

        sqlUp = "DELETE FROM question_pro WHERE question_pro_id=%s"
        cursor.execute(sqlUp,(data_new['question_pro_id']))

        sqlIn = "INSERT INTO question_pro (question_pro_id,question_pro_detail,type_question_pro,createby) VALUES (%s,%s,%s,%s)"
        cursor.execute(sqlIn,(result[0]['question_pro_id'],data_new['question_pro_detail'],data_new['type_question_pro'],data_new['createby']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/DeleteQuestion_pro', methods=['POST'])
@connect_sql()
def DeleteQuestion_pro(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT * FROM question_pro WHERE question_pro_id=%s"
        cursor.execute(sql,(data_new['question_pro_id']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Delete"

        sql_log = "INSERT INTO question_pro_log (question_pro_id,question_pro_detail,type_question_pro,createby,type_action) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(result[0]['question_pro_id'],result[0]['question_pro_detail'],result[0]['type_question_pro'],data_new['createby'],type_action))

        sqlUp = "DELETE FROM question_pro WHERE question_pro_id=%s"
        cursor.execute(sqlUp,(data_new['question_pro_id']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryQuestion_pro', methods=['POST'])
@connect_sql()
def QryQuestion_pro(cursor):
    try:
        sql = "SELECT question_pro_id,question_pro_detail,type_question_pro FROM question_pro"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
