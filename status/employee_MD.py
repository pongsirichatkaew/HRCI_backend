#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/InsertEmployee_MD', methods=['POST'])
@connect_sql()
def InsertEmployee_MD(cursor):
    try:
        data = request.json
        employeeid = data['employeeid']
        name_md = data['name_md']
        surname_md = data['surname_md']
        email_md = data['email_md']
        sql = "INSERT INTO employee_MD (employeeid,name_md,surname_md,email_md) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql,(employeeid,name_md,surname_md,email_md))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee_MD', methods=['POST'])
@connect_sql()
def EditEmployee_MD(cursor):
    try:
        data = request.json
        id = data['id']
        employeeid = data['employeeid']
        name_md = data['name_md']
        surname_md = data['surname_md']
        email_md = data['email_md']
        sqlUp = "UPDATE employee_MD SET validstatus = '0' WHERE id=%s"
        cursor.execute(sqlUp,(id))
        sqlIn = "INSERT INTO employee_MD (employeeid,name_md,surname_md,email_md) VALUES (%s,%s,%s,%s)"
        cursor.execute(sqlIn,(employeeid,name_md,surname_md,email_md))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryEmployee_MD', methods=['POST'])
@connect_sql()
def QryEmployee_MD(cursor):
    try:
        sql = "SELECT email_md,surname_md,name_md,employeeid,id FROM employee_MD WHERE validstatus=1"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
