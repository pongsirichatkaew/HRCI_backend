#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/InsertEmployee_Deputy_Manager_Hr', methods=['POST'])
@connect_sql()
def InsertEmployee_Deputy_Manager_Hr(cursor):
    try:
        data = request.json
        employeeid = data['employeeid']
        name_Deputy_Manager_Hr = data['name_Deputy_Manager_Hr']
        surname_Deputy_Manager_Hr = data['surname_Deputy_Manager_Hr']
        email_Deputy_Manager_Hr = data['email_Deputy_Manager_Hr']
        sql = "INSERT INTO employee_Deputy_Manager_Hr (employeeid,name_Deputy_Manager_Hr,surname_Deputy_Manager_Hr,email_Deputy_Manager_Hr) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql,(employeeid,name_Deputy_Manager_Hr,surname_Deputy_Manager_Hr,email_Deputy_Manager_Hr))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee_Deputy_Manager_Hr', methods=['POST'])
@connect_sql()
def EditEmployee_Deputy_Manager_Hr(cursor):
    try:
        data = request.json
        id = data['id']
        employeeid = data['employeeid']
        name_Deputy_Manager_Hr = data['name_Deputy_Manager_Hr']
        surname_Deputy_Manager_Hr = data['surname_Deputy_Manager_Hr']
        email_Deputy_Manager_Hr = data['email_Deputy_Manager_Hr']
        sqlUp = "UPDATE employee_Deputy_Manager_Hr SET validstatus = '0' WHERE id=%s"
        cursor.execute(sqlUp,(data['id']))
        sqlIn = "INSERT INTO employee_Deputy_Manager_Hr (employeeid,name_Deputy_Manager_Hr,surname_Deputy_Manager_Hr,email_Deputy_Manager_Hr) VALUES (%s,%s,%s,%s)"
        cursor.execute(sqlIn,(employeeid,name_Deputy_Manager_Hr,surname_Deputy_Manager_Hr,email_Deputy_Manager_Hr))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryEmployee_Deputy_Manager_Hr', methods=['POST'])
@connect_sql()
def QryEmployee_Deputy_Manager_Hr(cursor):
    try:
        sql = "SELECT employeeid,name_Deputy_Manager_Hr,surname_Deputy_Manager_Hr,email_Deputy_Manager_Hr,id FROM employee_Deputy_Manager_Hr WHERE validstatus=1"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
