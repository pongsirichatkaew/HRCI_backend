#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/InsertEmployee_Deputy_Manager_PayRoll', methods=['POST'])
@connect_sql()
def InsertEmployee_Deputy_Manager_PayRoll(cursor):
    try:
        data = request.json
        source = data['source']
        data_new = source
        employeeid = data_new['employeeid']
        name_Deputy_Manager_PayRoll = data_new['name_Deputy_Manager_PayRoll']
        surname_Deputy_Manager_PayRoll = data_new['surname_Deputy_Manager_PayRoll']
        email_Deputy_Manager_PayRoll = data_new['email_Deputy_Manager_PayRoll']
        validstatus = data_new['validstatus']
        position_Deputy_Manager_PayRoll = data_new['position_Deputy_Manager_PayRoll']
        sql = "INSERT INTO employee_Deputy_Manager_PayRoll (employeeid,name_Deputy_Manager_PayRoll,surname_Deputy_Manager_PayRoll,email_Deputy_Manager_PayRoll,validstatus,position_Deputy_Manager_PayRoll) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(employeeid,name_Deputy_Manager_PayRoll,surname_Deputy_Manager_PayRoll,email_Deputy_Manager_PayRoll,validstatus,position_Deputy_Manager_PayRoll))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee_Deputy_Manager_PayRoll', methods=['POST'])
@connect_sql()
def EditEmployee_Deputy_Manager_PayRoll(cursor):
    try:
        data = request.json
        source = data['source']
        data_new = source
        id = data_new['id']
        employeeid = data_new['employeeid']
        name_Deputy_Manager_PayRoll = data_new['name_Deputy_Manager_PayRoll']
        surname_Deputy_Manager_PayRoll = data_new['surname_Deputy_Manager_PayRoll']
        email_Deputy_Manager_PayRoll = data_new['email_Deputy_Manager_PayRoll']
        position_Deputy_Manager_PayRoll = data_new['position_Deputy_Manager_PayRoll']
        validstatus = data_new['validstatus']
        sqlUp = "UPDATE employee_Deputy_Manager_PayRoll SET employeeid = %s, name_Deputy_Manager_PayRoll = %s, surname_Deputy_Manager_PayRoll = %s,email_Deputy_Manager_PayRoll = %s,position_Deputy_Manager_PayRoll = %s,validstatus = %s WHERE id = %s"
        cursor.execute(sqlUp,(employeeid, name_Deputy_Manager_PayRoll, surname_Deputy_Manager_PayRoll, email_Deputy_Manager_PayRoll, position_Deputy_Manager_PayRoll, validstatus, id))
        # sqlIn = "INSERT INTO employee_Deputy_Manager_PayRoll (employeeid,name_Deputy_Manager_PayRoll,surname_Deputy_Manager_PayRoll,email_Deputy_Manager_PayRoll) VALUES (%s,%s)"
        # cursor.execute(sqlIn,(employeeid,name_Deputy_Manager_PayRoll,surname_Deputy_Manager_PayRoll,email_Deputy_Manager_PayRoll))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryEmployee_Deputy_Manager_PayRoll', methods=['POST'])
@connect_sql()
def QryEmployee_Deputy_Manager_PayRoll(cursor):
    try:
        sql = "SELECT id,employeeid,name_Deputy_Manager_PayRoll,surname_Deputy_Manager_PayRoll,email_Deputy_Manager_PayRoll,id,validstatus,position_Deputy_Manager_PayRoll FROM employee_Deputy_Manager_PayRoll"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
