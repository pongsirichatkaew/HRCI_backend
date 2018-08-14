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
        employeeid = data_new['employeeid']
        name_md = data_new['name_md']
        surname_md = data_new['surname_md']
        email_md = data_new['email_md']
        position = data_new['position']
        validstatus = data_new['validstatus']
        sql = "INSERT INTO employee_MD (employeeid,name_md,surname_md,email_md,validstatus,position) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(employeeid,name_md,surname_md,email_md,validstatus,position))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee_MD', methods=['POST'])
@connect_sql()
def EditEmployee_MD(cursor):
    try:
        data = request.json
        source = data['source']
        data_new = source
        id = data_new['id']
        employeeid = data_new['employeeid']
        name_md = data_new['name_md']
        surname_md = data_new['surname_md']
        position = data_new['position']
        email_md = data_new['email_md']
        validstatus = data_new['validstatus']
        sqlUp = "UPDATE employee_MD SET employeeid = %s,name_md  = %s,surname_md  = %s,email_md  = %s,validstatus  = %s,position  = %s  WHERE id=%s"
        cursor.execute(sqlUp,(employeeid,name_md,surname_md,email_md,validstatus,position,id))
        # sqlIn = "INSERT INTO employee_MD (employeeid,name_md,surname_md,email_md) VALUES (%s,%s,%s,%s)"
        # cursor.execute(sqlIn,(employeeid,name_md,surname_md,email_md))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryEmployee_MD', methods=['POST'])
@connect_sql()
def QryEmployee_MD(cursor):
    try:
        sql = "SELECT email_md,surname_md,name_md,employeeid,id,validstatus,position FROM employee_MD"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
