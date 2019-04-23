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

        # result_token = CheckTokenAssessor_kpi(data_new['createby'],data_new['token'])
        # if result_token!='pass':
        #     return 'token fail'

        sqlUp = "UPDATE employee_kpi SET totalGrade=%s,totalGradePercent=%s,old_grade=%s,gradeCompareWithPoint=%s,status=%s,positionChange=%s,specialMoney=%s,newKpiDescriptions=%s WHERE employeeid=%s AND year=%s AND term=%s"
        cursor.execute(sqlUp,(data_new['totalGrade'],data_new['totalGradePercent'],data_new['oldgrade'],data_new['gradeCompareWithPoint'],data_new['status'],data_new['positionChange'],data_new['specialMoney'],data_new['newKpiDescriptions'],data_new['employeeid'],data_new['year'],data_new['term']))

        i=1
        for i in xrange(len(data_new['portfolioLists'])):
            try:
                sqlQry = "SELECT project_kpi_id FROM project_kpi ORDER BY project_kpi_id DESC LIMIT 1"
                cursor.execute(sqlQry)
                columns = [column[0] for column in cursor.description]
                result = toJson(cursor.fetchall(),columns)
                project_kpi_id_last = int(result[0]['project_kpi_id'])+1
            except Exception as e:
                project_kpi_id_last = 1

            type_action = "ADD"

            sqlIn = "INSERT INTO project_kpi(year,term,employeeid,employeeid_kpi,project_kpi_id,expectedPortfolio,ExpectedLevel,CanDoLevel,summaryLevel,weightPortfolio,totalPoint,commentLevel_B_Up) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn,(data_new['year'],data_new['term'],employeeid,data_new['createby'],project_kpi_id_last,data_new['portfolioLists'][i]['expectedPortfolio'],data_new['portfolioLists'][i]['ExpectedLevel'],data_new['portfolioLists'][i]['CanDoLevel'],data_new['portfolioLists'][i]['summaryLevel'],data_new['portfolioLists'][i]['weightPortfolio'],data_new['portfolioLists'][i]['totalPoint'],data_new['portfolioLists'][i]['commentLevel_B_Up']))

            sqlIn_ = "INSERT INTO project_kpi_log(year,term,employeeid,employeeid_kpi,project_kpi_id,expectedPortfolio,ExpectedLevel,CanDoLevel,summaryLevel,weightPortfolio,totalPoint,commentLevel_B_Up,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_,(data_new['year'],data_new['term'],employeeid,data_new['createby'],project_kpi_id_last,data_new['portfolioLists'][i]['expectedPortfolio'],data_new['portfolioLists'][i]['ExpectedLevel'],data_new['portfolioLists'][i]['CanDoLevel'],data_new['portfolioLists'][i]['summaryLevel'],data_new['portfolioLists'][i]['weightPortfolio'],data_new['portfolioLists'][i]['totalPoint'],data_new['portfolioLists'][i]['commentLevel_B_Up'],type_action))

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

        sqlUp = "UPDATE employee_kpi SET totalGrade=%s,totalGradePercent=%s,old_grade=%s,gradeCompareWithPoint=%s,status=%s,positionChange=%s,specialMoney=%s,newKpiDescriptions=%s WHERE employeeid=%s AND year=%s AND term=%s"
        cursor.execute(sqlUp,(data_new['totalGrade'],data_new['totalGradePercent'],data_new['oldgrade'],data_new['gradeCompareWithPoint'],data_new['status'],data_new['positionChange'],data_new['specialMoney'],data_new['newKpiDescriptions'],data_new['employeeid'],data_new['year'],data_new['term']))

        sql = "SELECT * FROM project_kpi WHERE employeeid=%s AND project_kpi_id=%s AND year=%s AND term=%s"
        cursor.execute(sql,(data_new['employeeid'],data_new['project_kpi_id'],data_new['year'],data_new['term']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Edit"

        sqlIn_ = "INSERT INTO project_kpi_log(year,term,employeeid,employeeid_kpi,project_kpi_id,expectedPortfolio,ExpectedLevel,CanDoLevel,summaryLevel,weightPortfolio,totalPoint,commentLevel_B_Up,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_,(data_new['year'],data_new['term'],employeeid,data_new['createby'],data_new['portfolioLists'][0]['project_kpi_id'],result[0]['expectedPortfolio'],result[0]['ExpectedLevel'],result[0]['CanDoLevel'],result[0]['summaryLevel'],result[0]['weightPortfolio'],result[0]['totalPoint'],result[0]['commentLevel_B_Up'],type_action))


        sqlde = "DELETE FROM project_kpi WHERE employeeid=%s AND project_kpi_id=%s AND year=%s AND term=%s"
        cursor.execute(sqlde,(data_new['employeeid'],data_new['project_kpi_id'],data_new['year'],data_new['term']))

        sqlIn = "INSERT INTO project_kpi(year,term,employeeid,employeeid_kpi,project_kpi_id,expectedPortfolio,ExpectedLevel,CanDoLevel,summaryLevel,weightPortfolio,totalPoint,commentLevel_B_Up) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn,(data_new['year'],data_new['term'],employeeid,data_new['createby'],data_new['portfolioLists'][0]['project_kpi_id'],data_new['portfolioLists'][0]['expectedPortfolio'],data_new['portfolioLists'][0]['ExpectedLevel'],data_new['portfolioLists'][0]['CanDoLevel'],data_new['portfolioLists'][0]['summaryLevel'],data_new['portfolioLists'][0]['weightPortfolio'],data_new['portfolioLists'][0]['totalPoint'],data_new['portfolioLists'][0]['commentLevel_B_Up']))

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

        # result_token = CheckTokenAssessor_kpi(data_new['createby'],data_new['token'])
        # if result_token!='pass':
        #     return 'token fail'

        sqlUp = "UPDATE employee_kpi SET totalGrade=%s,totalGradePercent=%s,old_grade=%s,gradeCompareWithPoint=%s,status=%s,positionChange=%s,specialMoney=%s,newKpiDescriptions=%s WHERE employeeid=%s AND year=%s AND term=%s"
        cursor.execute(sqlUp,(data_new['totalGrade'],data_new['totalGradePercent'],data_new['oldgrade'],data_new['gradeCompareWithPoint'],data_new['status'],data_new['positionChange'],data_new['specialMoney'],data_new['newKpiDescriptions'],data_new['employeeid'],data_new['year'],data_new['term']))

        sql = "SELECT * FROM project_kpi WHERE employeeid=%s AND project_kpi_id=%s AND year=%s AND term=%s"
        cursor.execute(sql,(data_new['employeeid'],data_new['project_kpi_id'],data_new['year'],data_new['term']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Delete"

        sqlIn_ = "INSERT INTO project_kpi_log(year,term,employeeid,employeeid_kpi,project_kpi_id,expectedPortfolio,ExpectedLevel,CanDoLevel,summaryLevel,weightPortfolio,totalPoint,commentLevel_B_Up,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_,(data_new['year'],data_new['term'],employeeid,data_new['createby'],data_new['portfolioLists'][0]['project_kpi_id'],result[0]['expectedPortfolio'],result[0]['ExpectedLevel'],result[0]['CanDoLevel'],result[0]['summaryLevel'],result[0]['weightPortfolio'],result[0]['totalPoint'],result[0]['commentLevel_B_Up'],type_action))

        sqlde = "DELETE FROM project_kpi WHERE employeeid=%s AND project_kpi_id=%s AND year=%s AND term=%s"
        cursor.execute(sqlde,(data_new['employeeid'],data_new['project_kpi_id'],data_new['year'],data_new['term']))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Add_emp_kpi_tranfer', methods=['POST'])
@connect_sql()
def Add_emp_kpi_tranfer(cursor):
    # try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        employeeid_leadernew = str(data_new['employeeid_new'])
        try:
            sql44 = "SELECT name FROM employee_kpi WHERE employeeid=%s AND em_id_leader=%s AND year=%s AND term=%s"
            cursor.execute(sql44,(data_new['employeeid'],employeeid_leadernew,data_new['year'],data_new['term']))
            columns = [column[0] for column in cursor.description]
            result_44 = toJson(cursor.fetchall(),columns)
            name = result_44[0]['name']
            return "employee is duplicate"
        except Exception as e:
            pass

        try:
            sql44 = "SELECT name_asp FROM assessor_kpi WHERE companyid=%s AND employeeid=%s AND org_name_id=%s"
            cursor.execute(sql44,(data_new['companyid'],employeeid_leadernew,data_new['org_name_id']))
            columns = [column[0] for column in cursor.description]
            result_test = toJson(cursor.fetchall(),columns)
            name_test = result_test[0]['name_asp']
        except Exception as e:
            try:
                sqlQry = "SELECT assessor_kpi_id FROM assessor_kpi ORDER BY assessor_kpi_id DESC LIMIT 1"
                cursor.execute(sqlQry)
                columns = [column[0] for column in cursor.description]
                result = toJson(cursor.fetchall(),columns)
                assessor_kpi_id_last = result[0]['assessor_kpi_id']+1
            except Exception as e:
                assessor_kpi_id_last = 1

            sql = "INSERT INTO assessor_kpi (assessor_kpi_id,employeeid,companyid,name_asp,surname_asp,org_name_id,email_asp,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,(assessor_kpi_id_last,employeeid_leadernew,data_new['companyid'],data_new['name_asp'],data_new['surname_asp'],data_new['org_name_id'],data_new['email_asp'],data_new['createby']))

            type_action = "ADDtranfer"

            sql_log = "INSERT INTO assessor_kpi_log (assessor_kpi_id,employeeid,companyid,name_asp,surname_asp,org_name_id,email_asp,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql_log,(assessor_kpi_id_last,employeeid_leadernew,data_new['companyid'],data_new['name_asp'],data_new['surname_asp'],data_new['org_name_id'],data_new['email_asp'],data_new['createby'],type_action))


        sql_test = "SELECT * FROM employee_kpi WHERE employeeid=%s AND year=%s AND term=%s"
        cursor.execute(sql_test,(data_new['employeeid'],data_new['year'],data_new['term']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "tranfer"

        sqlIn_be2 = "INSERT INTO employee_kpi_log(year,term,companyid,em_id_leader,structure_salary,employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,group_kpi,star_date_kpi,status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_be2,(result[0]['year'],result[0]['term'],result[0]['companyid'],result[0]['employeeid'],result[0]['structure_salary'],data_new['employeeid'],result[0]['name'],result[0]['surname'],result[0]['org_name'],result[0]['position'],result[0]['work_date'],result[0]['work_month'],result[0]['work_year'],result[0]['old_grade'],result[0]['group_kpi'],result[0]['star_date_kpi'],result[0]['status'],data_new['createby'],type_action))

        sqlIn_tran = "INSERT INTO employee_kpi_tranfer(year,term,employeeid,em_id_leader,name_asp,surname_asp,createby) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_tran,(result[0]['year'],result[0]['term'],data_new['employeeid'],employeeid_leadernew,data_new['name_asp'],data_new['surname_asp'],data_new['createby']))

        sqlI9de = "DELETE FROM employee_kpi WHERE employeeid=%s AND em_id_leader=%s AND year=%s AND term=%s"
        cursor.execute(sqlI9de,(data_new['employeeid'],data_new['createby'],data_new['year'],data_new['term']))

        sqlIn_main = "INSERT INTO employee_kpi(year,term,companyid,em_id_leader,structure_salary,employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,group_kpi,star_date_kpi,status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_main,(result[0]['year'],result[0]['term'],result[0]['companyid'],employeeid_leadernew,result[0]['structure_salary'],result[0]['employeeid'],result[0]['name'],result[0]['surname'],result[0]['org_name'],result[0]['position'],result[0]['work_date'],result[0]['work_month'],result[0]['work_year'],result[0]['old_grade'],result[0]['group_kpi'],result[0]['star_date_kpi'],result[0]['status'],result[0]['createby']))

        return "Success"
    # except Exception as e:
    #     logserver(e)
    #     return "fail"
