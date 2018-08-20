#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/InsertEmployee_MD', methods=['POST'])
@connect_sql()
def InsertEmployee_MD(cursor):
    try:
        data = request.json
        source = data['source']
        data_new = source
        sqlQry = "SELECT employee_md_id FROM employee_MD ORDER BY employee_md_id DESC LIMIT 1"
        cursor.execute(sqlQry)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        employee_md_id_last=result[0]['employee_md_id']+1

        sql = "INSERT INTO employee_MD (employee_md_id,employeeid,company_id,name_md,surname_md,position,email_md) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(employee_md_id_last,data_new['employeeid'],data_new['company_id'],data_new['name_md'],data_new['surname_md'],data_new['position'],data_new['email_md']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee_MD', methods=['POST'])
@connect_sql()
def EditEmployee_MD(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sqlQry = "SELECT employee_md_id FROM employee_MD WHERE employee_md_id=%s"
        cursor.execute(sqlQry,data_new['employee_md_id'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sqlUp = "UPDATE employee_MD SET validstatus=0 WHERE employee_md_id=%s"
        cursor.execute(sqlUp,(data_new['employee_md_id']))

        sqlIn = "INSERT INTO employee_MD (employee_md_id,employeeid,company_id,name_md,surname_md,position,email_md) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn,(result[0]['employee_md_id'],data_new['employeeid'],data_new['company_id'],data_new['name_md'],data_new['surname_md'],data_new['position'],data_new['email_md']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryEmployee_MD', methods=['POST'])
@connect_sql()
def QryEmployee_MD(cursor):
    try:
        sql = "SELECT email_md,surname_md,name_md,employeeid,employee_md_id,company_id,position,id FROM employee_MD WHERE validstatus=1"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
