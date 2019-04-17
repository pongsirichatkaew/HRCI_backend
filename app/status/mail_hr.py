#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/Insertmail_hr', methods=['POST'])
@connect_sql()
def Insertmail_hr(cursor):
    try:
        data = request.json
        source = data['source']
        data_new = source

        try:
            sql44 = "SELECT name_hr FROM mail_hr WHERE employeeid=%s"
            cursor.execute(sql44,(data_new['employeeid']))
            columns = [column[0] for column in cursor.description]
            result_test = toJson(cursor.fetchall(),columns)
            name_test = result_test[0]['name_hr']
            return "employee is duplicate"
        except Exception as e:
            pass

        sqlQry = "SELECT mail_hr_id FROM mail_hr ORDER BY mail_hr_id DESC LIMIT 1"
        cursor.execute(sqlQry)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        try:
            mail_hr_id_last=result[0]['mail_hr_id']+1
        except Exception as e:
            mail_hr_id_last = 1 

        sql = "INSERT INTO mail_hr (mail_hr_id,employeeid,name_hr,surname_hr,nickname,phone,email_hr,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(mail_hr_id_last,data_new['employeeid'],data_new['name_hr'],data_new['surname_hr'],data_new['nickname'],data_new['phone'],data_new['email_hr'],data_new['createby']))

        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Editmail_hr', methods=['POST'])
@connect_sql()
def Editmail_hr(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sqlUp = "DELETE FROM mail_hr WHERE mail_hr_id=%s"
        cursor.execute(sqlUp,(data_new['mail_hr_id']))

        sqlIn = "INSERT INTO mail_hr (mail_hr_id,employeeid,name_hr,surname_hr,nickname,phone,email_hr,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn,(data_new['mail_hr_id'],data_new['employeeid'],data_new['name_hr'],data_new['surname_hr'],data_new['nickname'],data_new['phone'],data_new['email_hr'],data_new['createby']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qrymail_hr', methods=['POST'])
@connect_sql()
def Qrymail_hr(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT mail_hr_id,employeeid,name_hr,surname_hr,phone,nickname,email_hr FROM mail_hr WHERE employeeid=%s"
        cursor.execute(sql, (data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Deletemail_hr', methods=['POST'])
@connect_sql()
def Deletemail_hr(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sqlUp = "DELETE FROM mail_hr WHERE mail_hr_id=%s"
        cursor.execute(sqlUp,(data_new['mail_hr_id']))

        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
