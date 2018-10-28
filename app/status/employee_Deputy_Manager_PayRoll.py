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
        sqlQry = "SELECT employee_Deputy_Manager_PayRoll_id FROM employee_Deputy_Manager_PayRoll ORDER BY employee_Deputy_Manager_PayRoll_id DESC LIMIT 1"
        cursor.execute(sqlQry)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        employee_Deputy_Manager_PayRoll_id_last=result[0]['employee_Deputy_Manager_PayRoll_id']+1

        sql = "INSERT INTO employee_Deputy_Manager_PayRoll (employee_Deputy_Manager_PayRoll_id,employeeid,companyid,name_Deputy_Manager_PayRoll,surname_Deputy_Manager_PayRoll,position_id,email_Deputy_Manager_PayRoll,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(employee_Deputy_Manager_PayRoll_id_last,data_new['employeeid'],data_new['companyid'],data_new['name_Deputy_Manager_PayRoll'],data_new['surname_Deputy_Manager_PayRoll'],data_new['position_id'],data_new['email_Deputy_Manager_PayRoll'],data_new['createby']))

        type_action = "ADD"

        sql_log = "INSERT INTO employee_Deputy_Manager_PayRoll_log (employee_Deputy_Manager_PayRoll_id,employeeid,companyid,name_Deputy_Manager_PayRoll,surname_Deputy_Manager_PayRoll,position_id,email_Deputy_Manager_PayRoll,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(employee_Deputy_Manager_PayRoll_id_last,data_new['employeeid'],data_new['companyid'],data_new['name_Deputy_Manager_PayRoll'],data_new['surname_Deputy_Manager_PayRoll'],data_new['position_id'],data_new['email_Deputy_Manager_PayRoll'],data_new['createby'],type_action))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee_Deputy_Manager_PayRoll', methods=['POST'])
@connect_sql()
def EditEmployee_Deputy_Manager_PayRoll(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sqlQry = "SELECT * FROM employee_Deputy_Manager_PayRoll WHERE employee_Deputy_Manager_PayRoll_id=%s"
        cursor.execute(sqlQry,data_new['employee_Deputy_Manager_PayRoll_id'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Edit"

        sql_log = "INSERT INTO employee_Deputy_Manager_PayRoll_log (employee_Deputy_Manager_PayRoll_id,employeeid,companyid,name_Deputy_Manager_PayRoll,surname_Deputy_Manager_PayRoll,position_id,email_Deputy_Manager_PayRoll,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(result[0]['employee_Deputy_Manager_PayRoll_id'],result[0]['employeeid'],result[0]['companyid'],result[0]['name_Deputy_Manager_PayRoll'],result[0]['surname_Deputy_Manager_PayRoll'],result[0]['position_id'],result[0]['email_Deputy_Manager_PayRoll'],data_new['createby'],type_action))

        sqlDe = "DELETE FROM employee_Deputy_Manager_PayRoll WHERE employee_Deputy_Manager_PayRoll_id=%s"
        cursor.execute(sqlDe,(data_new['employee_Deputy_Manager_PayRoll_id']))

        sql = "INSERT INTO employee_Deputy_Manager_PayRoll (employee_Deputy_Manager_PayRoll_id,employeeid,companyid,name_Deputy_Manager_PayRoll,surname_Deputy_Manager_PayRoll,position_id,email_Deputy_Manager_PayRoll,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(result[0]['employee_Deputy_Manager_PayRoll_id'],data_new['employeeid'],data_new['companyid'],data_new['name_Deputy_Manager_PayRoll'],data_new['surname_Deputy_Manager_PayRoll'],data_new['position_id'],data_new['email_Deputy_Manager_PayRoll'],data_new['createby']))

        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryEmployee_Deputy_Manager_PayRoll', methods=['POST'])
@connect_sql()
def QryEmployee_Deputy_Manager_PayRoll(cursor):
    try:
        sql = "SELECT employee_Deputy_Manager_PayRoll.id, employee_Deputy_Manager_PayRoll.employee_Deputy_Manager_PayRoll_id, employee_Deputy_Manager_PayRoll.employeeid, company.companyname,company.companyid , employee_Deputy_Manager_PayRoll.name_Deputy_Manager_PayRoll, employee_Deputy_Manager_PayRoll.surname_Deputy_Manager_PayRoll, employee_Deputy_Manager_PayRoll.position_id,position.position_detail, employee_Deputy_Manager_PayRoll.email_Deputy_Manager_PayRoll, employee_Deputy_Manager_PayRoll.createby, employee_Deputy_Manager_PayRoll.create_at, employee_Deputy_Manager_PayRoll.validstatus FROM employee_Deputy_Manager_PayRoll INNER JOIN company ON employee_Deputy_Manager_PayRoll.companyid = company.companyid INNER JOIN position ON employee_Deputy_Manager_PayRoll.position_id = position.position_id"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/DeleteEmployee_Deputy_Manager_PayRoll', methods=['POST'])
@connect_sql()
def DeleteEmployee_Deputy_Manager_PayRoll(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sqlQry = "SELECT * FROM employee_Deputy_Manager_PayRoll WHERE employee_Deputy_Manager_PayRoll_id=%s"
        cursor.execute(sqlQry,data_new['employee_Deputy_Manager_PayRoll_id'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Delete"

        sql_log = "INSERT INTO employee_Deputy_Manager_PayRoll_log (employee_Deputy_Manager_PayRoll_id,employeeid,companyid,name_Deputy_Manager_PayRoll,surname_Deputy_Manager_PayRoll,position_id,email_Deputy_Manager_PayRoll,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(result[0]['employee_Deputy_Manager_PayRoll_id'],result[0]['employeeid'],result[0]['companyid'],result[0]['name_Deputy_Manager_PayRoll'],result[0]['surname_Deputy_Manager_PayRoll'],result[0]['position_id'],result[0]['email_Deputy_Manager_PayRoll'],data_new['createby'],type_action))

        sqlDe = "DELETE FROM employee_Deputy_Manager_PayRoll WHERE employee_Deputy_Manager_PayRoll_id=%s"
        cursor.execute(sqlDe,(data_new['employee_Deputy_Manager_PayRoll_id']))

    except Exception as e:
        logserver(e)
        return "fail"
