#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/checkuuidAccessor/<uuid>', methods=['GET'])
@connect_sql()
def checkuuidAccessor(cursor,uuid):
    try:
        sql_update_status = """SELECT * FROM `assessor_kpi` WHERE uuid_onechat =%s"""
        cursor.execute(sql_update_status,(uuid))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        print result[0]['employeeid']
        return jsonify(result[0]['employeeid'])
    except Exception as e:
        logserver(e)
        print str(e)
        return "fail"

@app.route('/checkuuidBoard/<uuid>', methods=['GET'])
@connect_sql()
def checkuuidBoard(cursor,uuid):
    try:
        sql_update_status = """SELECT * FROM `board_kpi_v2` WHERE uuid_onechat =%s"""
        cursor.execute(sql_update_status,(uuid))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        print result[0]['employeeid_board']
        return jsonify(result[0]['employeeid_board'])
    except Exception as e:
        logserver(e)
        print str(e)
        return "fail"

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
        year_term = "WHERE employee_kpi.em_id_leader="+'"'+employee['employeeid']+'"'
        print 'year_term',year_term
        resultJson = {}
        resultJson.update({'status_onechat':employee['status_onechat']})

        # หัวหน้า บอลูก
        if (employee['type']=='main')and(str(employee['companyid'])!='23'):
            print 'yearterm',year_term
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
                # try:
                #     encoded_Image=str("http://intranet.inet.co.th/assets/upload/staff/"+str(employee['employeeid'])+".jpg")
                #     open_path_ = urllib.urlopen(encoded_Image)
                #     htmlSource = open_path_.read()
                #     open_path_.close()
                #     test= htmlSource.decode('utf-8')
                #     encoded_Image=str("http://intranet.inet.co.th/assets/upload/staff/"+str(employee['employeeid'])+"s.jpg")
                #     employee.update({'image':encoded_Image})
                # except Exception as e:
                #     encoded_Image=str("http://intranet.inet.co.th/assets/upload/staff/"+str(employee['employeeid'])+".jpg")
                #     employee.update({'image':encoded_Image})
 
            resultJson.update({'employeeLists':result})
            return jsonify(resultJson)
        
        # หัวหน้า inet
        elif (employee['type']=='main')and(str(employee['companyid'])=='23'):
            print 'yearterm',year_term,'elseif'
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
                # try:
                #     encoded_Image=str("http://intranet.inet.co.th/assets/upload/staff/"+str(employee['employeeid'])+".jpg")
                #     open_path_ = urllib.urlopen(encoded_Image)
                #     htmlSource = open_path_.read()
                #     open_path_.close()
                #     test= htmlSource.decode('utf-8')
                #     encoded_Image=str("http://intranet.inet.co.th/assets/upload/staff/"+str(employee['employeeid'])+"s.jpg")
                #     employee.update({'image':encoded_Image})
                # except Exception as e:
                #     encoded_Image=str("http://intranet.inet.co.th/assets/upload/staff/"+str(employee['employeeid'])+".jpg")
                #     employee.update({'image':encoded_Image})
                
            resultJson.update({'employeeLists':result})
            return jsonify(resultJson)
        ### submain only
        else:
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
                # try:
                #     encoded_Image=str("http://intranet.inet.co.th/assets/upload/staff/"+str(employee['employeeid'])+".jpg")
                #     open_path_ = urllib.urlopen(encoded_Image)
                #     htmlSource = open_path_.read()
                #     open_path_.close()
                #     test= htmlSource.decode('utf-8')
                #     encoded_Image=str("http://intranet.inet.co.th/assets/upload/staff/"+str(employee['employeeid'])+"s.jpg")
                #     employee.update({'image':encoded_Image})
                # except Exception as e:
                #     encoded_Image=str("http://intranet.inet.co.th/assets/upload/staff/"+str(employee['employeeid'])+".jpg")
                #     employee.update({'image':encoded_Image})
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

@app.route('/QryEmployeeMobile', methods=['POST'])
@connect_sql()
def QryEmployeeMobile(cursor):
    try:
        sql = """SELECT employee.name_th,employee.employeeid,employee.surname_th,employee.email,employee.start_work,company.company_short_name,company.companyname,position.position_detail,section.sect_detail,org_name.org_name_detail,cost_center_name.cost_detail 
                    FROM employee LEFT JOIN company ON company.companyid = employee.company_id
                    LEFT JOIN position ON position.position_id = employee.position_id
                    LEFT JOIN section ON section.sect_id = employee.section_id
                    LEFT JOIN org_name ON org_name.org_name_id = employee.org_name_id
                    LEFT JOIN cost_center_name ON cost_center_name.cost_center_name_id = employee.cost_center_name_id"""
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
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

@app.route('/Qry_user_present_mobile/<employee_id>', methods=['GET'])
@connect_sql()
def Qry_user_present_mobile(cursor,employee_id):
    try:
        sql_select_accessor = """SELECT * FROM `assessor_kpi` WHERE employeeid = %s GROUP BY employeeid"""
        cursor.execute(sql_select_accessor,(employee_id))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        employee = result[0]
        year_term = "WHERE employee_kpi.em_id_leader="+'"'+employee['employeeid']+'" AND employee_kpi.present_kpi ="active"'
        print 'year_term',year_term
        resultJson = {}
        resultJson.update({'status_onechat':employee['status_onechat']})

        if (employee['type']=='main')and(str(employee['companyid'])!='23'):
            
            print 'yearterm',year_term
            sql = """SELECT employee_kpi.validstatus,employee_kpi.em_id_leader,employee_kpi.newKpiDescriptions_GM,employee_kpi.specialMoney_GM,employee_kpi.positionChange_GM,
                        employee_kpi.status_GM,employee_kpi.old_grade_GM,employee_kpi.createby,employee_kpi.comment_cancel,employee_kpi.year,employee_kpi.term,
                        employee_kpi.employeeid,employee_kpi.name,employee_kpi.companyid AS company_short_name,employee_kpi.surname,org_name.org_name_detail,position.position_detail,
                        employee_kpi.work_date,employee_kpi.work_month,employee_kpi.work_year,employee_kpi.old_grade,employee_kpi.grade,employee_kpi.comment_hr,
                        employee_kpi.present_kpi,employee_kpi.star_date_kpi,employee_kpi.status,employee_kpi.present_file  
                        FROM employee_kpi LEFT JOIN org_name ON employee_kpi.org_name = org_name.org_name_id
                        LEFT JOIN position ON employee_kpi.position = position.position_id
                         """+year_term
            cursor.execute(sql)
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            
            for employee in result:
                sql_projects = """SELECT * FROM project_kpi WHERE employeeid = %s AND year = %s AND term = %s"""
                cursor.execute(sql_projects,(employee['employeeid'],employee['year'],employee['term']))
                columns = [column[0] for column in cursor.description]
                result_projects = toJson(cursor.fetchall(),columns)
                employee.update({'projectKpi':result_projects})
                # try:
                #     encoded_Image=str("http://intranet.inet.co.th/assets/upload/staff/"+str(employee['employeeid'])+".jpg")
                #     open_path_ = urllib.urlopen(encoded_Image)
                #     htmlSource = open_path_.read()
                #     open_path_.close()
                #     test= htmlSource.decode('utf-8')
                #     encoded_Image=str("http://intranet.inet.co.th/assets/upload/staff/"+str(employee['employeeid'])+"s.jpg")
                #     employee.update({'image':encoded_Image})
                # except Exception as e:
                #     encoded_Image=str("http://intranet.inet.co.th/assets/upload/staff/"+str(employee['employeeid'])+".jpg")
                #     employee.update({'image':encoded_Image})
                
            resultJson.update({'employeeLists':result})
            return jsonify(resultJson)
        
        # หัวหน้า inet
        elif (employee['type']=='main')and(str(employee['companyid'])=='23'):
        
            sql = """SELECT employee_kpi.validstatus,employee_kpi.em_id_leader,employee_kpi.newKpiDescriptions_GM,employee_kpi.specialMoney_GM,employee_kpi.positionChange_GM,
                        employee_kpi.status_GM,employee_kpi.old_grade_GM,employee_kpi.createby,employee_kpi.comment_cancel,employee_kpi.year,employee_kpi.term,employee_kpi.employeeid,
                        employee_kpi.name,employee_kpi.companyid AS company_short_name,employee_kpi.surname,org_name.org_name_detail,position.position_detail,employee_kpi.work_date,
                        employee_kpi.work_month,employee_kpi.work_year,employee_kpi.old_grade,employee_kpi.grade,employee_kpi.comment_hr,employee_kpi.present_kpi,employee_kpi.star_date_kpi,
                        employee_kpi.status,employee_kpi.present_file FROM employee_kpi
                        LEFT JOIN org_name ON employee_kpi.org_name = org_name.org_name_id
                        LEFT JOIN position ON employee_kpi.position = position.position_id
                         """+year_term
            cursor.execute(sql)
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            
            for employee in result:
                sql_projects = """SELECT * FROM project_kpi WHERE employeeid = %s AND year = %s AND term = %s"""
                cursor.execute(sql_projects,(employee['employeeid'],employee['year'],employee['term']))
                columns = [column[0] for column in cursor.description]
                result_projects = toJson(cursor.fetchall(),columns)
                employee.update({'projectKpi':result_projects})
                # try:
                #     encoded_Image=str("http://intranet.inet.co.th/assets/upload/staff/"+str(employee['employeeid'])+".jpg")
                #     open_path_ = urllib.urlopen(encoded_Image)
                #     htmlSource = open_path_.read()
                #     open_path_.close()
                #     test= htmlSource.decode('utf-8')
                #     encoded_Image=str("http://intranet.inet.co.th/assets/upload/staff/"+str(employee['employeeid'])+"s.jpg")
                #     employee.update({'image':encoded_Image})
                # except Exception as e:
                #     encoded_Image=str("http://intranet.inet.co.th/assets/upload/staff/"+str(employee['employeeid'])+".jpg")
                #     employee.update({'image':encoded_Image})

            resultJson.update({'employeeLists':result})
            return jsonify(resultJson)
        ### submain only
        else:
            sql = """SELECT employee_kpi.validstatus,employee_kpi.em_id_leader,employee_kpi.newKpiDescriptions_GM,employee_kpi.specialMoney_GM,employee_kpi.positionChange_GM,
                        employee_kpi.status_GM,employee_kpi.old_grade_GM,employee_kpi.createby,employee_kpi.comment_cancel,employee_kpi.year,employee_kpi.term,employee_kpi.employeeid,
                        employee_kpi.name,employee_kpi.companyid AS company_short_name,employee_kpi.surname,org_name.org_name_detail,position.position_detail,employee_kpi.work_date,
                        employee_kpi.work_month,employee_kpi.work_year,employee_kpi.old_grade,employee_kpi.grade,employee_kpi.comment_hr,employee_kpi.present_kpi,employee_kpi.star_date_kpi,
                        employee_kpi.status,employee_kpi.present_file FROM employee_kpi
                        LEFT JOIN org_name ON employee_kpi.org_name = org_name.org_name_id
                        LEFT JOIN position ON employee_kpi.position = position.position_id
                        """+year_term
            cursor.execute(sql)
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            for employee in result:
                sql_projects = """SELECT * FROM project_kpi WHERE employeeid = %s AND year = %s AND term = %s"""
                cursor.execute(sql_projects,(employee['employeeid'],employee['year'],employee['term']))
                columns = [column[0] for column in cursor.description]
                result_projects = toJson(cursor.fetchall(),columns)
                employee.update({'projectKpi':result_projects})
                # try:
                #     encoded_Image=str("http://intranet.inet.co.th/assets/upload/staff/"+str(employee['employeeid'])+".jpg")
                #     open_path_ = urllib.urlopen(encoded_Image)
                #     htmlSource = open_path_.read()
                #     open_path_.close()
                #     test= htmlSource.decode('utf-8')
                #     encoded_Image=str("http://intranet.inet.co.th/assets/upload/staff/"+str(employee['employeeid'])+"s.jpg")
                #     employee.update({'image':encoded_Image})
                # except Exception as e:
                #     encoded_Image=str("http://intranet.inet.co.th/assets/upload/staff/"+str(employee['employeeid'])+".jpg")
                #     employee.update({'image':encoded_Image})
            resultJson.update({'employeeLists':result})
            return jsonify(resultJson)
        return jsonify(resultJson)
    except Exception as e:
        logserver(e)
        return "fail"
    
@app.route('/Qry_board_present_mobile/<employee_id>', methods=['GET'])
@connect_sql()
def Qry_user_board_mobile(cursor,employee_id):
    try:
        sql_select_board = """SELECT * FROM `board_kpi_v2` WHERE employeeid_board = %s AND validstatus = 1"""
        cursor.execute(sql_select_board,(employee_id))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        employee = result[0]
        resultJson = {}
        year_term = "WHERE employee_kpi.present_kpi = 'active'"
        sql = """SELECT employee_kpi.validstatus,employee_kpi.em_id_leader,employee_kpi.newKpiDescriptions_GM,employee_kpi.specialMoney_GM,employee_kpi.positionChange_GM,
                    employee_kpi.status_GM,employee_kpi.old_grade_GM,employee_kpi.createby,employee_kpi.comment_cancel,employee_kpi.year,employee_kpi.term,
                    employee_kpi.employeeid,employee_kpi.name,employee_kpi.companyid AS company_short_name,employee_kpi.surname,org_name.org_name_detail,position.position_detail,
                    employee_kpi.work_date,employee_kpi.work_month,employee_kpi.work_year,employee_kpi.old_grade,employee_kpi.grade,employee_kpi.comment_hr,
                    employee_kpi.present_kpi,employee_kpi.star_date_kpi,employee_kpi.status,employee_kpi.present_file  
                    FROM employee_kpi 
                    LEFT JOIN org_name ON employee_kpi.org_name = org_name.org_name_id
                    LEFT JOIN position ON employee_kpi.position = position.position_id
                        """+year_term
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        resultEmployeeList = []
        for employee in result:
            try:
                sql_board = """SELECT * FROM board_kpi WHERE employeeid = %s AND year = %s AND term = %s AND employeeid_board = %s AND status_onechat = 0 AND validstatus = 1"""
                cursor.execute(sql_board,(employee['employeeid'],employee['year'],employee['term'],employee_id))
                columns = [column[0] for column in cursor.description]
                result_board = toJson(cursor.fetchall(),columns)
                board = result_board[0]
                employee.update({'status_onechat':board['status_onechat']})
                
                sql_projects = """SELECT * FROM project_kpi WHERE employeeid = %s AND year = %s AND term = %s"""
                cursor.execute(sql_projects,(employee['employeeid'],employee['year'],employee['term']))
                columns = [column[0] for column in cursor.description]
                result_projects = toJson(cursor.fetchall(),columns)
                employee.update({'projectKpi':result_projects})
                resultEmployeeList.append(employee)
                # try:
                #     encoded_Image=str("http://intranet.inet.co.th/assets/upload/staff/"+str(employee['employeeid'])+".jpg")
                #     open_path_ = urllib.urlopen(encoded_Image)
                #     htmlSource = open_path_.read()
                #     open_path_.close()
                #     test= htmlSource.decode('utf-8')
                #     encoded_Image=str("http://intranet.inet.co.th/assets/upload/staff/"+str(employee['employeeid'])+"s.jpg")
                #     employee.update({'image':encoded_Image})
                # except Exception as e:
                #     encoded_Image=str("http://intranet.inet.co.th/assets/upload/staff/"+str(employee['employeeid'])+".jpg")
                #     employee.update({'image':encoded_Image})
            except Exception as e:
                pass 
        resultJson.update({'employeeLists':resultEmployeeList})
        return jsonify(resultJson)      
    except Exception as e:
        logserver(e)
        return "fail"