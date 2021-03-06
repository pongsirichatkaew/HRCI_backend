#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *
@app.route('/Qry_log_probation', methods=['POST'])
@connect_sql()
def Qry_log_probation(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT approve_probation_log.version,approve_probation_log.id,approve_probation_log.employeeid,approve_probation_log.employeeid_pro,approve_probation_log.name,approve_probation_log.lastname,approve_probation_log.tier_approve,approve_probation_log.position_detail,status.status_detail,approve_probation_log.comment,approve_probation_log.comment_orther,approve_probation_log.date_status FROM approve_probation_log LEFT JOIN status ON status.status_id = approve_probation_log.status_\
        WHERE approve_probation_log.employeeid=%s AND approve_probation_log.version=%s AND approve_probation_log.status_ IS NOT NULL"
        cursor.execute(sql,(data_new['employeeid'],data_new['version']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/UpdateStatus_probation', methods=['POST'])
@connect_sql()
def UpdateStatus_probation(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        tier_approve = str(data_new['tier_approve'])
        status_ = str(data_new['status_'])
        print(tier_approve)
        print(status_)
        result_token = CheckTokenAssessor(data_new['createby'],data_new['token'])
        if result_token!='pass':
            return 'token fail'

        sql_check_end = "SELECT validstatus FROM Emp_probation WHERE employeeid=%s AND version=%s"
        cursor.execute(sql_check_end,(data_new['employeeid'],data_new['version']))
        columns = [column[0] for column in cursor.description]
        result_check_end = toJson(cursor.fetchall(),columns)
        check_endpro = int(result_check_end[0]['validstatus'])
        if check_endpro==9:
            return "End Probation"
        if (tier_approve=='L4')&(status_=='Reject'):
            # sqlCheckList = "SELECT * FROM approve_probation WHERE employeeid=%s AND version=%s"
            # cursor.execute(sqlCheckList, (data_new['employeeid'],data_new['version']))
            # data_checkList = toJson(cursor.fetchall(), [column[0] for column in cursor.description])
            # L1 = False
            # L2 = False
            # L3 = False
            # L4 = False
            # for i in xrange(len(data_checkList)):
            #     if passdata_checkList['tier_approve'] == 'L1':
            #         L1 = True
            #     elif passdata_checkList['tier_approve'] == 'L2':
            #         L2 = True
            #     elif passdata_checkList['tier_approve'] == 'L3':
            #         L3 = True
            #     elif passdata_checkList['tier_approve'] == 'L4':
            #         L4 = True
            sqlUp = "UPDATE approve_probation SET status_=8,id_comment=%s,comment=%s,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
            cursor.execute(sqlUp,(data_new['id_comment'],data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],tier_approve))

            sqlUp_main = "UPDATE Emp_probation SET validstatus=8 WHERE employeeid=%s AND version=%s"
            cursor.execute(sqlUp_main,(data_new['employeeid'],data_new['version']))

            try:
                sqlUp_L3 = "UPDATE approve_probation SET status_=8 WHERE employeeid=%s AND tier_approve='L3' AND version=%s"
                cursor.execute(sqlUp_L3,(data_new['employeeid'],data_new['version']))

                sql_reject_l3 = "SELECT employee.name_eng,employee.surname_eng,employee.email FROM approve_probation  LEFT JOIN employee ON approve_probation.employeeid_pro = employee.employeeid\
                                 WHERE approve_probation.employeeid=%s AND approve_probation.tier_approve='L3' AND approve_probation.version=%s"
                cursor.execute(sql_reject_l3,(data_new['employeeid'],data_new['version']))
                columns = [column[0] for column in cursor.description]
                result_reject_l3 = toJson(cursor.fetchall(),columns)

                sql_reject_employee = "SELECT employee.name_th,employee.surname_th,position.position_detail,org_name.org_name_detail FROM employee LEFT JOIN position ON position.position_id = employee.position_id\
                                                                                                                                                   LEFT JOIN org_name ON org_name.org_name_id = employee.org_name_id\
                                       WHERE employee.employeeid=%s"
                cursor.execute(sql_reject_employee,(data_new['employeeid']))
                columns = [column[0] for column in cursor.description]
                result_reject_employee = toJson(cursor.fetchall(),columns)
                em_name = result_reject_employee[0]['name_th']
                em_surname = result_reject_employee[0]['surname_th']
                em_position = result_reject_employee[0]['position_detail']
                em_org = result_reject_employee[0]['org_name_detail']

                sql_picture = "SELECT mail_type,imageName FROM mail_pic WHERE mail_type='probation_mail'"
                cursor.execute(sql_picture)
                columns = [column[0] for column in cursor.description]
                result_picture = toJson(cursor.fetchall(),columns)

                for item in result_reject_l3:
                    sendToMail_reject(item['email'],item['name_eng'],item['surname_eng'],em_name,em_surname,em_position,em_org,result_picture[0]['imageName'],data_new['comment_orther'])

            except Exception as e:
                pass

            try:
                sqlUp_L2 = "UPDATE approve_probation SET status_=8 WHERE employeeid=%s AND tier_approve='L2' AND version=%s"
                cursor.execute(sqlUp_L2,(data_new['employeeid'],data_new['version']))

                sql_reject_l3 = "SELECT employee.name_eng,employee.surname_eng,employee.email FROM approve_probation  LEFT JOIN employee ON approve_probation.employeeid_pro = employee.employeeid\
                                 WHERE approve_probation.employeeid=%s AND approve_probation.tier_approve='L2' AND approve_probation.version=%s"
                cursor.execute(sql_reject_l3,(data_new['employeeid'],data_new['version']))
                columns = [column[0] for column in cursor.description]
                result_reject_l3 = toJson(cursor.fetchall(),columns)

                sql_reject_employee = "SELECT employee.name_th,employee.surname_th,position.position_detail,org_name.org_name_detail FROM employee LEFT JOIN position ON position.position_id = employee.position_id\
                                                                                                                                                   LEFT JOIN org_name ON org_name.org_name_id = employee.org_name_id\
                                       WHERE employee.employeeid=%s"
                cursor.execute(sql_reject_employee,(data_new['employeeid']))
                columns = [column[0] for column in cursor.description]
                result_reject_employee = toJson(cursor.fetchall(),columns)
                em_name = result_reject_employee[0]['name_th']
                em_surname = result_reject_employee[0]['surname_th']
                em_position = result_reject_employee[0]['position_detail']
                em_org = result_reject_employee[0]['org_name_detail']

                sql_picture = "SELECT mail_type,imageName FROM mail_pic WHERE mail_type='probation_mail'"
                cursor.execute(sql_picture)
                columns = [column[0] for column in cursor.description]
                result_picture = toJson(cursor.fetchall(),columns)

                for item in result_reject_l3:
                    sendToMail_reject(item['email'],item['name_eng'],item['surname_eng'],em_name,em_surname,em_position,em_org,result_picture[0]['imageName'],data_new['comment_orther'])

            except Exception as e:
                pass

            sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
            cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro'],data_new['version']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "reject_director"
            status_last = "8"

            sqlReject = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(data_new['version'],result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

        elif (tier_approve =='L3')&(status_ =='Reject'):

            sqlUp = "UPDATE approve_probation SET status_=7,comment=%s,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
            cursor.execute(sqlUp,(data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],tier_approve))

            sqlUp_main = "UPDATE Emp_probation SET validstatus=7 WHERE employeeid=%s AND version=%s"
            cursor.execute(sqlUp_main,(data_new['employeeid'],data_new['version']))

            try:
                sqlUp_L2 = "UPDATE approve_probation SET status_=7,comment=NULL,comment_orther=NULL,date_status=NULL WHERE employeeid=%s AND tier_approve='L2' AND version=%s"
                cursor.execute(sqlUp_L2,(data_new['employeeid'],data_new['version']))

                sql_reject_l3 = "SELECT employee.name_eng,employee.surname_eng,employee.email FROM approve_probation  LEFT JOIN employee ON approve_probation.employeeid_pro = employee.employeeid\
                                 WHERE approve_probation.employeeid=%s AND approve_probation.tier_approve='L2' AND approve_probation.version=%s"
                cursor.execute(sql_reject_l3,(data_new['employeeid'],data_new['version']))
                columns = [column[0] for column in cursor.description]
                result_reject_l3 = toJson(cursor.fetchall(),columns)

                sql_reject_employee = "SELECT employee.name_th,employee.surname_th,position.position_detail,org_name.org_name_detail FROM employee LEFT JOIN position ON position.position_id = employee.position_id\
                                                                                                                                                   LEFT JOIN org_name ON org_name.org_name_id = employee.org_name_id\
                                       WHERE employee.employeeid=%s"
                cursor.execute(sql_reject_employee,(data_new['employeeid']))
                columns = [column[0] for column in cursor.description]
                result_reject_employee = toJson(cursor.fetchall(),columns)
                em_name = result_reject_employee[0]['name_th']
                em_surname = result_reject_employee[0]['surname_th']
                em_position = result_reject_employee[0]['position_detail']
                em_org = result_reject_employee[0]['org_name_detail']

                sql_picture = "SELECT mail_type,imageName FROM mail_pic WHERE mail_type='probation_mail'"
                cursor.execute(sql_picture)
                columns = [column[0] for column in cursor.description]
                result_picture = toJson(cursor.fetchall(),columns)

                for item in result_reject_l3:
                    sendToMail_reject(item['email'],item['name_eng'],item['surname_eng'],em_name,em_surname,em_position,em_org,result_picture[0]['imageName'],data_new['comment_orther'])

            except Exception as e:
                pass

            sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
            cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro'],data_new['version']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "reject_deputy_director"
            status_last = "7"

            sqlReject = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(data_new['version'],result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

        elif (tier_approve =='L2')&(status_ =='Reject'):

            sqlUp = "UPDATE approve_probation SET status_=6,comment_orther=%s,comment=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
            cursor.execute(sqlUp,(data_new['comment_orther'],data_new['comment'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],tier_approve))

            sqlUp_main = "UPDATE Emp_probation SET validstatus=6 WHERE employeeid=%s AND version=%s"
            cursor.execute(sqlUp_main,(data_new['employeeid'],data_new['version']))

            try:
                sqlUp_L1 = "UPDATE approve_probation SET status_=6,date_status=NULL WHERE employeeid=%s AND tier_approve='L1' AND version=%s AND status_ != 13"
                cursor.execute(sqlUp_L1,(data_new['employeeid'],data_new['version']))

                sql_reject_l3 = "SELECT employee.name_eng,employee.surname_eng,employee.email FROM approve_probation  LEFT JOIN employee ON approve_probation.employeeid_pro = employee.employeeid\
                                 WHERE approve_probation.employeeid=%s AND approve_probation.tier_approve='L1' AND approve_probation.version=%s"
                cursor.execute(sql_reject_l3,(data_new['employeeid'],data_new['version']))
                columns = [column[0] for column in cursor.description]
                result_reject_l3 = toJson(cursor.fetchall(),columns)

                sql_reject_employee = "SELECT employee.name_th,employee.surname_th,position.position_detail,org_name.org_name_detail FROM employee LEFT JOIN position ON position.position_id = employee.position_id\
                                                                                                                                                   LEFT JOIN org_name ON org_name.org_name_id = employee.org_name_id\
                                       WHERE employee.employeeid=%s"
                cursor.execute(sql_reject_employee,(data_new['employeeid']))
                columns = [column[0] for column in cursor.description]
                result_reject_employee = toJson(cursor.fetchall(),columns)
                em_name = result_reject_employee[0]['name_th']
                em_surname = result_reject_employee[0]['surname_th']
                em_position = result_reject_employee[0]['position_detail']
                em_org = result_reject_employee[0]['org_name_detail']

                sql_picture = "SELECT mail_type,imageName FROM mail_pic WHERE mail_type='probation_mail'"
                cursor.execute(sql_picture)
                columns = [column[0] for column in cursor.description]
                result_picture = toJson(cursor.fetchall(),columns)

                for item in result_reject_l3:
                    sendToMail_reject(item['email'],item['name_eng'],item['surname_eng'],em_name,em_surname,em_position,em_org,result_picture[0]['imageName'],data_new['comment_orther'])

            except Exception as e:
                pass

            sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
            cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro'],data_new['version']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "reject_hr"
            status_last = "6"

            sqlReject = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(data_new['version'],result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))


        elif (tier_approve =='L4')&(status_ =='Approve'):

            sqlUp = "UPDATE approve_probation SET status_=14,id_comment=%s,comment=%s,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
            cursor.execute(sqlUp,(data_new['id_comment'],data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],tier_approve))

            sqlUp_main = "UPDATE Emp_probation SET validstatus=10 WHERE employeeid=%s AND version=%s"
            cursor.execute(sqlUp_main,(data_new['employeeid'],data_new['version']))

            sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
            cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],tier_approve))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "send_director"
            status_last = "9"

            sqlReject = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(data_new['version'],result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

            sql_check_status = "SELECT status_result,email FROM Emp_probation WHERE employeeid=%s AND version=%s"
            cursor.execute(sql_check_status,(data_new['employeeid'],data_new['version']))
            columns = [column[0] for column in cursor.description]
            result_status = toJson(cursor.fetchall(),columns)

            status_result = str(result_status[0]['status_result'])
            email_employee = result_status[0]['email']

            if status_result=='่ผ่านทดลองงาน':
                pass
                # for item in result:
                    # sendToMail_reject(data_new['comment_orther'])
            elif status_result=='่ไม่ผ่านทดลองงาน':
                pass
                # for item in result:
                    # sendToMail_reject(data_new['comment_orther'])
            elif status_result=='่ขยายเวลาทดลองงาน':
                pass
                # sql_insert_emp = """
                # INSERT INTO Emp_probation
                # (version, employeeid, citizenid, name_th, name_eng, surname_th, surname_eng, nickname_employee, salary, email, phone_company, position_id, section_id, org_name_id, cost_center_name_id, company_id, start_work, EndWork_probation, type_question, createby)
                # SELECT '%s', employeeid, citizenid, name_th, name_eng, surname_th, surname_eng, nickname_employee, salary, email, phone_company, position_id, section_id, org_name_id, cost_center_name_id, company_id, start_work, EndWork_probation, type_question, '%s'
                # FROM Emp_probation
                # WHERE employeeid = %s AND version = %s
                # """
                # cursor.execute(sql_insert_emp,(int(data_new['version'] + 1, data_new['employeeid_pro'], data_new['employeeid'], data_new['version'])))
                # sql_insert_assessor = """
                # INSERT INTO approve_probation
                # (version, employeeid, employeeid_pro, name, lastname, tier_approve, position_detail, createby)
                # SELECT '%s', employeeid, employeeid_pro, name, lastname, tier_approve, position_detail, '%s'
                # FROM approve_probation
                # WHERE employeeid = %s AND version = %s
                # """
                # cursor.execute(sql_insert_assessor, (int(data_new['version']) + 1, data_new['employeeid_pro'], data_new['employeeid'], data_new['version']))
                # for item in result:
                    # sendToMail_reject(data_new['comment_orther'])

        elif (tier_approve =='L3')&(status_=='Approve'):

            # sqlcheck_L4 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND employeeid=%s AND tier_approve='L4'"
            sqlcheck_L4 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND tier_approve='L4' AND version=%s"
            cursor.execute(sqlcheck_L4,(data_new['employeeid'],data_new['version']))
            columns = [column[0] for column in cursor.description]
            result_check_L4 = toJson(cursor.fetchall(),columns)

            if not result_check_L4:

                sqlUp = "UPDATE approve_probation SET status_=14,comment=%s,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
                cursor.execute(sqlUp,(data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],tier_approve))

                sqlUp_main = "UPDATE Emp_probation SET validstatus=10 WHERE employeeid=%s AND version=%s"
                cursor.execute(sqlUp_main,(data_new['employeeid'],data_new['version']))

                sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
                cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],tier_approve))
                columns = [column[0] for column in cursor.description]
                result = toJson(cursor.fetchall(),columns)

                type_action = "send_deputy_director"
                status_last = "9"

                sqlReject = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlReject,(data_new['version'],result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

            else:

                sqlUp = "UPDATE approve_probation SET status_=14,comment=%s,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
                cursor.execute(sqlUp,(data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],tier_approve))

                sqlUp_main = "UPDATE Emp_probation SET validstatus=5 WHERE employeeid=%s AND version=%s"
                cursor.execute(sqlUp_main,(data_new['employeeid'],data_new['version']))

                sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
                cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],tier_approve))
                columns = [column[0] for column in cursor.description]
                result = toJson(cursor.fetchall(),columns)

                type_action = "send_deputy_director"
                status_last = "5"

                sqlReject = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlReject,(data_new['version'],result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

        elif (tier_approve =='L2')&(status_ =='Approve'):

            # sqlcheck_L3 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND employeeid=%s AND tier_approve='L3'"
            sqlcheck_L3 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND tier_approve='L3' AND version=%s"
            cursor.execute(sqlcheck_L3,(data_new['employeeid'],data_new['version']))
            columns = [column[0] for column in cursor.description]
            result_check_L3 = toJson(cursor.fetchall(),columns)

            if not result_check_L3:

                sqlUp = "UPDATE approve_probation SET status_=14,comment=%s,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
                cursor.execute(sqlUp,(data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],tier_approve))

                sqlUp_main = "UPDATE Emp_probation SET validstatus=5 WHERE employeeid=%s AND version=%s"
                cursor.execute(sqlUp_main,(data_new['employeeid'],data_new['version']))

                sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
                cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],tier_approve))
                columns = [column[0] for column in cursor.description]
                result = toJson(cursor.fetchall(),columns)

                type_action = "send_hr_no_L3"
                status_last = "5"

                sqlReject = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlReject,(data_new['version'],result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))
            else:

                sqlUp = "UPDATE approve_probation SET status_=14,comment=%s,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
                cursor.execute(sqlUp,(data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],tier_approve))

                sqlUp_main = "UPDATE Emp_probation SET validstatus=4 WHERE employeeid=%s AND version=%s"
                cursor.execute(sqlUp_main,(data_new['employeeid'],data_new['version']))

                sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
                cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],tier_approve))
                columns = [column[0] for column in cursor.description]
                result = toJson(cursor.fetchall(),columns)

                type_action = "send_hr"
                status_last = "4"

                sqlReject = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlReject,(data_new['version'],result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))
        else:
            sqlcheck_L1 = "SELECT COUNT(employeeid_pro) AS total_l1 FROM approve_probation WHERE employeeid=%s AND tier_approve='L1' AND version=%s"
            cursor.execute(sqlcheck_L1,(data_new['employeeid'],data_new['version']))
            columns = [column[0] for column in cursor.description]
            result_check_L1 = toJson(cursor.fetchall(),columns)
            check_total_l1 = int(result_check_L1[0]['total_l1'])
            sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
            cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],data_new['tier_approve']))
            result_transfer = toJson(cursor.fetchall(), [column[0] for column in cursor.description])
            result_transfer = result_transfer[0]['comment']
            sql = "SELECT comment FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
            cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],data_new['tier_approve']))
            this_transfer = cursor.fetchall()[0][0]

            sqlcheck_L2 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND tier_approve='L2' AND version=%s"
            # sqlcheck_L2 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND employeeid=%s AND tier_approve='L2'"
            cursor.execute(sqlcheck_L2,(data_new['employeeid'],data_new['version']))
            columns = [column[0] for column in cursor.description]
            result_check_L2 = toJson(cursor.fetchall(),columns)

            # sqlcheck_L3 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND employeeid=%s AND tier_approve='L3'"
            sqlcheck_L3 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND tier_approve='L3' AND version=%s"
            cursor.execute(sqlcheck_L3,(data_new['employeeid'],data_new['version']))
            columns = [column[0] for column in cursor.description]
            result_check_L3 = toJson(cursor.fetchall(),columns)

            if not result_check_L2 and result_check_L3:
                # SAME CODE
                if check_total_l1 > 1:
                    if this_transfer != 'Transfer':
                        sqlUp_main = "UPDATE Emp_probation SET validstatus=15 WHERE employeeid=%s AND version=%s"
                        cursor.execute(sqlUp_main,(data_new['employeeid'],data_new['version']))
                        sqlUp = "UPDATE approve_probation SET status_=13,comment=%s,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
                        cursor.execute(sqlUp,("Approve",data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],tier_approve))
                    else:
                        sqlUp = "UPDATE approve_probation SET status_=14,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
                        cursor.execute(sqlUp,(data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],tier_approve))
                else:
                    sqlUp_main = "UPDATE Emp_probation SET validstatus=15 WHERE employeeid=%s AND version=%s"
                    cursor.execute(sqlUp_main,(data_new['employeeid'],data_new['version']))
                    sqlUp = "UPDATE approve_probation SET status_=14,comment=%s,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
                    cursor.execute(sqlUp,(data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],tier_approve))
                sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
                cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],tier_approve))
                columns = [column[0] for column in cursor.description]
                result = toJson(cursor.fetchall(),columns)

                type_action = "send_head_no_L2"
                status_last = "4"

                sqlReject = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlReject,(data_new['version'],result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

            elif (not result_check_L2)&(not result_check_L3):
                # SAME CODE
                if check_total_l1 > 1:
                    if this_transfer != 'Transfer':
                        sqlUp_main = "UPDATE Emp_probation SET validstatus=15 WHERE employeeid=%s AND version=%s"
                        cursor.execute(sqlUp_main,(data_new['employeeid'],data_new['version']))
                        sqlUp = "UPDATE approve_probation SET status_=13,comment=%s,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
                        cursor.execute(sqlUp,("Approve",data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],tier_approve))
                    else:
                        sqlUp = "UPDATE approve_probation SET status_=14,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
                        cursor.execute(sqlUp,(data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],tier_approve))
                else:
                    sqlUp_main = "UPDATE Emp_probation SET validstatus=15 WHERE employeeid=%s AND version=%s"
                    cursor.execute(sqlUp_main,(data_new['employeeid'],data_new['version']))
                    sqlUp = "UPDATE approve_probation SET status_=14,comment=%s,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
                    cursor.execute(sqlUp,(data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],tier_approve))
                sqlUp = "UPDATE approve_probation SET status_=14,comment=%s,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
                cursor.execute(sqlUp,(data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],tier_approve))

                sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
                cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],tier_approve))
                columns = [column[0] for column in cursor.description]
                result = toJson(cursor.fetchall(),columns)

                type_action = "send_head_no_L2_L3"
                status_last = "5"

                sqlReject = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlReject,(data_new['version'],result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))
            else:
                # SAME CODE
                if check_total_l1 > 1:
                    if this_transfer != 'Transfer' :
                        sqlUp_main = "UPDATE Emp_probation SET validstatus=15 WHERE employeeid=%s AND version=%s"
                        cursor.execute(sqlUp_main,(data_new['employeeid'],data_new['version']))
                        sqlUp = "UPDATE approve_probation SET status_=13,comment=%s,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
                        cursor.execute(sqlUp,("Approve",data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],tier_approve))
                    else:
                        sqlUp = "UPDATE approve_probation SET status_=14,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
                        cursor.execute(sqlUp,(data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],tier_approve))
                else:
                    sqlUp_main = "UPDATE Emp_probation SET validstatus=15 WHERE employeeid=%s AND version=%s"
                    cursor.execute(sqlUp_main,(data_new['employeeid'],data_new['version']))
                    sqlUp = "UPDATE approve_probation SET status_=14,comment=%s,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
                    cursor.execute(sqlUp,(data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],tier_approve))
                sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
                cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],tier_approve))
                columns = [column[0] for column in cursor.description]
                result = toJson(cursor.fetchall(),columns)

                type_action = "send_head"
                status_last = "3"

                sqlReject = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlReject,(data_new['version'],result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/UpdateStatus_probation_all', methods=['POST'])
@connect_sql()
def UpdateStatus_probation_all(cursor):
    # try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        tier_approve = str(data_new['tier_approve'])
        status_ = str(data_new['status_'])
        print data_new
        if (tier_approve =='L4'):
            i=0
            for i in xrange(len(data_new['employee'])):

                sqlUp = "UPDATE approve_probation SET status_=14,comment='อนุมัติ',date_status=%s WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
                cursor.execute(sqlUp,(data_new['date_status'],data_new['employee'][i]['employeeid'],data_new['employeeid_pro'],data_new['employee'][i]['version']))

                sqlUp_main = "UPDATE Emp_probation SET validstatus=10 WHERE employeeid=%s AND version=%s"
                cursor.execute(sqlUp_main,(data_new['employee'][i]['employeeid'],data_new['employee'][i]['version']))

                sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
                cursor.execute(sql,(data_new['employee'][i]['employeeid'],data_new['employeeid_pro'],data_new['employee'][i]['version']))
                columns = [column[0] for column in cursor.description]
                result = toJson(cursor.fetchall(),columns)

                type_action = "send_director"
                status_last = "9"

                sqlReject = "INSERT INTO approve_probation_log(version,employeeid,comment,employeeid_pro,name,lastname,tier_approve,position_detail,status_,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlReject,(data_new['employee'][i]['version'],result[0]['employeeid'],'อนุมัติ',result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['date_status'],data_new['createby'],type_action))

        elif (tier_approve =='L3'):
            i=0
            for i in xrange(len(data_new['employee'])):

                sqlcheck_L4 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND tier_approve='L4' AND version=%s"
                cursor.execute(sqlcheck_L4,(data_new['employee'][i]['employeeid'],data_new['employee'][i]['version']))
                columns = [column[0] for column in cursor.description]
                result_check_L4 = toJson(cursor.fetchall(),columns)

                if not result_check_L4:

                    print(data_new['employee'][i])
                    sqlUp = "UPDATE approve_probation SET status_=14,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
                    cursor.execute(sqlUp,(data_new['date_status'],data_new['employee'][i]['employeeid'],data_new['employeeid_pro'],data_new['employee'][i]['version'],tier_approve))

                    sqlUp_main = "UPDATE Emp_probation SET validstatus=15 WHERE employeeid=%s AND version=%s"
                    cursor.execute(sqlUp_main,(data_new['employee'][i]['employeeid'],data_new['employee'][i]['version']))

                    sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
                    cursor.execute(sql,(data_new['employee'][i]['employeeid'],data_new['employeeid_pro'],data_new['employee'][i]['version']))
                    columns = [column[0] for column in cursor.description]
                    result = toJson(cursor.fetchall(),columns)

                    type_action = "send_deputy_director"
                    status_last = "9"

                    sqlReject = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sqlReject,(data_new['employee'][i]['version'],result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['date_status'],data_new['createby'],type_action))

                else:

                    sqlUp = "UPDATE approve_probation SET status_=14,comment='อนุมัติ',date_status=%s WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
                    cursor.execute(sqlUp,(data_new['date_status'],data_new['employee'][i]['employeeid'],data_new['employeeid_pro'],data_new['employee'][i]['version'],tier_approve))

                    sqlUp_main = "UPDATE Emp_probation SET validstatus=5 WHERE employeeid=%s AND version=%s"
                    cursor.execute(sqlUp_main,(data_new['employee'][i]['employeeid'],data_new['employee'][i]['version']))

                    sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
                    cursor.execute(sql,(data_new['employee'][i]['employeeid'],data_new['employeeid_pro'],data_new['employee'][i]['version']))
                    columns = [column[0] for column in cursor.description]
                    result = toJson(cursor.fetchall(),columns)

                    type_action = "send_deputy_director"
                    status_last = "5"

                    sqlReject = "INSERT INTO approve_probation_log(version,employeeid,comment,employeeid_pro,name,lastname,tier_approve,position_detail,status_,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sqlReject,(data_new['employee'][i]['version'],result[0]['employeeid'],'อนุมัติ',result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['date_status'],data_new['createby'],type_action))

        # DEVELOPING IN PROGRESS
        elif (tier_approve =='L2'):
            for i in xrange(len(data_new['employee'])):
                sqlcheck_L3 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND tier_approve='L3' AND version=%s"
                cursor.execute(sqlcheck_L3,(data_new['employeeid'],data_new['version']))
                columns = [column[0] for column in cursor.description]
                result_check_L3 = toJson(cursor.fetchall(),columns)

                if not result_check_L3:

                    sqlUp = "UPDATE approve_probation SET status_=14,comment=%s,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
                    cursor.execute(sqlUp,(data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],tier_approve))

                    sqlUp_main = "UPDATE Emp_probation SET validstatus=5 WHERE employeeid=%s AND version=%s"
                    cursor.execute(sqlUp_main,(data_new['employeeid'],data_new['version']))

                    sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
                    cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],tier_approve))
                    columns = [column[0] for column in cursor.description]
                    result = toJson(cursor.fetchall(),columns)

                    type_action = "send_hr_no_L3"
                    status_last = "5"

                    sqlReject = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sqlReject,(data_new['version'],result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))
                else:

                    sqlUp = "UPDATE approve_probation SET status_=14,comment=%s,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
                    cursor.execute(sqlUp,(data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],tier_approve))

                    sqlUp_main = "UPDATE Emp_probation SET validstatus=4 WHERE employeeid=%s AND version=%s"
                    cursor.execute(sqlUp_main,(data_new['employeeid'],data_new['version']))

                    sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
                    cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],tier_approve))
                    columns = [column[0] for column in cursor.description]
                    result = toJson(cursor.fetchall(),columns)

                    type_action = "send_hr"
                    status_last = "4"

                    sqlReject = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sqlReject,(data_new['version'],result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))
        return "Success"
    # except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Send_probation', methods=['POST'])
@connect_sql()
def Send_probation(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sqlcheck_L1 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND tier_approve='L1' AND version=%s"
        cursor.execute(sqlcheck_L1,(data_new['employeeid'],data_new['version']))
        columns = [column[0] for column in cursor.description]
        result_check_L1 = toJson(cursor.fetchall(),columns)

        sqlcheck_L2 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND tier_approve='L2' AND version=%s"
        cursor.execute(sqlcheck_L2,(data_new['employeeid'],data_new['version']))
        columns = [column[0] for column in cursor.description]
        result_check_L2 = toJson(cursor.fetchall(),columns)

        sqlcheck_L3 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND tier_approve='L3' AND version=%s"
        cursor.execute(sqlcheck_L3,(data_new['employeeid'],data_new['version']))
        columns = [column[0] for column in cursor.description]
        result_check_L3 = toJson(cursor.fetchall(),columns)

        try:
            check_L3 = result_check_L3[0]['employeeid_pro']
        except Exception as e:
            return "No Level L3"

        sqlcheck_L4 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND tier_approve='L4' AND version=%s"
        cursor.execute(sqlcheck_L4,(data_new['employeeid'],data_new['version']))
        columns = [column[0] for column in cursor.description]
        result_check_L4 = toJson(cursor.fetchall(),columns)

        if (not result_check_L2)&(not result_check_L1):
            sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
            cursor.execute(sql,(data_new['employeeid'],result_check_L3[0]['employeeid_pro'],data_new['version']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "send_pro_no_L2"
            status_last = "4"

            sqlReject = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(data_new['version'],result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,result[0]['comment'],result[0]['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

            sqlUp = "UPDATE approve_probation SET status_=4,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
            cursor.execute(sqlUp,(data_new['date_status'],data_new['employeeid'],result_check_L3[0]['employeeid_pro'],data_new['version']))

            sqlUp_main = "UPDATE Emp_probation SET type_question=%s,validstatus=4 WHERE employeeid=%s AND version=%s"
            cursor.execute(sqlUp_main,(data_new['type_question'],data_new['employeeid'],data_new['version']))

        elif (not result_check_L2)&(not result_check_L3)&(not result_check_L1):
            sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
            cursor.execute(sql,(data_new['employeeid'],result_check_L2[0]['employeeid_pro'],data_new['version']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "send_pro_no_L2_L3_L1"
            status_last = "5"

            sqlReject = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(data_new['version'],result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,result[0]['comment'],result[0]['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

            sqlUp = "UPDATE approve_probation SET status_=5,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
            cursor.execute(sqlUp,(data_new['date_status'],data_new['employeeid'],result_check_L2[0]['employeeid_pro'],data_new['version']))

            sqlUp_main = "UPDATE Emp_probation SET type_question=%s,validstatus=5 WHERE employeeid=%s AND version=%s"
            cursor.execute(sqlUp_main,(data_new['type_question'],data_new['employeeid'],data_new['version']))
        elif not result_check_L1:
            sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
            cursor.execute(sql,(data_new['employeeid'],result_check_L2[0]['employeeid_pro'],data_new['version']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "send_pro_no_L1"
            status_last = "3"

            sqlReject = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(data_new['version'],result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,result[0]['comment'],result[0]['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

            sqlUp = "UPDATE approve_probation SET status_=3,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
            cursor.execute(sqlUp,(data_new['date_status'],data_new['employeeid'],result_check_L2[0]['employeeid_pro'],data_new['version']))

            sqlUp_main = "UPDATE Emp_probation SET type_question=%s,validstatus=3 WHERE employeeid=%s AND version=%s"
            cursor.execute(sqlUp_main,(data_new['type_question'],data_new['employeeid'],data_new['version']))
        else:
            sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
            cursor.execute(sql,(data_new['employeeid'],result_check_L1[0]['employeeid_pro'],data_new['version']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "send_pro"
            status_last = "2"

            sqlReject = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(data_new['version'],result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,result[0]['comment'],result[0]['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

            sqlUp = "UPDATE approve_probation SET status_=2,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
            cursor.execute(sqlUp,(data_new['employeeid'],data_new['date_status'],result_check_L1[0]['employeeid_pro'],data_new['version']))

            sqlUp_main = "UPDATE Emp_probation SET type_question=%s,validstatus=2 WHERE employeeid=%s AND version=%s"
            cursor.execute(sqlUp_main,(data_new['type_question'],data_new['employeeid'],data_new['version']))
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Approve_hr', methods=['POST'])
@connect_sql()
def Approve_hr(cursor):
    # try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sqlcheck_L2 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND tier_approve='L2' AND version=%s"
        cursor.execute(sqlcheck_L2,(data_new['employeeid'],data_new['version']))
        columns = [column[0] for column in cursor.description]
        result_check_L2 = toJson(cursor.fetchall(),columns)

        sqlcheck_L3 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND tier_approve='L3' AND version=%s"
        cursor.execute(sqlcheck_L3,(data_new['employeeid'],data_new['version']))
        columns = [column[0] for column in cursor.description]
        result_check_L3 = toJson(cursor.fetchall(),columns)

        sqlcheck_L4 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND tier_approve='L4' AND version=%s"
        cursor.execute(sqlcheck_L4,(data_new['employeeid'],data_new['version']))
        result_check_L4 = toJson(cursor.fetchall(),[column[0] for column in cursor.description])

        if not result_check_L2:

            sqlUp_main = "UPDATE Emp_probation SET validstatus=4 WHERE employeeid=%s AND version=%s"
            cursor.execute(sqlUp_main,(data_new['employeeid'],data_new['version']))

            sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND version=%S"
            cursor.execute(sql,(data_new['employeeid'],data_new['version']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "send_head_no_L2_by_hr"
            status_last = "4"

            sqlReject = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(data_new['version'],result[0]['employeeid'],data_new['createby'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

        elif (not result_check_L2)&(not result_check_L3):

            sqlUp_main = "UPDATE Emp_probation SET validstatus=5 WHERE employeeid=% AND version=%s"
            cursor.execute(sqlUp_main,(data_new['employeeid'],data_new['version']))

            sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND version=%s"
            cursor.execute(sql,(data_new['employeeid'],data_new['version']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "send_head_no_L2_L3_by_hr"
            status_last = "5"

            sqlReject = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(data_new['version'],[0]['employeeid'],data_new['createby'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

        else:
            sqlUp_main = "UPDATE Emp_probation SET validstatus=3 WHERE employeeid=%s AND version=%s"
            cursor.execute(sqlUp_main,(data_new['employeeid'],data_new['version']))

            sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
            cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro'],data_new['version']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "send_head_by_hr"
            status_last = "3"

            sqlReject = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(data_new['version'],result[0]['employeeid'],data_new['createby'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

        return "Success"
    # except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Abstract_hr', methods=['POST'])
@connect_sql()
def Abstract_hr(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        abstract = data_new['abstract']

        result_token = CheckTokenAdmin(data_new['createby'],data_new['token'])
        if result_token!='pass':
            return 'token fail'

        sqlcheck_L4 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND tier_approve='L4' AND version=%s"
        cursor.execute(sqlcheck_L4,(data_new['employeeid'],data_new['version']))
        columns = [column[0] for column in cursor.description]
        result_check_L4 = toJson(cursor.fetchall(),columns)

        sqlcheck_L2 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND tier_approve='L2' AND version=%s"
        cursor.execute(sqlcheck_L2,(data_new['employeeid'],data_new['version']))
        columns = [column[0] for column in cursor.description]
        result_check_L2 = toJson(cursor.fetchall(),columns)

        sqlcheck_L3 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND tier_approve='L3' AND version=%s"
        cursor.execute(sqlcheck_L3,(data_new['employeeid'],data_new['version']))
        columns = [column[0] for column in cursor.description]
        result_check_L3 = toJson(cursor.fetchall(),columns)

        if (abstract=='Pass'): # PASS PROBATION

            if not result_check_L2:

                sqlUp__ = "UPDATE Emp_probation SET validstatus=4,status_result='ผ่านทดลองงาน' WHERE employeeid=%s AND version=%s"
                cursor.execute(sqlUp__,(data_new['employeeid'],data_new['version']))

            elif (not result_check_L2)&(not result_check_L3):

                sqlUp__ = "UPDATE Emp_probation SET validstatus=5,status_result='ผ่านทดลองงาน' WHERE employeeid=%s AND version=%s"
                cursor.execute(sqlUp__,(data_new['employeeid'],data_new['version']))
            else:

                sqlUp__ = "UPDATE Emp_probation SET validstatus=3,status_result='ผ่านทดลองงาน' WHERE employeeid=%s AND version=%s"
                cursor.execute(sqlUp__,(data_new['employeeid'],data_new['version']))

            # sqlcheck_L1 = "SELECT COUNT(employeeid_pro) AS total_l1 FROM approve_probation WHERE employeeid=%s AND tier_approve='L1' AND version=%s"
            # cursor.execute(sqlcheck_L1,(data_new['employeeid'],data_new['version']))
            # columns = [column[0] for column in cursor.description]
            # result_check_L1 = toJson(cursor.fetchall(),columns)
            # check_total_l1 = int(result_check_L1[0]['total_l1'])
            #
            # sqlcheck_L2 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND tier_approve='L2' AND version=%s"
            # # sqlcheck_L2 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND employeeid=%s AND tier_approve='L2'"
            # cursor.execute(sqlcheck_L2,(data_new['employeeid'],data_new['version']))
            # columns = [column[0] for column in cursor.description]
            # result_check_L2 = toJson(cursor.fetchall(),columns)
            #
            # # sqlcheck_L3 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND employeeid=%s AND tier_approve='L3'"
            # sqlcheck_L3 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND tier_approve='L3' AND version=%s"
            # cursor.execute(sqlcheck_L3,(data_new['employeeid'],data_new['version']))
            # columns = [column[0] for column in cursor.description]
            # result_check_L3 = toJson(cursor.fetchall(),columns)
            #
            # if not result_check_L2:
            #
            #     # sqlUp = "UPDATE approve_probation SET status_=14,comment=%s,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
            #     # cursor.execute(sqlUp,(data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro'],data_new['version']))
            #
            #     if check_total_l1==1 :
            #         sqlUp_main = "UPDATE Emp_probation SET validstatus=4 WHERE employeeid=%s AND version=%s"
            #         cursor.execute(sqlUp_main,(data_new['employeeid'],data_new['version']))
            #     else:
            #         pass
                # sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
                # cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro'],data_new['version']))
                # columns = [column[0] for column in cursor.description]
                # result = toJson(cursor.fetchall(),columns)

                # type_action = "send_head_no_L2"
                # status_last = "4"
                #
                # sqlReject = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                # cursor.execute(sqlReject,(data_new['version'],result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

            # elif (not result_check_L2)&(not result_check_L3):
            #
            #     # sqlUp = "UPDATE approve_probation SET status_=14,comment=%s,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
            #     # cursor.execute(sqlUp,(data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro'],data_new['version']))
            #
            #     if check_total_l1==1 :
            #         sqlUp_main = "UPDATE Emp_probation SET validstatus=5 WHERE employeeid=%s AND version=%s"
            #         cursor.execute(sqlUp_main,(data_new['employeeid'],data_new['version']))
            #     else:
            #         pass

                # sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
                # cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro'],data_new['version']))
                # columns = [column[0] for column in cursor.description]
                # result = toJson(cursor.fetchall(),columns)

                # type_action = "send_head_no_L2_L3"
                # status_last = "5"
                #
                # sqlReject = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                # cursor.execute(sqlReject,(data_new['version'],result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

            # sqlUp_main = "UPDATE Emp_probation SET validstatus=9 WHERE employeeid=%s AND version=%s"
            # cursor.execute(sqlUp_main,(data_new['employeeid'],data_new['version']))
            # print 'AbstractHR_Pass',data_new


            sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND version=%s"
            cursor.execute(sql,(data_new['employeeid'],data_new['version']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "abstract_pass"
            status_last = "9"

            sqlReject = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(data_new['version'],result[0]['employeeid'],data_new['createby'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

            sql_reject_l3 = "SELECT username FROM Admin WHERE employeeid=%s"
            cursor.execute(sql_reject_l3,(data_new['createby']))
            columns = [column[0] for column in cursor.description]
            result_admin = toJson(cursor.fetchall(),columns)

            sql_reject_employee = "SELECT employee.name_th,employee.surname_th,employee.email,position.position_detail,org_name.org_name_detail FROM employee LEFT JOIN position ON position.position_id = employee.position_id\
            LEFT JOIN org_name ON org_name.org_name_id = employee.org_name_id  WHERE employee.employeeid=%s"
            cursor.execute(sql_reject_employee,(data_new['employeeid']))
            columns = [column[0] for column in cursor.description]
            result_reject_employee = toJson(cursor.fetchall(),columns)
            em_name = result_reject_employee[0]['name_th']
            em_surname = result_reject_employee[0]['surname_th']
            em_position = result_reject_employee[0]['position_detail']
            em_org = result_reject_employee[0]['org_name_detail']
            email = result_reject_employee[0]['email']

            sql_picture = "SELECT mail_type,imageName FROM mail_pic WHERE mail_type='probation_mail'"
            cursor.execute(sql_picture)
            columns = [column[0] for column in cursor.description]
            result_picture = toJson(cursor.fetchall(),columns)

            # sendpass_probation(email,em_name,em_surname,em_position,em_org,result_admin[0]['username'],result_picture[0]['imageName'])

            ## update to Emp_probation

            sql_check_prob = """SELECT employeeid FROM Emp_probation WHERE employeeid = %s AND version = %s AND position_id = %s AND section_id = %s AND org_name_id = %s AND cost_center_name_id = %s AND company_id = %s"""
            cursor.execute(sql_check_prob,(data_new['employeeid'],data_new['version'],data_new['position_id'],data_new['section_id'],data_new['org_name_id'],data_new['cost_center_name_id'],data_new['company_id']))
            columns = [column[0] for column in cursor.description]
            result_check_prob = toJson(cursor.fetchall(),columns)
            # print 'result_check_prob',result_check_prob
            if(len(result_check_prob)>0):
                print 'probExists'
                pass
            else:
                print 'probNotExists'
                sql_update_prob = """UPDATE `Emp_probation` SET position_id = %s ,section_id = %s, org_name_id = %s , cost_center_name_id = %s, company_id = %s WHERE employeeid = %s AND version = %s"""
                cursor.execute(sql_update_prob,(data_new['position_id'],data_new['section_id'],data_new['org_name_id'],data_new['cost_center_name_id'],data_new['company_id'],data_new['employeeid'],data_new['version']))

                sql_prob = """SELECT * FROM Emp_probation WHERE employeeid=%s AND version=%s"""
                cursor.execute(sql_prob,(data_new['employeeid'],data_new['version']))
                columns = [column[0] for column in cursor.description]
                result_prob = toJson(cursor.fetchall(),columns)
                type_action = 'relocate_pass'
                sqlEM_pro_log = "INSERT INTO Emp_probation_log (version,employeeid,citizenid,name_th,name_eng,surname_th,surname_eng,nickname_employee,salary,email,phone_company,position_id,section_id,org_name_id,cost_center_name_id,company_id,start_work,EndWork_probation,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlEM_pro_log,(result_prob[0]['version'],result_prob[0]['employeeid'],result_prob[0]['citizenid'],result_prob[0]['name_th'],result_prob[0]['name_eng'],result_prob[0]['surname_th'],result_prob[0]['surname_eng'],result_prob[0]['nickname_employee'],result_prob[0]['salary'],result_prob[0]['email'],result_prob[0]['phone_company'],result_prob[0]['position_id'],\
                result_prob[0]['section_id'],result_prob[0]['org_name_id'],result_prob[0]['cost_center_name_id'],result_prob[0]['company_id'],result_prob[0]['start_work'],result_prob[0]['EndWork_probation'],result_prob[0]['createby'],type_action))



        elif (abstract=='Not_pass'): #REJECT PROBATION

            if not result_check_L2:

                sqlUp__ = "UPDATE Emp_probation SET validstatus=4,status_result='ไม่ผ่านทดลองงาน' WHERE employeeid=%s AND version=%s"
                cursor.execute(sqlUp__,(data_new['employeeid'],data_new['version']))

            elif (not result_check_L2)&(not result_check_L3):

                sqlUp__ = "UPDATE Emp_probation SET validstatus=5,status_result='ไม่ผ่านทดลองงาน' WHERE employeeid=%s AND version=%s"
                cursor.execute(sqlUp__,(data_new['employeeid'],data_new['version']))
            else:

                sqlUp__ = "UPDATE Emp_probation SET validstatus=3,status_result='ไม่ผ่านทดลองงาน' WHERE employeeid=%s AND version=%s"
                cursor.execute(sqlUp__,(data_new['employeeid'],data_new['version']))

            sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND version=%s"
            cursor.execute(sql,(data_new['employeeid'],data_new['version']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "abstract_not_pass"
            status_last = "11"

            sqlReject = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(data_new['version'],result[0]['employeeid'],data_new['createby'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

        elif (abstract=='Reject'): # EDIT PROBATION

            # sqlUp = "UPDATE approve_probation SET status_=6,comment=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
            # cursor.execute(sqlUp,(data_new['comment'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro'],data_new['version']))

            sqlUp_main = "UPDATE Emp_probation SET validstatus=11 WHERE employeeid=%s AND version=%s"
            cursor.execute(sqlUp_main,(data_new['employeeid'],data_new['version']))

            sqlUp_approve = "UPDATE approve_probation SET status_ = 1 WHERE employeeid=%s AND version=%s AND tier_approve='L1' AND status_ != 13"
            cursor.execute(sqlUp_approve,(data_new['employeeid'],data_new['version']))

            try:
                # sqlUp_L1 = "UPDATE approve_probation SET status_=6,comment=NULL,date_status=NULL WHERE employeeid=%s AND tier_approve='L1' AND version=%s"
                # cursor.execute(sqlUp_L1,(data_new['employeeid'],data_new['version']))


                sql_reject_l3 = "SELECT employee.name_eng,employee.surname_eng,employee.email FROM approve_probation  LEFT JOIN employee ON approve_probation.employeeid_pro = employee.employeeid\
                                 WHERE approve_probation.employeeid=%s AND approve_probation.tier_approve='L1' AND approve_probation.version=%s"
                cursor.execute(sql_reject_l3,(data_new['employeeid'],data_new['version']))
                columns = [column[0] for column in cursor.description]
                result_reject_l3 = toJson(cursor.fetchall(),columns)

                sql_reject_employee = "SELECT employee.name_th,employee.surname_th,position.position_detail,org_name.org_name_detail FROM employee LEFT JOIN position ON position.position_id = employee.position_id\
                                                                                                                                                   LEFT JOIN org_name ON org_name.org_name_id = employee.org_name_id\
                                       WHERE employee.employeeid=%s"
                cursor.execute(sql_reject_employee,(data_new['employeeid']))
                columns = [column[0] for column in cursor.description]
                result_reject_employee = toJson(cursor.fetchall(),columns)
                em_name = result_reject_employee[0]['name_th']
                em_surname = result_reject_employee[0]['surname_th']
                em_position = result_reject_employee[0]['position_detail']
                em_org = result_reject_employee[0]['org_name_detail']

                sql_picture = "SELECT mail_type,imageName FROM mail_pic WHERE mail_type='probation_mail'"
                cursor.execute(sql_picture)
                columns = [column[0] for column in cursor.description]
                result_picture = toJson(cursor.fetchall(),columns)

                for item in result_reject_l3:
                    sendToMail_reject(item['email'],item['name_eng'],item['surname_eng'],em_name,em_surname,em_position,em_org,result_picture[0]['imageName'],data_new['comment_orther'])

            except Exception as e:
                pass

            sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND version=%s"
            cursor.execute(sql,(data_new['employeeid'],data_new['version']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "reject_hr_admin"
            status_last = "6"

            sqlReject = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(data_new['version'],result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))
        else: # EXTEND PROBATION
            print 'EXTEND'
            if not result_check_L2:

                sqlUp__ = "UPDATE Emp_probation SET validstatus=4,status_result='ขยายเวลาทดลองงาน' WHERE employeeid=%s AND version=%s"
                cursor.execute(sqlUp__,(data_new['employeeid'],data_new['version']))

            elif (not result_check_L2)&(not result_check_L3):

                sqlUp__ = "UPDATE Emp_probation SET validstatus=5,status_result='ขยายเวลาทดลองงาน' WHERE employeeid=%s AND version=%s"
                cursor.execute(sqlUp__,(data_new['employeeid'],data_new['version']))
            else:
                sqlUp__ = "UPDATE Emp_probation SET validstatus=3,status_result='ขยายเวลาทดลองงาน' WHERE employeeid=%s AND version=%s"
                cursor.execute(sqlUp__,(data_new['employeeid'],data_new['version']))

            sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND version=%s"
            cursor.execute(sql,(data_new['employeeid'],data_new['version']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "abstract_extend_work"
            status_last = "10"

            sqlReject = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(data_new['version'],result[0]['employeeid'],data_new['createby'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

            sql14 = "SELECT * FROM Emp_probation WHERE employeeid=%s AND version=%s ORDER BY version DESC LIMIT 1"
            cursor.execute(sql14,(data_new['employeeid'],data_new['version']))
            columns = [column[0] for column in cursor.description]
            result14 = toJson(cursor.fetchall(),columns)

            version_last = int(result14[0]['version'])+1
            date1 = result14[0]['EndWork_probation']
            long_date = 30
            star_date = date1.split("-")
            Day_s = int(star_date[0])
            Mon_s = int(star_date[1])
            year_s = int(star_date[2])
            next_3_mm = date(year_s,Mon_s,Day_s) + relativedelta(days=long_date)
            next_3_m2 = str(next_3_mm)
            end_date = next_3_m2.split("-")
            Day_e = end_date[2]
            Mon_e =end_date[1]
            year_e = end_date[0]
            End_probation_date = Day_e+"-"+Mon_e+"-"+year_e
            # encodedsalary = base64.b64encode(data_new['salary'])
            encodedsalary = data_new['salary']

            sqlEM_pro = "INSERT INTO Emp_probation (version,employeeid,citizenid,name_th,name_eng,surname_th,surname_eng,nickname_employee,salary,email,phone_company,position_id,section_id,org_name_id,cost_center_name_id,company_id,start_work,EndWork_probation,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlEM_pro,(version_last,result14[0]['employeeid'],result14[0]['citizenid'],result14[0]['name_th'],result14[0]['name_eng'],result14[0]['surname_th'],result14[0]['surname_eng'],result14[0]['nickname_employee'],encodedsalary,result14[0]['email'],result14[0]['phone_company'],data_new['position_id'],\
            data_new['section_id'],data_new['org_name_id'],data_new['cost_center_name_id'],data_new['company_id'],result14[0]['EndWork_probation'],End_probation_date,data_new['createby']))

            sqlEM_pro_log = "INSERT INTO Emp_probation_log (version,employeeid,citizenid,name_th,name_eng,surname_th,surname_eng,nickname_employee,salary,email,phone_company,position_id,section_id,org_name_id,cost_center_name_id,company_id,start_work,EndWork_probation,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlEM_pro_log,(version_last,result14[0]['employeeid'],result14[0]['citizenid'],result14[0]['name_th'],result14[0]['name_eng'],result14[0]['surname_th'],result14[0]['surname_eng'],result14[0]['nickname_employee'],encodedsalary,result14[0]['email'],result14[0]['phone_company'],data_new['position_id'],\
            data_new['section_id'],data_new['org_name_id'],data_new['cost_center_name_id'],data_new['company_id'],result14[0]['EndWork_probation'],End_probation_date,data_new['createby'],type_action))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/AddApprove_pro_tranfer', methods=['POST'])
@connect_sql()
def AddApprove_pro_tranfer(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        try:
            sql_check_empro = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
            cursor.execute(sql_check_empro,(data_new['employeeid'],data_new['employeeid_pro_2'],data_new['version'],data_new['tier_approve']))
            # sql_check_empro = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
            # cursor.execute(sql_check_empro,(data_new['employeeid'],data_new['employeeid_pro_2'],data_new['version']))
            columns = [column[0] for column in cursor.description]
            result_check_empro = toJson(cursor.fetchall(),columns)
            type_check = result_check_empro[0]['employeeid_pro']
            return "employeeid_pro duplicate"
        except Exception as e:
            pass
        # sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
        # cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro'],data_new['version']))
        # columns = [column[0] for column in cursor.description]
        # result = toJson(cursor.fetchall(),columns)
        # Tier_Approve_Owner = result[0]['tier_approve']

        sqlApprove = "INSERT INTO approve_probation(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,createby,comment) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'Transfer')"
        cursor.execute(sqlApprove,(data_new['version'],data_new['employeeid'],data_new['employeeid_pro_2'],data_new['name'],data_new['lastname'],data_new['tier_approve'],data_new['position_detail'],data_new['createby']))

        type_action = "ADD_tranfer"

        sqlApprove_log = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlApprove_log,(data_new['version'],data_new['employeeid'],data_new['employeeid_pro_2'],data_new['name'],data_new['lastname'],data_new['tier_approve'],data_new['position_detail'],data_new['createby'],type_action))

        sqlUp = "UPDATE approve_probation SET status_=13,comment=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
        cursor.execute(sqlUp,(data_new['comment'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],data_new['tier_approve']))

        type_action2 = "transfer"
        status_last = "13"

        sqlReject = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlReject,(data_new['version'],data_new['employeeid'],data_new['employeeid_pro'],data_new['name'],data_new['lastname'],data_new['tier_approve'],data_new['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action2))

        try:
            sql44 = "SELECT name_asp FROM assessor_pro WHERE companyid=%s AND tier_approve=%s AND employeeid=%s"
            cursor.execute(sql44,(data_new['companyid'],data_new['tier_approve'],data_new['employeeid_pro_2']))
            columns = [column[0] for column in cursor.description]
            result_test = toJson(cursor.fetchall(),columns)
            name_test = result_test[0]['name_asp']
        except Exception as e:

            sqlQry = "SELECT assessor_pro_id FROM assessor_pro ORDER BY assessor_pro_id DESC LIMIT 1"
            cursor.execute(sqlQry)
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            assessor_pro_id_last=result[0]['assessor_pro_id']+1

            sql = "INSERT INTO assessor_pro (assessor_pro_id,employeeid,companyid,name_asp,surname_asp,position_id,tier_approve,email_asp,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,(assessor_pro_id_last,data_new['employeeid_pro_2'],data_new['companyid'],data_new['name'],data_new['lastname'],data_new['position_id'],data_new['tier_approve'],data_new['email_asp'],data_new['createby']))

            type_action = "ADD"

            sql_log = "INSERT INTO assessor_pro_log (assessor_pro_id,employeeid,companyid,name_asp,surname_asp,position_id,tier_approve,email_asp,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql_log,(assessor_pro_id_last,data_new['employeeid_pro'],data_new['companyid'],data_new['name'],data_new['lastname'],data_new['position_id'],data_new['tier_approve'],data_new['email_asp'],data_new['createby'],type_action))

        return "Success"
    except Exception as e:
            logserver(e)
            return "fail"
@app.route('/QueryApprove_pro_tranfer', methods=['POST'])
@connect_sql()
def QueryApprove_pro_tranfer(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = """
        SELECT *
        FROM approve_probation
        WHERE employeeid=%s AND comment='Transfer' AND version=%s
        """
        # sql = "SELECT * FROM approve_probation_log WHERE employeeid=%s AND createby=%s AND type_action='ADD_tranfer' AND version=%s"
        # cursor.execute(sql,(data_new['employeeid'],data_new['createby',data_new['version']))
        cursor.execute(sql,(data_new['employeeid'],data_new['version']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
            logserver(e)
            return "fail"
@app.route('/AddApprove_pro_together', methods=['POST'])
@connect_sql()
def AddApprove_pro_together(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        try:
            sql_check_empro = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
            cursor.execute(sql_check_empro,(data_new['employeeid'],data_new['employeeid_pro_2'],data_new['version']))
            columns = [column[0] for column in cursor.description]
            result_check_empro = toJson(cursor.fetchall(),columns)
            type_check = result_check_empro[0]['employeeid_pro']
            return "employeeid_pro duplicate"
        except Exception as e:
            pass

        sql = "SELECT tier_approve FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
        cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro'],data_new['version']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        Tier_Approve_Owner = result[0]['tier_approve']

        sqlApprove = "INSERT INTO approve_probation(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlApprove,(data_new['version'],data_new['employeeid'],data_new['employeeid_pro_2'],data_new['name'],data_new['lastname'],result[0]['tier_approve'],data_new['position_detail'],data_new['createby']))

        type_action = "ADD_together"

        sqlApprove_log = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlApprove_log,(data_new['version'],data_new['employeeid'],data_new['employeeid_pro_2'],data_new['name'],data_new['lastname'],result[0]['tier_approve'],data_new['position_detail'],data_new['createby'],type_action))

        try:
            sql44 = "SELECT name_asp FROM assessor_pro WHERE companyid=%s AND tier_approve=%s AND employeeid=%s"
            cursor.execute(sql44,(data_new['companyid'],result[0]['tier_approve'],data_new['employeeid_pro']))
            columns = [column[0] for column in cursor.description]
            result_test = toJson(cursor.fetchall(),columns)
            name_test = result_test[0]['name_asp']
        except Exception as e:

            sqlQry = "SELECT assessor_pro_id FROM assessor_pro ORDER BY assessor_pro_id DESC LIMIT 1"
            cursor.execute(sqlQry)
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            assessor_pro_id_last=result[0]['assessor_pro_id']+1

            sql = "INSERT INTO assessor_pro (assessor_pro_id,employeeid,companyid,name_asp,surname_asp,position_id,tier_approve,email_asp,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,(assessor_pro_id_last,data_new['employeeid_pro'],data_new['companyid'],data_new['name'],data_new['lastname'],data_new['position_id'],Tier_Approve_Owner,data_new['email_asp'],data_new['createby']))

            type_action = "ADD"

            sql_log = "INSERT INTO assessor_pro_log (assessor_pro_id,employeeid,companyid,name_asp,surname_asp,position_id,tier_approve,email_asp,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql_log,(assessor_pro_id_last,data_new['employeeid_pro'],data_new['companyid'],data_new['name'],data_new['lastname'],data_new['position_id'],Tier_Approve_Owner,data_new['email_asp'],data_new['createby'],type_action))

        return "Success"
    except Exception as e:
            logserver(e)
            return "fail"
@app.route('/removeTransfer_pro', methods=['POST'])
@connect_sql()
def removeTransfer_pro(cursor):
    try:
        data = request.json
        data = data['source']
        try:
            sqlcheck_ans = "SELECT name FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND date_status IS NULL AND tier_approve=%s"
            cursor.execute(sqlcheck_ans,(data['employeeid'],data['employeeid_pro'],data['version'],data['tier_approve']))
            result_check = toJson(cursor.fetchall(), [column[0] for column in cursor.description])
            result_name = result_check[0]['name']
        except Exception as e:
            return "Not Remove"
        sql = "DELETE FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
        cursor.execute(sql,(data['employeeid'],data['employeeid_pro'],data['version'],data['tier_approve']))
        sql_check_all_transfer = "SELECT * FROM approve_probation WHERE employeeid=%s AND version=%s AND comment='Transfer'"
        cursor.execute(sql_check_all_transfer,(data['employeeid'],data['version']))
        result_all_transfer = cursor.fetchall()
        if len(result_all_transfer) == 0:
            sql_update = "UPDATE approve_probation SET status_=1, date_status=NULL WHERE employeeid=%s AND version=%s AND tier_approve=%s"
            cursor.execute(sql_update,(data['employeeid'],data['version'],data['tier_approve']))
        return "success"
    except Exception as e:
        return "fail"

@app.route('/removeApprove_pro_together', methods=['POST'])
@connect_sql()
def removeApprove_pro_together(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        try:
            sqlcheck_ans = "SELECT name FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND date_status IS NULL"
            cursor.execute(sqlcheck_ans,(data_new['employeeid'],data_new['employeeid_pro_2'],data_new['version']))
            columns = [column[0] for column in cursor.description]
            result_check_ans = toJson(cursor.fetchall(),columns)
            result_chs = result_check_ans[0]['name']
        except Exception as e:
            return "Not remove"

        sql = "SELECT tier_approve FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
        cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro'],data_new['version']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        Tier_Approve_Owner = result[0]['tier_approve']

        sqlApprove = "DELETE FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND tier_approve=%s AND createby=%s AND version=%s"
        cursor.execute(sqlApprove,(data_new['employeeid'],data_new['employeeid_pro_2'],result[0]['tier_approve'],data_new['createby'],data_new['version']))

        return "Success"
    except Exception as e:
            logserver(e)
            return "fail"
@app.route('/QueryApprove_pro_together', methods=['POST'])
@connect_sql()
def QueryApprove_pro_together(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND createby=%s AND version=%s"
        cursor.execute(sql,(data_new['employeeid'],data_new['createby'],data_new['version']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
            logserver(e)
            return "fail"
@app.route('/QryApprove_probation', methods=['POST'])
@connect_sql()
def QryApprove_probation(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT *,(SELECT COUNT(*) FROM employee_pro WHERE employee_pro.employeeid = approve_probation.employeeid AND employee_pro.createby = approve_probation.employeeid_pro) AS ans_count FROM approve_probation WHERE employeeid=%s AND version=%s ORDER BY tier_approve"
        cursor.execute(sql,(data_new['employeeid'],data_new['version']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sql2 = "SELECT validstatus FROM Emp_probation WHERE employeeid=%s AND version=%s"
        cursor.execute(sql2,(data_new['employeeid'],data_new['version']))
        columns = [column[0] for column in cursor.description]
        result2 = toJson(cursor.fetchall(),columns)
        for item in result:
            validstatus = []
            item['validstatus'] = result2[0]['validstatus']

        return jsonify(result)
        # return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryApprove_Probation_Info', methods=['POST'])
@connect_sql()
def QryApprove_Probation_Info(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        if 'tier_approve' in data_new:
            sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
            cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],data_new['tier_approve']))
        else:
            sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
            cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro'],data_new['version']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/AddApprove_probation', methods=['POST'])
@connect_sql()
def AddApprove_probation(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        # print 'AddApprove_probation',data_new

        try:
            sql_check_empro = "SELECT * FROM `assessor_pro` WHERE employeeid = %s"
            cursor.execute(sql_check_empro,(data_new['employeeid_pro']))
            columns = [column[0] for column in cursor.description]
            result_assessor_pro = toJson(cursor.fetchall(),columns)
            type_check = result_assessor_pro[0]
            if(type_check['tier_approve'] != data_new['tier_approve']):
                return "employeeid_pro duplicate"
        except Exception as e:
            pass

        try:
            sql_check_empro = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
            cursor.execute(sql_check_empro,(data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],data_new['tier_approve']))
            columns = [column[0] for column in cursor.description]
            result_check_empro = toJson(cursor.fetchall(),columns)
            type_check = result_check_empro[0]['employeeid_pro']
            return "employeeid_pro duplicate"
        except Exception as e:
            pass

        sqlApprove = "INSERT INTO approve_probation(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlApprove,(data_new['version'],data_new['employeeid'],data_new['employeeid_pro'],data_new['name'],data_new['lastname'],data_new['tier_approve'],data_new['position_detail'],data_new['createby']))

        type_action = "ADD"

        sqlApprove = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlApprove,(data_new['version'],data_new['employeeid'],data_new['employeeid_pro'],data_new['name'],data_new['lastname'],data_new['tier_approve'],data_new['position_detail'],data_new['createby'],type_action))

        try:
            sql44 = "SELECT name_asp FROM assessor_pro WHERE companyid=%s AND tier_approve=%s AND employeeid=%s"
            cursor.execute(sql44,(data_new['companyid'],data_new['tier_approve'],data_new['employeeid_pro']))
            columns = [column[0] for column in cursor.description]
            result_test = toJson(cursor.fetchall(),columns)
            name_test = result_test[0]['name_asp']
        except Exception as e:
            sqlQry = "SELECT assessor_pro_id FROM assessor_pro ORDER BY assessor_pro_id DESC LIMIT 1"
            cursor.execute(sqlQry)
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            if(len(result)<1):
                assessor_pro_id_last = 1
            else:
                assessor_pro_id_last=result[0]['assessor_pro_id']+1
            print 'idassessor_pro',assessor_pro_id_last

            sql = "INSERT INTO assessor_pro (assessor_pro_id,employeeid,companyid,name_asp,surname_asp,position_id,tier_approve,email_asp,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,(assessor_pro_id_last,data_new['employeeid_pro'],data_new['companyid'],data_new['name'],data_new['lastname'],data_new['position_id'],data_new['tier_approve'],data_new['email_asp'],data_new['createby']))

            type_action = "ADD"

            sql_log = "INSERT INTO assessor_pro_log (assessor_pro_id,employeeid,companyid,name_asp,surname_asp,position_id,tier_approve,email_asp,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql_log,(assessor_pro_id_last,data_new['employeeid_pro'],data_new['companyid'],data_new['name'],data_new['lastname'],data_new['position_id'],data_new['tier_approve'],data_new['email_asp'],data_new['createby'],type_action))

        return "Success"
    except Exception as e:
            logserver(e)
            return "fail"
@app.route('/AddApprove_probation_many', methods=['POST'])
@connect_sql()
def AddApprove_probation_many(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        i=0
        for i in xrange(len(data_new['em_pro'])):
            sqlApprove = "INSERT INTO approve_probation(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlApprove,(data_new['version'],data_new['employeeid'],data_new['em_pro'][i]['employeeid_pro'],data_new['em_pro'][i]['name'],data_new['em_pro'][i]['lastname'],data_new['em_pro'][i]['tier_approve'],data_new['em_pro'][i]['position_detail'],data_new['createby']))

            type_action = "ADD"

            sqlApprove = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlApprove,(data_new['version'],data_new['employeeid'],data_new['em_pro'][i]['employeeid_pro'],data_new['em_pro'][i]['name'],data_new['em_pro'][i]['lastname'],data_new['em_pro'][i]['tier_approve'],data_new['em_pro'][i]['position_detail'],data_new['createby'],type_action))

            try:
                sql44 = "SELECT name_asp FROM assessor_pro WHERE companyid=%s AND tier_approve=%s AND employeeid=%s"
                cursor.execute(sql44,(data_new['em_pro'][i]['companyid'],data_new['em_pro'][i]['tier_approve'],data_new['em_pro'][i]['employeeid_pro']))
                columns = [column[0] for column in cursor.description]
                result_test = toJson(cursor.fetchall(),columns)
                name_test = result_test[0]['name_asp']
            except Exception as e:

                sqlQry = "SELECT assessor_pro_id FROM assessor_pro ORDER BY assessor_pro_id DESC LIMIT 1"
                cursor.execute(sqlQry)
                columns = [column[0] for column in cursor.description]
                result = toJson(cursor.fetchall(),columns)
                assessor_pro_id_last=result[0]['assessor_pro_id']+1

                sql = "INSERT INTO assessor_pro (assessor_pro_id,employeeid,companyid,name_asp,surname_asp,position_id,tier_approve,email_asp,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql,(assessor_pro_id_last,data_new['em_pro'][i]['employeeid_pro'],data_new['em_pro'][i]['companyid'],data_new['em_pro'][i]['name'],data_new['em_pro'][i]['lastname'],data_new['em_pro'][i]['position_id'],data_new['em_pro'][i]['tier_approve'],data_new['em_pro'][i]['Email_Employee'],data_new['createby']))

                type_action = "ADD"

                sql_log = "INSERT INTO assessor_pro_log (assessor_pro_id,employeeid,companyid,name_asp,surname_asp,position_id,tier_approve,email_asp,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql_log,(assessor_pro_id_last,data_new['em_pro'][i]['employeeid_pro'],data_new['em_pro'][i]['companyid'],data_new['em_pro'][i]['name'],data_new['em_pro'][i]['lastname'],data_new['em_pro'][i]['position_id'],data_new['em_pro'][i]['tier_approve'],data_new['em_pro'][i]['Email_Employee'],data_new['createby'],type_action))

        return "Success"
    except Exception as e:
            logserver(e)
            return "fail"
@app.route('/DeleteApprove_probation', methods=['POST'])
@connect_sql()
def DeleteApprove_probation(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        try:
            sqlcheck_ans = "SELECT name FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND date_status IS NULL"
            cursor.execute(sqlcheck_ans,(data_new['employeeid'],data_new['employeeid_pro'],data_new['version']))
            columns = [column[0] for column in cursor.description]
            result_check_ans = toJson(cursor.fetchall(),columns)
            result_chs = result_check_ans[0]['name']
        except Exception as e:
            return "Not remove"

        sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
        cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro'],data_new['version']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Delete"

        sqlApprove = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlApprove,(data_new['version'],data_new['employeeid'],data_new['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],result[0]['status_'],data_new['createby'],type_action))

        sqlDe = "DELETE FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s AND tier_approve=%s"
        cursor.execute(sqlDe,(data_new['employeeid'],data_new['employeeid_pro'],data_new['version'],result[0]['tier_approve']))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryEm_oneperson', methods=['POST'])
@connect_sql()
def QryEm_oneperson(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sqlEmployee = "SELECT employee.employeeid,employee.citizenid,employee.name_th,employee.surname_th,employee.email,employee.phone_company,employee.position_id,employee.company_id,employee.salary,employee.section_id,employee.org_name_id,employee.cost_center_name_id,employee.start_work,position.position_detail,section.sect_detail,org_name.org_name_detail,cost_center_name.cost_detail,company.companyname FROM employee LEFT JOIN company ON company.companyid = employee.company_id\
                                      LEFT JOIN position ON position.position_id = employee.position_id\
                                      LEFT JOIN section ON section.sect_id = employee.section_id\
                                      LEFT JOIN org_name ON org_name.org_name_id = employee.org_name_id\
                                      LEFT JOIN cost_center_name ON cost_center_name.cost_center_name_id = employee.cost_center_name_id\
        WHERE employee.employeeid=%s"
        cursor.execute(sqlEmployee,data_new['employeeid'])
        columnsEmployee = [column[0] for column in cursor.description]
        resultEmployee = toJson(cursor.fetchall(),columnsEmployee)
        return jsonify(resultEmployee)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryEmployee_probation', methods=['POST'])
def QryEmployee_probation():
    try:
        status_id = ""
        try:
            dataInput = request.json
            source = dataInput['source']
            data_new = source
            and_ = ""
            if data_new['status_id'] == "all":
                status_id = 'WHERE'
            else:
                and_ = " AND"
                status_id = 'WHERE validstatus='+'"'+str(data_new['status_id'])+'"'
            if 'pro_status' in data_new:
                if data_new['pro_status'] == "NULL":
                    status_id = status_id + and_ + " status_result IS NULL"
                elif data_new['pro_status'] == "ทั้งหมด":
                    pass
                else:
                    status_id = status_id + and_ + " status_result = '" + data_new['pro_status'] + "'"
        except Exception as e:
            pass
        connection = mysql.connect()
        cursor = connection.cursor()
        sql = """SELECT Emp_probation.version,Emp_probation.name_th,Emp_probation.employeeid,Emp_probation.surname_th,Emp_probation.status_result,Emp_probation.type_question,Emp_probation.citizenid,Emp_probation.start_work,Emp_probation.EndWork_probation,Emp_probation.validstatus,company.company_short_name,position.position_detail,section.sect_detail,org_name.org_name_detail,cost_center_name.cost_detail,status.status_detail,status.path_color,status.font_color,Emp_probation.status_result
        FROM Emp_probation
        LEFT JOIN company ON company.companyid = Emp_probation.company_id
        LEFT JOIN position ON position.position_id = Emp_probation.position_id
        LEFT JOIN section ON section.sect_id = Emp_probation.section_id
        LEFT JOIN org_name ON org_name.org_name_id = Emp_probation.org_name_id
        LEFT JOIN cost_center_name ON cost_center_name.cost_center_name_id = Emp_probation.cost_center_name_id
        LEFT JOIN status ON status.status_id = Emp_probation.validstatus """ + status_id + " "
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        for item in result:
            long_date = []
            date1 = item['EndWork_probation']
            star_date = date1.split("-")
            Day_s = int(star_date[0])
            Mon_s = int(star_date[1])
            year_s = int(star_date[2])
            d0 = date(year_s,Mon_s,Day_s)
            today = str(date.today())
            today = today.split("-")
            Day_s = int(star_date[0])
            Day_now = int(today[2])
            Mon_now = int(today[1])
            year_now = int(today[0])
            d1 = date(year_now,Mon_now,Day_now)
            delta = d0 - d1
            str_date = str(delta)
            split_str = str_date.split(",")
            last = split_str[0]
            if last=="0:00:00":
                last = "0 days"
            item['long_date'] = last
        connection.close()
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"

@app.route('/delete_comment_transfer', methods=['POST'])
@connect_sql()
def deleteCommentTransfer(cursor):
    data = request.json
    data = data['source']
    try:
        sql = "UPDATE approve_probation SET status_ = 1 WHERE employeeid=%s AND employeeid_pro=%s AND version = %s AND tier_approve=%s"
        cursor.execute(sql, (data['employeeid'],data['employeeid_pro'],data['version'],data['tier_approve']))
        return "success"
    except Exception as e:
        return "fail"

@app.route('/QryEmp_pro_leader', methods=['POST'])
def QryEmp_pro_leader():
    try:
        status_id = ""
        try:
            dataInput = request.json
            source = dataInput['source']
            data_new = source
            if data_new['tier_approve'] == 'L1':
                status_id = 'validstatus IN (2,6,11) AND b.status_ != 14'
            elif data_new['tier_approve'] == 'L2':
                status_id = 'validstatus IN (3,7)'
            elif data_new['tier_approve'] == 'L3':
                status_id = 'validstatus IN (4,8)'
            else:
                status_id = 'validstatus = 5'
        except Exception as e:
            pass
        connection = mysql.connect()
        cursor = connection.cursor()
        sql = """
        SELECT Emp_probation.version,Emp_probation.name_th,Emp_probation.employeeid,Emp_probation.surname_th,Emp_probation.status_result,
        Emp_probation.type_question,Emp_probation.citizenid,Emp_probation.start_work,Emp_probation.EndWork_probation,
        company.company_short_name,position.position_detail,section.sect_detail,org_name.org_name_detail,cost_center_name.cost_detail,
        status.status_detail,status.path_color,status.font_color,b.tier_approve,question_pro_type.question_pro_detail_type,
        (SELECT COUNT(*) FROM approve_probation AS a WHERE a.employeeid = b.employeeid AND comment='Transfer' AND status_ = 14 AND a.version = b.version) AS transfer_approve,
        (SELECT COUNT(*) FROM approve_probation AS a WHERE a.employeeid = b.employeeid AND comment='Transfer' AND a.version = b.version) AS total_transfer,
        b.comment, Emp_probation.status_result
        FROM Emp_probation LEFT JOIN company ON company.companyid = Emp_probation.company_id
                                      LEFT JOIN position ON position.position_id = Emp_probation.position_id
                                      LEFT JOIN section ON section.sect_id = Emp_probation.section_id
                                      LEFT JOIN org_name ON org_name.org_name_id = Emp_probation.org_name_id
                                      LEFT JOIN cost_center_name ON cost_center_name.cost_center_name_id = Emp_probation.cost_center_name_id
                                      LEFT JOIN approve_probation AS b ON b.employeeid = Emp_probation.employeeid AND b.version = Emp_probation.version
                                      LEFT JOIN question_pro_type ON question_pro_type.question_pro_id_type = Emp_probation.type_question
                                      LEFT JOIN status ON status.status_id = Emp_probation.validstatus WHERE employeeid_pro=%s AND """ + status_id + " AND tier_approve = %s"
        cursor.execute(sql,(data_new['employeeid_pro'],data_new['tier_approve']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        for item in result:
            long_date = []
            date1 = item['EndWork_probation']
            star_date = date1.split("-")
            Day_s = int(star_date[0])
            Mon_s = int(star_date[1])
            year_s = int(star_date[2])
            d0 = date(year_s,Mon_s,Day_s)
            today = str(date.today())
            today = today.split("-")
            Day_s = int(star_date[0])
            Day_now = int(today[2])
            Mon_now = int(today[1])
            year_now = int(today[0])
            d1 = date(year_now,Mon_now,Day_now)
            delta = d0 - d1
            str_date = str(delta)
            split_str = str_date.split(",")
            last = split_str[0]
            item['long_date'] = last
        connection.close()
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryEmpPro_l2_l4', methods=['POST'])
def QryEmpPro_l2_l4():
    try:

        dataInput = request.json
        source = dataInput['source']
        data_new = source

        connection = mysql.connect()
        cursor = connection.cursor()
        sql = "SELECT Emp_probation.version,Emp_probation.name_th,Emp_probation.employeeid,Emp_probation.surname_th,Emp_probation.type_question,Emp_probation.citizenid,Emp_probation.start_work,Emp_probation.EndWork_probation,company.company_short_name,position.position_detail,section.sect_detail,org_name.org_name_detail,cost_center_name.cost_detail,status.status_detail,status.path_color,status.font_color,approve_probation.tier_approve,question_pro_type.question_pro_detail_type FROM Emp_probation LEFT JOIN company ON company.companyid = Emp_probation.company_id\
                                      LEFT JOIN position ON position.position_id = Emp_probation.position_id\
                                      LEFT JOIN section ON section.sect_id = Emp_probation.section_id\
                                      LEFT JOIN org_name ON org_name.org_name_id = Emp_probation.org_name_id\
                                      LEFT JOIN cost_center_name ON cost_center_name.cost_center_name_id = Emp_probation.cost_center_name_id\
                                      LEFT JOIN approve_probation ON approve_probation.employeeid = Emp_probation.employeeid\
                                      LEFT JOIN question_pro_type ON question_pro_type.question_pro_id_type = Emp_probation.type_question\
                                      LEFT JOIN status ON status.status_id = Emp_probation.validstatus WHERE employeeid_pro=%s AND Emp_probation.status_result IS NOT NULL "
        cursor.execute(sql,data_new['employeeid_pro'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        for item in result:
            long_date = []
            date1 = item['EndWork_probation']
            star_date = date1.split("-")
            Day_s = int(star_date[0])
            Mon_s = int(star_date[1])
            year_s = int(star_date[2])
            d0 = date(year_s,Mon_s,Day_s)
            today = str(date.today())
            today = today.split("-")
            Day_s = int(star_date[0])
            Day_now = int(today[2])
            Mon_now = int(today[1])
            year_now = int(today[0])
            d1 = date(year_now,Mon_now,Day_now)
            delta = d0 - d1
            str_date = str(delta)
            split_str = str_date.split(",")
            last = split_str[0]
            item['long_date'] = last
        connection.close()
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Insert_ans_pro', methods=['POST'])
@connect_sql()
def Insert_ans_pro(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        employeeid = data_new['employeeid']
        sql = "SELECT citizenid FROM Emp_probation WHERE employeeid=%s AND version=%s"
        cursor.execute(sql,(employeeid,data_new['version']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "ADD"

        try:
            sqlUp_de = "DELETE FROM employee_pro WHERE version=%s AND employeeid=%s AND citizenid=%s AND createby=%s"
            cursor.execute(sqlUp_de,(data_new['version'],employeeid,result[0]['citizenid'],data_new['createby']))
        except Exception as e:
            pass

        i=0
        for i in xrange(len(data_new['answer_pro'])):
            sqlIn_be = "INSERT INTO employee_pro(version,employeeid,citizenid,question_pro_id,pro_values,type_check,group_q,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_be,(data_new['version'],employeeid,result[0]['citizenid'],data_new['answer_pro'][i]['question_pro_id'],data_new['answer_pro'][i]['pro_values'],data_new['answer_pro'][i]['type_check'],data_new['answer_pro'][i]['group_q'],data_new['createby']))

        i=0
        for i in xrange(len(data_new['answer_pro'])):
            sqlIn_be_log = "INSERT INTO employee_pro_log(version,employeeid,citizenid,question_pro_id,pro_values,type_check,group_q,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_be_log,(data_new['version'],employeeid,result[0]['citizenid'],data_new['answer_pro'][i]['question_pro_id'],data_new['answer_pro'][i]['pro_values'],data_new['answer_pro'][i]['type_check'],data_new['answer_pro'][i]['group_q'],data_new['createby'],type_action))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Edit_ans_pro', methods=['POST'])
@connect_sql()
def Edit_ans_pro(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT citizenid,question_pro_id,pro_values,type_check,group_q FROM employee_pro WHERE employeeid=%s AND question_pro_id=%s AND version=%s AND createby=%s"
        cursor.execute(sql,(data_new['employeeid'],data_new['question_pro_id'],data_new['version'],data_new['createby']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Edit"

        sqlIn = "INSERT INTO employee_pro_log (version,employeeid,citizenid,question_pro_id,pro_values,type_check,group_q,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn,(data_new['version'],data_new['employeeid'],result[0]['citizenid'],result[0]['question_pro_id'],result[0]['pro_values'],result[0]['type_check'],result[0]['group_q'],data_new['createby'],type_action))

        sqlde = "DELETE FROM employee_pro WHERE employeeid=%s AND question_pro_id=% AND version=%s AND createby=%s"
        cursor.execute(sqlde,(data_new['employeeid'],data_new['question_pro_id'],data_new['version'],data_new['createby']))

        sqlIn = "INSERT INTO employee_pro(version,employeeid,citizenid,question_pro_id,pro_values,type_check,group_q,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn,(data_new['version'],data_new['employeeid'],data_new['citizenid'],data_new['question_pro_id'],data_new['pro_values'],data_new['type_check'],data_new['group_q'],data_new['createby']))
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qry_probation', methods=['POST'])
@connect_sql()
def Qry_probation(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        createby_id = ""
        try:
            createby_id = 'AND createby=' + '"' + str(data_new['createby_id']) + '"'
        except Exception as e:
            pass
        sql = "SELECT Emp_probation.version,Emp_probation.name_th,Emp_probation.employeeid,Emp_probation.surname_th,Emp_probation.type_question,Emp_probation.citizenid,Emp_probation.start_work,Emp_probation.EndWork_probation,Emp_probation.validstatus,position.position_detail,section.sect_detail,org_name.org_name_detail,cost_center_name.cost_detail,company.imageName FROM Emp_probation LEFT JOIN position ON position.position_id = Emp_probation.position_id\
                                      LEFT JOIN section ON section.sect_id = Emp_probation.section_id\
                                      LEFT JOIN org_name ON org_name.org_name_id = Emp_probation.org_name_id\
                                      LEFT JOIN cost_center_name ON cost_center_name.cost_center_name_id = Emp_probation.cost_center_name_id\
                                      LEFT JOIN company ON company.companyid = Emp_probation.company_id\
        WHERE Emp_probation.employeeid=%s AND version=%s"
        cursor.execute(sql,(data_new['employeeid'],data_new['version']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        for item in result:
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
            item['start_work']= str(Day_s)+" "+Mounth_name_str+" "+yer_last_str
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
            item['EndWork_probation']= str(int_day_e)+" "+Mounth_name_end+" "+yer_last_end
            d0 = date(year_s,Mon_s,Day_s)
            d1 = date(int_year_e,int_mon_e,int_day_e)
            delta = d1 - d0
            str_date = str(delta)
            split_str = str_date.split(",")
            last = split_str[0].split(" ")
            item['long_date_pro'] = str(int(last[0])+1)

            employeeid_ = data_new['employeeid']
            version_id = data_new['version']
            question = []
            sql1pro = "SELECT question_pro_id,pro_values,type_check,group_q FROM employee_pro WHERE employeeid=%s AND version=%s " + createby_id + " ORDER BY question_pro_id ASC"
            cursor.execute(sql1pro,(employeeid_,version_id))
            # print(sql1pro)
            columns = [column[0] for column in cursor.description]
            data2 = toJson(cursor.fetchall(),columns)
            for i2 in data2 :
                question.append(i2)
            item['question'] = question
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qry_probation_active', methods=['POST'])
@connect_sql()
def Qry_probation_active(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        # createby_id = ""
        # try:
        #     createby_id = 'AND createby='+'"'+str(data_new['createby_id'])+'"'
        # except Exception as e:
        #     pass
        sql = "SELECT Emp_probation.version,Emp_probation.name_th,Emp_probation.employeeid,Emp_probation.surname_th,Emp_probation.type_question,Emp_probation.citizenid,Emp_probation.start_work,Emp_probation.EndWork_probation,Emp_probation.validstatus,position.position_detail,section.sect_detail,org_name.org_name_detail,cost_center_name.cost_detail,company.imageName FROM Emp_probation LEFT JOIN position ON position.position_id = Emp_probation.position_id\
                                      LEFT JOIN section ON section.sect_id = Emp_probation.section_id\
                                      LEFT JOIN org_name ON org_name.org_name_id = Emp_probation.org_name_id\
                                      LEFT JOIN cost_center_name ON cost_center_name.cost_center_name_id = Emp_probation.cost_center_name_id\
                                      LEFT JOIN company ON company.companyid = Emp_probation.company_id\
        WHERE Emp_probation.employeeid=%s AND version=%s"
        cursor.execute(sql,(data_new['employeeid'],data_new['version']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        for item in result:
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
            item['start_work']= str(Day_s)+" "+Mounth_name_str+" "+yer_last_str
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
            item['EndWork_probation']= str(int_day_e)+" "+Mounth_name_end+" "+yer_last_end
            d0 = date(year_s,Mon_s,Day_s)
            d1 = date(int_year_e,int_mon_e,int_day_e)
            delta = d1 - d0
            str_date = str(delta)
            split_str = str_date.split(",")
            last = split_str[0].split(" ")
            item['long_date_pro'] = str(int(last[0])+1)

            employeeid_ = data_new['employeeid']
            version_id = data_new['version']
            question = []
            # sql1pro = "SELECT question_pro_id,pro_values,type_check,group_q FROM employee_pro WHERE employeeid={} AND validstatus=1 AND version={} ORDER BY question_pro_id ASC".format(employeeid_,version_id)
            sql1pro = """SELECT employee_pro.question_pro_id, employee_pro.pro_values, employee_pro.type_check,employee_pro.createby, employee_pro.group_q, question_pro_form.question_pro_detail FROM employee_pro \
                        INNER JOIN question_pro_form ON employee_pro.question_pro_id = question_pro_form.question_pro_id \
                        WHERE employee_pro.employeeid=%s AND employee_pro.validstatus=1 AND employee_pro.version=%s ORDER BY employee_pro.question_pro_id ASC"""
            cursor.execute(sql1pro,(employeeid_,version_id))
            # print(sql1pro)
            columns = [column[0] for column in cursor.description]
            data2 = toJson(cursor.fetchall(),columns)
            for i3 in data2:
                question.append(i3)
            item['question'] = question
            for i1 in data2:
                comment_title = []
                sql1 = """  SELECT *
                            FROM approve_probation
                            WHERE employeeid_pro=%s AND employeeid=%s AND version=%s"""
                cursor.execute(sql1,(i1['createby'],data_new['employeeid'],data_new['version']))
                columns = [column[0] for column in cursor.description]
                data4 = toJson(cursor.fetchall(),columns)
                for i2 in data4 :
                    comment_title.append(i2)
                item['comment_title'] = comment_title
            sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND version=%s"
            cursor.execute(sql, (employeeid_, version_id))
            comments = toJson(cursor.fetchall(), [column[0] for column in cursor.description])
            item['all_assessor'] = comments
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Update_probation_deactive', methods=['POST'])
@connect_sql()
def Update_probation_deactive(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        result_token = CheckTokenAdmin(data_new['createby'],data_new['token'])
        if result_token!='pass':
            return 'token fail'
        i=0
        for i in xrange(len(data_new['employeeid_pro'])):
            sqlde = "UPDATE employee_pro SET validstatus=0 WHERE createby=%s AND version=%s"
            cursor.execute(sqlde,(data_new['employeeid_pro'][i]['createby'],data_new['employeeid_pro'][i]['version']))
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Update_probation_active', methods=['POST'])
@connect_sql()
def Update_probation_active(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        result_token = CheckTokenAdmin(data_new['createby'],data_new['token'])
        if result_token!='pass':
            return 'token fail'
        i=0
        for i in xrange(len(data_new['employeeid_pro'])):
            sqlde = "UPDATE employee_pro SET validstatus=1 WHERE createby=%s AND version=%s"
            cursor.execute(sqlde,(data_new['employeeid_pro'][i]['createby'],data_new['employeeid_pro'][i]['version']))
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/upload_user', methods=['POST'])
@connect_sql()
def upload_user(cursor):
    try:
        sqlqry = "SELECT citizenid FROM employee WHERE employeeid=%s"
        cursor.execute(sqlqry,request.form['employeeid'])
        columns = [column[0] for column in cursor.description]
        resultsqlqry = toJson(cursor.fetchall(),columns)
        ID_CardNo = resultsqlqry[0]['citizenid']

        try:
            sqlDe = "DELETE FROM employee_upload WHERE ID_CardNo=%s AND version=%s"
            cursor.execute(sqlDe,(ID_CardNo,request.form['version']))
        except Exception as e:
            pass

        Type = 'probation'
        employeeid = request.form['employeeid']
        version = request.form['version']
        # path = 'uploads/'+employeeid+'/'+'probation'
        path = '../uploads/'+employeeid+'/'+'probation'+'/'+str(request.form['version'])
        if not os.path.exists(path):
            os.makedirs(path)
        file = request.files.getlist('file')
        for idx, fileList in enumerate(file):
            fileName = fileList.filename
            fileType = fileName.split('.')[-1]
            fileList.filename = 'Probation' + '' + '' + str(idx + 1) + '.' + fileType
            try:
                os.remove(os.path.join(path, fileList.filename))
            except OSError:
                pass
            if file and allowed_file(fileList.filename):
                fileList.save(os.path.join(path, fileList.filename))
                PathFile = employeeid+'/'+'probation'+'/'+str(request.form['version'])+'/'+str(fileList.filename)
                sql = "INSERT INTO employee_upload (version,ID_CardNo,FileName,Type,PathFile,createby) VALUES (%s,%s,%s,%s,%s,%s)"
                # cursor.execute(sql,(ID_CardNo,Type,PathFile,request.form['createby']))
                cursor.execute(sql,(version,ID_CardNo,fileName,Type,PathFile,request.form['createby']))
            else:
                return "file is not allowed"
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qry_upload_file', methods=['POST'])
@connect_sql()
def Qry_upload_file(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sqlqry = "SELECT citizenid FROM employee WHERE employeeid=%s"
        cursor.execute(sqlqry,(data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        resultsqlqry = toJson(cursor.fetchall(),columns)
        ID_CardNo = resultsqlqry[0]['citizenid']

        sql = "SELECT ID_CardNo,FileName,Type,PathFile FROM employee_upload WHERE ID_CardNo=%s AND createby=%s AND version=%s"
        cursor.execute(sql,(ID_CardNo,data_new['employeeid_pro'],data_new['version']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        for item_ in result:
            img_base64 = []
            # item_['PathFile'] = '../app/uploads/'+str(item_['PathFile'])
            item_['PathFile'] = '../uploads/'+str(item_['PathFile'])
            tranImage = item_['PathFile']
            with open(tranImage, 'rb') as image_file:
                encoded_Image = base64.b64encode(image_file.read())
            item_['img_base64'] = encoded_Image
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/sendEmail', methods = ['GET'])
@connect_sql()
def send_email(cursor):
    # sql_picture = "SELECT mail_type,imageName FROM mail_pic WHERE mail_type='probation_mail'"
    # cursor.execute(sql_picture)
    # columns = [column[0] for column in cursor.description]
    # result_picture = toJson(cursor.fetchall(),columns)

    # sql_L1 = "SELECT employeeid,email_asp,tier_approve FROM assessor_pro WHERE tier_approve='L1' GROUP BY email_asp "
    # cursor.execute(sql_L1)
    # columns = [column[0] for column in cursor.description]
    # result = toJson(cursor.fetchall(),columns)
    # for i1 in result:
    #     total_em = []
    #     sql1_total = "SELECT COUNT(approve_probation.employeeid) AS total_em FROM approve_probation LEFT JOIN assessor_pro ON approve_probation.employeeid_pro = assessor_pro.employeeid\
    #                                                                                                 LEFT JOIN Emp_probation ON approve_probation.employeeid = Emp_probation.employeeid\
    #                    WHERE approve_probation.employeeid_pro = %s AND Emp_probation.validstatus IN(2,6)"
    #     cursor.execute(sql1_total,(i1['employeeid']))
    #     columns = [column[0] for column in cursor.description]
    #     data1 = toJson(cursor.fetchall(),columns)
    #     i1['total_em'] = str(data1[0]['total_em'])
    # for item in result:
    #     count = int(item['total_em'])
    #     if count>0:
    #         print 'count',count
    #         sendToMail(item['email_asp'], item['total_em'],result_picture[0]['imageName'])
    # sql_L2 = "SELECT employeeid,email_asp,tier_approve FROM assessor_pro WHERE tier_approve='L2' GROUP BY email_asp "
    # cursor.execute(sql_L2)
    # columns = [column[0] for column in cursor.description]
    # result2 = toJson(cursor.fetchall(),columns)
    # for i2 in result2:
    #     total_em2 = []
    #     sql1_total2 = "SELECT COUNT(approve_probation.employeeid) AS total_em FROM approve_probation LEFT JOIN assessor_pro ON approve_probation.employeeid_pro = assessor_pro.employeeid\
    #                                                                                                 LEFT JOIN Emp_probation ON approve_probation.employeeid = Emp_probation.employeeid\
    #                    WHERE approve_probation.employeeid_pro = %s AND Emp_probation.validstatus IN(3,7,8)"
    #     cursor.execute(sql1_total2,(i2['employeeid']))
    #     columns = [column[0] for column in cursor.description]
    #     data2 = toJson(cursor.fetchall(),columns)
    #     i2['total_em'] = str(data2[0]['total_em'])
    # for item2 in result2:
    #     count2 = int(item2['total_em'])
    #     if count2>0:
    #         sendToMail(item2['email_asp'], item2['total_em'],result_picture[0]['imageName'])
    # sql_L3 = "SELECT employeeid,email_asp,tier_approve FROM assessor_pro WHERE tier_approve='L3' GROUP BY email_asp "
    # cursor.execute(sql_L3)
    # columns = [column[0] for column in cursor.description]
    # result3 = toJson(cursor.fetchall(),columns)
    # for i3 in result3:
    #     total_em3 = []
    #     sql1_total3 = "SELECT COUNT(approve_probation.employeeid) AS total_em FROM approve_probation LEFT JOIN assessor_pro ON approve_probation.employeeid_pro = assessor_pro.employeeid\
    #                                                                                                 LEFT JOIN Emp_probation ON approve_probation.employeeid = Emp_probation.employeeid\
    #                    WHERE approve_probation.employeeid_pro = %s AND Emp_probation.validstatus IN(4,8)"
    #     cursor.execute(sql1_total3,(i3['employeeid']))
    #     columns = [column[0] for column in cursor.description]
    #     data3 = toJson(cursor.fetchall(),columns)
    #     i3['total_em'] = str(data3[0]['total_em'])
    # for item3 in result3:
    #     count3 = int(item3['total_em'])
    #     if count3>0:
    #         sendToMail(item3['email_asp'], item3['total_em'],result_picture[0]['imageName'])
    # sql_L4 = "SELECT employeeid,email_asp,tier_approve FROM assessor_pro WHERE tier_approve='L4' GROUP BY email_asp "
    # cursor.execute(sql_L4)
    # columns = [column[0] for column in cursor.description]
    # result4 = toJson(cursor.fetchall(),columns)
    # for i4 in result4:
    #     total_em4 = []
    #     sql1_total4 = "SELECT COUNT(approve_probation.employeeid) AS total_em FROM approve_probation LEFT JOIN assessor_pro ON approve_probation.employeeid_pro = assessor_pro.employeeid\
    #                                                                                                 LEFT JOIN Emp_probation ON approve_probation.employeeid = Emp_probation.employeeid\
    #                    WHERE approve_probation.employeeid_pro = %s AND Emp_probation.validstatus IN(5)"
    #     cursor.execute(sql1_total4,(i4['employeeid']))
    #     columns = [column[0] for column in cursor.description]
    #     data4 = toJson(cursor.fetchall(),columns)
    #     i4['total_em'] = str(data4[0]['total_em'])
    # for item4 in result4:
    #     count4 = int(item4['total_em'])
    #     if count4>0:
    #         sendToMail(item4['email_asp'], item4['total_em'],result_picture[0]['imageName'])

    # ## SEND MAIL EMP_PROBATION
    # sql_prob = """SELECT  Emp_probation.version,Emp_probation.employeeid,Emp_probation.citizenid,Emp_probation.email,Emp_probation.name_th,Emp_probation.surname_th,Emp_probation.name_eng,Emp_probation.surname_eng,Emp_probation.email_status,
    #                 Emp_probation.status_result,org_name.org_name_detail,position.position_detail FROM `Emp_probation`
    #                 LEFT JOIN position ON Emp_probation.position_id = position.position_id
    #                 LEFT JOIN org_name ON Emp_probation.org_name_id = org_name.org_name_id
    #                 WHERE `validstatus` = 10"""
    # cursor.execute(sql_prob)
    # columns = [column[0] for column in cursor.description]
    # result5 = toJson(cursor.fetchall(),columns)
    # for prob in result5:
    #     # print 'mail_status',prob['email_status']
    #     if prob['email_status'] != 1:
    #         print str(prob['status_result'])
    #         if str(prob['status_result']) == 'ผ่านทดลองงาน':
    #             sql_relocate =  """SELECT * FROM `Emp_probation_log`
    #                                 WHERE employeeid = %s AND version = %s AND type_action = 'relocate_pass'"""
    #             cursor.execute(sql_relocate,(prob['employeeid'],prob['version']))
    #             columns = [column[0] for column in cursor.description]
    #             result_relocate = toJson(cursor.fetchall(),columns)
    #             if(len(result_relocate)>0):
    #                 sql_old_relocate =  """SELECT org_name.org_name_detail,position.position_detail FROM `Emp_probation_log`
    #                                 LEFT JOIN position ON Emp_probation_log.position_id = position.position_id
    #                                 LEFT JOIN org_name ON Emp_probation_log.org_name_id = org_name.org_name_id
    #                                 WHERE Emp_probation_log.create_at<(SELECT MAX(Emp_probation_log.create_at) FROM Emp_probation_log) AND
    #                                 employeeid = %s AND version = %s ORDER BY Emp_probation_log.create_at DESC"""
    #                 cursor.execute(sql_old_relocate,(prob['employeeid'],prob['version']))
    #                 columns = [column[0] for column in cursor.description]
    #                 result_old = toJson(cursor.fetchall(),columns)
    #                 isRelocate = sendpass_relocate(prob['version'],prob['email'],prob['name_th'],prob['surname_th'],prob['position_detail'],prob['org_name_detail'],'Hr Management <recruitment@inet.co.th>',result_picture[0]['imageName'],result_old[0])
    #                 sql_update_email_status = """UPDATE Emp_probation SET email_status = 1 WHERE employeeid = %s AND version = %s"""
    #                 cursor.execute(sql_update_email_status,(prob['employeeid'],prob['version']))
    #             else:
    #                 isPass = sendpass_probation(prob['email'],prob['name_th'],prob['surname_th'],prob['position_detail'],prob['org_name_detail'],'Hr Management <recruitment@inet.co.th>',result_picture[0]['imageName'])
    #                 # isPass = sendpass_probation(prob['email'],prob['name_th'],prob['surname_th'],prob['position_detail'],prob['org_name_detail'],'Hr Management <recruitment@inet.co.th>',result_picture[0]['imageName'])
    #                 sql_update_email_status = """UPDATE Emp_probation SET email_status = 1 WHERE employeeid = %s AND version = %s"""
    #                 cursor.execute(sql_update_email_status,(prob['employeeid'],prob['version']))
    #         elif str(prob['status_result']) == 'ไม่ผ่านทดลองงาน':
    #             isRejected = sendToMail_reject(prob['version'],prob['employeeid'],prob['citizenid'],prob['email'],prob['name_eng'],prob['surname_eng'],prob['name_th'],prob['surname_th'],prob['position_detail'],prob['org_name_detail'],result_picture[0]['imageName'],str(prob['status_result']))
    #             # isRejected = sendToMail_reject(prob['email'],prob['name_eng'],prob['surname_eng'],prob['name_th'],prob['surname_th'],prob['position_detail'],prob['org_name_detail'],result_picture[0]['imageName'],str(prob['status_result']))
    #             sql_update_email_status = """UPDATE Emp_probation SET email_status = 1 WHERE employeeid = %s AND version = %s"""
    #             cursor.execute(sql_update_email_status,(prob['employeeid'],prob['version']))
    #         elif str(prob['status_result']) == 'ขยายเวลาทดลองงาน':
    #             isExtended = sendextend_probation(prob['version'],prob['employeeid'],prob['citizenid'],prob['email'],prob['name_eng'],prob['surname_eng'],prob['name_th'],prob['surname_th'],prob['position_detail'],prob['org_name_detail'],result_picture[0]['imageName'],str(prob['status_result']))
    #             # isRejected = sendToMail_reject(prob['email'],prob['name_eng'],prob['surname_eng'],prob['name_th'],prob['surname_th'],prob['position_detail'],prob['org_name_detail'],result_picture[0]['imageName'],str(prob['status_result']))
    #             sql_update_email_status = """UPDATE Emp_probation SET email_status = 1 WHERE employeeid = %s AND version = %s"""
    #             cursor.execute(sql_update_email_status,(prob['employeeid'],prob['version']))

    # TODO Send Probation
    try:
        sqlselect_emp_pro_1 = """SELECT * FROM Emp_probation INNER JOIN approve_probation
                                ON (Emp_probation.employeeid = approve_probation.employeeid AND Emp_probation.version = approve_probation.version)
                                WHERE Emp_probation.validstatus = 1"""
        cursor.execute(sqlselect_emp_pro_1)
        columns = [column[0] for column in cursor.description]
        result_emp_pro_1 = toJson(cursor.fetchall(),columns)
        for emp in result_emp_pro_1:
            split_date = emp['start_work'].split('-')
            start_work = datetime(int(split_date[2]),int(split_date[1]),int(split_date[0]))
            sent_pro = (start_work+relativedelta(months=1))+timedelta(days=28)
            print emp['employeeid'].encode('utf-8'),sent_pro ,datetime.now()
            # sql_select = """SELECT * FROM `approve_probation` WHERE `employeeid` = %s AND version = %s"""
            # cursor.execute(sql_select,(emp['employeeid'],emp['version']))
            # columns = [column[0] for column in cursor.description]
            # result = toJson(cursor.fetchall(),columns)
            # if(len(result)>0):
            #     for employ in result:
            #         print employ['employeeid'],employ['employeeid_pro'],emp['version']

        # sqlcheck_L1 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND tier_approve='L1' AND version=%s"
        # cursor.execute(sqlcheck_L1,(data_new['employeeid'],data_new['version']))
        # columns = [column[0] for column in cursor.description]
        # result_check_L1 = toJson(cursor.fetchall(),columns)

        # sqlcheck_L2 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND tier_approve='L2' AND version=%s"
        # cursor.execute(sqlcheck_L2,(data_new['employeeid'],data_new['version']))
        # columns = [column[0] for column in cursor.description]
        # result_check_L2 = toJson(cursor.fetchall(),columns)

        # sqlcheck_L3 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND tier_approve='L3' AND version=%s"
        # cursor.execute(sqlcheck_L3,(data_new['employeeid'],data_new['version']))
        # columns = [column[0] for column in cursor.description]
        # result_check_L3 = toJson(cursor.fetchall(),columns)

        # try:
        #     check_L3 = result_check_L3[0]['employeeid_pro']
        # except Exception as e:
        #     return "No Level L3"

        # sqlcheck_L4 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND tier_approve='L4' AND version=%s"
        # cursor.execute(sqlcheck_L4,(data_new['employeeid'],data_new['version']))
        # columns = [column[0] for column in cursor.description]
        # result_check_L4 = toJson(cursor.fetchall(),columns)

        # if (not result_check_L2)&(not result_check_L1):
        #     sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
        #     cursor.execute(sql,(data_new['employeeid'],result_check_L3[0]['employeeid_pro'],data_new['version']))
        #     columns = [column[0] for column in cursor.description]
        #     result = toJson(cursor.fetchall(),columns)

        #     type_action = "send_pro_no_L2"
        #     status_last = "4"

        #     sqlReject = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        #     cursor.execute(sqlReject,(data_new['version'],result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,result[0]['comment'],result[0]['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

        #     sqlUp = "UPDATE approve_probation SET status_=4,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
        #     cursor.execute(sqlUp,(data_new['date_status'],data_new['employeeid'],result_check_L3[0]['employeeid_pro'],data_new['version']))

        #     sqlUp_main = "UPDATE Emp_probation SET type_question=%s,validstatus=4 WHERE employeeid=%s AND version=%s"
        #     cursor.execute(sqlUp_main,(data_new['type_question'],data_new['employeeid'],data_new['version']))

        # elif (not result_check_L2)&(not result_check_L3)&(not result_check_L1):
        #     sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
        #     cursor.execute(sql,(data_new['employeeid'],result_check_L2[0]['employeeid_pro'],data_new['version']))
        #     columns = [column[0] for column in cursor.description]
        #     result = toJson(cursor.fetchall(),columns)

        #     type_action = "send_pro_no_L2_L3_L1"
        #     status_last = "5"

        #     sqlReject = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        #     cursor.execute(sqlReject,(data_new['version'],result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,result[0]['comment'],result[0]['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

        #     sqlUp = "UPDATE approve_probation SET status_=5,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
        #     cursor.execute(sqlUp,(data_new['date_status'],data_new['employeeid'],result_check_L2[0]['employeeid_pro'],data_new['version']))

        #     sqlUp_main = "UPDATE Emp_probation SET type_question=%s,validstatus=5 WHERE employeeid=%s AND version=%s"
        #     cursor.execute(sqlUp_main,(data_new['type_question'],data_new['employeeid'],data_new['version']))
        # elif not result_check_L1:
        #     sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
        #     cursor.execute(sql,(data_new['employeeid'],result_check_L2[0]['employeeid_pro'],data_new['version']))
        #     columns = [column[0] for column in cursor.description]
        #     result = toJson(cursor.fetchall(),columns)

        #     type_action = "send_pro_no_L1"
        #     status_last = "3"

        #     sqlReject = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        #     cursor.execute(sqlReject,(data_new['version'],result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,result[0]['comment'],result[0]['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

        #     sqlUp = "UPDATE approve_probation SET status_=3,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
        #     cursor.execute(sqlUp,(data_new['date_status'],data_new['employeeid'],result_check_L2[0]['employeeid_pro'],data_new['version']))

        #     sqlUp_main = "UPDATE Emp_probation SET type_question=%s,validstatus=3 WHERE employeeid=%s AND version=%s"
        #     cursor.execute(sqlUp_main,(data_new['type_question'],data_new['employeeid'],data_new['version']))
        # else:
        #     sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
        #     cursor.execute(sql,(data_new['employeeid'],result_check_L1[0]['employeeid_pro'],data_new['version']))
        #     columns = [column[0] for column in cursor.description]
        #     result = toJson(cursor.fetchall(),columns)

        #     type_action = "send_pro"
        #     status_last = "2"

        #     sqlReject = "INSERT INTO approve_probation_log(version,employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        #     cursor.execute(sqlReject,(data_new['version'],result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,result[0]['comment'],result[0]['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

        #     sqlUp = "UPDATE approve_probation SET status_=2,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s AND version=%s"
        #     cursor.execute(sqlUp,(data_new['employeeid'],data_new['date_status'],result_check_L1[0]['employeeid_pro'],data_new['version']))

        #     sqlUp_main = "UPDATE Emp_probation SET type_question=%s,validstatus=2 WHERE employeeid=%s AND version=%s"
        #     cursor.execute(sqlUp_main,(data_new['type_question'],data_new['employeeid'],data_new['version']))
        return "Success"
    except Exception as e:
        print str(e)
        logserver(e)
        return "fail"

    return jsonify('success')
def sendToMail(email, total_em,imageName):
    send_from = "Hr Management <recruitment@inet.co.th>"
    send_to = email
    subject = "แจ้งประเมินทดลองงานของพนักงาน"
    text = """\
                <html>
                  <body>
                    <b style="font-size: 18px;">เรียน  ต้นสังกัดที่เกี่ยวข้อง</b></br>
                    <p style="text-indent: 30px; font-size: 16px; padding: 10px;">
                        ฝ่ายทรัพยากรบุคคลขอแจ้งประเมินทดลองงานของพนักงานที่จะครบทดลองงาน """ + total_em + """ คน รบกวนต้นสังกัดประเมินพนักงานภายในระยะเวลา 15 วัน ก่อนครบทดลองงาน หากล่าช้าจะส่งผลต่อสวัสดิการพนักงาน
                        ผู้ประเมินทุกท่านสามารถเข้าไปทำการประเมินพนักงาน ได้ที่ <a href="http://hr-management.inet.co.th">Hr Management</a>
                    </p>
                    <img style="width: 1024px; height: auto;" src="http://hr-management.inet.co.th:8888/userGetFileImageMail/"""+imageName+"""""></br>
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
    print 'send_to',send_to
    try:
        smtp = smtplib.SMTP(server)
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.close()
        result = {'status' : 'done', 'statusDetail' : 'Send email has done'}
        return jsonify(result)
    except:
        result = {'status' : 'error', 'statusDetail' : 'Send email has error : This system cannot send email'}
        return jsonify(result)

@connect_sql()
def sendToMail_reject(cursor,version,employeeid,citizenid,email,name_eng,surname_eng,em_name,em_surname,em_position,em_org,imageName,comment):
    sql_reject_kpi = """SELECT * FROM `employee_pro` WHERE employeeid = %s AND version = %s AND group_q = 'SectionKPI'"""
    cursor.execute(sql_reject_kpi,(employeeid,version))
    columns = [column[0] for column in cursor.description]
    result_reject = toJson(cursor.fetchall(),columns)
    index = 1
    kpi_html = ""
    for i in result_reject:
        kpi_html = kpi_html+"""<p style="font-size: 16px;">"""+str(index)+') '+i['pro_values']+"""</p>"""
        index = index + 1
    print 'kpi_html',kpi_html

    sql_user_kpi = """SELECT * FROM `employee_upload` WHERE ID_CardNo = %s AND version = %s """
    cursor.execute(sql_user_kpi,(citizenid,version))
    columns = [column[0] for column in cursor.description]
    result_user = toJson(cursor.fetchall(),columns)
    index = 1
    kpi_user = ""
    for i in result_user:
        ### TODO fixed tag a to real host ###
        kpi_user = kpi_user+ """<p style="font-size: 16px;">"""+str(index)+""") <a href="http://localhost:8888/userGetFileProbation/"""+i['PathFile']+"""">"""+i['FileName']+"""</a></p>"""
        print 'pathFile',i['PathFile']
        index = index + 1
    print 'kpi_user',kpi_user

    send_from = "Hr Management <recruitment@inet.co.th>"
    send_to = email
    subject = "ประเมินพนักงานผ่านทดลองงาน (ไม่ผ่านการอนุมัติ)"
    text = """\
                <html>
                  <body>
                    <b style="font-size: 18px;">เรียนคุณ  """ + em_name + """ """ + em_surname + """</b></br>
                     <p style="text-indent: 30px; font-size: 16px; padding: 10px;">
                        เนื่องจากทางต้นสังกัดได้ประเมินผลการปฏิบัติงานของ คุณ""" + em_name + """ """ + em_surname + """ ซึ่งผลการปฏิบัติงานคือ “ไม่ผ่านทดลองงาน” โดยทางต้นสังกัดให้เหตุผลว่า ไม่ผ่าน KPI ค่ะ ซึ่ง KPI ที่ทางต้นสังกัดให้ปฏิบัติมีดังนี้
                    </p>
                    """+kpi_html+"""
                    <p style="font-size: 16px;">และผลงานที่คุณ""" + em_name + """ """ + em_surname +""" สามารถปฏิบัติได้มีดังนี้ </p>
                    """+kpi_user+"""
                    <p style="font-size: 16px;">ทั้งนี้หากมีข้อสงสัยในผลการประเมิน</p>
                    <p style="font-size: 16px;">กรุณาติดต่อทางต้นสังกัดค่ะ</p>
                    <p style="font-size: 16px;">Best Regard</p>
                    <img style="width: 1024px; height: auto;" src="http://hr-management.inet.co.th:8888/userGetFileImageMail/"""+imageName+""""">
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
        # not send email
        smtp = smtplib.SMTP(server)
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.close()
        result = {'status' : 'done', 'statusDetail' : 'Send email has done'}
        return jsonify(result)
    except:
        result = {'status' : 'error', 'statusDetail' : 'Send email has error : This system cannot send email'}
        return jsonify(result)

@connect_sql()
def sendextend_probation(cursor,version,employeeid,citizenid,email,name_eng,surname_eng,em_name,em_surname,em_position,em_org,imageName,comment):
    sql_work_probation = """SELECT * FROM Emp_probation Where employeeid = %s AND version = %s"""
    cursor.execute(sql_work_probation,(employeeid,str(int(version)+1)))
    columns = [column[0] for column in cursor.description]
    result_work = toJson(cursor.fetchall(),columns)

    sql_user_kpi = """SELECT * FROM `employee_upload` WHERE ID_CardNo = %s AND version = %s """
    cursor.execute(sql_user_kpi,(citizenid,version))
    columns = [column[0] for column in cursor.description]
    result_user = toJson(cursor.fetchall(),columns)
    index = 1
    kpi_user = ""
    for i in result_user:
        ### TODO fixed tag a to real host ###
        kpi_user = kpi_user+ """<p style="font-size: 16px;">"""+str(index)+""") <a href="http://localhost:8888/userGetFileProbation/"""+i['PathFile']+"""">"""+i['FileName']+"""</a></p>"""
        print 'pathFile',i['PathFile']
        index = index + 1
    print 'kpi_user',kpi_user

    send_from = "Hr Management <recruitment@inet.co.th>"
    send_to = email
    subject = "ประเมินพนักงานผ่านทดลองงาน (ขยายเวลาทดลองงาน)"
    text = """\
                <html>
                  <body>
                    <b style="font-size: 18px;">เรียนคุณ  """ + em_name + """ """ + em_surname + """</b></br>
                     <p style="text-indent: 30px; font-size: 16px; padding: 10px;">
                        เนื่องจาก คุณ""" + em_name + """ """ + em_surname + """ มีผลการประเมิน “ขยายทดลองงาน” ตั้งแต่วันที่ """+result_work[0]['start_work']+"""ถึงวันที่ """+result_work[0]['EndWork_probation']+""" (ตามที่ต้นสังกัดได้ประเมินมา)
                    </p>
                    <p style="font-size: 16px;">ซึ่ง KPI ในช่วงขยายทดลองงานมีดังนี้</p>
                    """+kpi_user+"""
                    <p style="font-size: 16px;">ฝ่ายทรัพยากรบุคคลขอเป็นกำลังใจให้ คุณ""" + em_name + """ """ + em_surname +"""</p>
                    <p style="font-size: 16px;">ตั้งใจปฏิบัติงานตาม KPI ในช่วงขยายทดลองงานต่อไปค่ะ</p>
                    <p style="font-size: 16px;">Best Regard</p>
                    <img style="width: 1024px; height: auto;" src="http://hr-management.inet.co.th:8888/userGetFileImageMail/"""+imageName+""""">
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
        # not send email
        smtp = smtplib.SMTP(server)
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.close()
        result = {'status' : 'done', 'statusDetail' : 'Send email has done'}
        return jsonify(result)
    except:
        result = {'status' : 'error', 'statusDetail' : 'Send email has error : This system cannot send email'}
        return jsonify(result)

def sendpass_probation(email,em_name,em_surname,em_position,em_org,email_hr,imageName):
    send_from = "Hr Management <recruitment@inet.co.th>"
    send_to = email
    send_cc = email_hr
    send_bcc = email_hr
    subject = "แจ้งผ่านการทดลองงาน"
    text = """\
                <html>
                  <body>
                    <b style="font-size: 18px;">เรียนคุณ  """ + em_name + """ """ + em_surname + """</b></br>
                    <p style="text-indent: 30px; font-size: 16px; padding: 10px;">
                        ฝ่ายทรัพยากรบุคคลขอแสดงความยินดีกับ คุณ""" + em_name + """ """ + em_surname + """  เนื่องจาก คุณ""" + em_name + """ """ + em_surname +""" มีผลการประเมิน “ผ่านทดลองงาน” ในตำแหน่ง """+ em_position + """ """ + em_org + """ ซึ่งมีผลในวันที่ """ +datetime.now().strftime("%x")+ """ ค่ะ
                    </p>
                    <p style="font-size: 16px;">Best Regard </p>
                    <img style="width: 1024px; height: auto;" src="http://hr-management.inet.co.th:8888/userGetFileImageMail/"""+imageName+"""">
                  </body>
                </html>
        """
    server="mailtx.inet.co.th"

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Cc'] = send_cc
    msg['Bcc'] = send_bcc
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(text, "html","utf-8"))

    try:
        smtp = smtplib.SMTP(server)
        smtp.sendmail(send_from,[send_to,send_cc,send_bcc], msg.as_string())
        smtp.close()
        result = {'status' : 'done', 'statusDetail' : 'Send email has done'}
        return jsonify(result)
    except:
        result = {'status' : 'error', 'statusDetail' : 'Send email has error : This system cannot send email'}
        return jsonify(result)

@connect_sql()
def sendpass_relocate(cursor,version,email,em_name,em_surname,em_position,em_org,email_hr,imageName,relocate):
    print 'relocate',relocate['position_detail']
    send_from = "Hr Management <recruitment@inet.co.th>"
    send_to = email
    send_cc = email_hr
    send_bcc = email_hr
    subject = "แจ้งผ่านการทดลองงาน(ปรับตำแหน่ง)"
    text = """\
                <html>
                  <body>
                    <b style="font-size: 18px;">เรียนคุณ  """ + em_name + """ """ + em_surname + """</b></br>
                    <p style="text-indent: 30px; font-size: 16px; padding: 10px;">
                        ฝ่ายทรัพยากรบุคคลขอแสดงความยินดีกับ คุณ""" + em_name + """ """ + em_surname + """  เนื่องจาก คุณ""" + em_name + """ """ + em_surname +""" มีผลการประเมิน “ผ่านทดลองงาน” และปรับตำแหน่งจาก """+ relocate['position_detail'] + """ """ + relocate['org_name_detail'] + """
                        เป็นตำแหน่ง """+ em_position+""" ฝ่าย """+em_org+""" ซึ่งมีผลในวันที่ """ +datetime.now().strftime("%x")+ """ ค่ะ
                    </p>
                    <p style="font-size: 16px;">Best Regard </p>
                    <img style="width: 1024px; height: auto;" src="http://hr-management.inet.co.th:8888/userGetFileImageMail/"""+imageName+"""">
                  </body>
                </html>
        """
    server="mailtx.inet.co.th"

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Cc'] = send_cc
    msg['Bcc'] = send_bcc
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(text, "html","utf-8"))

    try:
        smtp = smtplib.SMTP(server)
        smtp.sendmail(send_from,[send_to,send_cc,send_bcc], msg.as_string())
        smtp.close()
        result = {'status' : 'done', 'statusDetail' : 'Send email has done'}
        return jsonify(result)
    except:
        result = {'status' : 'error', 'statusDetail' : 'Send email has error : This system cannot send email'}
        return jsonify(result)



@app.route('/userGetFileProbation/<employeeid>/<filetype>/<version>/<fileName>', methods=['GET'])
def userGetFileProbation(employeeid,filetype,version,fileName):
    # path = '../app/uploads/' + employeeid + "/" + filetype + "/" + version + "/"
    path = '../../uploads/' + employeeid + "/" + filetype + "/" + version + "/"
    # path = '../uploads/' + employeeid + "/" + filetype + "/" + version + "/"
    # current_app.logger.info(path)
    # current_app.logger.info(fileName)
    return send_from_directory(path, fileName)
    # return send_from_directory('../uploads/' + path)

@app.route('/Export_Employee_Probation', methods=['POST'])
@connect_sql()
def Export_Employee_Probation(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        year=str(int(data_new['year']) - 543)
        month=str(data_new['month'])
        try:
            sql = """SELECT Emp_probation.employeeid, Emp_probation.name_th, Emp_probation.surname_th,Emp_probation.name_eng, Emp_probation.surname_eng,table1.position_detail as old_position, table1.org_name_detail as old_org_name,
                    Emp_probation.start_work, Emp_probation.EndWork_probation, Emp_probation.status_result, position.position_detail,section.sect_detail, org_name.org_name_detail,
                    benefit_1.pro_values AS value_1,benefit_2.pro_values AS value_2,benefit_3.pro_values AS value_3,benefit_4.pro_values AS value_4,benefit_5.pro_values AS value_5,
                    benefit_6.sales_volume,benefit_6.date_con FROM `Emp_probation`
                    LEFT JOIN position ON position.position_id = Emp_probation.position_id
                    LEFT JOIN section ON section.sect_id = Emp_probation.section_id
                    LEFT JOIN org_name ON org_name.org_name_id = Emp_probation.org_name_id
                    LEFT JOIN ((SELECT position.position_detail, org_name.org_name_detail, Emp_probation_log.type_action, Emp_probation_log.employeeid FROM Emp_probation_log
                               LEFT JOIN position ON position.position_id = Emp_probation_log.position_id
                               LEFT JOIN org_name ON org_name.org_name_id = Emp_probation_log.org_name_id ) as table1)
                               ON table1.employeeid = Emp_probation.employeeid
                    LEFT JOIN ((SELECT Emp_probation.employeeid, employee_pro.question_pro_id, employee_pro.group_q,employee_pro.pro_values FROM `Emp_probation`
                           LEFT JOIN employee_pro ON employee_pro.employeeid = Emp_probation.employeeid
                           WHERE Emp_probation.validstatus = 10 AND Emp_probation.EndWork_probation LIKE '%""" + month + """-""" + year + """') as benefit_1 )
                           ON benefit_1.employeeid = Emp_probation.employeeid
                    LEFT JOIN ((SELECT Emp_probation.employeeid, employee_pro.question_pro_id, employee_pro.group_q,employee_pro.pro_values FROM `Emp_probation`
                           LEFT JOIN employee_pro ON employee_pro.employeeid = Emp_probation.employeeid
                           WHERE Emp_probation.validstatus = 10 AND Emp_probation.EndWork_probation LIKE '%""" + month + """-""" + year + """') as benefit_2 )
                           ON benefit_2.employeeid = Emp_probation.employeeid
                    LEFT JOIN ((SELECT Emp_probation.employeeid, employee_pro.question_pro_id, employee_pro.group_q,employee_pro.pro_values FROM `Emp_probation`
                           LEFT JOIN employee_pro ON employee_pro.employeeid = Emp_probation.employeeid
                           WHERE Emp_probation.validstatus = 10 AND Emp_probation.EndWork_probation LIKE '%""" + month + """-""" + year + """') as benefit_3 )
                           ON benefit_3.employeeid = Emp_probation.employeeid
                    LEFT JOIN ((SELECT Emp_probation.employeeid, employee_pro.question_pro_id, employee_pro.group_q,employee_pro.pro_values FROM `Emp_probation`
                           LEFT JOIN employee_pro ON employee_pro.employeeid = Emp_probation.employeeid
                           WHERE Emp_probation.validstatus = 10 AND Emp_probation.EndWork_probation LIKE '%""" + month + """-""" + year + """') as benefit_4 )
                           ON benefit_4.employeeid = Emp_probation.employeeid
                    LEFT JOIN ((SELECT Emp_probation.employeeid, employee_pro.question_pro_id, employee_pro.group_q,employee_pro.pro_values FROM `Emp_probation`
                           LEFT JOIN employee_pro ON employee_pro.employeeid = Emp_probation.employeeid
                           WHERE Emp_probation.validstatus = 10 AND Emp_probation.EndWork_probation LIKE '%""" + month + """-""" + year + """') as benefit_5 )
                           ON benefit_5.employeeid = Emp_probation.employeeid
                    LEFT JOIN ((SELECT Contract_log_sales.ID_CardNo, Contract_log_sales.sales_volume,Contract_log_sales.date_con FROM Emp_probation
                    	   LEFT JOIN Contract_log_sales ON Contract_log_sales.ID_CardNo = Emp_probation.citizenid
                           WHERE Emp_probation.validstatus = 10 AND Emp_probation.EndWork_probation LIKE '%""" + month + """-""" + year + """') as benefit_6 )
                           ON benefit_6.ID_CardNo = Emp_probation.citizenid
                    WHERE table1.type_action = 'ADD_appform' AND Emp_probation.validstatus = 10 AND benefit_1.question_pro_id = 24 AND benefit_2.question_pro_id = 26 AND benefit_3.question_pro_id = 25 AND benefit_4.question_pro_id = 28 AND benefit_5.question_pro_id = 27
                    AND Emp_probation.EndWork_probation LIKE '%""" + month + """-""" + year + """' """
            cursor.execute(sql)
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
        except Exception as e:
            logserver(e)
            return "No_Data"
        isSuccess = True
        reasonCode = 200
        reasonText = ""
        now = datetime.now()
        datetimeStr = now.strftime('%Y%m%d_%H%M%S%f')
        filename_tmp = secure_filename('{}_{}'.format(datetimeStr, 'Employee_Probation.xlsx'))
        wb = load_workbook('Template/Template_Employee_Probation_Payroll.xlsx')
        if len(result) > 0:
            sheet = wb['Sheet1']
            sheet['A'+str(1)] = 'สรุปประเมินผลทดลองงาน เดือน '+month+'/'+year+' (New Staff)'
            offset = 4
            i = 0
            for i in xrange(len(result)):
                date1 = result[i]['EndWork_probation']
                one_date = 1
                star_date = date1.split("-")
                Day_s = int(star_date[0])
                Mon_s = int(star_date[1])
                year_s = int(star_date[2])
                next_3_mm = date(year_s,Mon_s,Day_s) + relativedelta(days=one_date)
                next_3_m2 = str(next_3_mm)
                end_date = next_3_m2.split("-")
                Day_e = end_date[2]
                Mon_e =end_date[1]
                year_e = end_date[0]
                End_probation_date = Day_e+"-"+Mon_e+"-"+year_e

                sheet['A'+str(offset + i)] = i+1
                sheet['B'+str(offset + i)] = result[i]['employeeid']
                sheet['C'+str(offset + i)] = result[i]['name_th']
                sheet['D'+str(offset + i)] = result[i]['surname_th']
                sheet['E'+str(offset + i)] = result[i]['name_eng']
                sheet['F'+str(offset + i)] = result[i]['surname_eng']
                sheet['G'+str(offset + i)] = result[i]['old_position']
                sheet['H'+str(offset + i)] = result[i]['old_org_name']
                sheet['I'+str(offset + i)] = result[i]['start_work']
                sheet['J'+str(offset + i)] = result[i]['EndWork_probation']
                if result[i]['status_result'] != 'ขยายเวลาทดลองงาน':
                    sheet['K'+str(offset + i)] = result[i]['status_result']
                else:
                    sheet['L'+str(offset + i)] = result[i]['status_result']

                sheet['M'+str(offset + i)] = result[i]['value_1']
                sheet['N'+str(offset + i)] = result[i]['value_2']
                sheet['O'+str(offset + i)] = result[i]['value_3']
                sheet['P'+str(offset + i)] = result[i]['value_4']
                sheet['Q'+str(offset + i)] = result[i]['value_5']
                try:
                    sheet['R'+str(offset + i)] = result[i]['sales_volume']
                except Exception as e:
                    print e
                sheet['S'+str(offset + i)] = result[i]['date_con']
                sheet['T'+str(offset + i)] = result[i]['position_detail']
                sheet['U'+str(offset + i)] = result[i]['sect_detail']
                sheet['V'+str(offset + i)] = result[i]['org_name_detail']
                # sheet['W'+str(offset + i)] = result[i]['org_name_detail']
                sheet['X'+str(offset + i)] = End_probation_date

                i = i + 1
        wb.save(filename_tmp)
        with open(filename_tmp, "rb") as f:
            encoded_string = base64.b64encode(f.read())
        os.remove(filename_tmp)
        displayColumns = ['isSuccess','reasonCode','reasonText','excel_base64']
        displayData = [(isSuccess,reasonCode,reasonText,encoded_string)]
        return jsonify(toDict(displayData,displayColumns))
        # return 'success'
    except Exception as e:
        logserver(e)
        print e
        return "fail"
