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

        sqlUp = "UPDATE employee_kpi SET totalGrade=%s,totalGradePercent=%s,old_grade=%s,gradeCompareWithPoint=%s,status=%s,positionChange=%s,specialMoney=%s,newKpiDescriptions=%s,date_bet=%s,validstatus=2 WHERE employeeid=%s AND year=%s AND term=%s"
        cursor.execute(sqlUp,(data_new['totalGrade'],data_new['totalGradePercent'],data_new['oldgrade'],data_new['gradeCompareWithPoint'],data_new['status'],data_new['positionChange'],data_new['specialMoney'],data_new['newKpiDescriptions'],data_new['date_bet'],data_new['employeeid'],data_new['year'],data_new['term']))

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
@app.route('/Add_project_bet', methods=['POST'])
@connect_sql()
def Add_project_bet(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        employeeid = data_new['employeeid']

        result_token = CheckTokenAssessor_kpi(data_new['createby'],data_new['token'])
        if result_token!='pass':
            return 'token fail'

        # sqlUp = "UPDATE employee_kpi SET totalGrade=%s,totalGradePercent=%s,old_grade=%s,gradeCompareWithPoint=%s,status=%s,positionChange=%s,specialMoney=%s,newKpiDescriptions=%s WHERE employeeid=%s AND year=%s AND term=%s"
        # cursor.execute(sqlUp,(data_new['totalGrade'],data_new['totalGradePercent'],data_new['oldgrade'],data_new['gradeCompareWithPoint'],data_new['status'],data_new['positionChange'],data_new['specialMoney'],data_new['newKpiDescriptions'],data_new['employeeid'],data_new['year'],data_new['term']))

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

            sqlIn = "INSERT INTO project_kpi(year,term,employeeid,employeeid_kpi,project_kpi_id,expectedPortfolio) VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn,(data_new['year'],data_new['term'],employeeid,data_new['createby'],project_kpi_id_last,data_new['portfolioLists'][i]['expectedPortfolio']))

            sqlIn_ = "INSERT INTO project_kpi_log(year,term,employeeid,employeeid_kpi,project_kpi_id,expectedPortfolio,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_,(data_new['year'],data_new['term'],employeeid,data_new['createby'],project_kpi_id_last,data_new['portfolioLists'][i]['expectedPortfolio'],type_action))

            sqlUp_main = "UPDATE employee_kpi SET Pass=%s,comment_pass=%s,date_bet=%s,positionChange=%s,specialMoney=%s,newKpiDescriptions=%s,positionChange_bet=%s,status=%s,date_bet=%s,validstatus=2  WHERE employeeid=%s AND year=%s AND term=%s"
            cursor.execute(sqlUp_main,(data_new['Pass'],data_new['comment_pass'],data_new['date_bet'],data_new['positionChange'],data_new['specialMoney'],data_new['newKpiDescriptions'],data_new['positionChange_bet'],data_new['status'],data_new['date_bet'],data_new['employeeid'],data_new['year'],data_new['term']))

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

        sqlUp = "UPDATE employee_kpi SET totalGrade=%s,totalGradePercent=%s,old_grade=%s,gradeCompareWithPoint=%s,status=%s,positionChange=%s,specialMoney=%s,newKpiDescriptions=%s,date_bet=%s,validstatus=2 WHERE employeeid=%s AND year=%s AND term=%s"
        cursor.execute(sqlUp,(data_new['totalGrade'],data_new['totalGradePercent'],data_new['oldgrade'],data_new['gradeCompareWithPoint'],data_new['status'],data_new['positionChange'],data_new['specialMoney'],data_new['newKpiDescriptions'],data_new['date_bet'],data_new['employeeid'],data_new['year'],data_new['term']))

        i=0
        for i in xrange(len(data_new['portfolioLists'])):
            try:
                sql = "SELECT * FROM project_kpi WHERE employeeid=%s AND project_kpi_id=%s AND year=%s AND term=%s"
                cursor.execute(sql,(data_new['employeeid'],data_new['portfolioLists'][i]['project_kpi_id'],data_new['year'],data_new['term']))
                columns = [column[0] for column in cursor.description]
                result = toJson(cursor.fetchall(),columns)

                type_action = "Edit"

                try:
                    sqlIn_ = "INSERT INTO project_kpi_log(year,term,employeeid,employeeid_kpi,project_kpi_id,expectedPortfolio,ExpectedLevel,CanDoLevel,summaryLevel,weightPortfolio,totalPoint,commentLevel_B_Up,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sqlIn_,(data_new['year'],data_new['term'],employeeid,data_new['createby'],data_new['portfolioLists'][i]['project_kpi_id'],result[0]['expectedPortfolio'],result[0]['ExpectedLevel'],result[0]['CanDoLevel'],result[0]['summaryLevel'],result[0]['weightPortfolio'],result[0]['totalPoint'],result[0]['commentLevel_B_Up'],type_action))
                except Exception as e:
                    sqlde = "DELETE FROM project_kpi WHERE employeeid=%s AND project_kpi_id=%s AND year=%s AND term=%s"
                    cursor.execute(sqlde,(data_new['employeeid'],data_new['portfolioLists'][i]['project_kpi_id'],data_new['year'],data_new['term']))
                # try:
                sqlde = "DELETE FROM project_kpi WHERE employeeid=%s AND project_kpi_id=%s AND year=%s AND term=%s"
                cursor.execute(sqlde,(data_new['employeeid'],data_new['portfolioLists'][i]['project_kpi_id'],data_new['year'],data_new['term']))
                # except Exception as e:
                #     pass

                sqlIn = "INSERT INTO project_kpi(year,term,employeeid,employeeid_kpi,project_kpi_id,expectedPortfolio,ExpectedLevel,CanDoLevel,summaryLevel,weightPortfolio,totalPoint,commentLevel_B_Up) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn,(data_new['year'],data_new['term'],employeeid,data_new['createby'],data_new['portfolioLists'][i]['project_kpi_id'],data_new['portfolioLists'][i]['expectedPortfolio'],data_new['portfolioLists'][i]['ExpectedLevel'],data_new['portfolioLists'][i]['CanDoLevel'],data_new['portfolioLists'][i]['summaryLevel'],data_new['portfolioLists'][i]['weightPortfolio'],data_new['portfolioLists'][i]['totalPoint'],data_new['portfolioLists'][i]['commentLevel_B_Up']))
            except Exception as e:
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

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Edit_project_bet', methods=['POST'])
@connect_sql()
def Edit_project_bet(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        employeeid = data_new['employeeid']

        result_token = CheckTokenAssessor_kpi(data_new['createby'],data_new['token'])
        if result_token!='pass':
            return 'token fail'

        sqlUp_main = "UPDATE employee_kpi SET Pass=%s,comment_pass=%s,date_bet=%s,positionChange=%s,specialMoney=%s,newKpiDescriptions=%s,positionChange_bet=%s,status=%s,validstatus=2  WHERE employeeid=%s AND year=%s AND term=%s"
        cursor.execute(sqlUp_main,(data_new['Pass'],data_new['comment_pass'],data_new['date_bet'],data_new['positionChange'],data_new['specialMoney'],data_new['newKpiDescriptions'],data_new['positionChange_bet'],data_new['status'],data_new['employeeid'],data_new['year'],data_new['term']))

        i=0
        for i in xrange(len(data_new['portfolioLists'])):
            try:
                sql = "SELECT * FROM project_kpi WHERE employeeid=%s AND project_kpi_id=%s AND year=%s AND term=%s"
                cursor.execute(sql,(data_new['employeeid'],data_new['portfolioLists'][i]['project_kpi_id'],data_new['year'],data_new['term']))
                columns = [column[0] for column in cursor.description]
                result = toJson(cursor.fetchall(),columns)

                type_action = "Edit"

                try:
                    sqlIn_ = "INSERT INTO project_kpi_log(year,term,employeeid,employeeid_kpi,project_kpi_id,expectedPortfolio,ExpectedLevel,CanDoLevel,summaryLevel,weightPortfolio,totalPoint,commentLevel_B_Up,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sqlIn_,(data_new['year'],data_new['term'],employeeid,data_new['createby'],data_new['portfolioLists'][i]['project_kpi_id'],result[0]['expectedPortfolio'],result[0]['ExpectedLevel'],result[0]['CanDoLevel'],result[0]['summaryLevel'],result[0]['weightPortfolio'],result[0]['totalPoint'],result[0]['commentLevel_B_Up'],type_action))
                except Exception as e:
                    sqlde = "DELETE FROM project_kpi WHERE employeeid=%s AND project_kpi_id=%s AND year=%s AND term=%s"
                    cursor.execute(sqlde,(data_new['employeeid'],data_new['portfolioLists'][i]['project_kpi_id'],data_new['year'],data_new['term']))
                # try:
                sqlde = "DELETE FROM project_kpi WHERE employeeid=%s AND project_kpi_id=%s AND year=%s AND term=%s"
                cursor.execute(sqlde,(data_new['employeeid'],data_new['portfolioLists'][i]['project_kpi_id'],data_new['year'],data_new['term']))
                # except Exception as e:
                #     pass

                sqlIn = "INSERT INTO project_kpi(year,term,employeeid,employeeid_kpi,project_kpi_id,expectedPortfolio) VALUES (%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn,(data_new['year'],data_new['term'],employeeid,data_new['createby'],data_new['portfolioLists'][i]['project_kpi_id'],data_new['portfolioLists'][i]['expectedPortfolio']))
            except Exception as e:
                try:
                    sqlQry = "SELECT project_kpi_id FROM project_kpi ORDER BY project_kpi_id DESC LIMIT 1"
                    cursor.execute(sqlQry)
                    columns = [column[0] for column in cursor.description]
                    result = toJson(cursor.fetchall(),columns)
                    project_kpi_id_last = int(result[0]['project_kpi_id'])+1
                except Exception as e:
                    project_kpi_id_last = 1

                type_action = "ADD"

                sqlIn = "INSERT INTO project_kpi(year,term,employeeid,employeeid_kpi,project_kpi_id,expectedPortfolio) VALUES (%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn,(data_new['year'],data_new['term'],employeeid,data_new['createby'],project_kpi_id_last,data_new['portfolioLists'][i]['expectedPortfolio']))

                sqlIn_ = "INSERT INTO project_kpi_log(year,term,employeeid,employeeid_kpi,project_kpi_id,expectedPortfolio,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn_,(data_new['year'],data_new['term'],employeeid,data_new['createby'],project_kpi_id_last,data_new['portfolioLists'][i]['expectedPortfolio'],type_action))

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

        sqlUp = "UPDATE employee_kpi SET totalGrade=%s,totalGradePercent=%s,old_grade=%s,gradeCompareWithPoint=%s,status=%s,positionChange=%s,specialMoney=%s,newKpiDescriptions=%s,validstatus=2 WHERE employeeid=%s AND year=%s AND term=%s"
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
@app.route('/Delete_project_bet', methods=['POST'])
@connect_sql()
def Delete_project_bet(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        employeeid = data_new['employeeid']

        result_token = CheckTokenAssessor_kpi(data_new['createby'],data_new['token'])
        if result_token!='pass':
            return 'token fail'

        sqlUp = "UPDATE employee_kpi SET validstatus=2 WHERE employeeid=%s AND year=%s AND term=%s"
        cursor.execute(sqlUp,(data_new['employeeid'],data_new['year'],data_new['term']))

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
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        result_token = CheckTokenAssessor_kpi(data_new['createby'],data_new['token'])
        if result_token!='pass':
            return 'token fail'

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
                result_ass = toJson(cursor.fetchall(),columns)
                assessor_kpi_id_last = result_ass[0]['assessor_kpi_id']+1
            except Exception as e:
                assessor_kpi_id_last = 1
            type = 'submain'
            sql = "INSERT INTO assessor_kpi (assessor_kpi_id,employeeid,companyid,name_asp,surname_asp,org_name_id,email_asp,createby,type) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,(assessor_kpi_id_last,employeeid_leadernew,data_new['companyid'],data_new['name_asp'],data_new['surname_asp'],data_new['org_name_id'],data_new['email_asp'],data_new['createby'],type))

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

        sqlI9de = "DELETE FROM employee_kpi WHERE employeeid=%s AND year=%s AND term=%s"
        cursor.execute(sqlI9de,(data_new['employeeid'],data_new['year'],data_new['term']))

        sqlIn_main = "INSERT INTO employee_kpi(year,term,companyid,em_id_leader,structure_salary,employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,group_kpi,star_date_kpi,status,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_main,(result[0]['year'],result[0]['term'],result[0]['companyid'],employeeid_leadernew,result[0]['structure_salary'],result[0]['employeeid'],result[0]['name'],result[0]['surname'],result[0]['org_name'],result[0]['position'],result[0]['work_date'],result[0]['work_month'],result[0]['work_year'],result[0]['old_grade'],result[0]['group_kpi'],result[0]['star_date_kpi'],result[0]['status'],data_new['createby']))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/cancel_emp_kpi_tranfer', methods=['POST'])
@connect_sql()
def cancel_emp_kpi_tranfer(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        # employeeid_leadernew = str(data_new['employeeid_new'])
        result_token = CheckTokenAssessor_kpi(data_new['createby'],data_new['token'])
        if result_token!='pass':
            return 'token fail'

        try:
            sql_check = "SELECT employeeid FROM employee_kpi WHERE employeeid=%s AND year=%s AND term=%s AND last_name IS NOT NULL"
            cursor.execute(sql_check,(data_new['employeeid'],data_new['year'],data_new['term']))
            columns = [column[0] for column in cursor.description]
            result_check = toJson(cursor.fetchall(),columns)
            test_ = result_check['employeeid']
            return "Evaluate end"
        except Exception as e:
            pass

        sql_test = "SELECT * FROM employee_kpi WHERE employeeid=%s AND year=%s AND term=%s"
        cursor.execute(sql_test,(data_new['employeeid'],data_new['year'],data_new['term']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sql_revers = "SELECT createby FROM employee_kpi_tranfer WHERE employeeid=%s AND year=%s AND term=%s AND em_id_leader=%s"
        cursor.execute(sql_revers,(data_new['employeeid'],data_new['year'],data_new['term'],data_new['old_emid_leader']))
        columns = [column[0] for column in cursor.description]
        result_revers = toJson(cursor.fetchall(),columns)

        type_action = "cancel_hr"

        sqlIn_be2 = "INSERT INTO employee_kpi_log(year,term,companyid,em_id_leader,structure_salary,employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,group_kpi,star_date_kpi,status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_be2,(result[0]['year'],result[0]['term'],result[0]['companyid'],result[0]['employeeid'],result[0]['structure_salary'],data_new['employeeid'],result[0]['name'],result[0]['surname'],result[0]['org_name'],result[0]['position'],result[0]['work_date'],result[0]['work_month'],result[0]['work_year'],result[0]['old_grade'],result[0]['group_kpi'],result[0]['star_date_kpi'],result[0]['status'],data_new['old_emid_leader'],type_action))

        sqlI9de = "DELETE FROM employee_kpi WHERE employeeid=%s AND em_id_leader=%s AND year=%s AND term=%s"
        cursor.execute(sqlI9de,(data_new['employeeid'],data_new['old_emid_leader'],data_new['year'],data_new['term']))

        if not result_revers:
            sqlIn_main = "INSERT INTO employee_kpi(year,term,companyid,structure_salary,employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,group_kpi,star_date_kpi,status,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_main,(result[0]['year'],result[0]['term'],result[0]['companyid'],result[0]['structure_salary'],result[0]['employeeid'],result[0]['name'],result[0]['surname'],result[0]['org_name'],result[0]['position'],result[0]['work_date'],result[0]['work_month'],result[0]['work_year'],result[0]['old_grade'],result[0]['group_kpi'],result[0]['star_date_kpi'],result[0]['status'],data_new['old_emid_leader']))

            sqlUp_main = "UPDATE employee_kpi SET comment_cancel=%s,validstatus=4  WHERE employeeid=%s AND year=%s AND term=%s"
            cursor.execute(sqlUp_main,(data_new['comment_cancel'],data_new['employeeid'],data_new['year'],data_new['term']))

        else:
            sqlIn_main = "INSERT INTO employee_kpi(year,term,companyid,em_id_leader,structure_salary,employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,group_kpi,star_date_kpi,status,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_main,(result[0]['year'],result[0]['term'],result[0]['companyid'],result_revers[0]['createby'],result[0]['structure_salary'],result[0]['employeeid'],result[0]['name'],result[0]['surname'],result[0]['org_name'],result[0]['position'],result[0]['work_date'],result[0]['work_month'],result[0]['work_year'],result[0]['old_grade'],result[0]['group_kpi'],result[0]['star_date_kpi'],result[0]['status'],data_new['old_emid_leader']))

            sqlUp_main = "UPDATE employee_kpi SET comment_cancel=%s,validstatus=4  WHERE employeeid=%s AND year=%s AND term=%s"
            cursor.execute(sqlUp_main,(data_new['comment_cancel'],data_new['employeeid'],data_new['year'],data_new['term']))

        try:
            sqlI9de_tranfer = "DELETE FROM employee_kpi_tranfer WHERE employeeid=%s AND em_id_leader=%s AND year=%s AND term=%s"
            cursor.execute(sqlI9de_tranfer,(data_new['employeeid'],data_new['old_emid_leader'],data_new['year'],data_new['term']))
        except Exception as e:
            pass

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/reverse_emp_kpi_tranfer', methods=['POST'])
@connect_sql()
def reverse_emp_kpi_tranfer(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        # employeeid_leadernew = str(data_new['employeeid_new'])
        result_token = CheckTokenAssessor_kpi(data_new['createby'],data_new['token'])
        if result_token!='pass':
            return 'token fail'

        try:
            sql_check = "SELECT employeeid FROM employee_kpi WHERE employeeid=%s AND year=%s AND term=%s OR validstatus=2 "
            cursor.execute(sql_check,(data_new['employeeid'],data_new['year'],data_new['term']))
            columns = [column[0] for column in cursor.description]
            result_check = toJson(cursor.fetchall(),columns)
            test_ = result_check['employeeid']
            return "Evaluate end"
        except Exception as e:
            pass

        sql_test = "SELECT * FROM employee_kpi WHERE employeeid=%s AND year=%s AND term=%s"
        cursor.execute(sql_test,(data_new['employeeid'],data_new['year'],data_new['term']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sql_revers = "SELECT createby FROM employee_kpi_tranfer WHERE employeeid=%s AND year=%s AND term=%s AND em_id_leader=%s"
        cursor.execute(sql_revers,(data_new['employeeid'],data_new['year'],data_new['term'],data_new['old_emid_leader']))
        columns = [column[0] for column in cursor.description]
        result_revers = toJson(cursor.fetchall(),columns)

        type_action = "canceltranfer"

        sqlIn_be2 = "INSERT INTO employee_kpi_log(year,term,companyid,em_id_leader,structure_salary,employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,group_kpi,star_date_kpi,status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_be2,(result[0]['year'],result[0]['term'],result[0]['companyid'],result[0]['employeeid'],result[0]['structure_salary'],data_new['employeeid'],result[0]['name'],result[0]['surname'],result[0]['org_name'],result[0]['position'],result[0]['work_date'],result[0]['work_month'],result[0]['work_year'],result[0]['old_grade'],result[0]['group_kpi'],result[0]['star_date_kpi'],result[0]['status'],data_new['old_emid_leader'],type_action))

        sqlI9de = "DELETE FROM employee_kpi WHERE employeeid=%s AND em_id_leader=%s AND year=%s AND term=%s"
        cursor.execute(sqlI9de,(data_new['employeeid'],data_new['old_emid_leader'],data_new['year'],data_new['term']))

        if not result_revers:
            sqlIn_main = "INSERT INTO employee_kpi(year,term,companyid,structure_salary,employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,group_kpi,star_date_kpi,status,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_main,(result[0]['year'],result[0]['term'],result[0]['companyid'],result[0]['structure_salary'],result[0]['employeeid'],result[0]['name'],result[0]['surname'],result[0]['org_name'],result[0]['position'],result[0]['work_date'],result[0]['work_month'],result[0]['work_year'],result[0]['old_grade'],result[0]['group_kpi'],result[0]['star_date_kpi'],result[0]['status'],data_new['old_emid_leader']))
        else:
            sqlIn_main = "INSERT INTO employee_kpi(year,term,companyid,em_id_leader,structure_salary,employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,group_kpi,star_date_kpi,status,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_main,(result[0]['year'],result[0]['term'],result[0]['companyid'],result_revers[0]['createby'],result[0]['structure_salary'],result[0]['employeeid'],result[0]['name'],result[0]['surname'],result[0]['org_name'],result[0]['position'],result[0]['work_date'],result[0]['work_month'],result[0]['work_year'],result[0]['old_grade'],result[0]['group_kpi'],result[0]['star_date_kpi'],result[0]['status'],data_new['old_emid_leader']))

        try:
            sqlI9de_tranfer = "DELETE FROM employee_kpi_tranfer WHERE employeeid=%s AND em_id_leader=%s AND year=%s AND term=%s"
            cursor.execute(sqlI9de_tranfer,(data_new['employeeid'],data_new['old_emid_leader'],data_new['year'],data_new['term']))
        except Exception as e:
            pass

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Update_grade_GM', methods=['POST'])
@connect_sql()
def Update_grade_GM(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        result_token = CheckTokenGM(data_new['createby'],data_new['token'])
        if result_token!='pass':
            return 'token fail'

        sqlUp_main = "UPDATE employee_kpi SET old_grade_GM=%s,status_GM=%s,positionChange_GM=%s,specialMoney_GM=%s,newKpiDescriptions_GM=%s,date_bet_gm=%s,validstatus=3  WHERE employeeid=%s AND year=%s AND term=%s"
        cursor.execute(sqlUp_main,(data_new['old_grade_GM'],data_new['status_GM'],data_new['positionChange_GM'],data_new['specialMoney_GM'],data_new['newKpiDescriptions_GM'],data_new['date_bet_gm'],data_new['employeeid'],data_new['year'],data_new['term']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qry_user_kpi_tranfer', methods=['POST'])
@connect_sql()
def Qry_user_kpi_tranfer(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        year_term = ""

        try:
            year_term = 'AND employee_kpi_tranfer.year='+'"'+str(data_new['year'])+'"'+'AND employee_kpi_tranfer.term='+'"'+str(data_new['term'])+'"'
        except Exception as e:
            pass

        sql = "SELECT employee_kpi_tranfer.*,employee_kpi.name,employee_kpi.surname FROM employee_kpi\
                INNER JOIN employee_kpi_tranfer ON employee_kpi.employeeid = employee_kpi_tranfer.employeeid\
        WHERE employee_kpi_tranfer.createby="+data_new['createby']+" "+year_term+""
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qry_Dashboard', methods=['POST'])
@connect_sql()
def Qry_Dashboard(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        if (str(data_new['type'])=='main')and(str(data_new['companyid'])!='23'):
            sql = "SELECT  (SELECT COUNT(employeeid) FROM employee_kpi WHERE old_grade='A') AS grade_A\
                          ,(SELECT COUNT(employeeid) FROM employee_kpi WHERE old_grade='B+') AS grade_B_plus\
                          ,(SELECT COUNT(employeeid) FROM employee_kpi WHERE old_grade='B') AS grade_B\
                          ,(SELECT COUNT(employeeid) FROM employee_kpi WHERE old_grade='C+') AS grade_C_plus\
                          ,(SELECT COUNT(employeeid) FROM employee_kpi WHERE old_grade='C') AS grade_C\
                          ,(SELECT COUNT(employeeid) FROM employee_kpi WHERE old_grade='D+') AS grade_D_plus\
                          ,(SELECT COUNT(employeeid) FROM employee_kpi WHERE old_grade='D') AS grade_D\
                          ,(SELECT COUNT(employeeid) FROM employee_kpi WHERE old_grade='E') AS grade_E\
                          ,(SELECT COUNT(employeeid) FROM employee_kpi WHERE validstatus=1) AS not_grade\
                          ,(SELECT COUNT(employeeid) FROM employee_kpi) AS Total_employee\
             FROM employee_kpi WHERE year=%s AND term=%s AND companyid=%s GROUP BY employeeid LIMIT 1"
            cursor.execute(sql,(data_new['year'],data_new['term'],data_new['companyid']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            return jsonify(result)
        else:
            sql = "SELECT  (SELECT COUNT(employeeid) FROM employee_kpi WHERE old_grade='A') AS grade_A\
                          ,(SELECT COUNT(employeeid) FROM employee_kpi WHERE old_grade='B+') AS grade_B_plus\
                          ,(SELECT COUNT(employeeid) FROM employee_kpi WHERE old_grade='B') AS grade_B\
                          ,(SELECT COUNT(employeeid) FROM employee_kpi WHERE old_grade='C+') AS grade_C_plus\
                          ,(SELECT COUNT(employeeid) FROM employee_kpi WHERE old_grade='C') AS grade_C\
                          ,(SELECT COUNT(employeeid) FROM employee_kpi WHERE old_grade='D+') AS grade_D_plus\
                          ,(SELECT COUNT(employeeid) FROM employee_kpi WHERE old_grade='D') AS grade_D\
                          ,(SELECT COUNT(employeeid) FROM employee_kpi WHERE old_grade='E') AS grade_E\
                          ,(SELECT COUNT(employeeid) FROM employee_kpi WHERE validstatus=1) AS not_grade\
                          ,(SELECT COUNT(employeeid) FROM employee_kpi) AS Total_employee\
             FROM employee_kpi WHERE year=%s AND term=%s GROUP BY employeeid LIMIT 1"
            cursor.execute(sql,(data_new['year'],data_new['term']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
