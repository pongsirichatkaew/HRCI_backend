#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *
@app.route('/UpdateStatus_probation', methods=['POST'])
@connect_sql()
def UpdateStatus_probation(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        tier_approve = str(data_new['tier_approve'])
        status_ = str(data_new['status_'])

        sql_check_end = "SELECT validstatus FROM Emp_probation WHERE employeeid=%s"
        cursor.execute(sql_check_end,(data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        result_check_end = toJson(cursor.fetchall(),columns)
        check_endpro = int(result_check_end[0]['validstatus'])
        if check_endpro==9:
            return "End Probation"
        if (tier_approve=='L4')&(status_=='Reject'):

            sqlUp = "UPDATE approve_probation SET status_=8,id_comment=%s,comment=%s,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s"
            cursor.execute(sqlUp,(data_new['id_comment'],data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro']))

            sqlUp_main = "UPDATE Emp_probation SET validstatus=8 WHERE employeeid=%s"
            cursor.execute(sqlUp_main,(data_new['employeeid']))

            try:
                sqlUp_L3 = "UPDATE approve_probation SET status_=12 WHERE employeeid=%s AND tier_approve='L3'"
                cursor.execute(sqlUp_L3,(data_new['employeeid']))
            except Exception as e:
                pass

            try:
                sqlUp_L2 = "UPDATE approve_probation SET status_=12 WHERE employeeid=%s AND tier_approve='L2'"
                cursor.execute(sqlUp_L2,(data_new['employeeid']))
            except Exception as e:
                pass

            sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s"
            cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "reject_director"
            status_last = "8"

            sqlReject = "INSERT INTO approve_probation_log(employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

        elif (tier_approve =='L3')&(status_ =='Reject'):

            sqlUp = "UPDATE approve_probation SET status_=7,comment=%s,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s"
            cursor.execute(sqlUp,(data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro']))

            sqlUp_main = "UPDATE Emp_probation SET validstatus=7 WHERE employeeid=%s"
            cursor.execute(sqlUp_main,(data_new['employeeid']))

            try:
                sqlUp_L2 = "UPDATE approve_probation SET status_=12,comment=NULL,comment_orther=NULL,date_status=NULL WHERE employeeid=%s AND tier_approve='L2'"
                cursor.execute(sqlUp_L2,(data_new['employeeid']))
            except Exception as e:
                pass

            sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s"
            cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "reject_deputy_director"
            status_last = "7"

            sqlReject = "INSERT INTO approve_probation_log(employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

        elif (tier_approve =='L2')&(status_ =='Reject'):

            sqlUp = "UPDATE approve_probation SET status_=6,comment=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s"
            cursor.execute(sqlUp,(data_new['comment'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro']))

            sqlUp_main = "UPDATE Emp_probation SET validstatus=6 WHERE employeeid=%s"
            cursor.execute(sqlUp_main,(data_new['employeeid']))

            try:
                sqlUp_L1 = "UPDATE approve_probation SET status_=12,comment=NULL,date_status=NULL WHERE employeeid=%s AND tier_approve='L1'"
                cursor.execute(sqlUp_L1,(data_new['employeeid']))
            except Exception as e:
                pass

            sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s"
            cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "reject_hr"
            status_last = "6"

            sqlReject = "INSERT INTO approve_probation_log(employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))


        elif (tier_approve =='L4')&(status_ =='Approve'):

            sqlUp = "UPDATE approve_probation SET status_=14,id_comment=%s,comment=%s,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s"
            cursor.execute(sqlUp,(data_new['id_comment'],data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro']))

            sqlUp_main = "UPDATE Emp_probation SET validstatus=9 WHERE employeeid=%s"
            cursor.execute(sqlUp_main,(data_new['employeeid']))

            sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s"
            cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "send_director"
            status_last = "9"

            sqlReject = "INSERT INTO approve_probation_log(employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

        elif (tier_approve =='L3')&(status_=='Approve'):

            # sqlcheck_L4 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND employeeid=%s AND tier_approve='L4'"
            sqlcheck_L4 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND tier_approve='L4'"
            cursor.execute(sqlcheck_L4,(data_new['employeeid']))
            columns = [column[0] for column in cursor.description]
            result_check_L4 = toJson(cursor.fetchall(),columns)

            if not result_check_L4:

                sqlUp = "UPDATE approve_probation SET status_=14,comment=%s,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s"
                cursor.execute(sqlUp,(data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro']))

                sqlUp_main = "UPDATE Emp_probation SET validstatus=9 WHERE employeeid=%s"
                cursor.execute(sqlUp_main,(data_new['employeeid']))

                sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s"
                cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro']))
                columns = [column[0] for column in cursor.description]
                result = toJson(cursor.fetchall(),columns)

                type_action = "send_deputy_director"
                status_last = "9"

                sqlReject = "INSERT INTO approve_probation_log(employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlReject,(result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

            else:

                sqlUp = "UPDATE approve_probation SET status_=14,comment=%s,comment_orther=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s"
                cursor.execute(sqlUp,(data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro']))

                sqlUp_main = "UPDATE Emp_probation SET validstatus=5 WHERE employeeid=%s"
                cursor.execute(sqlUp_main,(data_new['employeeid']))

                sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s"
                cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro']))
                columns = [column[0] for column in cursor.description]
                result = toJson(cursor.fetchall(),columns)

                type_action = "send_deputy_director"
                status_last = "5"

                sqlReject = "INSERT INTO approve_probation_log(employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlReject,(result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

        elif (tier_approve =='L2')&(status_ =='Approve'):

            # sqlcheck_L3 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND employeeid=%s AND tier_approve='L3'"
            sqlcheck_L3 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND tier_approve='L3'"
            cursor.execute(sqlcheck_L3,(data_new['employeeid']))
            columns = [column[0] for column in cursor.description]
            result_check_L3 = toJson(cursor.fetchall(),columns)

            if not result_check_L3:

                sqlUp = "UPDATE approve_probation SET status_=14,comment=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s"
                cursor.execute(sqlUp,(data_new['comment'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro']))

                sqlUp_main = "UPDATE Emp_probation SET validstatus=5 WHERE employeeid=%s"
                cursor.execute(sqlUp_main,(data_new['employeeid']))

                sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s"
                cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro']))
                columns = [column[0] for column in cursor.description]
                result = toJson(cursor.fetchall(),columns)

                type_action = "send_hr_no_L3"
                status_last = "5"

                sqlReject = "INSERT INTO approve_probation_log(employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlReject,(result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))
            else:

                sqlUp = "UPDATE approve_probation SET status_=14,comment=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s"
                cursor.execute(sqlUp,(data_new['comment'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro']))

                sqlUp_main = "UPDATE Emp_probation SET validstatus=4 WHERE employeeid=%s"
                cursor.execute(sqlUp_main,(data_new['employeeid']))

                sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s"
                cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro']))
                columns = [column[0] for column in cursor.description]
                result = toJson(cursor.fetchall(),columns)

                type_action = "send_hr"
                status_last = "4"

                sqlReject = "INSERT INTO approve_probation_log(employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlReject,(result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))
        else:
            sqlcheck_L1 = "SELECT COUNT(employeeid_pro) AS total_l1 FROM approve_probation WHERE employeeid=%s AND tier_approve='L1'"
            cursor.execute(sqlcheck_L1,(data_new['employeeid']))
            columns = [column[0] for column in cursor.description]
            result_check_L1 = toJson(cursor.fetchall(),columns)
            check_total_l1 = int(result_check_L1[0]['total_l1'])

            sqlcheck_L2 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND tier_approve='L2'"
            # sqlcheck_L2 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND employeeid=%s AND tier_approve='L2'"
            cursor.execute(sqlcheck_L2,(data_new['employeeid']))
            columns = [column[0] for column in cursor.description]
            result_check_L2 = toJson(cursor.fetchall(),columns)

            # sqlcheck_L3 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND employeeid=%s AND tier_approve='L3'"
            sqlcheck_L3 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND tier_approve='L3'"
            cursor.execute(sqlcheck_L3,(data_new['employeeid']))
            columns = [column[0] for column in cursor.description]
            result_check_L3 = toJson(cursor.fetchall(),columns)

            if not result_check_L2:

                sqlUp = "UPDATE approve_probation SET status_=14,comment=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s"
                cursor.execute(sqlUp,(data_new['comment'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro']))

                if check_total_l1==1 :
                    sqlUp_main = "UPDATE Emp_probation SET validstatus=4 WHERE employeeid=%s"
                    cursor.execute(sqlUp_main,(data_new['employeeid']))
                else:
                    pass
                sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s"
                cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro']))
                columns = [column[0] for column in cursor.description]
                result = toJson(cursor.fetchall(),columns)

                type_action = "send_head_no_L2"
                status_last = "4"

                sqlReject = "INSERT INTO approve_probation_log(employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlReject,(result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

            elif (not result_check_L2)&(not result_check_L3):

                sqlUp = "UPDATE approve_probation SET status_=14,comment=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s"
                cursor.execute(sqlUp,(data_new['comment'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro']))

                if check_total_l1==1 :
                    sqlUp_main = "UPDATE Emp_probation SET validstatus=5 WHERE employeeid=%s"
                    cursor.execute(sqlUp_main,(data_new['employeeid']))
                else:
                    pass

                sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s"
                cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro']))
                columns = [column[0] for column in cursor.description]
                result = toJson(cursor.fetchall(),columns)

                type_action = "send_head_no_L2_L3"
                status_last = "5"

                sqlReject = "INSERT INTO approve_probation_log(employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlReject,(result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))
            else:
                sqlUp = "UPDATE approve_probation SET status_=14,comment=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s"
                cursor.execute(sqlUp,(data_new['comment'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro']))

                if check_total_l1==1 :
                    sqlUp_main = "UPDATE Emp_probation SET validstatus=3 WHERE employeeid=%s"
                    cursor.execute(sqlUp_main,(data_new['employeeid']))
                else:
                    pass

                sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s"
                cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro']))
                columns = [column[0] for column in cursor.description]
                result = toJson(cursor.fetchall(),columns)

                type_action = "send_head"
                status_last = "3"

                sqlReject = "INSERT INTO approve_probation_log(employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlReject,(result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Send_probation', methods=['POST'])
@connect_sql()
def Send_probation(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sqlcheck_L1 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND tier_approve='L1'"
        cursor.execute(sqlcheck_L1,(data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        result_check_L1 = toJson(cursor.fetchall(),columns)

        sqlcheck_L2 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND tier_approve='L2'"
        # sqlcheck_L2 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND employeeid=%s AND tier_approve='L2'"
        cursor.execute(sqlcheck_L2,(data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        result_check_L2 = toJson(cursor.fetchall(),columns)

        # sqlcheck_L3 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND employeeid=%s AND tier_approve='L3'"
        sqlcheck_L3 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND tier_approve='L3'"
        cursor.execute(sqlcheck_L3,(data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        result_check_L3 = toJson(cursor.fetchall(),columns)

        try:
            check_L3 = result_check_L3[0]['employeeid_pro']
        except Exception as e:
            return "No Level L3"

        sqlcheck_L4 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND tier_approve='L4'"
        cursor.execute(sqlcheck_L4,(data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        result_check_L4 = toJson(cursor.fetchall(),columns)

        if (not result_check_L2)&(not result_check_L1):
            sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s"
            cursor.execute(sql,(data_new['employeeid'],result_check_L3[0]['employeeid_pro']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "send_pro_no_L2"
            status_last = "4"

            sqlReject = "INSERT INTO approve_probation_log(employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,result[0]['comment'],result[0]['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

            sqlUp = "UPDATE approve_probation SET status_=4,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s"
            cursor.execute(sqlUp,(data_new['date_status'],data_new['employeeid'],result_check_L3[0]['employeeid_pro']))

            sqlUp_main = "UPDATE Emp_probation SET type_question=%s,validstatus=4 WHERE employeeid=%s"
            cursor.execute(sqlUp_main,(data_new['type_question'],data_new['employeeid']))

        elif (not result_check_L2)&(not result_check_L3)&(not result_check_L1):
            sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s"
            cursor.execute(sql,(data_new['employeeid'],result_check_L2[0]['employeeid_pro']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "send_pro_no_L2_L3_L1"
            status_last = "5"

            sqlReject = "INSERT INTO approve_probation_log(employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,result[0]['comment'],result[0]['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

            sqlUp = "UPDATE approve_probation SET status_=5,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s"
            cursor.execute(sqlUp,(data_new['date_status'],data_new['employeeid'],result_check_L2[0]['employeeid_pro']))

            sqlUp_main = "UPDATE Emp_probation SET type_question=%s,validstatus=5 WHERE employeeid=%s"
            cursor.execute(sqlUp_main,(data_new['type_question'],data_new['employeeid']))
        elif not result_check_L1:
            sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s"
            cursor.execute(sql,(data_new['employeeid'],result_check_L2[0]['employeeid_pro']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "send_pro_no_L1"
            status_last = "3"

            sqlReject = "INSERT INTO approve_probation_log(employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,result[0]['comment'],result[0]['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

            sqlUp = "UPDATE approve_probation SET status_=3,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s"
            cursor.execute(sqlUp,(data_new['date_status'],data_new['employeeid'],result_check_L2[0]['employeeid_pro']))

            sqlUp_main = "UPDATE Emp_probation SET type_question=%s,validstatus=3 WHERE employeeid=%s"
            cursor.execute(sqlUp_main,(data_new['type_question'],data_new['employeeid']))
        else:
            sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s"
            cursor.execute(sql,(data_new['employeeid'],result_check_L1[0]['employeeid_pro']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "send_pro"
            status_last = "2"

            sqlReject = "INSERT INTO approve_probation_log(employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,result[0]['comment'],result[0]['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

            sqlUp = "UPDATE approve_probation SET status_=2,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s"
            cursor.execute(sqlUp,(data_new['employeeid'],data_new['date_status'],result_check_L1[0]['employeeid_pro']))

            sqlUp_main = "UPDATE Emp_probation SET type_question=%s,validstatus=2 WHERE employeeid=%s"
            cursor.execute(sqlUp_main,(data_new['type_question'],data_new['employeeid']))
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Approve_hr', methods=['POST'])
@connect_sql()
def Approve_hr(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sqlcheck_L2 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND tier_approve='L2'"
        # sqlcheck_L2 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND employeeid=%s AND tier_approve='L2'"
        cursor.execute(sqlcheck_L2,(data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        result_check_L2 = toJson(cursor.fetchall(),columns)

        # sqlcheck_L3 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND employeeid=%s AND tier_approve='L3'"
        sqlcheck_L3 = "SELECT employeeid_pro FROM approve_probation WHERE employeeid=%s AND tier_approve='L3'"
        cursor.execute(sqlcheck_L3,(data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        result_check_L3 = toJson(cursor.fetchall(),columns)

        if not result_check_L2:

            sqlUp_main = "UPDATE Emp_probation SET validstatus=4 WHERE employeeid=%s"
            cursor.execute(sqlUp_main,(data_new['employeeid']))

            sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s"
            cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "send_head_no_L2_by_hr"
            status_last = "4"

            sqlReject = "INSERT INTO approve_probation_log(employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

        elif (not result_check_L2)&(not result_check_L3):

            sqlUp_main = "UPDATE Emp_probation SET validstatus=5 WHERE employeeid=%s"
            cursor.execute(sqlUp_main,(data_new['employeeid']))

            sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s"
            cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "send_head_no_L2_L3_by_hr"
            status_last = "5"

            sqlReject = "INSERT INTO approve_probation_log(employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

        else:
            sqlUp_main = "UPDATE Emp_probation SET validstatus=3 WHERE employeeid=%s"
            cursor.execute(sqlUp_main,(data_new['employeeid']))

            sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s"
            cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "send_head_by_hr"
            status_last = "3"

            sqlReject = "INSERT INTO approve_probation_log(employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlReject,(result[0]['employeeid'],result[0]['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action))

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

        sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s"
        cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sqlApprove = "INSERT INTO approve_probation(employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,createby) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlApprove,(data_new['employeeid'],data_new['employeeid_pro_2'],data_new['name'],data_new['lastname'],result[0]['tier_approve'],data_new['position_detail'],data_new['createby']))

        type_action = "ADD_tranfer"

        sqlApprove = "INSERT INTO approve_probation_log(employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlApprove,(data_new['employeeid'],data_new['employeeid_pro_2'],data_new['name'],data_new['lastname'],result[0]['tier_approve'],data_new['position_detail'],data_new['createby'],type_action))

        sqlUp = "UPDATE approve_probation SET status_=13,comment=%s,date_status=%s WHERE employeeid=%s AND employeeid_pro=%s"
        cursor.execute(sqlUp,(data_new['comment'],data_new['date_status'],data_new['employeeid'],data_new['employeeid_pro']))

        type_action2 = "transfer"
        status_last = "13"

        sqlReject = "INSERT INTO approve_probation_log(employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,comment,comment_orther,date_status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlReject,(data_new['employeeid'],data_new['employeeid_pro'],data_new['name'],data_new['lastname'],result[0]['tier_approve'],data_new['position_detail'],status_last,data_new['comment'],data_new['comment_orther'],data_new['date_status'],data_new['createby'],type_action2))


        return "Success"
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

        sql = "SELECT tier_approve FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s"
        cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sqlApprove = "INSERT INTO approve_probation(employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,createby) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlApprove,(data_new['employeeid'],data_new['employeeid_pro_2'],data_new['name'],data_new['lastname'],result[0]['tier_approve'],data_new['position_detail'],data_new['createby']))

        type_action = "ADD_together"

        sqlApprove = "INSERT INTO approve_probation_log(employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlApprove,(data_new['employeeid'],data_new['employeeid_pro_2'],data_new['name'],data_new['lastname'],result[0]['tier_approve'],data_new['position_detail'],data_new['createby'],type_action))

        return "Success"
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
        sql = "SELECT * FROM approve_probation WHERE employeeid=%s"
        cursor.execute(sql,(data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sql2 = "SELECT validstatus FROM Emp_probation WHERE employeeid=%s"
        cursor.execute(sql2,(data_new['employeeid']))
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
        sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s"
        cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro']))
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

        sqlApprove = "INSERT INTO approve_probation(employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,createby) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlApprove,(data_new['employeeid'],data_new['employeeid_pro'],data_new['name'],data_new['lastname'],data_new['tier_approve'],data_new['position_detail'],data_new['createby']))

        type_action = "ADD"

        sqlApprove = "INSERT INTO approve_probation_log(employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlApprove,(data_new['employeeid'],data_new['employeeid_pro'],data_new['name'],data_new['lastname'],data_new['tier_approve'],data_new['position_detail'],data_new['createby'],type_action))

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

        sql = "SELECT * FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s"
        cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_pro']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Delete"

        sqlApprove = "INSERT INTO approve_probation_log(employeeid,employeeid_pro,name,lastname,tier_approve,position_detail,status_,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlApprove,(data_new['employeeid'],data_new['employeeid_pro'],result[0]['name'],result[0]['lastname'],result[0]['tier_approve'],result[0]['position_detail'],result[0]['status_'],data_new['createby'],type_action))

        sqlDe = "DELETE FROM approve_probation WHERE employeeid=%s AND employeeid_pro=%s"
        cursor.execute(sqlDe,(data_new['employeeid'],data_new['employeeid_pro']))

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
        sqlEmployee = "SELECT * FROM employee LEFT JOIN company ON company.companyid = employee.company_id\
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
            status_id = 'WHERE validstatus='+'"'+str(data_new['status_id'])+'"'
        except Exception as e:
            pass
        connection = mysql.connect()
        cursor = connection.cursor()
        sql = "SELECT Emp_probation.name_th,Emp_probation.employeeid,Emp_probation.surname_th,Emp_probation.type_question,Emp_probation.citizenid,Emp_probation.start_work,Emp_probation.EndWork_probation,company.company_short_name,position.position_detail,section.sect_detail,org_name.org_name_detail,cost_center_name.cost_detail,status.status_detail,status.path_color,status.font_color FROM Emp_probation LEFT JOIN company ON company.companyid = Emp_probation.company_id\
                                      LEFT JOIN position ON position.position_id = Emp_probation.position_id\
                                      LEFT JOIN section ON section.sect_id = Emp_probation.section_id\
                                      LEFT JOIN org_name ON org_name.org_name_id = Emp_probation.org_name_id\
                                      LEFT JOIN cost_center_name ON cost_center_name.cost_center_name_id = Emp_probation.cost_center_name_id\
                                      LEFT JOIN status ON status.status_id = Emp_probation.validstatus "+status_id+" "
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
@app.route('/QryEmp_pro_leader', methods=['POST'])
def QryEmp_pro_leader():
    try:
        status_id = ""
        try:
            dataInput = request.json
            source = dataInput['source']
            data_new = source
            status_id = 'AND validstatus='+'"'+str(data_new['status_id'])+'"'
        except Exception as e:
            pass
        connection = mysql.connect()
        cursor = connection.cursor()
        sql = "SELECT Emp_probation.name_th,Emp_probation.employeeid,Emp_probation.surname_th,Emp_probation.type_question,Emp_probation.citizenid,Emp_probation.start_work,Emp_probation.EndWork_probation,company.company_short_name,position.position_detail,section.sect_detail,org_name.org_name_detail,cost_center_name.cost_detail,status.status_detail,status.path_color,status.font_color,approve_probation.tier_approve,question_pro_type.question_pro_detail_type FROM Emp_probation LEFT JOIN company ON company.companyid = Emp_probation.company_id\
                                      LEFT JOIN position ON position.position_id = Emp_probation.position_id\
                                      LEFT JOIN section ON section.sect_id = Emp_probation.section_id\
                                      LEFT JOIN org_name ON org_name.org_name_id = Emp_probation.org_name_id\
                                      LEFT JOIN cost_center_name ON cost_center_name.cost_center_name_id = Emp_probation.cost_center_name_id\
                                      LEFT JOIN approve_probation ON approve_probation.employeeid = Emp_probation.employeeid\
                                      LEFT JOIN question_pro_type ON question_pro_type.question_pro_id_type = Emp_probation.type_question\
                                      LEFT JOIN status ON status.status_id = Emp_probation.validstatus WHERE employeeid_pro=%s "+status_id+" "
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
        sql = "SELECT citizenid FROM Emp_probation WHERE employeeid=%s"
        cursor.execute(sql,(employeeid))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "ADD"

        i=0
        for i in xrange(len(data_new['answer_pro'])):
            sqlIn_be = "INSERT INTO employee_pro(employeeid,citizenid,question_pro_id,pro_values,type_check,group_q,createby) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_be,(employeeid,result[0]['citizenid'],data_new['answer_pro'][i]['question_pro_id'],data_new['answer_pro'][i]['pro_values'],data_new['answer_pro'][i]['type_check'],data_new['answer_pro'][i]['group_q'],data_new['createby']))

        i=0
        for i in xrange(len(data_new['answer_pro'])):
            sqlIn_be_log = "INSERT INTO employee_pro_log(employeeid,citizenid,question_pro_id,pro_values,type_check,group_q,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_be_log,(employeeid,result[0]['citizenid'],data_new['answer_pro'][i]['question_pro_id'],data_new['answer_pro'][i]['pro_values'],data_new['answer_pro'][i]['type_check'],data_new['answer_pro'][i]['group_q'],data_new['createby'],type_action))

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
        sql = "SELECT citizenid,question_pro_id,pro_values,type_check,group_q FROM employee_pro WHERE employeeid=%s AND question_pro_id=%s"
        cursor.execute(sql,(data_new['employeeid'],data_new['question_pro_id']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Edit"

        sqlIn = "INSERT INTO employee_pro_log (employeeid,citizenid,question_pro_id,pro_values,type_check,group_q,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn,(data_new['employeeid'],result[0]['citizenid'],result[0]['question_pro_id'],result[0]['pro_values'],result[0]['type_check'],result[0]['group_q'],data_new['createby'],type_action))

        sqlde = "DELETE FROM employee_pro WHERE employeeid=%s AND question_pro_id=%s"
        cursor.execute(sqlde,(data_new['employeeid'],data_new['question_pro_id']))

        sqlIn = "INSERT INTO employee_pro(employeeid,citizenid,question_pro_id,pro_values,type_check,group_q,createby) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn,(data_new['employeeid'],data_new['citizenid'],data_new['question_pro_id'],data_new['pro_values'],data_new['type_check'],data_new['group_q'],data_new['createby']))
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
            createby_id = 'AND createby='+'"'+str(data_new['createby_id'])+'"'
        except Exception as e:
            pass
        sql = "SELECT Emp_probation.name_th,Emp_probation.employeeid,Emp_probation.surname_th,Emp_probation.type_question,Emp_probation.citizenid,Emp_probation.start_work,Emp_probation.EndWork_probation,Emp_probation.validstatus,position.position_detail,section.sect_detail,org_name.org_name_detail,cost_center_name.cost_detail,company.imageName FROM Emp_probation LEFT JOIN position ON position.position_id = Emp_probation.position_id\
                                      LEFT JOIN section ON section.sect_id = Emp_probation.section_id\
                                      LEFT JOIN org_name ON org_name.org_name_id = Emp_probation.org_name_id\
                                      LEFT JOIN cost_center_name ON cost_center_name.cost_center_name_id = Emp_probation.cost_center_name_id\
                                      LEFT JOIN company ON company.companyid = Emp_probation.company_id\
        WHERE Emp_probation.employeeid=%s"
        cursor.execute(sql,(data_new['employeeid']))
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
            question = []
            sql1pro = "SELECT question_pro_id,pro_values,type_check,group_q FROM employee_pro WHERE employeeid={} AND validstatus=1 {} ORDER BY question_pro_id ASC".format(employeeid_,createby_id)
            cursor.execute(sql1pro)
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
            sqlDe = "DELETE FROM employee_upload WHERE ID_CardNo=%s"
            cursor.execute(sqlDe,(ID_CardNo))
        except Exception as e:
            pass

        Type = 'probation'
        employeeid = request.form['employeeid']
        # path = 'uploads/'+employeeid+'/'+'probation'
        path = '../uploads/'+employeeid+'/'+'probation'
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
                PathFile = employeeid+'/'+'probation'+'/'+str(fileList.filename)
                sql = "INSERT INTO employee_upload(ID_CardNo,FileName,Type,PathFile,createby) VALUES (%s,%s,%s,%s,%s)"
                # cursor.execute(sql,(ID_CardNo,Type,PathFile,request.form['createby']))
                cursor.execute(sql,(ID_CardNo,fileName,Type,PathFile,request.form['createby']))
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

        sql = "SELECT ID_CardNo,FileName,Type,PathFile FROM employee_upload WHERE ID_CardNo=%s "
        cursor.execute(sql,(ID_CardNo))
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
@app.route('/sendEmail', methods = ['POST'])
@connect_sql()
def send_email(cursor):
    sql_L1 = "SELECT employeeid,email_asp,tier_approve FROM assessor_pro WHERE tier_approve='L1' GROUP BY email_asp "
    cursor.execute(sql_L1)
    columns = [column[0] for column in cursor.description]
    result = toJson(cursor.fetchall(),columns)
    for i1 in result:
        total_em = []
        sql1_total = "SELECT COUNT(approve_probation.employeeid) AS total_em FROM approve_probation LEFT JOIN assessor_pro ON approve_probation.employeeid_pro = assessor_pro.employeeid\
                                                                                                    LEFT JOIN Emp_probation ON approve_probation.employeeid = Emp_probation.employeeid\
                       WHERE approve_probation.employeeid_pro = %s AND Emp_probation.validstatus IN(2,12)"
        cursor.execute(sql1_total,(i1['employeeid']))
        columns = [column[0] for column in cursor.description]
        data1 = toJson(cursor.fetchall(),columns)
        i1['total_em'] = str(data1[0]['total_em'])
    for item in result:
        count = int(item['total_em'])
        if count>0:
            sendToMail(item['email_asp'], item['total_em'])
    sql_L2 = "SELECT employeeid,email_asp,tier_approve FROM assessor_pro WHERE tier_approve='L2' GROUP BY email_asp "
    cursor.execute(sql_L2)
    columns = [column[0] for column in cursor.description]
    result2 = toJson(cursor.fetchall(),columns)
    for i2 in result2:
        total_em2 = []
        sql1_total2 = "SELECT COUNT(approve_probation.employeeid) AS total_em FROM approve_probation LEFT JOIN assessor_pro ON approve_probation.employeeid_pro = assessor_pro.employeeid\
                                                                                                    LEFT JOIN Emp_probation ON approve_probation.employeeid = Emp_probation.employeeid\
                       WHERE approve_probation.employeeid_pro = %s AND Emp_probation.validstatus IN(3,6,12)"
        cursor.execute(sql1_total2,(i2['employeeid']))
        columns = [column[0] for column in cursor.description]
        data2 = toJson(cursor.fetchall(),columns)
        i2['total_em'] = str(data2[0]['total_em'])
    for item2 in result2:
        count2 = int(item2['total_em'])
        if count2>0:
            sendToMail(item2['email_asp'], item2['total_em'])
    sql_L3 = "SELECT employeeid,email_asp,tier_approve FROM assessor_pro WHERE tier_approve='L3' GROUP BY email_asp "
    cursor.execute(sql_L3)
    columns = [column[0] for column in cursor.description]
    result3 = toJson(cursor.fetchall(),columns)
    for i3 in result3:
        total_em3 = []
        sql1_total3 = "SELECT COUNT(approve_probation.employeeid) AS total_em FROM approve_probation LEFT JOIN assessor_pro ON approve_probation.employeeid_pro = assessor_pro.employeeid\
                                                                                                    LEFT JOIN Emp_probation ON approve_probation.employeeid = Emp_probation.employeeid\
                       WHERE approve_probation.employeeid_pro = %s AND Emp_probation.validstatus IN(4,7,12)"
        cursor.execute(sql1_total3,(i3['employeeid']))
        columns = [column[0] for column in cursor.description]
        data3 = toJson(cursor.fetchall(),columns)
        i3['total_em'] = str(data3[0]['total_em'])
    for item3 in result3:
        count3 = int(item3['total_em'])
        if count3>0:
            sendToMail(item3['email_asp'], item3['total_em'])
    sql_L4 = "SELECT employeeid,email_asp,tier_approve FROM assessor_pro WHERE tier_approve='L4' GROUP BY email_asp "
    cursor.execute(sql_L4)
    columns = [column[0] for column in cursor.description]
    result4 = toJson(cursor.fetchall(),columns)
    for i4 in result4:
        total_em4 = []
        sql1_total4 = "SELECT COUNT(approve_probation.employeeid) AS total_em FROM approve_probation LEFT JOIN assessor_pro ON approve_probation.employeeid_pro = assessor_pro.employeeid\
                                                                                                    LEFT JOIN Emp_probation ON approve_probation.employeeid = Emp_probation.employeeid\
                       WHERE approve_probation.employeeid_pro = %s AND Emp_probation.validstatus IN(5,8,12)"
        cursor.execute(sql1_total4,(i4['employeeid']))
        columns = [column[0] for column in cursor.description]
        data4 = toJson(cursor.fetchall(),columns)
        i4['total_em'] = str(data4[0]['total_em'])
    for item4 in result4:
        count4 = int(item4['total_em'])
        if count4>0:
            sendToMail(item4['email_asp'], item4['total_em'])
    return jsonify(result)
def sendToMail(email, total_em):
    send_from = "Hr Management <jirakit.da@inet.co.th>"
    send_to = email
    subject = "ประเมินพนักงานผ่านทดลองงาน"
    text = """\
                <html>
                  <body>
                  <img src="https://intranet.inet.co.th/assets/images/news/1521011167Slide1.JPG"></br>
                    <b>เรียน  ผู้บริหารและพนักงานทุกท่าน</b></br>
                      <p>จะมีพนักงานผ่านการทดลองงานจำนวน """ + total_em + """ คน ขอเชิญผู้ประเมินทุกท่านสามารถเข้าไปทำการประเมินพนักงาน ได้ที่<br>
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
