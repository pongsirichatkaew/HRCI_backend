#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/InsertEmployee_Deputy_Manager_PayRoll', methods=['POST'])
@connect_sql()
def InsertEmployee_Deputy_Manager_PayRoll(cursor):
    try:
        data = request.json
        employeeid = data['employeeid']
        name_Deputy_Manager_PayRoll = data['name_Deputy_Manager_PayRoll']
        surname_Deputy_Manager_PayRoll = data['surname_Deputy_Manager_PayRoll']
        email_Deputy_Manager_PayRoll = data['email_Deputy_Manager_PayRoll']
        sql = "INSERT INTO employee_Deputy_Manager_PayRoll (position_id,position_detail) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql,(employeeid,name_Deputy_Manager_PayRoll,surname_Deputy_Manager_PayRoll,email_Deputy_Manager_PayRoll))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee_Deputy_Manager_PayRoll', methods=['POST'])
@connect_sql()
def EditEmployee_Deputy_Manager_PayRoll(cursor):
    try:
        data = request.json
        id = data['id']
        employeeid = data['employeeid']
        name_Deputy_Manager_PayRoll = data['name_Deputy_Manager_PayRoll']
        surname_Deputy_Manager_PayRoll = data['surname_Deputy_Manager_PayRoll']
        email_Deputy_Manager_PayRoll = data['email_Deputy_Manager_PayRoll']
        sqlUp = "UPDATE employee_Deputy_Manager_PayRoll SET validstatus = '0' WHERE id=%s"
        cursor.execute(sqlUp,(data['id']))
        sqlIn = "INSERT INTO employee_Deputy_Manager_PayRoll (employeeid,name_Deputy_Manager_PayRoll,surname_Deputy_Manager_PayRoll,email_Deputy_Manager_PayRoll) VALUES (%s,%s)"
        cursor.execute(sqlIn,(employeeid,name_Deputy_Manager_PayRoll,surname_Deputy_Manager_PayRoll,email_Deputy_Manager_PayRoll))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryEmployee_Deputy_Manager_PayRoll', methods=['POST'])
@connect_sql()
def QryEmployee_Deputy_Manager_PayRoll(cursor):
    try:
        sql = "SELECT employeeid,name_Deputy_Manager_PayRoll,surname_Deputy_Manager_PayRoll,email_Deputy_Manager_PayRoll,id FROM employee_Deputy_Manager_PayRoll WHERE validstatus=1"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
