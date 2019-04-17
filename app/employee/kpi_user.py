#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *
@app.route('/Add_project', methods=['POST'])
@connect_sql()
def Add_project(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        employeeid = data_new['employeeid']

        result_token = CheckTokenAssessor_kpi(data_new['createby'],data_new['token'])
        if result_token!='pass':
            return 'token fail'

        i=0
        for i in xrange(len(data_new['project'])):

            sqlQry = "SELECT project_kpi_id FROM project_kpi ORDER BY project_kpi_id DESC LIMIT 1"
            cursor.execute(sqlQry)
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            try:
                project_kpi_id_last = result[0]['project_kpi_id']+1
            except Exception as e:
                project_kpi_id_last = 1

            type_action = "ADD"

            sqlIn_be = "INSERT INTO project_kpi(employeeid,employeeid_kpi,project_kpi_id,project_id,project_values,type_check,createby) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_be,(employeeid,data_new['createby'],project_kpi_id_last,data_new['project'][i]['project_id'],data_new['project'][i]['project_values'],data_new['project'][i]['type_check'],data_new['createby']))

            sqlIn_be_log = "INSERT INTO project_kpi_log(employeeid,employeeid_kpi,project_kpi_id,project_id,project_values,type_check,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_be_log,(employeeid,data_new['createby'],project_kpi_id_last,data_new['project'][i]['project_id'],data_new['project'][i]['project_values'],data_new['project'][i]['type_check'],data_new['createby'],type_action))

        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Edit_project', methods=['POST'])
@connect_sql()
def Edit_project(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        result_token = CheckTokenAssessor_kpi(data_new['createby'],data_new['token'])
        if result_token!='pass':
            return 'token fail'

        sql = "SELECT citizenid,project_kpi_id,benefits_values,type_check FROM project_kpi WHERE employeeid=%s AND project_kpi_id=%s"
        cursor.execute(sql,(data_new['employeeid'],data_new['project_kpi_id']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Edit"

        sqlIn = "INSERT INTO project_kpi_log (employeeid,citizenid,project_kpi_id,benefits_values,type_check,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn,(data_new['employeeid'],result[0]['citizenid'],result[0]['project_kpi_id'],result[0]['benefits_values'],result[0]['type_check'],data_new['createby'],type_action))

        sqlde = "DELETE FROM project_kpi WHERE employeeid=%s AND project_kpi_id=%s"
        cursor.execute(sqlde,(data_new['employeeid'],data_new['project_kpi_id']))

        sqlIn = "INSERT INTO project_kpi(employeeid,citizenid,project_kpi_id,benefits_values,type_check,createby) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn,(data_new['employeeid'],data_new['citizenid'],data_new['project_kpi_id'],data_new['benefits_values'],data_new['type_check'],data_new['createby']))
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Delete_project', methods=['POST'])
@connect_sql()
def Delete_project(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        result_token = CheckTokenAssessor_kpi(data_new['createby'],data_new['token'])
        if result_token!='pass':
            return 'token fail'
            
        sql = "SELECT citizenid,project_kpi_id,benefits_values,type_check FROM project_kpi WHERE employeeid=%s AND project_kpi_id=%s"
        cursor.execute(sql,(data_new['employeeid'],data_new['project_kpi_id']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Delete"

        sqlIn = "INSERT INTO project_kpi_log (employeeid,citizenid,project_kpi_id,benefits_values,type_check,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn,(data_new['employeeid'],result[0]['citizenid'],result[0]['project_kpi_id'],result[0]['benefits_values'],result[0]['type_check'],data_new['createby'],type_action))

        sqlde = "UPDATE project_kpi SET validstatus=0 WHERE employeeid=%s AND project_kpi_id=%s"
        cursor.execute(sqlde,(data_new['employeeid'],data_new['project_kpi_id']))
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
