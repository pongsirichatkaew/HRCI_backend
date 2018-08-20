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
        sqlQry = "SELECT employee_Deputy_Manager_Hr_id FROM employee_Deputy_Manager_Hr ORDER BY employee_Deputy_Manager_Hr_id DESC LIMIT 1"
        cursor.execute(sqlQry)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        employee_Deputy_Manager_Hr_id_last=result[0]['employee_Deputy_Manager_Hr_id']+1

        sql = "INSERT INTO employee_Deputy_Manager_Hr (employee_Deputy_Manager_Hr_id,employeeid,company_id,name_Deputy_Manager_Hr,surname_Deputy_Manager_Hr,position_Deputy_Manager_Hr,email_Deputy_Manager_Hr) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(employee_Deputy_Manager_Hr_id_last,data_new['employeeid'],data_new['company_id'],data_new['name_Deputy_Manager_Hr'],data_new['surname_Deputy_Manager_Hr'],data_new['position_Deputy_Manager_Hr'],data_new['email_Deputy_Manager_Hr']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee_Deputy_Manager_Hr', methods=['POST'])
@connect_sql()
def EditEmployee_Deputy_Manager_Hr(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sqlQry = "SELECT employee_Deputy_Manager_Hr_id FROM employee_Deputy_Manager_Hr WHERE employee_Deputy_Manager_Hr_id=%s"
        cursor.execute(sqlQry,data_new['employee_Deputy_Manager_Hr_id'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sqlUp = "UPDATE employee_Deputy_Manager_Hr SET validstatus=0 WHERE employee_Deputy_Manager_Hr_id=%s"
        cursor.execute(sqlUp,(data_new['employee_Deputy_Manager_Hr_id']))

        sql = "INSERT INTO employee_Deputy_Manager_Hr (employee_Deputy_Manager_Hr_id,employeeid,company_id,name_Deputy_Manager_Hr,surname_Deputy_Manager_Hr,position_Deputy_Manager_Hr,email_Deputy_Manager_Hr) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(result[0]['employee_Deputy_Manager_Hr_id'],data_new['employeeid'],data_new['company_id'],data_new['name_Deputy_Manager_Hr'],data_new['surname_Deputy_Manager_Hr'],data_new['position_Deputy_Manager_Hr'],data_new['email_Deputy_Manager_Hr']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryEmployee_Deputy_Manager_Hr', methods=['POST'])
@connect_sql()
def QryEmployee_Deputy_Manager_Hr(cursor):
    try:
        sql = "SELECT employee_Deputy_Manager_Hr_id,companyid,employeeid,name_Deputy_Manager_Hr,surname_Deputy_Manager_Hr,email_Deputy_Manager_Hr,position_Deputy_Manager_Hr,id FROM employee_Deputy_Manager_Hr WHERE validstatus=1"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
