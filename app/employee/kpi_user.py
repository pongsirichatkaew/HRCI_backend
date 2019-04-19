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

        sqlUp = "UPDATE employee_kpi SET totalGrade=%s,totalGradePercent=%s,oldgrade=%s,status=%s,positionChange=%s,specialMoney=%s,newKpiDescriptions=%s WHERE employeeid=%s AND year=%s AND term=%s"
        cursor.execute(sqlUp,(data_new['totalGrade'],data_new['totalGradePercent'],data_new['oldgrade'],data_new['status'],data_new['positionChange'],data_new['specialMoney'],data_new['newKpiDescriptions'],data_new['employeeid'],data_new['year'],data_new['term']))

        i=0
        for i in xrange(len(data_new['portfolioLists'])):

            sqlQry = "SELECT project_kpi_id FROM project_kpi ORDER BY project_kpi_id DESC LIMIT 1"
            cursor.execute(sqlQry)
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            try:
                project_kpi_id_last = result[0]['project_kpi_id']+1
            except Exception as e:
                project_kpi_id_last = 1

            type_action = "ADD"

            sqlIn = "INSERT INTO project_kpi(employeeid,employeeid_kpi,project_kpi_id,expectedPortfolio,ExpectedLevel,CanDoLevel,summaryLevel,weightPortfolio,totalPoint,commentLevel_B_Up) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn,(employeeid,data_new['createby'],project_kpi_id_last,data_new['portfolioLists'][i]['expectedPortfolio'],data_new['portfolioLists'][i]['ExpectedLevel'],data_new['portfolioLists'][i]['CanDoLevel'],data_new['portfolioLists'][i]['summaryLevel'],data_new['portfolioLists'][i]['weightPortfolio'],data_new['portfolioLists'][i]['totalPoint'],data_new['portfolioLists'][i]['commentLevel_B_Up']))

            sqlIn_ = "INSERT INTO project_kpi_log(employeeid,employeeid_kpi,project_kpi_id,expectedPortfolio,ExpectedLevel,CanDoLevel,summaryLevel,weightPortfolio,totalPoint,commentLevel_B_Up,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_,(employeeid,data_new['createby'],project_kpi_id_last,data_new['portfolioLists'][i]['expectedPortfolio'],data_new['portfolioLists'][i]['ExpectedLevel'],data_new['portfolioLists'][i]['CanDoLevel'],data_new['portfolioLists'][i]['summaryLevel'],data_new['portfolioLists'][i]['weightPortfolio'],data_new['portfolioLists'][i]['totalPoint'],data_new['portfolioLists'][i]['commentLevel_B_Up'],type_action))

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
        employeeid = data_new['employeeid']

        result_token = CheckTokenAssessor_kpi(data_new['createby'],data_new['token'])
        if result_token!='pass':
            return 'token fail'

        sqlUp = "UPDATE employee_kpi SET totalGrade=%s,totalGradePercent=%s,oldgrade=%s,status=%s,positionChange=%s,specialMoney=%s,newKpiDescriptions=%s WHERE employeeid=%s AND year=%s AND term=%s"
        cursor.execute(sqlUp,(data_new['totalGrade'],data_new['totalGradePercent'],data_new['oldgrade'],data_new['status'],data_new['positionChange'],data_new['specialMoney'],data_new['newKpiDescriptions'],data_new['employeeid'],data_new['year'],data_new['term']))

        sql = "SELECT * FROM project_kpi WHERE employeeid=%s AND project_kpi_id=%s"
        cursor.execute(sql,(data_new['employeeid'],data_new['project_kpi_id']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Edit"

        sqlIn_ = "INSERT INTO project_kpi_log(employeeid,employeeid_kpi,project_kpi_id,expectedPortfolio,ExpectedLevel,CanDoLevel,summaryLevel,weightPortfolio,totalPoint,commentLevel_B_Up,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_,(employeeid,data_new['createby'],data_new['portfolioLists'][0]['project_kpi_id'],result[0]['expectedPortfolio'],result[0]['ExpectedLevel'],result[0]['CanDoLevel'],result[0]['summaryLevel'],result[0]['weightPortfolio'],result[0]['totalPoint'],result[0]['commentLevel_B_Up'],type_action))


        sqlde = "DELETE FROM project_kpi WHERE employeeid=%s AND project_kpi_id=%s"
        cursor.execute(sqlde,(data_new['employeeid'],data_new['project_kpi_id']))

        sqlIn = "INSERT INTO project_kpi(employeeid,employeeid_kpi,project_kpi_id,expectedPortfolio,ExpectedLevel,CanDoLevel,summaryLevel,weightPortfolio,totalPoint,commentLevel_B_Up) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn,(employeeid,data_new['createby'],data_new['portfolioLists'][0]['project_kpi_id'],data_new['portfolioLists'][0]['expectedPortfolio'],data_new['portfolioLists'][0]['ExpectedLevel'],data_new['portfolioLists'][0]['CanDoLevel'],data_new['portfolioLists'][0]['summaryLevel'],data_new['portfolioLists'][0]['weightPortfolio'],data_new['portfolioLists'][0]['totalPoint'],data_new['portfolioLists'][0]['commentLevel_B_Up']))

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
        employeeid = data_new['employeeid']

        result_token = CheckTokenAssessor_kpi(data_new['createby'],data_new['token'])
        if result_token!='pass':
            return 'token fail'

        sqlUp = "UPDATE employee_kpi SET totalGrade=%s,totalGradePercent=%s,oldgrade=%s,status=%s,positionChange=%s,specialMoney=%s,newKpiDescriptions=%s WHERE employeeid=%s AND year=%s AND term=%s"
        cursor.execute(sqlUp,(data_new['totalGrade'],data_new['totalGradePercent'],data_new['oldgrade'],data_new['status'],data_new['positionChange'],data_new['specialMoney'],data_new['newKpiDescriptions'],data_new['employeeid'],data_new['year'],data_new['term']))

        sql = "SELECT * FROM project_kpi WHERE employeeid=%s AND project_kpi_id=%s"
        cursor.execute(sql,(data_new['employeeid'],data_new['project_kpi_id']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Delete"

        sqlIn_ = "INSERT INTO project_kpi_log(employeeid,employeeid_kpi,project_kpi_id,expectedPortfolio,ExpectedLevel,CanDoLevel,summaryLevel,weightPortfolio,totalPoint,commentLevel_B_Up,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_,(employeeid,data_new['createby'],data_new['project_kpi_id'],result[0]['expectedPortfolio'],result[0]['ExpectedLevel'],result[0]['CanDoLevel'],result[0]['summaryLevel'],result[0]['weightPortfolio'],result[0]['totalPoint'],result[0]['commentLevel_B_Up'],type_action))

        sqlde = "DELETE FROM project_kpi WHERE employeeid=%s AND project_kpi_id=%s"
        cursor.execute(sqlde,(data_new['employeeid'],data_new['project_kpi_id']))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
