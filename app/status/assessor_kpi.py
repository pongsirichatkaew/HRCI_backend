#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/InsertAssessor_kpi', methods=['POST'])
@connect_sql()
def InsertAssessor_kpi(cursor):
    try:
        data = request.json
        source = data['source']
        data_new = source

        try:
            sql44 = "SELECT name_asp FROM assessor_kpi WHERE companyid=%s AND tier_approve=%s AND employeeid=%s"
            cursor.execute(sql44,(data_new['companyid'],data_new['tier_approve'],data_new['employeeid']))
            columns = [column[0] for column in cursor.description]
            result_test = toJson(cursor.fetchall(),columns)
            name_test = result_test[0]['name_asp']
            return "employee is duplicate"
        except Exception as e:
            pass

        sqlQry = "SELECT assessor_kpi_id FROM assessor_kpi ORDER BY assessor_kpi_id DESC LIMIT 1"
        cursor.execute(sqlQry)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        try:
            assessor_kpi_id_last = result[0]['assessor_kpi_id']+1
        except Exception as e:
            assessor_kpi_id_last = 1

        sql = "INSERT INTO assessor_kpi (assessor_kpi_id,employeeid,companyid,name_asp,surname_asp,cost_center_name_id,tier_approve,email_asp,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(assessor_kpi_id_last,data_new['employeeid'],data_new['companyid'],data_new['name_asp'],data_new['surname_asp'],data_new['cost_center_name_id'],data_new['tier_approve'],data_new['email_asp'],data_new['createby']))

        type_action = "ADD"

        sql_log = "INSERT INTO assessor_kpi_log (assessor_kpi_id,employeeid,companyid,name_asp,surname_asp,cost_center_name_id,tier_approve,email_asp,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(assessor_kpi_id_last,data_new['employeeid'],data_new['companyid'],data_new['name_asp'],data_new['surname_asp'],data_new['cost_center_name_id'],data_new['tier_approve'],data_new['email_asp'],data_new['createby'],type_action))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditAssessor_kpi', methods=['POST'])
@connect_sql()
def EditAssessor_kpi(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        try:
            sql44 = "SELECT name_asp FROM assessor_kpi WHERE companyid=%s AND tier_approve=%s AND employeeid=%s"
            cursor.execute(sql44,(data_new['companyid'],data_new['tier_approve'],data_new['employeeid']))
            columns = [column[0] for column in cursor.description]
            result_test = toJson(cursor.fetchall(),columns)
            name_test = result_test[0]['name_asp']
            return "employee is duplicate"
        except Exception as e:
            pass

        sqlQry = "SELECT * FROM assessor_kpi WHERE assessor_kpi_id=%s"
        cursor.execute(sqlQry,data_new['assessor_kpi_id'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Edit"

        sql_log = "INSERT INTO assessor_kpi_log (assessor_kpi_id,employeeid,companyid,name_asp,surname_asp,cost_center_name_id,tier_approve,email_asp,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(result[0]['assessor_kpi_id'],result[0]['employeeid'],result[0]['companyid'],result[0]['name_asp'],result[0]['surname_asp'],result[0]['cost_center_name_id'],result[0]['tier_approve'],result[0]['email_asp'],data_new['createby'],type_action))

        sqlUp = "DELETE FROM assessor_kpi WHERE assessor_kpi_id=%s"
        cursor.execute(sqlUp,(data_new['assessor_kpi_id']))

        sqlIn = "INSERT INTO assessor_kpi (assessor_kpi_id,employeeid,companyid,name_asp,surname_asp,cost_center_name_id,tier_approve,email_asp,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn,(result[0]['assessor_kpi_id'],data_new['employeeid'],data_new['companyid'],data_new['name_asp'],data_new['surname_asp'],data_new['cost_center_name_id'],data_new['tier_approve'],data_new['email_asp'],data_new['createby']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryAssessor_kpi', methods=['POST'])
@connect_sql()
def QryAssessor_kpi(cursor):
    try:
        company_id = ""
        try:
            dataInput = request.json
            source = dataInput['source']
            data_new = source
            company_id = 'WHERE assessor_kpi.companyid='+'"'+str(data_new['companyid'])+'"'+' '+'AND assessor_kpi.tier_approve IN'+"('L2','L3','L4')"
        except Exception as e:
            pass
        sql = "SELECT assessor_kpi.assessor_kpi_id,assessor_kpi.employeeid,assessor_kpi.companyid,company.companyname,assessor_kpi.name_asp,assessor_kpi.surname_asp,assessor_kpi.tier_approve,assessor_kpi.cost_center_name_id,cost_center_name.cost_detail,assessor_kpi.email_asp FROM assessor_kpi INNER JOIN company ON assessor_kpi.companyid = company.companyid INNER JOIN cost_center_name ON assessor_kpi.cost_center_name_id = cost_center_name.cost_center_name_id "+company_id+" "
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/DeleteAssessor_kpi', methods=['POST'])
@connect_sql()
def DeleteAssessor_kpi(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sqlQry = "SELECT * FROM assessor_kpi WHERE assessor_kpi_id=%s"
        cursor.execute(sqlQry,data_new['assessor_kpi_id'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Delete"

        sql_log = "INSERT INTO assessor_kpi_log (assessor_kpi_id,employeeid,companyid,name_asp,surname_asp,cost_center_name_id,tier_approve,email_asp,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(result[0]['assessor_kpi_id'],result[0]['employeeid'],result[0]['companyid'],result[0]['name_asp'],result[0]['surname_asp'],result[0]['cost_center_name_id'],result[0]['tier_approve'],result[0]['email_asp'],data_new['createby'],type_action))

        sqlUp = "DELETE FROM assessor_kpi WHERE assessor_kpi_id=%s"
        cursor.execute(sqlUp,(data_new['assessor_kpi_id']))

        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
