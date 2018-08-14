#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/InsertEmployee_Deputy_Manager_Hr', methods=['POST'])
@connect_sql()
def InsertEmployee_Deputy_Manager_Hr(cursor):
    try:
        data = request.json
        source = data['source']
        data_new = source
        employeeid = data_new['employeeid']
        name_Deputy_Manager_Hr = data_new['name_Deputy_Manager_Hr']
        surname_Deputy_Manager_Hr = data_new['surname_Deputy_Manager_Hr']
        email_Deputy_Manager_Hr = data_new['email_Deputy_Manager_Hr']
        position_Deputy_Manager_Hr = data_new['position_Deputy_Manager_Hr']
        validstatus = data_new['validstatus']
        sql = "INSERT INTO employee_Deputy_Manager_Hr (employeeid,name_Deputy_Manager_Hr,surname_Deputy_Manager_Hr,email_Deputy_Manager_Hr,validstatus,position_Deputy_Manager_Hr) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(employeeid,name_Deputy_Manager_Hr,surname_Deputy_Manager_Hr,email_Deputy_Manager_Hr,validstatus,position_Deputy_Manager_Hr))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee_Deputy_Manager_Hr', methods=['POST'])
@connect_sql()
def EditEmployee_Deputy_Manager_Hr(cursor):
    try:
        data = request.json
        source = data['source']
        data_new = source
        id = data_new['id']
        employeeid = data_new['employeeid']
        name_Deputy_Manager_Hr = data_new['name_Deputy_Manager_Hr']
        surname_Deputy_Manager_Hr = data_new['surname_Deputy_Manager_Hr']
        position_Deputy_Manager_Hr = data_new['position_Deputy_Manager_Hr']
        email_Deputy_Manager_Hr = data_new['email_Deputy_Manager_Hr']
        validstatus = data_new['validstatus']
        sqlUp = "UPDATE employee_Deputy_Manager_Hr SET employeeid = %s, name_Deputy_Manager_Hr = %s, surname_Deputy_Manager_Hr = %s,email_Deputy_Manager_Hr = %s,position_Deputy_Manager_Hr = %s,validstatus = %s WHERE id = %s"
        cursor.execute(sqlUp,(employeeid, name_Deputy_Manager_Hr, surname_Deputy_Manager_Hr, email_Deputy_Manager_Hr, position_Deputy_Manager_Hr, validstatus, id))
        # sqlIn = "INSERT INTO employee_Deputy_Manager_Hr (employeeid,name_Deputy_Manager_Hr,surname_Deputy_Manager_Hr,email_Deputy_Manager_Hr) VALUES (%s,%s,%s,%s)"
        # cursor.execute(sqlIn,(employeeid,name_Deputy_Manager_Hr,surname_Deputy_Manager_Hr,email_Deputy_Manager_Hr))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryEmployee_Deputy_Manager_Hr', methods=['POST'])
@connect_sql()
def QryEmployee_Deputy_Manager_Hr(cursor):
    try:
        sql = "SELECT employeeid,name_Deputy_Manager_Hr,surname_Deputy_Manager_Hr,email_Deputy_Manager_Hr,id,validstatus,position_Deputy_Manager_Hr FROM employee_Deputy_Manager_Hr"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
