#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *
@app.route('/Qry_user_kpi_mobile/<employee_id>', methods=['GET'])
@connect_sql()
def Qry_user_kpi_mobile(cursor,employee_id):
    try:
        print 'id',employee_id        
        sql_select_accessor = """SELECT * FROM `assessor_kpi` WHERE employeeid = %s GROUP BY employeeid"""
        cursor.execute(sql_select_accessor,(employee_id))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        employee = result[0]
        print employee['type'],employee['companyid']
        year_term = "WHERE employee_kpi.em_id_leader="+'"'+employee['employeeid']+'"'
        resultJson = {}
        resultJson.update({'status_onechat':employee['status_onechat']})

        # หัวหน้า บอลูก
        if (employee['type']=='main')and(str(employee['companyid'])!='23'):

            # try:
            #     year_term = "WHERE employee_kpi.companyid="+"'"+employee['companyid']+"'"+' AND employee_kpi.year='+'"'+str(data_new['year'])+'"'+'AND employee_kpi.term='+'"'+str(data_new['term'])+'"'+' OR employee_kpi.em_id_leader='+'"'+str(data_new['em_id_leader'])+'"'
            # except Exception as e:
            # year_term = "WHERE employee_kpi.companyid="+"'"+str(employee['companyid'])+"''employee_kpi.em_id_leader='+'"'+str(employee['employeeid'])+'"'

            print 'yearterm',year_term
            # sql = """SELECT employee_kpi.validstatus,employee_kpi.em_id_leader,employee_kpi.newKpiDescriptions_GM,employee_kpi.specialMoney_GM,employee_kpi.positionChange_GM,
            #             employee_kpi.status_GM,employee_kpi.old_grade_GM,employee_kpi.createby,employee_kpi.comment_cancel,employee_kpi.year,employee_kpi.term,
            #             employee_kpi.employeeid,employee_kpi.name,employee_kpi.companyid AS company_short_name,employee_kpi.surname,org_name.org_name_detail,position.position_detail,
            #             employee_kpi.work_date,employee_kpi.work_month,employee_kpi.work_year,employee_kpi.old_grade,employee_kpi.grade,employee_kpi.comment_hr,
            #             employee_kpi.present_kpi,employee_kpi.star_date_kpi,employee_kpi.status,project_kpi.present_file 
            #             FROM employee_kpi LEFT JOIN org_name ON employee_kpi.org_name = org_name.org_name_id
            #             LEFT JOIN position ON employee_kpi.position = position.position_id
            #             LEFT JOIN project_kpi ON project_kpi.employeeid = employee_kpi.employeeid """+year_term
            sql = "SELECT employee_kpi.validstatus,employee_kpi.em_id_leader,employee_kpi.structure_salary,employee_kpi.date_bet,employee_kpi.newKpiDescriptions,employee_kpi.newKpiDescriptions_GM,employee_kpi.specialMoney_GM,employee_kpi.positionChange,employee_kpi.positionChange_GM,employee_kpi.status_GM,employee_kpi.old_grade_GM,employee_kpi.createby,employee_kpi.comment_cancel,employee_kpi.year,employee_kpi.term,employee_kpi.employeeid,employee_kpi.name,employee_kpi.companyid AS company_short_name,employee_kpi.surname,org_name.org_name_detail,position.position_detail,employee_kpi.work_date,employee_kpi.work_month,employee_kpi.work_year,employee_kpi.old_grade,employee_kpi.grade,employee_kpi.comment_hr,employee_kpi.present_kpi,employee_kpi.star_date_kpi,employee_kpi.status FROM employee_kpi\
                                                                                            LEFT JOIN org_name ON employee_kpi.org_name = org_name.org_name_id\
                                                                                            LEFT JOIN position ON employee_kpi.position = position.position_id\
            "+year_term+" GROUP BY employee_kpi.employeeid"
            cursor.execute(sql)
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            
            for employee in result:
                sql_projects = """SELECT * FROM project_kpi WHERE employeeid = %s AND year = %s AND term = %s"""
                cursor.execute(sql_projects,(employee['employeeid'],employee['year'],employee['term']))
                columns = [column[0] for column in cursor.description]
                result_projects = toJson(cursor.fetchall(),columns)
                employee.update({'projectKpi':result_projects})
                
            resultJson.update({'employeeLists':result})
            return jsonify(resultJson)
        
        # หัวหน้า inet
        elif (employee['type']=='main')and(str(employee['companyid'])=='23'):
            # try:
            #     print 'try'
            #     year_term = "WHERE employee_kpi.companyid="+"'"+str(data_new['companyid'])+"'"+' AND employee_kpi.org_name ='+'"'+str(data_new['org_name_id'])+'"'+' AND employee_kpi.year='+'"'+str(data_new['year'])+'"'+'AND employee_kpi.term='+'"'+str(data_new['term'])+'"'+' OR employee_kpi.em_id_leader='+'"'+str(data_new['em_id_leader'])+'"'
            # except Exception as e:
            #     print str(e)
            # year_term = "WHERE employee_kpi.companyid="+"'"+str(employee['companyid'])+"'"+' AND employee_kpi.org_name='+'"'+str(employee['org_name_id'])+'"'+' OR employee_kpi.em_id_leader='+'"'+str(employee['employeeid'])+'"'
            print 'yearterm',year_term,'elseif'
            # sql = """"SELECT employee_kpi.validstatus,employee_kpi.em_id_leader,employee_kpi.newKpiDescriptions_GM,employee_kpi.specialMoney_GM,employee_kpi.positionChange_GM,
            #             employee_kpi.status_GM,employee_kpi.old_grade_GM,employee_kpi.createby,employee_kpi.comment_cancel,employee_kpi.year,employee_kpi.term,employee_kpi.employeeid,
            #             employee_kpi.name,employee_kpi.companyid AS company_short_name,employee_kpi.surname,org_name.org_name_detail,position.position_detail,employee_kpi.work_date,
            #             employee_kpi.work_month,employee_kpi.work_year,employee_kpi.old_grade,employee_kpi.grade,employee_kpi.comment_hr,employee_kpi.present_kpi,employee_kpi.star_date_kpi,
            #             employee_kpi.status,project_kpi.present_file FROM employee_kpi
            #             LEFT JOIN org_name ON employee_kpi.org_name = org_name.org_name_id
            #             LEFT JOIN position ON employee_kpi.position = position.position_id
            #             LEFT JOIN project_kpi ON project_kpi.employeeid = employee_kpi.employeeid """+year_term
            sql = "SELECT employee_kpi.validstatus,employee_kpi.em_id_leader,employee_kpi.structure_salary,employee_kpi.date_bet,employee_kpi.newKpiDescriptions,employee_kpi.newKpiDescriptions_GM,employee_kpi.specialMoney_GM,employee_kpi.positionChange,employee_kpi.positionChange_GM,employee_kpi.status_GM,employee_kpi.old_grade_GM,employee_kpi.createby,employee_kpi.comment_cancel,employee_kpi.year,employee_kpi.term,employee_kpi.employeeid,employee_kpi.name,employee_kpi.companyid AS company_short_name,employee_kpi.surname,org_name.org_name_detail,position.position_detail,employee_kpi.work_date,employee_kpi.work_month,employee_kpi.work_year,employee_kpi.old_grade,employee_kpi.grade,employee_kpi.comment_hr,employee_kpi.present_kpi,employee_kpi.star_date_kpi,employee_kpi.status FROM employee_kpi\
                                                                                            LEFT JOIN org_name ON employee_kpi.org_name = org_name.org_name_id\
                                                                                            LEFT JOIN position ON employee_kpi.position = position.position_id\
            "+year_term+" "
            cursor.execute(sql)
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            
            for employee in result:
                sql_projects = """SELECT * FROM project_kpi WHERE employeeid = %s AND year = %s AND term = %s"""
                cursor.execute(sql_projects,(employee['employeeid'],employee['year'],employee['term']))
                columns = [column[0] for column in cursor.description]
                result_projects = toJson(cursor.fetchall(),columns)
                employee.update({'projectKpi':result_projects})

            resultJson.update({'employeeLists':result})
            return jsonify(resultJson)
        ### submain only
        else:
            # try:
            #     year_term = "WHERE employee_kpi.em_id_leader="+'"'+str(data_new['em_id_leader'])+'"'+' AND employee_kpi.year='+'"'+str(data_new['year'])+'"'+'AND employee_kpi.term='+'"'+str(data_new['term'])+'"'
            # except Exception as e:
            year_term = "WHERE employee_kpi.em_id_leader="+'"'+str(employee['employeeid'])+'" GROUP BY employee_kpi.em_id_leader'
            
            # sql = """SELECT employee_kpi.validstatus,employee_kpi.em_id_leader,employee_kpi.newKpiDescriptions_GM,employee_kpi.specialMoney_GM,employee_kpi.positionChange_GM,
            #             employee_kpi.status_GM,employee_kpi.old_grade_GM,employee_kpi.createby,employee_kpi.comment_cancel,employee_kpi.year,employee_kpi.term,employee_kpi.employeeid,
            #             employee_kpi.name,employee_kpi.companyid AS company_short_name,employee_kpi.surname,org_name.org_name_detail,position.position_detail,employee_kpi.work_date,
            #             employee_kpi.work_month,employee_kpi.work_year,employee_kpi.old_grade,employee_kpi.grade,employee_kpi.comment_hr,employee_kpi.present_kpi,employee_kpi.star_date_kpi,
            #             employee_kpi.status,project_kpi.present_file FROM employee_kpi\
            #             LEFT JOIN org_name ON employee_kpi.org_name = org_name.org_name_id
            #             LEFT JOIN position ON employee_kpi.position = position.position_id
            #             LEFT JOIN project_kpi ON project_kpi.employeeid = employee_kpi.employeeid """+year_term
            
            sql = "SELECT employee_kpi.validstatus,employee_kpi.em_id_leader,employee_kpi.structure_salary,employee_kpi.date_bet,employee_kpi.newKpiDescriptions,employee_kpi.newKpiDescriptions_GM,employee_kpi.specialMoney_GM,employee_kpi.positionChange,employee_kpi.positionChange_GM,employee_kpi.status_GM,employee_kpi.old_grade_GM,employee_kpi.createby,employee_kpi.comment_cancel,employee_kpi.year,employee_kpi.term,employee_kpi.employeeid,employee_kpi.name,employee_kpi.companyid AS company_short_name,employee_kpi.surname,org_name.org_name_detail,position.position_detail,employee_kpi.work_date,employee_kpi.work_month,employee_kpi.work_year,employee_kpi.old_grade,employee_kpi.grade,employee_kpi.comment_hr,employee_kpi.present_kpi,employee_kpi.star_date_kpi,employee_kpi.status FROM employee_kpi\
                                                                                            LEFT JOIN org_name ON employee_kpi.org_name = org_name.org_name_id\
                                                                                            LEFT JOIN position ON employee_kpi.position = position.position_id\
            "+year_term+" GROUP BY employee_kpi.employeeid"
            
            cursor.execute(sql)
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            for employee in result:
                sql_projects = """SELECT * FROM project_kpi WHERE employeeid = %s AND year = %s AND term = %s"""
                cursor.execute(sql_projects,(employee['employeeid'],employee['year'],employee['term']))
                columns = [column[0] for column in cursor.description]
                result_projects = toJson(cursor.fetchall(),columns)
                employee.update({'projectKpi':result_projects})
            resultJson.update({'employeeLists':result})
            return jsonify(resultJson)
        return jsonify(resultJson)
    except Exception as e:
        logserver(e)
        return "fail"


@app.route('/cancel_emp_kpi_mobile', methods=['POST'])
@connect_sql()
def cancel_emp_kpi_mobile(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

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

        sqlIn_be2 = "INSERT INTO employee_kpi_log(year,term,companyid,em_id_leader,structure_salary,employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,star_date_kpi,status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_be2,(result[0]['year'],result[0]['term'],result[0]['companyid'],result[0]['employeeid'],result[0]['structure_salary'],data_new['employeeid'],result[0]['name'],result[0]['surname'],result[0]['org_name'],result[0]['position'],result[0]['work_date'],result[0]['work_month'],result[0]['work_year'],result[0]['old_grade'],result[0]['star_date_kpi'],result[0]['status'],data_new['old_emid_leader'],type_action))

        sqlI9de = "DELETE FROM employee_kpi WHERE employeeid=%s AND em_id_leader=%s AND year=%s AND term=%s"
        cursor.execute(sqlI9de,(data_new['employeeid'],data_new['old_emid_leader'],data_new['year'],data_new['term']))

        if not result_revers:
            sqlIn_main = "INSERT INTO employee_kpi(year,term,companyid,structure_salary,employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,star_date_kpi,status,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_main,(result[0]['year'],result[0]['term'],result[0]['companyid'],result[0]['structure_salary'],result[0]['employeeid'],result[0]['name'],result[0]['surname'],result[0]['org_name'],result[0]['position'],result[0]['work_date'],result[0]['work_month'],result[0]['work_year'],result[0]['old_grade'],result[0]['star_date_kpi'],result[0]['status'],data_new['old_emid_leader']))

            sqlUp_main = "UPDATE employee_kpi SET comment_cancel=%s,validstatus=4  WHERE employeeid=%s AND year=%s AND term=%s"
            cursor.execute(sqlUp_main,(data_new['comment_cancel'],data_new['employeeid'],data_new['year'],data_new['term']))

        else:
            sqlIn_main = "INSERT INTO employee_kpi(year,term,companyid,em_id_leader,structure_salary,employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,star_date_kpi,status,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_main,(result[0]['year'],result[0]['term'],result[0]['companyid'],result_revers[0]['createby'],result[0]['structure_salary'],result[0]['employeeid'],result[0]['name'],result[0]['surname'],result[0]['org_name'],result[0]['position'],result[0]['work_date'],result[0]['work_month'],result[0]['work_year'],result[0]['old_grade'],result[0]['star_date_kpi'],result[0]['status'],data_new['old_emid_leader']))

            sqlUp_main = "UPDATE employee_kpi SET comment_cancel=%s WHERE employeeid=%s AND year=%s AND term=%s"
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
    
@app.route('/confirm_all_kpi_mobile', methods=['POST'])
@connect_sql()
def confirm_all_kpi(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql_update_status = """UPDATE `assessor_kpi` SET `status_onechat`=1 WHERE employeeid = %s"""
        cursor.execute(sql_update_status,(data_new['employeeid']))
        return "Success"
    except Exception as e:
        logserver(e)
        print str(e)
        return "fail"
    
@app.route('/add_project_mobile', methods=['POST'])
@connect_sql()
def add_project_mobile(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        employeeid = data_new['employeeid']

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

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"

@app.route('/edit_project_mobile', methods=['POST'])
@connect_sql()
def edit_project_mobile(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        employeeid = data_new['employeeid']
        print data_new
        
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
        print str(e)
        return "fail"