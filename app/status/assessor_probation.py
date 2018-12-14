#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/InsertAssessor_pro', methods=['POST'])
@connect_sql()
def InsertAssessor_pro(cursor):
    try:
        data = request.json
        source = data['source']
        data_new = source
        sqlQry = "SELECT assessor_pro_id FROM assessor_pro ORDER BY assessor_pro_id DESC LIMIT 1"
        cursor.execute(sqlQry)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        assessor_pro_id_last=result[0]['assessor_pro_id']+1

        sql = "INSERT INTO assessor_pro (assessor_pro_id,employeeid,companyid,name_asp,surname_asp,position_id,org_name_id,email_asp,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(assessor_pro_id_last,data_new['employeeid'],data_new['companyid'],data_new['name_asp'],data_new['surname_asp'],data_new['position_id'],data_new['org_name_id'],data_new['email_asp'],data_new['createby']))

        type_action = "ADD"

        sql_log = "INSERT INTO assessor_pro_log (assessor_pro_id,employeeid,companyid,name_asp,surname_asp,position_id,org_name_id,email_asp,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(assessor_pro_id_last,data_new['employeeid'],data_new['companyid'],data_new['name_asp'],data_new['surname_asp'],data_new['position_id'],data_new['org_name_id'],data_new['email_asp'],data_new['createby'],type_action))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditAssessor_pro', methods=['POST'])
@connect_sql()
def EditAssessor_pro(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sqlQry = "SELECT * FROM assessor_pro WHERE assessor_pro_id=%s"
        cursor.execute(sqlQry,data_new['assessor_pro_id'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Edit"

        sql_log = "INSERT INTO assessor_pro_log (assessor_pro_id,employeeid,companyid,name_asp,surname_asp,position_id,org_name_id,email_asp,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(result[0]['assessor_pro_id'],result[0]['employeeid'],result[0]['companyid'],result[0]['name_asp'],result[0]['surname_asp'],result[0]['position_id'],result[0]['org_name_id'],result[0]['email_asp'],data_new['createby'],type_action))

        sqlUp = "DELETE FROM assessor_pro WHERE assessor_pro_id=%s"
        cursor.execute(sqlUp,(data_new['assessor_pro_id']))

        sqlIn = "INSERT INTO assessor_pro (assessor_pro_id,employeeid,companyid,name_asp,surname_asp,position_id,org_name_id,email_asp,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn,(result[0]['assessor_pro_id'],data_new['employeeid'],data_new['companyid'],data_new['name_asp'],data_new['surname_asp'],data_new['position_id'],data_new['org_name_id'],data_new['email_asp'],data_new['createby']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryAssessor_pro', methods=['POST'])
@connect_sql()
def QryAssessor_pro(cursor):
    try:
        sql = "SELECT assessor_pro.assessor_pro_id,assessor_pro.employeeid,assessor_pro.companyid,company.companyname,assessor_pro.name_asp,assessor_pro.surname_asp,assessor_pro.position_id,position.position_detail,org_name.org_name_detail,assessor_pro.email_asp FROM assessor_pro INNER JOIN company ON assessor_pro.companyid = company.companyid INNER JOIN position ON assessor_pro.position_id = position.position_id INNER JOIN org_name ON assessor_pro.org_name_id = org_name.org_name_id"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/DeleteAssessor_pro', methods=['POST'])
@connect_sql()
def DeleteAssessor_pro(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sqlQry = "SELECT * FROM assessor_pro WHERE assessor_pro_id=%s"
        cursor.execute(sqlQry,data_new['assessor_pro_id'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Delete"

        sql_log = "INSERT INTO assessor_pro_log (assessor_pro_id,employeeid,companyid,name_asp,surname_asp,position_id,org_name_id,email_asp,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(result[0]['assessor_pro_id'],result[0]['employeeid'],result[0]['companyid'],result[0]['name_asp'],result[0]['surname_asp'],result[0]['position_id'],result[0]['org_name_id'],result[0]['email_asp'],data_new['createby'],type_action))

        sqlUp = "DELETE FROM assessor_pro WHERE assessor_pro_id=%s"
        cursor.execute(sqlUp,(data_new['assessor_pro_id']))

        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
