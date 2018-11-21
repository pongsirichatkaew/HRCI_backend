#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *
@app.route('/Insert_type_Question_pro', methods=['POST'])
@connect_sql()
def Insert_type_Question_pro(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sqlQry = "SELECT question_pro_id_type FROM question_pro_type ORDER BY question_pro_id_type DESC LIMIT 1"
        cursor.execute(sqlQry)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        question_pro_id_last_type=result[0]['question_pro_id_type']+1

        sql = "INSERT INTO question_pro_type (question_pro_id_type,question_pro_detail_type,createby) VALUES (%s,%s,%s)"
        cursor.execute(sql,(question_pro_id_last_type,data_new['question_pro_detail_type'],data_new['createby']))

        type_action = "ADD"

        sql_log = "INSERT INTO question_pro_log_type (question_pro_id_type,question_pro_detail_type,createby,type_action) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql_log,(question_pro_id_last_type,data_new['question_pro_detail_type'],data_new['createby'],type_action))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Edit_type_Question_pro', methods=['POST'])
@connect_sql()
def Edit_type_Question_pro(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT * FROM question_pro_type WHERE question_pro_id_type=%s"
        cursor.execute(sql,(data_new['question_pro_id_type']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Edit"

        sql_log = "INSERT INTO question_pro_log_type (question_pro_id_type,question_pro_detail_type,createby,type_action) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql_log,(result[0]['question_pro_id_type'],result[0]['question_pro_detail_type'],data_new['createby'],type_action))

        sqlUp = "DELETE FROM question_pro_type WHERE question_pro_id_type=%s"
        cursor.execute(sqlUp,(data_new['question_pro_id_type']))

        sqlIn = "INSERT INTO question_pro_type (question_pro_id_type,question_pro_detail_type,createby) VALUES (%s,%s,%s)"
        cursor.execute(sqlIn,(result[0]['question_pro_id_type'],data_new['question_pro_detail_type'],data_new['createby']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Delete_type_Question_pro', methods=['POST'])
@connect_sql()
def Delete_type_Question_pro(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT * FROM question_pro_type WHERE question_pro_id_type=%s"
        cursor.execute(sql,(data_new['question_pro_id_type']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Delete"

        sql_log = "INSERT INTO question_pro_log_type (question_pro_id_type,question_pro_detail_type,createby,type_action) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql_log,(result[0]['question_pro_id_type'],result[0]['question_pro_detail_type'],data_new['createby'],type_action))

        sqlUp = "DELETE FROM question_pro_type WHERE question_pro_id_type=%s"
        cursor.execute(sqlUp,(data_new['question_pro_id_type']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qry_type_Question_pro', methods=['POST'])
@connect_sql()
def Qry_type_Question_pro(cursor):
    try:
        sql = "SELECT question_pro_id_type,question_pro_detail_type FROM question_pro_type"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Insert_form_Question_pro', methods=['POST'])
@connect_sql()
def Insert_form_Question_pro(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        i=0
        for i in xrange(len(data_new['question_pro'])):
            try:
                sqlQry = "SELECT question_pro_id FROM question_pro_form ORDER BY question_pro_id DESC LIMIT 1"
                cursor.execute(sqlQry)
                columns = [column[0] for column in cursor.description]
                result = toJson(cursor.fetchall(),columns)
                question_pro_id_last=result[0]['question_pro_id']+1
            except Exception as e:
                question_pro_id_last = 1
            sql = "INSERT INTO question_pro_form (question_pro_id,question_pro_id_type,question_pro_detail,type_check,group_q,createby) VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,(question_pro_id_last,data_new['question_pro_id_type'],data_new['question_pro'][i]['question_pro_detail'],data_new['question_pro'][i]['type'],data_new['question_pro'][i]['group'],data_new['createby']))

            type_action = "ADD"

            sql_log = "INSERT INTO question_pro_log_form (question_pro_id,question_pro_id_type,question_pro_detail,type_check,group_q,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql_log,(question_pro_id_last,data_new['question_pro_id_type'],data_new['question_pro'][i]['question_pro_detail'],data_new['question_pro'][i]['type'],data_new['question_pro'][i]['group'],data_new['createby'],type_action))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Edit_form_Question_pro', methods=['POST'])
@connect_sql()
def Edit_form_Question_pro(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT * FROM question_pro_form WHERE question_pro_id=%s AND question_pro_id_type=%s"
        cursor.execute(sql,(data_new['question_pro_id'],data_new['question_pro_id_type']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Edit"

        sql_log = "INSERT INTO question_pro_log_form (question_pro_id,question_pro_id_type,question_pro_detail,type_check,createby,type_action) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(result[0]['question_pro_id'],result[0]['question_pro_id_type'],result[0]['question_pro_detail'],result[0]['type_check'],data_new['createby'],type_action))

        sqlUp = "UPDATE question_pro_form SET question_pro_id_type=%s,question_pro_detail=%s,type_check=%s,createby=%s WHERE question_pro_id=%s AND question_pro_id_type=%s"
        cursor.execute(sqlUp,(data_new['New_question_pro_id_type'],data_new['New_question_pro_detail'],data_new['New_type_check'],data_new['createby'],data_new['question_pro_id'],data_new['question_pro_id_type']))

        # sqlIn = "INSERT INTO question_pro_form (question_pro_id_type,question_pro_detail,type_check,createby) VALUES (%s,%s,%s,%s)"
        # cursor.execute(sqlIn,(data_new['New_question_pro_id_type'],data_new['New_question_pro_id'],data_new['New_type_check'],data_new['createby']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Delete_form_Question_pro', methods=['POST'])
@connect_sql()
def Delete_form_Question_pro(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT * FROM question_pro_form WHERE question_pro_id=%s AND question_pro_id_type=%s"
        cursor.execute(sql,(data_new['question_pro_id'],data_new['question_pro_id_type']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Delete"

        sql_log = "INSERT INTO question_pro_log_form (question_pro_id_type,question_pro_detail,type_check,createby,type_action) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(result[0]['question_pro_id_type'],result[0]['question_pro_detail'],result[0]['type_check'],result[0]['createby'],type_action))

        sqlUp = "UPDATE question_pro_form SET validstatus=0 WHERE question_pro_id=%s AND question_pro_id_type=%s"
        cursor.execute(sqlUp,(data_new['question_pro_id'],data_new['question_pro_id_type']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qry_form_Question_pro', methods=['POST'])
@connect_sql()
def Qry_form_Question_pro(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT question_pro_detail_type FROM question_pro_type WHERE question_pro_id_type=%s"
        cursor.execute(sql,(data_new['question_pro_id_type']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        for i1 in result:
            question = []
            sql1 = """  SELECT question_pro_detail,type_check,group_q FROM question_pro_form WHERE question_pro_id_type = %s AND validstatus=1 ORDER BY question_pro_id ASC"""
            cursor.execute(sql1,(data_new['question_pro_id_type']))
            columns = [column[0] for column in cursor.description]
            data2 = toJson(cursor.fetchall(),columns)
            for i2 in data2 :
                question.append(i2)
            i1['question'] = question
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
