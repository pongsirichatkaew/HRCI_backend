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
            sql44 = "SELECT name_asp FROM assessor_kpi WHERE companyid=%s AND employeeid=%s AND org_name_id=%s"
            cursor.execute(sql44,(data_new['companyid'],data_new['employeeid'],data_new['org_name_id']))
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

        sql = "INSERT INTO assessor_kpi (assessor_kpi_id,employeeid,companyid,name_asp,surname_asp,org_name_id,email_asp,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(assessor_kpi_id_last,data_new['employeeid'],data_new['companyid'],data_new['name_asp'],data_new['surname_asp'],data_new['org_name_id'],data_new['email_asp'],data_new['createby']))

        type_action = "ADD"

        sql_log = "INSERT INTO assessor_kpi_log (assessor_kpi_id,employeeid,companyid,name_asp,surname_asp,org_name_id,email_asp,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(assessor_kpi_id_last,data_new['employeeid'],data_new['companyid'],data_new['name_asp'],data_new['surname_asp'],data_new['org_name_id'],data_new['email_asp'],data_new['createby'],type_action))
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
            sql44 = "SELECT name_asp FROM assessor_kpi WHERE companyid=%s AND employeeid=%s"
            cursor.execute(sql44,(data_new['companyid'],data_new['employeeid']))
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

        sql_log = "INSERT INTO assessor_kpi_log (assessor_kpi_id,employeeid,companyid,name_asp,surname_asp,org_name_id,email_asp,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(result[0]['assessor_kpi_id'],result[0]['employeeid'],result[0]['companyid'],result[0]['name_asp'],result[0]['surname_asp'],result[0]['org_name_id'],result[0]['email_asp'],data_new['createby'],type_action))

        sqlUp = "DELETE FROM assessor_kpi WHERE assessor_kpi_id=%s"
        cursor.execute(sqlUp,(data_new['assessor_kpi_id']))

        sqlIn = "INSERT INTO assessor_kpi (assessor_kpi_id,employeeid,companyid,name_asp,surname_asp,org_name_id,email_asp,createby,type) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn,(result[0]['assessor_kpi_id'],data_new['employeeid_new'],data_new['companyid_new'],data_new['name_asp_new'],data_new['surname_asp_new'],data_new['org_name_id_new'],data_new['email_asp_new'],data_new['createby'],result[0]['type']))

        sqlUp_main = "UPDATE employee_kpi SET em_id_leader=%s WHERE em_id_leader=%s"
        cursor.execute(sqlUp_main,(data_new['employeeid_new'],data_new['employeeid']))

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
            company_id = 'WHERE assessor_kpi.companyid='+'"'+str(data_new['companyid'])+'"'
        except Exception as e:
            pass
        sql = "SELECT assessor_kpi.type,assessor_kpi.status,assessor_kpi.assessor_kpi_id,assessor_kpi.employeeid,assessor_kpi.companyid,company.companyname,company.company_short_name,assessor_kpi.name_asp,assessor_kpi.surname_asp,assessor_kpi.org_name_id,org_name.org_name_detail,assessor_kpi.email_asp FROM assessor_kpi INNER JOIN company ON assessor_kpi.companyid = company.companyid INNER JOIN org_name ON assessor_kpi.org_name_id = org_name.org_name_id "+company_id+" "
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        for i1 in result:
            employee = []
            kpi_ful = []
            sql2 = "SELECT (SELECT COUNT(employeeid) FROM employee_kpi WHERE em_id_leader=%s) AS total\
                          ,(SELECT COUNT(employeeid) FROM employee_kpi WHERE em_id_leader=%s AND old_grade IS NOT NULL) AS Do\
                          ,(SELECT COUNT(employeeid) FROM employee_kpi WHERE em_id_leader=%s AND `old_grade` IS NULL) AS Not_Do\
            FROM assessor_kpi LIMIT 1"
            cursor.execute(sql2,(i1['employeeid'],i1['employeeid'],i1['employeeid']))
            columns = [column[0] for column in cursor.description]
            data2 = toJson(cursor.fetchall(),columns)
            for i2 in data2 :
                kpi_ful.append(i2)
            i1['employee'] = kpi_ful
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

        sql_log = "INSERT INTO assessor_kpi_log (assessor_kpi_id,employeeid,companyid,name_asp,surname_asp,org_name_id,email_asp,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(result[0]['assessor_kpi_id'],result[0]['employeeid'],result[0]['companyid'],result[0]['name_asp'],result[0]['surname_asp'],result[0]['org_name_id'],result[0]['email_asp'],data_new['createby'],type_action))

        sqlUp = "DELETE FROM assessor_kpi WHERE assessor_kpi_id=%s"
        cursor.execute(sqlUp,(data_new['assessor_kpi_id']))

        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Not_edit_assessor_kpi', methods=['POST'])
@connect_sql()
def Not_edit_assessor_kpi(cursor):
    try:
        sqlUp_main = "UPDATE assessor_kpi SET status='deactive'"
        cursor.execute(sqlUp_main)
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/AD_edit_assessor_kpi', methods=['POST'])
@connect_sql()
def AD_edit_assessor_kpi(cursor):
    try:
        sqlUp_main = "UPDATE assessor_kpi SET status='active'"
        cursor.execute(sqlUp_main)
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Not_edit_assessor_kpi_one', methods=['POST'])
@connect_sql()
def Not_edit_assessor_kpi_one(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sqlUp_main = "UPDATE assessor_kpi SET status='deactive' WHERE assessor_kpi_id=%s"
        cursor.execute(sqlUp_main,(data_new['assessor_kpi_id']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/AD_edit_assessor_kpi_one', methods=['POST'])
@connect_sql()
def AD_edit_assessor_kpi_one(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sqlUp_main = "UPDATE assessor_kpi SET status='active' WHERE assessor_kpi_id=%s "
        cursor.execute(sqlUp_main,(data_new['assessor_kpi_id']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/qry_count_assessorKPI', methods=['POST'])
@connect_sql()
def qry_count_assessorKPI(cursor):
    try:
        sqlQry = "SELECT COUNT(employeeid) AS Total_active FROM assessor_kpi WHERE status='active'"
        cursor.execute(sqlQry)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sqlQry2 = "SELECT COUNT(employeeid) AS Total_deactive FROM assessor_kpi WHERE status='deactive'"
        cursor.execute(sqlQry2)
        columns = [column[0] for column in cursor.description]
        result2 = toJson(cursor.fetchall(),columns)

        all={}
        all['total_active'] = result[0]['Total_active']
        all['total_deactive'] = result2[0]['Total_deactive']
        return jsonify(all)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryName_leader_kpi', methods=['POST'])
@connect_sql()
def QryName_leader_kpi(cursor):
    try:

        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT assessor_kpi.employeeid,assessor_kpi.name_asp,assessor_kpi.surname_asp,org_name.org_name_detail,assessor_kpi.email_asp,assessor_kpi.companyid,assessor_kpi.org_name_id FROM assessor_kpi\
        INNER JOIN org_name ON assessor_kpi.org_name_id = org_name.org_name_id\
        INNER JOIN employee_kpi ON assessor_kpi.employeeid = employee_kpi.em_id_leader\
        WHERE assessor_kpi.employeeid=%s AND employee_kpi.employeeid=%s"
        cursor.execute(sql,(data_new['em_id_leader'],data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditName_leader_kpi_one', methods=['POST'])
@connect_sql()
def EditName_leader_kpi_one(cursor):
    try:

        dataInput = request.json
        source = dataInput['source']
        data_new = source

        try:
            sql44 = "SELECT name_asp FROM assessor_kpi WHERE employeeid=%s AND companyid=%s"
            cursor.execute(sql44,(data_new['employeeid_new'],data_new['companyid']))
            columns = [column[0] for column in cursor.description]
            result_test = toJson(cursor.fetchall(),columns)
            name_test = result_test[0]['name_asp']
        except Exception as e:
            sqlQry = "SELECT assessor_kpi_id FROM assessor_kpi ORDER BY assessor_kpi_id DESC LIMIT 1"
            cursor.execute(sqlQry)
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            try:
                assessor_kpi_id_last = result[0]['assessor_kpi_id']+1
            except Exception as e:
                assessor_kpi_id_last = 1

            sql = "INSERT INTO assessor_kpi (assessor_kpi_id,employeeid,companyid,name_asp,surname_asp,org_name_id,email_asp,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,(assessor_kpi_id_last,data_new['employeeid_new'],data_new['companyid'],data_new['name_asp'],data_new['surname_asp'],data_new['org_name_id'],data_new['email_asp'],data_new['createby']))

            type_action = "ADD"

            sql_log = "INSERT INTO assessor_kpi_log (assessor_kpi_id,employeeid,companyid,name_asp,surname_asp,org_name_id,email_asp,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql_log,(assessor_kpi_id_last,data_new['employeeid_new'],data_new['companyid'],data_new['name_asp'],data_new['surname_asp'],data_new['org_name_id'],data_new['email_asp'],data_new['createby'],type_action))

        sqlUp_main = "UPDATE employee_kpi SET em_id_leader=%s WHERE em_id_leader=%s AND employeeid=%s"
        cursor.execute(sqlUp_main,(data_new['employeeid_new'],data_new['employeeid'],data_new['employeeid_self']))

        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryAssessor_status', methods=['POST'])
@connect_sql()
def QryAssessor_status(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql2 = "SELECT status FROM assessor_kpi WHERE employeeid=%s"
        cursor.execute(sql2,(data_new['em_id_leader']))
        columns = [column[0] for column in cursor.description]
        data2 = toJson(cursor.fetchall(),columns)
        return jsonify(data2)
    except Exception as e:
        logserver(e)
        return "fail"
