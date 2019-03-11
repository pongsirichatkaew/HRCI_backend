#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/QryEm_request', methods=['POST'])
@connect_sql()
def QryEm_request(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT employee.name_th,employee.employeeid,employee.surname_th,employee.citizenid,employee.salary,Personal.NicknameTh,Personal.Age,employee.start_work,employee.EndWork_probation,position.position_detail,org_name.org_name_detail,company.company_short_name FROM employee LEFT JOIN position ON position.position_id = employee.position_id\
                                      LEFT JOIN org_name ON org_name.org_name_id = employee.org_name_id\
                                      LEFT JOIN Personal ON Personal.ID_CardNo = employee.citizenid\
                                      LEFT JOIN company ON company.companyid = employee.company_id\
        WHERE employee.employeeid=%s"
        cursor.execute(sql,(data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        for item in result:
            salary_thai = []
            try:
                decodesalary = base64.b64decode(item['salary'])
                item['salary'] = decodesalary
                salary = decodesalary
                salary= (str(salary)[::-1])
                thai_number = ("ศูนย์","หนึ่ง","สอง","สาม","สี่","ห้า","หก","เจ็ด","แปด","เก้า")
                unit = ("","สิบ","ร้อย","พัน","หมื่น","แสน","ล้าน")
                length = len(salary) > 1
                resultSalary = ""
                for index, current in enumerate(map(int, salary)):
                    if current:
                        if index:
                           resultSalary = unit[index] + resultSalary
                        if length and current == 1 and index == 0:
                            resultSalary += 'เอ็ด'
                        elif index == 1 and current == 2:
                            resultSalary = 'ยี่' + resultSalary
                        elif index != 1 or current != 1:
                            resultSalary = thai_number[current] + resultSalary
                item['salary_thai'] = resultSalary
            except Exception as e:
                item['salary'] = ""
                item['salary_thai'] = ""
            long_date = []
            date1 = result[0]['start_work']
            star_date = date1.split("-")
            Day_s = int(star_date[0])
            Mon_s = int(star_date[1])
            year_s = int(star_date[2])
            if   Mon_s==1:
                 Mounth_name_str ="ม.ค."
            elif Mon_s==2:
                 Mounth_name_str="ก.พ."
            elif Mon_s==3:
                 Mounth_name_str="มี.ค."
            elif Mon_s==4:
                 Mounth_name_str="เม.ย."
            elif Mon_s==5:
                 Mounth_name_str="พ.ค."
            elif Mon_s==6:
                 Mounth_name_str="มิ.ย."
            elif Mon_s==7:
                 Mounth_name_str="ก.ค."
            elif Mon_s==8:
                 Mounth_name_str="ส.ค."
            elif Mon_s==9:
                 Mounth_name_str="ก.ย."
            elif Mon_s==10:
                 Mounth_name_str="ต.ค."
            elif Mon_s==11:
                 Mounth_name_str="พ.ย."
            else:
                 Mounth_name_str="ธ.ค."
            year_str = str(year_s+543)
            yer_last_str = year_str[-2:]
            item['start_work']= str(Day_s)+" "+Mounth_name_str+""+yer_last_str
            next_3_m2 = result[0]['EndWork_probation']
            end_date = next_3_m2.split("-")
            int_day_e =int(end_date[0])
            int_mon_e = int(end_date[1])
            int_year_e = int(end_date[2])
            if   int_mon_e==1:
                 Mounth_name_end ="ม.ค."
            elif int_mon_e==2:
                 Mounth_name_end="ก.พ."
            elif int_mon_e==3:
                 Mounth_name_end="มี.ค."
            elif int_mon_e==4:
                 Mounth_name_end="เม.ย."
            elif int_mon_e==5:
                 Mounth_name_end="พ.ค."
            elif int_mon_e==6:
                 Mounth_name_end="มิ.ย."
            elif int_mon_e==7:
                 Mounth_name_end="ก.ค."
            elif int_mon_e==8:
                 Mounth_name_end="ส.ค."
            elif int_mon_e==9:
                 Mounth_name_end="ก.ย."
            elif int_mon_e==10:
                 Mounth_name_end="ต.ค."
            elif int_mon_e==11:
                 Mounth_name_end="พ.ย."
            else:
                 Mounth_name_end="ธ.ค."
            year_end = str(int_year_e+543)
            yer_last_end = year_end[-2:]
            item['EndWork_probation']= str(int_day_e)+" "+Mounth_name_end+""+yer_last_end
            d0 = date(year_s,Mon_s,Day_s)
            d1 = date(int_year_e,int_mon_e,int_day_e)
            delta = d1 - d0
            str_date = str(delta)
            split_str = str_date.split(",")
            last = split_str[0].split(" ")
            item['long_date_pro'] = str(int(last[0])+1)

        sql9 = "SELECT Education.EducationLevel,Education.Institute,Education.StartYear,Education.EndYear,Education.Qualification,Education.Major,Education.GradeAvg,Education.ExtraCurricularActivities FROM Education INNER JOIN Personal ON Personal.ID_CardNo=Education.ID_CardNo \
        WHERE Personal.ID_CardNo=%s"
        cursor.execute(sql9,result[0]['citizenid'])
        columns9 = [column[0] for column in cursor.description]
        result_Education = toJson(cursor.fetchall(),columns9)

        sql10 = "SELECT Employment.CompanyName,Employment.CompanyAddress,Employment.PositionHeld,Employment.StartSalary,Employment.EndSalary,Employment.StartYear,Employment.EndYear,Employment.Responsibility,Employment.ReasonOfLeaving,Employment.Descriptionofwork FROM Employment INNER JOIN Personal ON Personal.ID_CardNo=Employment.ID_CardNo \
        WHERE Personal.ID_CardNo=%s"
        cursor.execute(sql10,result[0]['citizenid'])
        columns10 = [column[0] for column in cursor.description]
        result_Employment = toJson(cursor.fetchall(),columns10)

        sql_be = "SELECT benefits.benefits_detail,benefits.type_benefits,employee_benefits.benefits_id,employee_benefits.benefits_values,employee_benefits.type_check FROM employee_benefits LEFT JOIN benefits ON employee_benefits.benefits_id = benefits.benefits_id \
         WHERE employee_benefits.citizenid=%s"
        cursor.execute(sql_be,result[0]['citizenid'])
        columns = [column[0] for column in cursor.description]
        result_benefits = toJson(cursor.fetchall(),columns)

        sql_approver = "SELECT * FROM approve_request WHERE employeeid=%s"
        cursor.execute(sql_approver,(data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        result_approver = toJson(cursor.fetchall(),columns)

        result_all={}
        result_all["employee"] = result
        result_all["employee_Education"] = result_Education
        result_all["employee_Employment"] = result_Employment
        result_all["employee_Benefits"] = result_benefits
        result_all["employee_Approver"] = result_approver

        return jsonify(result_all)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryEmployee_request', methods=['POST'])
@connect_sql()
def QryEmployee_request(cursor):
    try:
        status_id = ""
        try:
            dataInput = request.json
            source = dataInput['source']
            data_new = source
            status_id = 'WHERE validstatus_request='+'"'+str(data_new['status_id'])+'"'
        except Exception as e:
            pass
        sql = "SELECT employee.name_th,employee.employeeid,employee.surname_th,employee.citizenid,employee.start_work,employee.validstatus_request,employee.EndWork_probation,company.company_short_name,position.position_detail,org_name.org_name_detail,status_request.status_detail,status_request.path_color,status_request.font_color FROM employee LEFT JOIN company ON company.companyid = employee.company_id\
                                      LEFT JOIN position ON position.position_id = employee.position_id\
                                      LEFT JOIN org_name ON org_name.org_name_id = employee.org_name_id\
                                      LEFT JOIN status_request ON status_request.status_id = employee.validstatus_request "+status_id+" "
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/AddApprove_request', methods=['POST'])
@connect_sql()
def AddApprove_request(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        try:
            sql_check_empro = "SELECT employeeid_request FROM approve_request WHERE employeeid=%s AND employeeid_reques=%s"
            cursor.execute(sql_check_empro,(data_new['employeeid'],data_new['employeeid_reques']))
            columns = [column[0] for column in cursor.description]
            result_check_empro = toJson(cursor.fetchall(),columns)
            type_check = result_check_empro[0]['employeeid_reques']
            return "employeeid_reques duplicate"
        except Exception as e:
            pass

        sqlApprove = "INSERT INTO approve_request(employeeid,employeeid_reques,name,lastname,tier_approve,position_detail,createby) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlApprove,(data_new['employeeid'],data_new['employeeid_reques'],data_new['name'],data_new['lastname'],data_new['tier_approve'],data_new['position_detail'],data_new['createby']))

        type_action = "ADD"

        sqlApprove = "INSERT INTO approve_request_log(employeeid,employeeid_reques,name,lastname,tier_approve,position_detail,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlApprove,(data_new['employeeid'],data_new['employeeid_reques'],data_new['name'],data_new['lastname'],data_new['tier_approve'],data_new['position_detail'],data_new['createby'],type_action))

        try:
            sql44 = "SELECT name_asp FROM assessor_quota WHERE companyid=%s AND tier_approve=%s AND employeeid=%s"
            cursor.execute(sql44,(data_new['companyid'],data_new['tier_approve'],data_new['employeeid_reques']))
            columns = [column[0] for column in cursor.description]
            result_test = toJson(cursor.fetchall(),columns)
            name_test = result_test[0]['name_asp']
        except Exception as e:

            sqlQry = "SELECT assessor_quota_id FROM assessor_quota ORDER BY assessor_quota_id DESC LIMIT 1"
            cursor.execute(sqlQry)
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            assessor_quota_id_last=result[0]['assessor_quota_id']+1

            sql = "INSERT INTO assessor_quota (assessor_quota_id,employeeid,companyid,name_asp,surname_asp,position_id,tier_approve,email_asp,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,(assessor_quota_id_last,data_new['employeeid_reques'],data_new['companyid'],data_new['name'],data_new['lastname'],data_new['position_id'],data_new['tier_approve'],data_new['email_asp'],data_new['createby']))

            type_action = "ADD"

            sql_log = "INSERT INTO assessor_quota_log (assessor_quota_id,employeeid,companyid,name_asp,surname_asp,position_id,tier_approve,email_asp,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql_log,(assessor_quota_id_last,data_new['employeeid_reques'],data_new['companyid'],data_new['name'],data_new['lastname'],data_new['position_id'],data_new['tier_approve'],data_new['email_asp'],data_new['createby'],type_action))

        return "Success"
    except Exception as e:
            logserver(e)
            return "fail"
@app.route('/Update_quotaid', methods=['POST'])
@connect_sql()
def Update_quotaid(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT * FROM employee WHERE employeeid=%s"
        cursor.execute(sql,(data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Edit"

        sqlEM = "INSERT INTO employee_log (employeeid,citizenid,name_th,name_eng,surname_th,surname_eng,nickname_employee,salary,email,phone_company,position_id,section_id,org_name_id,cost_center_name_id,company_id,type_em,start_work,EndWork_probation,quota_id,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlEM,(data_new['employeeid'],result[0]['citizenid'],result[0]['name_th'],result[0]['name_eng'],result[0]['surname_th'],result[0]['surname_eng'],result[0]['nickname_employee'],result[0]['salary'],result[0]['email'],result[0]['phone_company'],result[0]['position_id'],\
        result[0]['section_id'],result[0]['org_name_id'],result[0]['cost_center_name_id'],result[0]['company_id'],result[0]['type_em'],result[0]['start_work'],result[0]['EndWork_probation'],result[0]['quota_id'],data_new['createby'],type_action))

        sqlUp = "UPDATE employee SET quota_id=%s WHERE employeeid=%s"
        cursor.execute(sqlUp,(data_new['quota_id'],data_new['employeeid']))

        return "Success"
    except Exception as e:
            logserver(e)
            return "fail"
@app.route('/Addapprove_request_many', methods=['POST'])
@connect_sql()
def Addapprove_request_many(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sqlUp = "UPDATE employee SET quota_id=%s WHERE employeeid=%s"
        cursor.execute(sqlUp,(data_new['quota_id'],data_new['employeeid']))

        sqlUp_log = "UPDATE employee_log SET quota_id=%s WHERE employeeid=%s"
        cursor.execute(sqlUp_log,(data_new['quota_id'],data_new['employeeid']))

        i=0
        for i in xrange(len(data_new['em_request'])):
            sqlApprove = "INSERT INTO approve_request(employeeid,employeeid_reques,name,lastname,tier_approve,position_detail,createby) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlApprove,(data_new['employeeid'],data_new['em_request'][i]['employeeid_reques'],data_new['em_request'][i]['name'],data_new['em_request'][i]['lastname'],data_new['em_request'][i]['tier_approve'],data_new['em_request'][i]['position_detail'],data_new['createby']))

            type_action = "ADD"

            sqlApprove = "INSERT INTO approve_request_log(employeeid,employeeid_reques,name,lastname,tier_approve,position_detail,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlApprove,(data_new['employeeid'],data_new['em_request'][i]['employeeid_reques'],data_new['em_request'][i]['name'],data_new['em_request'][i]['lastname'],data_new['em_request'][i]['tier_approve'],data_new['em_request'][i]['position_detail'],data_new['createby'],type_action))

            try:
                sql44 = "SELECT name_asp FROM assessor_quota WHERE companyid=%s AND tier_approve=%s AND employeeid=%s"
                cursor.execute(sql44,(data_new['em_request'][i]['companyid'],data_new['em_request'][i]['tier_approve'],data_new['em_request'][i]['employeeid_reques']))
                columns = [column[0] for column in cursor.description]
                result_test = toJson(cursor.fetchall(),columns)
                name_test = result_test[0]['name_asp']
            except Exception as e:

                sqlQry = "SELECT assessor_quota_id FROM assessor_quota ORDER BY assessor_quota_id DESC LIMIT 1"
                cursor.execute(sqlQry)
                columns = [column[0] for column in cursor.description]
                result = toJson(cursor.fetchall(),columns)
                assessor_quota_id_last=result[0]['assessor_quota_id']+1

                sql = "INSERT INTO assessor_quota (assessor_quota_id,employeeid,companyid,name_asp,surname_asp,position_id,tier_approve,email_asp,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql,(assessor_quota_id_last,data_new['em_request'][i]['employeeid_reques'],data_new['em_request'][i]['companyid'],data_new['em_request'][i]['name'],data_new['em_request'][i]['lastname'],data_new['em_request'][i]['position_id'],data_new['em_request'][i]['tier_approve'],data_new['em_request'][i]['Email_Employee'],data_new['createby']))

                type_action = "ADD"

                sql_log = "INSERT INTO assessor_quota_log (assessor_quota_id,employeeid,companyid,name_asp,surname_asp,position_id,tier_approve,email_asp,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql_log,(assessor_quota_id_last,data_new['em_request'][i]['employeeid_reques'],data_new['em_request'][i]['companyid'],data_new['em_request'][i]['name'],data_new['em_request'][i]['lastname'],data_new['em_request'][i]['position_id'],data_new['em_request'][i]['tier_approve'],data_new['em_request'][i]['Email_Employee'],data_new['createby'],type_action))

        return "Success"
    except Exception as e:
            logserver(e)
            return "fail"
@app.route('/Deleteapprove_request', methods=['POST'])
@connect_sql()
def Deleteapprove_request(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT * FROM approve_request WHERE employeeid=%s AND employeeid_reques=%s"
        cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_reques']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Delete"

        sqlApprove = "INSERT INTO approve_request_log(employeeid,employeeid_reques,name,lastname,tier_approve,position_detail,status_,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlApprove,(data_new['employeeid'],data_new['employeeid_reques'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],result[0]['status_'],data_new['createby'],type_action))

        sqlDe = "DELETE FROM approve_request WHERE employeeid=%s AND employeeid_reques=%s"
        cursor.execute(sqlDe,(data_new['employeeid'],data_new['employeeid_reques']))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryApprove_request', methods=['POST'])
@connect_sql()
def QryApprove_request(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT * FROM approve_request WHERE employeeid=%s"
        cursor.execute(sql,(data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sql2 = "SELECT quota_id FROM employee WHERE employeeid=%s"
        cursor.execute(sql2,(data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        result2 = toJson(cursor.fetchall(),columns)

        sql3 = "SELECT quota.quota_id,quota.year,company.companyid,company.company_short_name,position.position_detail,quota.position_id,quota.member FROM quota LEFT JOIN company ON company.companyid = quota.companyid\
                                                                                                                                   LEFT JOIN position ON position.position_id = quota.position_id WHERE quota.quota_id = %s"
        cursor.execute(sql3,(result2[0]['quota_id']))
        columns = [column[0] for column in cursor.description]
        result3 = toJson(cursor.fetchall(),columns)

        result_all={}
        result_all["employee"] = result
        result_all["quota"] = result3
        return jsonify(result_all)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryApprove_request_Info', methods=['POST'])
@connect_sql()
def QryApprove_request_Info(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT * FROM approve_request WHERE employeeid=%s AND employeeid_reques=%s"
        cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_reques']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Send_request', methods=['POST'])
@connect_sql()
def Send_request(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sqlcheck_L1 = "SELECT employeeid_reques FROM approve_request WHERE employeeid=%s AND tier_approve='L1'"
        cursor.execute(sqlcheck_L1,(data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        result_check_L1 = toJson(cursor.fetchall(),columns)

        sqlcheck_L2 = "SELECT employeeid_reques FROM approve_request WHERE employeeid=%s AND tier_approve='L2'"
        cursor.execute(sqlcheck_L2,(data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        result_check_L2 = toJson(cursor.fetchall(),columns)

        sqlcheck_L3 = "SELECT employeeid_reques FROM approve_request WHERE employeeid=%s AND tier_approve='L3'"
        cursor.execute(sqlcheck_L3,(data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        result_check_L3 = toJson(cursor.fetchall(),columns)

        try:
            check_L3 = result_check_L3[0]['employeeid_reques']
        except Exception as e:
            return "No Level L3"

        sqlcheck_L4 = "SELECT employeeid_reques FROM approve_request WHERE employeeid=%s AND tier_approve='L4'"
        cursor.execute(sqlcheck_L4,(data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        result_check_L4 = toJson(cursor.fetchall(),columns)

        if (not result_check_L2)&(not result_check_L1):
            sql = "SELECT * FROM approve_request WHERE employeeid=%s AND employeeid_reques=%s"
            cursor.execute(sql,(data_new['employeeid'],result_check_L3[0]['employeeid_reques']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "send_pro_no_L2"
            status_last = "4"

            sqlReject = "INSERT INTO approve_request_log(employeeid,employeeid_reques,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(result[0]['employeeid'],result[0]['employeeid_reques'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,result[0]['comment'],result[0]['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

            sqlUp = "UPDATE approve_request SET status_=4,date_status=%s WHERE employeeid=%s AND employeeid_reques=%s"
            cursor.execute(sqlUp,(data_new['date_status'],data_new['employeeid'],result_check_L3[0]['employeeid_reques']))

            sqlUp_main = "UPDATE employee SET validstatus_request=4 WHERE employeeid=%s"
            cursor.execute(sqlUp_main,(data_new['employeeid']))

        elif (not result_check_L2)&(not result_check_L3)&(not result_check_L1):
            sql = "SELECT * FROM approve_request WHERE employeeid=%s AND employeeid_reques=%s"
            cursor.execute(sql,(data_new['employeeid'],result_check_L2[0]['employeeid_reques']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "send_pro_no_L2_L3_L1"
            status_last = "5"

            sqlReject = "INSERT INTO approve_request_log(employeeid,employeeid_reques,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(result[0]['employeeid'],result[0]['employeeid_reques'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,result[0]['comment'],result[0]['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

            sqlUp = "UPDATE approve_request SET status_=5,date_status=%s WHERE employeeid=%s AND employeeid_reques=%s"
            cursor.execute(sqlUp,(data_new['date_status'],data_new['employeeid'],result_check_L2[0]['employeeid_reques']))

            sqlUp_main = "UPDATE employee SET validstatus_request=5 WHERE employeeid=%s"
            cursor.execute(sqlUp_main,(data_new['employeeid']))
        elif not result_check_L1:
            sql = "SELECT * FROM approve_request WHERE employeeid=%s AND employeeid_reques=%s"
            cursor.execute(sql,(data_new['employeeid'],result_check_L2[0]['employeeid_reques']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "send_pro_no_L1"
            status_last = "3"

            sqlReject = "INSERT INTO approve_request_log(employeeid,employeeid_reques,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(result[0]['employeeid'],result[0]['employeeid_reques'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,result[0]['comment'],result[0]['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

            sqlUp = "UPDATE approve_request SET status_=3,date_status=%s WHERE employeeid=%s AND employeeid_reques=%s"
            cursor.execute(sqlUp,(data_new['date_status'],data_new['employeeid'],result_check_L2[0]['employeeid_reques']))

            sqlUp_main = "UPDATE employee SET validstatus_request=3 WHERE employeeid=%s"
            cursor.execute(sqlUp_main,(data_new['employeeid']))
        else:
            sql = "SELECT * FROM approve_request WHERE employeeid=%s AND employeeid_reques=%s"
            cursor.execute(sql,(data_new['employeeid'],result_check_L1[0]['employeeid_reques']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "send_pro"
            status_last = "2"

            sqlReject = "INSERT INTO approve_request_log(employeeid,employeeid_reques,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(result[0]['employeeid'],result[0]['employeeid_reques'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,result[0]['comment'],result[0]['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

            sqlUp = "UPDATE approve_request SET status_=2,date_status=%s WHERE employeeid=%s AND employeeid_reques=%s"
            cursor.execute(sqlUp,(data_new['employeeid'],data_new['date_status'],result_check_L1[0]['employeeid_reques']))

            sqlUp_main = "UPDATE employee SET validstatus_request=2 WHERE employeeid=%s"
            cursor.execute(sqlUp_main,(data_new['employeeid']))
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryStatus_request', methods=['POST'])
@connect_sql()
def QryStatus_request(cursor):
    try:
        sql = "SELECT id,status_id,status_detail,path_color,id,font_color FROM status_request"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/UpdateStatus_request', methods=['POST'])
@connect_sql()
def UpdateStatus_request(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        tier_approve = str(data_new['tier_approve'])
        status_ = str(data_new['status_'])

        sql_picture = "SELECT mail_type,imageName FROM mail_pic WHERE mail_type='probation_mail'"
        cursor.execute(sql_picture)
        columns = [column[0] for column in cursor.description]
        result_picture = toJson(cursor.fetchall(),columns)

        sql_check_end = "SELECT validstatus_request FROM employee WHERE employeeid=%s"
        cursor.execute(sql_check_end,(data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        result_check_end = toJson(cursor.fetchall(),columns)
        check_endpro = int(result_check_end[0]['validstatus_request'])
        if check_endpro==9:
            return "End Probation"
        if (tier_approve=='L4')&(status_=='Reject'):

            sqlUp = "UPDATE approve_request SET status_=8,id_comment=%s,comment=%s,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_reques=%s"
            cursor.execute(sqlUp,(data_new['id_comment'],data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_reques']))

            sqlUp_main = "UPDATE employee SET validstatus_request=8 WHERE employeeid=%s"
            cursor.execute(sqlUp_main,(data_new['employeeid']))

            try:
                sqlUp_L3 = "UPDATE approve_request SET status_=8 WHERE employeeid=%s AND tier_approve='L3'"
                cursor.execute(sqlUp_L3,(data_new['employeeid']))

                # sql_reject_l3 = "SELECT employee.name_eng,employee.surname_eng,employee.email FROM approve_request  LEFT JOIN employee ON approve_request.employeeid_reques = employee.employeeid\
                #                  WHERE approve_request.employeeid=%s AND approve_request.tier_approve='L3'"
                # cursor.execute(sql_reject_l3,(data_new['employeeid']))
                # columns = [column[0] for column in cursor.description]
                # result_reject_l3 = toJson(cursor.fetchall(),columns)
                #
                # sql_reject_employee = "SELECT employee.name_th,employee.surname_th,position.position_detail,org_name.org_name_detail FROM employee LEFT JOIN position ON position.position_id = employee.position_id\
                #                                                                                                                                    LEFT JOIN org_name ON org_name.org_name_id = employee.org_name_id\
                #                        WHERE employee.employeeid=%s"
                # cursor.execute(sql_reject_employee,(data_new['employeeid']))
                # columns = [column[0] for column in cursor.description]
                # result_reject_employee = toJson(cursor.fetchall(),columns)
                # em_name = result_reject_employee[0]['name_th']
                # em_surname = result_reject_employee[0]['surname_th']
                # em_position = result_reject_employee[0]['position_detail']
                # em_org = result_reject_employee[0]['org_name_detail']
                #
                # for item in result_reject_l3:
                #     sendToMail_reject_request(item['email'],item['name_eng'],item['surname_eng'],em_name,em_surname,em_position,em_org,result_picture[0]['imageName'])

            except Exception as e:
                pass

            try:
                sqlUp_L2 = "UPDATE approve_request SET status_=8 WHERE employeeid=%s AND tier_approve='L2'"
                cursor.execute(sqlUp_L2,(data_new['employeeid']))

                # sql_reject_l3 = "SELECT employee.name_eng,employee.surname_eng,employee.email FROM approve_request  LEFT JOIN employee ON approve_request.employeeid_reques = employee.employeeid\
                #                  WHERE approve_request.employeeid=%s AND approve_request.tier_approve='L2'"
                # cursor.execute(sql_reject_l3,(data_new['employeeid']))
                # columns = [column[0] for column in cursor.description]
                # result_reject_l3 = toJson(cursor.fetchall(),columns)
                #
                # sql_reject_employee = "SELECT employee.name_th,employee.surname_th,position.position_detail,org_name.org_name_detail FROM employee LEFT JOIN position ON position.position_id = employee.position_id\
                #                                                                                                                                    LEFT JOIN org_name ON org_name.org_name_id = employee.org_name_id\
                #                        WHERE employee.employeeid=%s"
                # cursor.execute(sql_reject_employee,(data_new['employeeid']))
                # columns = [column[0] for column in cursor.description]
                # result_reject_employee = toJson(cursor.fetchall(),columns)
                # em_name = result_reject_employee[0]['name_th']
                # em_surname = result_reject_employee[0]['surname_th']
                # em_position = result_reject_employee[0]['position_detail']
                # em_org = result_reject_employee[0]['org_name_detail']
                #
                # for item in result_reject_l3:
                #     sendToMail_reject_request(item['email'],item['name_eng'],item['surname_eng'],em_name,em_surname,em_position,em_org,result_picture[0]['imageName'])

            except Exception as e:
                pass

            sql = "SELECT * FROM approve_request WHERE employeeid=%s AND employeeid_reques=%s"
            cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_reques']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "reject_director"
            status_last = "8"

            sqlReject = "INSERT INTO approve_request_log(employeeid,employeeid_reques,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(result[0]['employeeid'],result[0]['employeeid_reques'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

        elif (tier_approve =='L3')&(status_ =='Reject'):

            sqlUp = "UPDATE approve_request SET status_=7,comment=%s,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_reques=%s"
            cursor.execute(sqlUp,(data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_reques']))

            sqlUp_main = "UPDATE employee SET validstatus_request=7 WHERE employeeid=%s"
            cursor.execute(sqlUp_main,(data_new['employeeid']))

            try:
                sqlUp_L2 = "UPDATE approve_request SET status_=7,comment=NULL,comment_orther=NULL,date_status=NULL WHERE employeeid=%s AND tier_approve='L2'"
                cursor.execute(sqlUp_L2,(data_new['employeeid']))

                # sql_reject_l3 = "SELECT employee.name_eng,employee.surname_eng,employee.email FROM approve_request  LEFT JOIN employee ON approve_request.employeeid_reques = employee.employeeid\
                #                  WHERE approve_request.employeeid=%s AND approve_request.tier_approve='L2'"
                # cursor.execute(sql_reject_l3,(data_new['employeeid']))
                # columns = [column[0] for column in cursor.description]
                # result_reject_l3 = toJson(cursor.fetchall(),columns)
                #
                # sql_reject_employee = "SELECT employee.name_th,employee.surname_th,position.position_detail,org_name.org_name_detail FROM employee LEFT JOIN position ON position.position_id = employee.position_id\
                #                                                                                                                                    LEFT JOIN org_name ON org_name.org_name_id = employee.org_name_id\
                #                        WHERE employee.employeeid=%s"
                # cursor.execute(sql_reject_employee,(data_new['employeeid']))
                # columns = [column[0] for column in cursor.description]
                # result_reject_employee = toJson(cursor.fetchall(),columns)
                # em_name = result_reject_employee[0]['name_th']
                # em_surname = result_reject_employee[0]['surname_th']
                # em_position = result_reject_employee[0]['position_detail']
                # em_org = result_reject_employee[0]['org_name_detail']
                #
                # for item in result_reject_l3:
                #     sendToMail_reject_request(item['email'],item['name_eng'],item['surname_eng'],em_name,em_surname,em_position,em_org,result_picture[0]['imageName'])

            except Exception as e:
                pass

            sql = "SELECT * FROM approve_request WHERE employeeid=%s AND employeeid_reques=%s"
            cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_reques']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "reject_deputy_director"
            status_last = "7"

            sqlReject = "INSERT INTO approve_request_log(employeeid,employeeid_reques,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(result[0]['employeeid'],result[0]['employeeid_reques'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

        elif (tier_approve =='L2')&(status_ =='Reject'):

            sqlUp = "UPDATE approve_request SET status_=6,comment=%s,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_reques=%s"
            cursor.execute(sqlUp,(data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_reques']))

            sqlUp_main = "UPDATE employee SET validstatus_request=6 WHERE employeeid=%s"
            cursor.execute(sqlUp_main,(data_new['employeeid']))

            try:
                sqlUp_L1 = "UPDATE approve_request SET status_=6,comment=NULL,comment_orther=NULL,date_status=NULL WHERE employeeid=%s AND tier_approve='L1'"
                cursor.execute(sqlUp_L1,(data_new['employeeid']))

                # sql_reject_l3 = "SELECT employee.name_eng,employee.surname_eng,employee.email FROM approve_request  LEFT JOIN employee ON approve_request.employeeid_reques = employee.employeeid\
                #                  WHERE approve_request.employeeid=%s AND approve_request.tier_approve='L1'"
                # cursor.execute(sql_reject_l3,(data_new['employeeid']))
                # columns = [column[0] for column in cursor.description]
                # result_reject_l3 = toJson(cursor.fetchall(),columns)
                #
                # sql_reject_employee = "SELECT employee.name_th,employee.surname_th,position.position_detail,org_name.org_name_detail FROM employee LEFT JOIN position ON position.position_id = employee.position_id\
                #                                                                                                                                    LEFT JOIN org_name ON org_name.org_name_id = employee.org_name_id\
                #                        WHERE employee.employeeid=%s"
                # cursor.execute(sql_reject_employee,(data_new['employeeid']))
                # columns = [column[0] for column in cursor.description]
                # result_reject_employee = toJson(cursor.fetchall(),columns)
                # em_name = result_reject_employee[0]['name_th']
                # em_surname = result_reject_employee[0]['surname_th']
                # em_position = result_reject_employee[0]['position_detail']
                # em_org = result_reject_employee[0]['org_name_detail']
                #
                # for item in result_reject_l3:
                #     sendToMail_reject_request(item['email'],item['name_eng'],item['surname_eng'],em_name,em_surname,em_position,em_org,result_picture[0]['imageName'])

            except Exception as e:
                pass

            sql = "SELECT * FROM approve_request WHERE employeeid=%s AND employeeid_reques=%s"
            cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_reques']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "reject_hr"
            status_last = "6"

            sqlReject = "INSERT INTO approve_request_log(employeeid,employeeid_reques,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(result[0]['employeeid'],result[0]['employeeid_reques'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))


        elif (tier_approve =='L4')&(status_ =='Approve'):

            sqlUp = "UPDATE approve_request SET status_=14,id_comment=%s,comment=%s,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_reques=%s"
            cursor.execute(sqlUp,(data_new['id_comment'],data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_reques']))

            sqlUp_main = "UPDATE employee SET validstatus_request=15 WHERE employeeid=%s"
            cursor.execute(sqlUp_main,(data_new['employeeid']))

            sql = "SELECT * FROM approve_request WHERE employeeid=%s AND employeeid_reques=%s"
            cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_reques']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "send_director"
            status_last = "9"

            sqlReject = "INSERT INTO approve_request_log(employeeid,employeeid_reques,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(result[0]['employeeid'],result[0]['employeeid_reques'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

        elif (tier_approve =='L3')&(status_=='Approve'):

            # sqlcheck_L4 = "SELECT employeeid_reques FROM approve_request WHERE employeeid=%s AND employeeid=%s AND tier_approve='L4'"
            sqlcheck_L4 = "SELECT employeeid_reques FROM approve_request WHERE employeeid=%s AND tier_approve='L4'"
            cursor.execute(sqlcheck_L4,(data_new['employeeid']))
            columns = [column[0] for column in cursor.description]
            result_check_L4 = toJson(cursor.fetchall(),columns)

            if not result_check_L4:

                sqlUp = "UPDATE approve_request SET status_=14,comment=%s,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_reques=%s"
                cursor.execute(sqlUp,(data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_reques']))

                sqlUp_main = "UPDATE employee SET validstatus_request=15 WHERE employeeid=%s"
                cursor.execute(sqlUp_main,(data_new['employeeid']))

                sql = "SELECT * FROM approve_request WHERE employeeid=%s AND employeeid_reques=%s"
                cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_reques']))
                columns = [column[0] for column in cursor.description]
                result = toJson(cursor.fetchall(),columns)

                type_action = "send_deputy_director"
                status_last = "9"

                sqlReject = "INSERT INTO approve_request_log(employeeid,employeeid_reques,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlReject,(result[0]['employeeid'],result[0]['employeeid_reques'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

            else:

                sqlUp = "UPDATE approve_request SET status_=14,comment=%s,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_reques=%s"
                cursor.execute(sqlUp,(data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_reques']))

                sqlUp_main = "UPDATE employee SET validstatus_request=5 WHERE employeeid=%s"
                cursor.execute(sqlUp_main,(data_new['employeeid']))

                sql = "SELECT * FROM approve_request WHERE employeeid=%s AND employeeid_reques=%s"
                cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_reques']))
                columns = [column[0] for column in cursor.description]
                result = toJson(cursor.fetchall(),columns)

                type_action = "send_deputy_director"
                status_last = "5"

                sqlReject = "INSERT INTO approve_request_log(employeeid,employeeid_reques,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlReject,(result[0]['employeeid'],result[0]['employeeid_reques'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

        elif (tier_approve =='L2')&(status_ =='Approve'):

            # sqlcheck_L3 = "SELECT employeeid_reques FROM approve_request WHERE employeeid=%s AND employeeid=%s AND tier_approve='L3'"
            sqlcheck_L3 = "SELECT employeeid_reques FROM approve_request WHERE employeeid=%s AND tier_approve='L3'"
            cursor.execute(sqlcheck_L3,(data_new['employeeid']))
            columns = [column[0] for column in cursor.description]
            result_check_L3 = toJson(cursor.fetchall(),columns)

            if not result_check_L3:

                sqlUp = "UPDATE approve_request SET status_=14,comment=%s,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_reques=%s"
                cursor.execute(sqlUp,(data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_reques']))

                sqlUp_main = "UPDATE employee SET validstatus_request=5 WHERE employeeid=%s"
                cursor.execute(sqlUp_main,(data_new['employeeid']))

                sql = "SELECT * FROM approve_request WHERE employeeid=%s AND employeeid_reques=%s"
                cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_reques']))
                columns = [column[0] for column in cursor.description]
                result = toJson(cursor.fetchall(),columns)

                type_action = "send_hr_no_L3"
                status_last = "5"

                sqlReject = "INSERT INTO approve_request_log(employeeid,employeeid_reques,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlReject,(result[0]['employeeid'],result[0]['employeeid_reques'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))
            else:

                sqlUp = "UPDATE approve_request SET status_=14,comment=%s,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_reques=%s"
                cursor.execute(sqlUp,(data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_reques']))

                sqlUp_main = "UPDATE employee SET validstatus_request=4 WHERE employeeid=%s"
                cursor.execute(sqlUp_main,(data_new['employeeid']))

                sql = "SELECT * FROM approve_request WHERE employeeid=%s AND employeeid_reques=%s"
                cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_reques']))
                columns = [column[0] for column in cursor.description]
                result = toJson(cursor.fetchall(),columns)

                type_action = "send_hr"
                status_last = "4"

                sqlReject = "INSERT INTO approve_request_log(employeeid,employeeid_reques,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlReject,(result[0]['employeeid'],result[0]['employeeid_reques'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))
        else:
            sqlcheck_L1 = "SELECT COUNT(employeeid_reques) AS total_l1 FROM approve_request WHERE employeeid=%s AND tier_approve='L1'"
            cursor.execute(sqlcheck_L1,(data_new['employeeid']))
            columns = [column[0] for column in cursor.description]
            result_check_L1 = toJson(cursor.fetchall(),columns)
            check_total_l1 = int(result_check_L1[0]['total_l1'])

            sqlcheck_L2 = "SELECT employeeid_reques FROM approve_request WHERE employeeid=%s AND tier_approve='L2'"
            # sqlcheck_L2 = "SELECT employeeid_reques FROM approve_request WHERE employeeid=%s AND employeeid=%s AND tier_approve='L2'"
            cursor.execute(sqlcheck_L2,(data_new['employeeid']))
            columns = [column[0] for column in cursor.description]
            result_check_L2 = toJson(cursor.fetchall(),columns)

            # sqlcheck_L3 = "SELECT employeeid_reques FROM approve_request WHERE employeeid=%s AND employeeid=%s AND tier_approve='L3'"
            sqlcheck_L3 = "SELECT employeeid_reques FROM approve_request WHERE employeeid=%s AND tier_approve='L3'"
            cursor.execute(sqlcheck_L3,(data_new['employeeid']))
            columns = [column[0] for column in cursor.description]
            result_check_L3 = toJson(cursor.fetchall(),columns)

            if not result_check_L2:

                sqlUp = "UPDATE approve_request SET status_=14,comment=%s,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_reques=%s"
                cursor.execute(sqlUp,(data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_reques']))

                if check_total_l1==1 :
                    sqlUp_main = "UPDATE employee SET validstatus_request=4 WHERE employeeid=%s"
                    cursor.execute(sqlUp_main,(data_new['employeeid']))
                else:
                    pass
                sql = "SELECT * FROM approve_request WHERE employeeid=%s AND employeeid_reques=%s"
                cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_reques']))
                columns = [column[0] for column in cursor.description]
                result = toJson(cursor.fetchall(),columns)

                type_action = "send_head_no_L2"
                status_last = "4"

                sqlReject = "INSERT INTO approve_request_log(employeeid,employeeid_reques,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlReject,(result[0]['employeeid'],result[0]['employeeid_reques'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

            elif (not result_check_L2)&(not result_check_L3):

                sqlUp = "UPDATE approve_request SET status_=14,comment=%s,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_reques=%s"
                cursor.execute(sqlUp,(data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_reques']))

                if check_total_l1==1 :
                    sqlUp_main = "UPDATE employee SET validstatus_request=5 WHERE employeeid=%s"
                    cursor.execute(sqlUp_main,(data_new['employeeid']))
                else:
                    pass

                sql = "SELECT * FROM approve_request WHERE employeeid=%s AND employeeid_reques=%s"
                cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_reques']))
                columns = [column[0] for column in cursor.description]
                result = toJson(cursor.fetchall(),columns)

                type_action = "send_head_no_L2_L3"
                status_last = "5"

                sqlReject = "INSERT INTO approve_request_log(employeeid,employeeid_reques,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlReject,(result[0]['employeeid'],result[0]['employeeid_reques'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))
            else:
                sqlUp = "UPDATE approve_request SET status_=14,comment=%s,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_reques=%s"
                cursor.execute(sqlUp,(data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_reques']))

                if check_total_l1==1 :
                    sqlUp_main = "UPDATE employee SET validstatus_request=3 WHERE employeeid=%s"
                    cursor.execute(sqlUp_main,(data_new['employeeid']))
                else:
                    pass

                sql = "SELECT * FROM approve_request WHERE employeeid=%s AND employeeid_reques=%s"
                cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_reques']))
                columns = [column[0] for column in cursor.description]
                result = toJson(cursor.fetchall(),columns)

                type_action = "send_head"
                status_last = "3"

                sqlReject = "INSERT INTO approve_request_log(employeeid,employeeid_reques,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlReject,(result[0]['employeeid'],result[0]['employeeid_reques'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryEmp_request_leader', methods=['POST'])
def QryEmp_request_leader():
    try:
        status_id = ""
        try:
            dataInput = request.json
            source = dataInput['source']
            data_new = source
            status_id = 'AND validstatus_request='+'"'+str(data_new['status_id'])+'"'
        except Exception as e:
            pass
        connection = mysql.connect()
        cursor = connection.cursor()
        sql = "SELECT employee.name_th,employee.employeeid,employee.surname_th,employee.citizenid,employee.start_work,employee.EndWork_probation,company.company_short_name,position.position_detail,section.sect_detail,org_name.org_name_detail,cost_center_name.cost_detail,status.status_detail,status.path_color,status.font_color,approve_request.tier_approve FROM employee LEFT JOIN company ON company.companyid = employee.company_id\
                                      LEFT JOIN position ON position.position_id = employee.position_id\
                                      LEFT JOIN section ON section.sect_id = employee.section_id\
                                      LEFT JOIN org_name ON org_name.org_name_id = employee.org_name_id\
                                      LEFT JOIN cost_center_name ON cost_center_name.cost_center_name_id = employee.cost_center_name_id\
                                      LEFT JOIN approve_request ON approve_request.employeeid = employee.employeeid\
                                      LEFT JOIN status ON status.status_id = employee.validstatus_request WHERE employeeid_reques=%s AND NOT employee.validstatus_request=1 "+status_id+" "
        cursor.execute(sql,data_new['employeeid_reques'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        connection.close()
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Abstract_hr_request', methods=['POST'])
@connect_sql()
def Abstract_hr_request(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        abstract = data_new['abstract']

        if (abstract=='Pass'):

            sqlUp_main = "UPDATE employee SET validstatus_request=9 WHERE employeeid=%s"
            cursor.execute(sqlUp_main,(data_new['employeeid']))

            sql = "SELECT * FROM approve_request WHERE employeeid=%s"
            cursor.execute(sql,(data_new['employeeid']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "abstract_pass"
            status_last = "9"

            sqlReject = "INSERT INTO approve_request_log(employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(result[0]['employeeid'],data_new['createby'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

        elif (abstract=='Not_pass'):

            sqlUp_main = "UPDATE employee SET validstatus_request=11 WHERE employeeid=%s"
            cursor.execute(sqlUp_main,(data_new['employeeid']))

            sql = "SELECT * FROM approve_request WHERE employeeid=%s"
            cursor.execute(sql,(data_new['employeeid']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "abstract_not_pass"
            status_last = "11"

            sqlReject = "INSERT INTO approve_request_log(employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(result[0]['employeeid'],data_new['createby'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))
        else:
            return "fail"
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/sendEmail_request', methods = ['GET'])
@connect_sql()
def sendEmail_request(cursor):
    sql_picture = "SELECT mail_type,imageName FROM mail_pic WHERE mail_type='request_mail'"
    cursor.execute(sql_picture)
    columns = [column[0] for column in cursor.description]
    result_picture = toJson(cursor.fetchall(),columns)

    sql_L1 = "SELECT employeeid,email_asp,tier_approve FROM assessor_quota WHERE tier_approve='L1' GROUP BY email_asp "
    cursor.execute(sql_L1)
    columns = [column[0] for column in cursor.description]
    result = toJson(cursor.fetchall(),columns)
    for i1 in result:
        total_em = []
        sql1_total = "SELECT COUNT(approve_request.employeeid) AS total_em FROM approve_request LEFT JOIN assessor_quota ON approve_request.employeeid_pro = assessor_quota.employeeid\
                                                                                                    LEFT JOIN employee ON approve_request.employeeid = employee.employeeid\
                       WHERE approve_request.employeeid_pro = %s AND employee.validstatus_request IN(2,6)"
        cursor.execute(sql1_total,(i1['employeeid']))
        columns = [column[0] for column in cursor.description]
        data1 = toJson(cursor.fetchall(),columns)
        i1['total_em'] = str(data1[0]['total_em'])
    for item in result:
        count = int(item['total_em'])
        if count>0:
            sendToMail_request(item['email_asp'], item['total_em'],result_picture[0]['imageName'])
    sql_L2 = "SELECT employeeid,email_asp,tier_approve FROM assessor_quota WHERE tier_approve='L2' GROUP BY email_asp "
    cursor.execute(sql_L2)
    columns = [column[0] for column in cursor.description]
    result2 = toJson(cursor.fetchall(),columns)
    for i2 in result2:
        total_em2 = []
        sql1_total2 = "SELECT COUNT(approve_request.employeeid) AS total_em FROM approve_request LEFT JOIN assessor_quota ON approve_request.employeeid_pro = assessor_quota.employeeid\
                                                                                                    LEFT JOIN employee ON approve_request.employeeid = employee.employeeid\
                       WHERE approve_request.employeeid_pro = %s AND employee.validstatus_request IN(3,7,8)"
        cursor.execute(sql1_total2,(i2['employeeid']))
        columns = [column[0] for column in cursor.description]
        data2 = toJson(cursor.fetchall(),columns)
        i2['total_em'] = str(data2[0]['total_em'])
    for item2 in result2:
        count2 = int(item2['total_em'])
        if count2>0:
            sendToMail_request(item2['email_asp'], item2['total_em'],result_picture[0]['imageName'])
    sql_L3 = "SELECT employeeid,email_asp,tier_approve FROM assessor_quota WHERE tier_approve='L3' GROUP BY email_asp "
    cursor.execute(sql_L3)
    columns = [column[0] for column in cursor.description]
    result3 = toJson(cursor.fetchall(),columns)
    for i3 in result3:
        total_em3 = []
        sql1_total3 = "SELECT COUNT(approve_request.employeeid) AS total_em FROM approve_request LEFT JOIN assessor_quota ON approve_request.employeeid_pro = assessor_quota.employeeid\
                                                                                                    LEFT JOIN employee ON approve_request.employeeid = employee.employeeid\
                       WHERE approve_request.employeeid_pro = %s AND employee.validstatus_request IN(4,8)"
        cursor.execute(sql1_total3,(i3['employeeid']))
        columns = [column[0] for column in cursor.description]
        data3 = toJson(cursor.fetchall(),columns)
        i3['total_em'] = str(data3[0]['total_em'])
    for item3 in result3:
        count3 = int(item3['total_em'])
        if count3>0:
            sendToMail_request(item3['email_asp'], item3['total_em'],result_picture[0]['imageName'])
    sql_L4 = "SELECT employeeid,email_asp,tier_approve FROM assessor_quota WHERE tier_approve='L4' GROUP BY email_asp "
    cursor.execute(sql_L4)
    columns = [column[0] for column in cursor.description]
    result4 = toJson(cursor.fetchall(),columns)
    for i4 in result4:
        total_em4 = []
        sql1_total4 = "SELECT COUNT(approve_request.employeeid) AS total_em FROM approve_request LEFT JOIN assessor_quota ON approve_request.employeeid_pro = assessor_quota.employeeid\
                                                                                                    LEFT JOIN employee ON approve_request.employeeid = employee.employeeid\
                       WHERE approve_request.employeeid_pro = %s AND employee.validstatus_request IN(5)"
        cursor.execute(sql1_total4,(i4['employeeid']))
        columns = [column[0] for column in cursor.description]
        data4 = toJson(cursor.fetchall(),columns)
        i4['total_em'] = str(data4[0]['total_em'])
    for item4 in result4:
        count4 = int(item4['total_em'])
        if count4>0:
            sendToMail_request(item4['email_asp'], item4['total_em'],result_picture[0]['imageName'])
    return jsonify(result)
def sendToMail_request(email, total_em,imageName):
    send_from = "Hr Management <recruitment@inet.co.th>"
    send_to = email
    subject = "อนุมัติพนักงานเข้าทำงาน"
    text = """\
                <html>
                  <body>
                  <img src="http://hr.devops.inet.co.th:8888/userGetFileImageMail/"""+imageName+"""""></br>
                    <b>เรียน  ผู้บริหารและพนักงานทุกท่าน</b></br>
                      <p>จะมีพนักงานรอการอนุมัติเข้าทำงานจำนวน """ + total_em + """ คน ขอเชิญผู้ประเมินทุกท่านสามารถเข้าไปทำการดำเนินการ ได้ที่<br>
                       <a href="http://hr.devops.inet.co.th">Hr Management</a></p>
                  </body>
                </html>
        """
    server="mailtx.inet.co.th"

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(text, "html","utf-8"))

    try:
        smtp = smtplib.SMTP(server)
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.close()
        result = {'status' : 'done', 'statusDetail' : 'Send email has done'}
        return jsonify(result)
    except:
        result = {'status' : 'error', 'statusDetail' : 'Send email has error : This system cannot send email'}
        return jsonify(result)
def sendToMail_reject_request(email,name_eng,surname_eng,em_name,em_surname,em_position,em_org,imageName):
    send_from = "Hr Management <recruitment@inet.co.th>"
    send_to = email
    subject = "ประเมินพนักงานผ่านทดลองงาน"
    text = """\
                <html>
                  <body>
                  <img src="http://hr.devops.inet.co.th:8888/userGetFileImageMail/"""+imageName+"""""></br>
                    <b>Dear  """ + name_eng + """ """ + surname_eng + """</b></br>
                      <p>พนักงานไม่ได้รับการอนุมัติ """ + em_name + """ """ + em_surname + """ """ + em_position + """ """ + em_org + """ ขอเชิญผู้ประเมินเข้าไปทำการประเมินพนักงาน ได้ที่<br>
                       <a href="http://hr.devops.inet.co.th">Hr Management</a></p>
                  </body>
                </html>
        """
    server="mailtx.inet.co.th"

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(text, "html","utf-8"))

    try:
        smtp = smtplib.SMTP(server)
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.close()
        result = {'status' : 'done', 'statusDetail' : 'Send email has done'}
        return jsonify(result)
    except:
        result = {'status' : 'error', 'statusDetail' : 'Send email has error : This system cannot send email'}
        return jsonify(result)
