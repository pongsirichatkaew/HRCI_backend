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

        result_all={}
        result_all["employee"] = result
        result_all["employee_Education"] = result_Education
        result_all["employee_Employment"] = result_Employment
        result_all["employee_Benefits"] = result_benefits

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

        sqlApprove = "INSERT INTO approve_request(employeeid,employeeid_reques,name,lastname,tier_approve,position_detail,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlApprove,(data_new['employeeid'],data_new['employeeid_reques'],data_new['name'],data_new['lastname'],data_new['tier_approve'],data_new['position_detail'],data_new['createby']))

        type_action = "ADD"

        sqlApprove = "INSERT INTO approve_request_log(employeeid,employeeid_reques,name,lastname,tier_approve,position_detail,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
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
@app.route('/Addapprove_request_many', methods=['POST'])
@connect_sql()
def Addapprove_request_many(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        i=0
        for i in xrange(len(data_new['em_request'])):
            sqlApprove = "INSERT INTO approve_request(employeeid,employeeid_reques,name,lastname,tier_approve,position_detail,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlApprove,(data_new['employeeid'],data_new['em_request'][i]['employeeid_reques'],data_new['em_request'][i]['name'],data_new['em_request'][i]['lastname'],data_new['em_request'][i]['tier_approve'],data_new['em_request'][i]['position_detail'],data_new['createby']))

            type_action = "ADD"

            sqlApprove = "INSERT INTO approve_request_log(employeeid,employeeid_reques,name,lastname,tier_approve,position_detail,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
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

        sqlApprove = "INSERT INTO approve_request_log(employeeid,employeeid_reques,name,lastname,tier_approve,position_detail,status_,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlApprove,(data_new['employeeid'],data_new['employeeid_reques'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],result[0]['status_'],data_new['createby'],type_action))

        sqlDe = "DELETE FROM approve_request WHERE employeeid=%s AND employeeid_reques=%s"
        cursor.execute(sqlDe,(data_new['employeeid'],data_new['employeeid_reques']))

        return "Success"
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

            sqlReject = "INSERT INTO approve_request_log(employeeid,employeeid_reques,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
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

            sqlReject = "INSERT INTO approve_request_log(employeeid,employeeid_reques,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
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

            sqlReject = "INSERT INTO approve_request_log(employeeid,employeeid_reques,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
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

            sqlReject = "INSERT INTO approve_request_log(employeeid,employeeid_reques,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(result[0]['employeeid'],result[0]['employeeid_reques'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,result[0]['comment'],result[0]['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

            sqlUp = "UPDATE approve_request SET status_=2,date_status=%s WHERE employeeid=%s AND employeeid_reques=%s"
            cursor.execute(sqlUp,(data_new['employeeid'],data_new['date_status'],result_check_L1[0]['employeeid_reques']))

            sqlUp_main = "UPDATE employee SET validstatus_request=2 WHERE employeeid=%s"
            cursor.execute(sqlUp_main,(data_new['employeeid']))
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
