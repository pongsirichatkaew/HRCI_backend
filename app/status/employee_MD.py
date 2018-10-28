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

        sql = "INSERT INTO employee_MD (employee_md_id,employeeid,companyid,name_md,surname_md,position_id,email_md,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(employee_md_id_last,data_new['employeeid'],data_new['companyid'],data_new['name_md'],data_new['surname_md'],data_new['position_id'],data_new['email_md'],data_new['createby']))

        type_action = "ADD"

        sql_log = "INSERT INTO employee_MD_log (employee_md_id,employeeid,companyid,name_md,surname_md,position_id,email_md,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(employee_md_id_last,data_new['employeeid'],data_new['companyid'],data_new['name_md'],data_new['surname_md'],data_new['position_id'],data_new['email_md'],data_new['createby'],type_action))
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
        sqlQry = "SELECT * FROM employee_MD WHERE employee_md_id=%s"
        cursor.execute(sqlQry,data_new['employee_md_id'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Edit"

        sql_log = "INSERT INTO employee_MD_log (employee_md_id,employeeid,companyid,name_md,surname_md,position_id,email_md,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(result[0]['employee_md_id'],result[0]['employeeid'],result[0]['companyid'],result[0]['name_md'],result[0]['surname_md'],result[0]['position_id'],result[0]['email_md'],data_new['createby'],type_action))

        sqlUp = "DELETE FROM employee_MD WHERE employee_md_id=%s"
        cursor.execute(sqlUp,(data_new['employee_md_id']))

        sqlIn = "INSERT INTO employee_MD (employee_md_id,employeeid,companyid,name_md,surname_md,position_id,email_md,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn,(result[0]['employee_md_id'],data_new['employeeid'],data_new['companyid'],data_new['name_md'],data_new['surname_md'],data_new['position_id'],data_new['email_md'],data_new['createby']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryEmployee_MD', methods=['POST'])
@connect_sql()
def QryEmployee_MD(cursor):
    try:
        sql = "SELECT employee_MD.employee_md_id,employee_MD.employeeid,employee_MD.companyid,company.companyname,employee_MD.name_md,employee_MD.surname_md,employee_MD.position_id,position.position_detail,employee_MD.email_md FROM employee_MD INNER JOIN company ON employee_MD.companyid = company.companyid INNER JOIN position ON employee_MD.position_id = position.position_id"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/DeleteEmployee_MD', methods=['POST'])
@connect_sql()
def DeleteEmployee_MD(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sqlQry = "SELECT * FROM employee_MD WHERE employee_md_id=%s"
        cursor.execute(sqlQry,data_new['employee_md_id'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Delete"

        sql_log = "INSERT INTO employee_MD_log (employee_md_id,employeeid,companyid,name_md,surname_md,position_id,email_md,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(result[0]['employee_md_id'],result[0]['employeeid'],result[0]['companyid'],result[0]['name_md'],result[0]['surname_md'],result[0]['position_id'],result[0]['email_md'],data_new['createby'],type_action))

        sqlUp = "DELETE FROM employee_MD WHERE employee_md_id=%s"
        cursor.execute(sqlUp,(data_new['employee_md_id']))

        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryEmployeeid_hrci', methods=['POST'])
@connect_sql2()
def QryEmployeeid_hrci(cursor2):
    try:
        sql = "SELECT code FROM hrci  WHERE workstatus='Active' "
        cursor2.execute(sql)
        columns = [column[0] for column in cursor2.description]
        result = toJson(cursor2.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryEmployee_hrci_by_employeeid', methods=['POST'])
@connect_sql2()
def QryEmployee_hrci_by_employeeid(cursor2):
    try:
        data_new = request.json
        source = data_new['source']
        data_new = source
        sql = "SELECT thainame,email FROM hrci  WHERE workstatus='Active'AND code=%s "
        cursor2.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor2.description]
        result = toJson(cursor2.fetchall(),columns)
        test = result[0]['thainame']
        typename = test.split(" ")
        name = typename[0]
        surname = typename[1]
        resultlast={}
        resultlast['email'] = result[0]['email']
        resultlast['name'] = name
        resultlast['surname'] = surname
        return jsonify(resultlast)
    except Exception as e:
        logserver(e)
        return "fail"
