#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *
@app.route('/QryEmployee_kpi', methods=['POST'])
@connect_sql()
def QryEmployee_kpi(cursor):
    try:
        group_kpi_id = ""
        try:
            dataInput = request.json
            source = dataInput['source']
            data_new = source
            year_ = ''
            try:
                year_ = '"'+str(data_new['year'])+'"'
                year_ = ' AND employee_kpi.year='+'"'+str(data_new['year'])+'"'
            except Exception as e:
                pass
            term_ = ''
            try:
                term_ = '"'+str(data_new['term'])+'"'
                term_ = ' AND employee_kpi.term='+'"'+str(data_new['term'])+'"'
            except Exception as e:
                pass
            group_ = str(data_new['group_kpi_id'])
            group_kpi_id = 'WHERE group_kpi='+'"'+group_+'"'+year_+term_
        except Exception as e:
            pass
        try:
            dataInput = request.json
            source = dataInput['source']
            data_new = source
            year_ = ''
            try:
                year_ ='"'+str(data_new['year'])+'"'
                year_ = ' AND employee_kpi.year='+'"'+str(data_new['year'])+'"'
            except Exception as e:
                pass
            term_ = ''
            try:
                term_ = '"'+str(data_new['term'])+'"'
                term_ = ' AND employee_kpi.term='+'"'+str(data_new['term'])+'"'
            except Exception as e:
                pass
            group_2 = str(data_new['group_kpi_id2'])
            group_kpi_id = 'WHERE group_kpi IN ('+'"'+group_+'"'+','+'"'+group_2+'"'+')'+year_+term_
        except Exception as e:
            pass
        sql = "SELECT employee_kpi.previous_grade,employee_kpi.validstatus,employee_kpi.newKpiDescriptions_GM,employee_kpi.specialMoney_GM,employee_kpi.positionChange_GM,employee_kpi.status_GM,employee_kpi.old_grade_GM,employee_kpi.createby,employee_kpi.comment_cancel,employee_kpi.year,employee_kpi.term,employee_kpi.employeeid,employee_kpi.name,employee_kpi.companyid AS company_short_name,employee_kpi.surname,org_name.org_name_detail,position.position_detail,employee_kpi.work_date,employee_kpi.work_month,employee_kpi.work_year,employee_kpi.old_grade,employee_kpi.grade,employee_kpi.comment_hr,employee_kpi.group_kpi,employee_kpi.star_date_kpi,employee_kpi.status,employee_kpi.em_id_leader FROM employee_kpi\
                                                                                        INNER JOIN org_name ON employee_kpi.org_name = org_name.org_name_id\
                                                                                        INNER JOIN position ON employee_kpi.position = position.position_id\
        "+group_kpi_id+" GROUP BY employee_kpi.employeeid "
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        print result[0]
        for i1 in result:
            # sql2 = "SELECT company_short_name FROM company WHERE companyid=%s"
            # cursor.execute(sql2,(i1['company_short_name']))
            # columns = [column[0] for column in cursor.description]
            # data2 = toJson(cursor.fetchall(),columns)

            sql3 = "SELECT *, MAX(CAST(create_at AS CHAR))max_date FROM `project_kpi_log` WHERE employeeid = %s GROUP BY employeeid"
            cursor.execute(sql3,(i1['employeeid']))
            columns = [column[0] for column in cursor.description]
            data3 = toJson(cursor.fetchall(),columns)
            if len(data3) >0 :
                # print data3[0]['max_date']
                i1['edit_at'] =  data3[0]['max_date']
            # i1['company_short_name'] = data2[0]['company_short_name']
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"

# ------------------------------------------------------------------------------------------------------

@app.route('/QryEmployee_kpi_eiei', methods=['POST'])
@connect_sql()
def QryEmployee_kpi_eiei(cursor):
    try:

        try:
            dataInput = request.json
            source = dataInput['source']
            data_new = source
            year_ = ''
            try:
                year_ ='"'+str(data_new['year'])+'"'
                year_ = ' AND employee_kpi.year='+'"'+str(data_new['year'])+'"'
            except Exception as e:
                pass
            term_ = ''
            try:
                term_ = '"'+str(data_new['term'])+'"'
                term_ = ' AND employee_kpi.term='+'"'+str(data_new['term'])+'"'
            except Exception as e:
                pass
            group_kpi_id = 'WHERE group_kpi IN '+str(tuple(group_list))+year_+term_
        except Exception as e:
            pass
        sql = "SELECT employee_kpi.validstatus,employee_kpi.newKpiDescriptions_GM,employee_kpi.specialMoney_GM,employee_kpi.positionChange_GM,employee_kpi.status_GM,employee_kpi.old_grade_GM,employee_kpi.createby,employee_kpi.comment_cancel,employee_kpi.year,employee_kpi.term,employee_kpi.employeeid,employee_kpi.name,employee_kpi.companyid AS company_short_name,employee_kpi.surname,org_name.org_name_detail,position.position_detail,employee_kpi.work_date,employee_kpi.work_month,employee_kpi.work_year,employee_kpi.old_grade,employee_kpi.grade,employee_kpi.comment_hr,employee_kpi.group_kpi,employee_kpi.star_date_kpi,employee_kpi.status,employee_kpi.em_id_leader FROM employee_kpi\
                                                                                        INNER JOIN org_name ON employee_kpi.org_name = org_name.org_name_id\
                                                                                        INNER JOIN position ON employee_kpi.position = position.position_id\
        "+group_kpi_id+" GROUP BY employee_kpi.employeeid "
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        for i1 in result:
            sql2 = "SELECT company_short_name FROM company WHERE companyid=%s"
            cursor.execute(sql2,(i1['company_short_name']))
            columns = [column[0] for column in cursor.description]
            data2 = toJson(cursor.fetchall(),columns)
            i1['company_short_name'] = data2[0]['company_short_name']
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"








# --------------------------------------------------------------------------------------------------------
@app.route('/QryEmployee_kpi_search', methods=['POST'])
@connect_sql()
def QryEmployee_kpi_search(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT employee_kpi.validstatus,employee_kpi.createby,employee_kpi.comment_cancel,employee_kpi.year,employee_kpi.term,employee_kpi.employeeid,employee_kpi.name,company.company_short_name,employee_kpi.surname,org_name.org_name_detail,position.position_detail,employee_kpi.work_date,employee_kpi.work_month,employee_kpi.work_year,employee_kpi.old_grade,employee_kpi.grade,employee_kpi.comment_hr,employee_kpi.group_kpi,employee_kpi.star_date_kpi,employee_kpi.status,employee_kpi.em_id_leader FROM employee_kpi\
                                                                                        INNER JOIN company ON employee_kpi.companyid = company.companyid\
                                                                                        INNER JOIN org_name ON employee_kpi.org_name = org_name.org_name_id\
                                                                                        INNER JOIN position ON employee_kpi.position = position.position_id\
        WHERE employee_kpi.year=%s AND employee_kpi.term =%s "
        cursor.execute(sql,(data_new['year'],data_new['term']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryEmployee_kpi_oldkpi', methods=['POST'])
@connect_sql()
def QryEmployee_kpi_oldkpi(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT employee_kpi.validstatus,employee_kpi.createby,employee_kpi.comment_cancel,employee_kpi.year,employee_kpi.term,employee_kpi.employeeid,employee_kpi.name,company.company_short_name,employee_kpi.surname,org_name.org_name_detail,position.position_detail,employee_kpi.work_date,employee_kpi.work_month,employee_kpi.work_year,employee_kpi.old_grade,employee_kpi.grade,employee_kpi.comment_hr,employee_kpi.group_kpi,employee_kpi.star_date_kpi,employee_kpi.status FROM employee_kpi\
                                                                                        INNER JOIN company ON employee_kpi.companyid = company.companyid\
                                                                                        INNER JOIN org_name ON employee_kpi.org_name = org_name.org_name_id\
                                                                                        INNER JOIN position ON employee_kpi.position = position.position_id\
        WHERE employee_kpi.em_id_leader=%s AND employee_kpi.structure_salary IN ('') OR employee_kpi.structure_salary IS NULL"
        cursor.execute(sql,(data_new['em_id_leader']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryEmployee_kpi_oldkpi_search', methods=['POST'])
@connect_sql()
def QryEmployee_kpi_oldkpi_search(cursor):
    try:

        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT employee_kpi.validstatus,employee_kpi.createby,employee_kpi.comment_cancel,employee_kpi.year,employee_kpi.term,employee_kpi.employeeid,employee_kpi.name,company.company_short_name,employee_kpi.surname,org_name.org_name_detail,position.position_detail,employee_kpi.work_date,employee_kpi.work_month,employee_kpi.work_year,employee_kpi.old_grade,employee_kpi.grade,employee_kpi.comment_hr,employee_kpi.group_kpi,employee_kpi.star_date_kpi,employee_kpi.status FROM employee_kpi\
                                                                                        INNER JOIN company ON employee_kpi.companyid = company.companyid\
                                                                                        INNER JOIN org_name ON employee_kpi.org_name = org_name.org_name_id\
                                                                                        INNER JOIN position ON employee_kpi.position = position.position_id\
        WHERE employee_kpi.year=%s AND employee_kpi.term =%s AND em_id_leader=%s AND employee_kpi.structure_salary IN ('') OR employee_kpi.structure_salary IS NULL"
        cursor.execute(sql,(data_new['year'],data_new['term'],data_new['em_id_leader']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryEmployee_kpi_one', methods=['POST'])
@connect_sql()
def QryEmployee_kpi_one(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        try:
            sql = "SELECT employee_kpi.positionChange_bet,employee_kpi.date_bet,employee_kpi.comment_pass,employee_kpi.Pass,org_name.org_name_detail,employee_kpi.positionChange,position.position_detail,company.company_short_name,employee_kpi.employeeid,employee_kpi.name,employee_kpi.surname,employee_kpi.work_date,employee_kpi.org_name,employee_kpi.position,employee_kpi.work_month,employee_kpi.work_year,employee_kpi.old_grade,employee_kpi.grade,employee_kpi.comment_hr,employee_kpi.group_kpi,employee_kpi.star_date_kpi,employee_kpi.status,employee_kpi.companyid,employee_kpi.year,employee_kpi.term,employee_kpi.structure_salary,employee_kpi.totalGrade,employee_kpi.totalGradePercent,employee_kpi.positionChange AS positionChange_detail,employee_kpi.specialMoney,employee_kpi.newKpiDescriptions FROM employee_kpi\
            INNER JOIN org_name ON employee_kpi.org_name = org_name.org_name_id\
            INNER JOIN position ON employee_kpi.position = position.position_id\
            INNER JOIN company ON employee_kpi.companyid = company.companyid\
            WHERE employeeid=%s AND year=%s AND term=%s"
            cursor.execute(sql,(data_new['employeeid'],data_new['year'],data_new['term']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            for i1 in result:
                sql2 = "SELECT position_detail FROM position WHERE position_id=%s"
                cursor.execute(sql2,(i1['positionChange_detail']))
                columns = [column[0] for column in cursor.description]
                data2 = toJson(cursor.fetchall(),columns)
                i1['positionChange_detail'] = data2[0]['position_detail']
        except Exception as e:
            sql = "SELECT employee_kpi.positionChange_bet,employee_kpi.date_bet,employee_kpi.comment_pass,employee_kpi.Pass,org_name.org_name_detail,employee_kpi.positionChange,position.position_detail,company.company_short_name,employee_kpi.employeeid,employee_kpi.name,employee_kpi.surname,employee_kpi.work_date,employee_kpi.org_name,employee_kpi.position,employee_kpi.work_month,employee_kpi.work_year,employee_kpi.old_grade,employee_kpi.grade,employee_kpi.comment_hr,employee_kpi.group_kpi,employee_kpi.star_date_kpi,employee_kpi.status,employee_kpi.companyid,employee_kpi.year,employee_kpi.term,employee_kpi.structure_salary,employee_kpi.totalGrade,employee_kpi.totalGradePercent,employee_kpi.positionChange AS positionChange_detail,employee_kpi.specialMoney,employee_kpi.newKpiDescriptions FROM employee_kpi\
            INNER JOIN org_name ON employee_kpi.org_name = org_name.org_name_id\
            INNER JOIN position ON employee_kpi.position = position.position_id\
            INNER JOIN company ON employee_kpi.companyid = company.companyid\
            WHERE employeeid=%s AND year=%s AND term=%s"
            cursor.execute(sql,(data_new['employeeid'],data_new['year'],data_new['term']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

        sql2 = "SELECT employeeid_board,name_kpi,surname_kpi,position_kpi,grade_board,pass_board,comment FROM board_kpi WHERE employeeid=%s AND year=%s AND term=%s AND validstatus=1"
        cursor.execute(sql2,(data_new['employeeid'],data_new['year'],data_new['term']))
        columns = [column[0] for column in cursor.description]
        result2 = toJson(cursor.fetchall(),columns)

        # if data_new['project_kpi_id'] :
        sql3 = "SELECT * FROM project_kpi WHERE employeeid=%s AND year=%s AND term=%s"
        cursor.execute(sql3,(data_new['employeeid'],data_new['year'],data_new['term']))
        columns = [column[0] for column in cursor.description]
        result3 = toJson(cursor.fetchall(),columns)

        sqlGM = "SELECT employee_kpi.date_bet_gm,employee_kpi.old_grade_GM,employee_kpi.status_GM,position.position_detail AS positionChange_GM_detail,employee_kpi.positionChange_GM,employee_kpi.specialMoney_GM,employee_kpi.newKpiDescriptions_GM FROM employee_kpi\
        INNER JOIN position ON employee_kpi.positionChange_GM = position.position_id\
        WHERE employee_kpi.employeeid=%s AND employee_kpi.year=%s AND employee_kpi.term=%s"
        cursor.execute(sqlGM,(data_new['employeeid'],data_new['year'],data_new['term']))
        columns = [column[0] for column in cursor.description]
        result_GM = toJson(cursor.fetchall(),columns)

        if not result_GM:
            sqlGM = "SELECT employee_kpi.date_bet_gm,employee_kpi.old_grade_GM,employee_kpi.status_GM,employee_kpi.positionChange_GM,employee_kpi.specialMoney_GM,employee_kpi.newKpiDescriptions_GM FROM employee_kpi\
            WHERE employee_kpi.employeeid=%s AND employee_kpi.year=%s AND employee_kpi.term=%s"
            cursor.execute(sqlGM,(data_new['employeeid'],data_new['year'],data_new['term']))
            columns = [column[0] for column in cursor.description]
            result_GM = toJson(cursor.fetchall(),columns)

        try:
            sqlAss = "SELECT status,type FROM assessor_kpi WHERE employeeid=%s"
            cursor.execute(sqlAss,(data_new['createby']))
            columns = [column[0] for column in cursor.description]
            result_ass = toJson(cursor.fetchall(),columns)
        except Exception as e:
            result_ass = ''
        try:
            encoded_Image=str("http://intranet.inet.co.th/assets/upload/staff/"+str(data_new['employeeid'])+".jpg")
            open_path_ = urllib.urlopen(encoded_Image)
            htmlSource = open_path_.read()
            open_path_.close()
            test= htmlSource.decode('utf-8')
            encoded_Image=str("http://intranet.inet.co.th/assets/upload/staff/"+str(data_new['employeeid'])+"s.jpg")
        except Exception as e:
            encoded_Image=str("http://intranet.inet.co.th/assets/upload/staff/"+str(data_new['employeeid'])+".jpg")

        try:
            # encoded_Image=str("http://intranet.inet.co.th/assets/upload/staff/"+str(data_new['employeeid'])+".jpg")
            open_path_ = urllib.urlopen(encoded_Image)
            htmlSource = open_path_.read()
            open_path_.close()
            test= htmlSource.decode('utf-8')
            encoded_Image=str("http://intranet.inet.co.th/assets/upload/staff/"+str(data_new['employeeid'])+".JPG")
        except Exception as e:
            pass

        sum={}
        sum["employee"] = result
        sum["board"] = result2
        sum["project"] = result3
        sum["image"] = encoded_Image
        sum["grade_GM"] = result_GM
        sum["permission_leader"] = result_ass

        return jsonify(sum)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Add_emp_kpi', methods=['POST'])
@connect_sql()
def Add_emp_kpi(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        employeeid = str(data_new['employeeid'])
        # check_board = str(data_new['employeeid_board'])
        try:
            sql44 = "SELECT name FROM employee_kpi WHERE employeeid=%s AND year=%s AND term=%s"
            cursor.execute(sql44,(employeeid,data_new['year'],data_new['term']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            name = result[0]['name']
            return "employee is duplicate"
        except Exception as e:
            pass

        # sql44 = "SELECT employeeid FROM assessor_kpi WHERE companyid=%s AND org_name_id=%s AND type='main'"
        # sql44 = "SELECT employeeid FROM assessor_kpi WHERE companyid=%s AND type='main'"

        # cursor.execute(sql44,(data_new['companyid']))
        sql44_ = "SELECT employeeid FROM assessor_kpi WHERE employeeid=%s AND companyid=%s  AND type='main'"
        cursor.execute(sql44_,(data_new['createby'],data_new['companyid']))

        columns = [column[0] for column in cursor.description]
        result_test = toJson(cursor.fetchall(),columns)
        print data_new['org_name']
        print data_new['companyid']
        if not result_test:
            print "no org_name"
            return "no org_name"

        now = datetime.now()
        n = data_new['start_work']
        date = n.split("-")
        date_day = int(date[0])
        date_month = int(date[1])
        date_year = int(date[2])
        year = now.year
        month = now.month
        day = now.day
        if date_day <= day :
            if date_month <= month :
                year = year - date_year
                month = month - date_month
            else :
                year = (year - 1) - date_year
                month = 12 - (date_month - month)
            day = day - date_day
        else :
            if date_month >= month :
                year = (year - 1) - date_year
                month = 11 - (date_month - month)
            else:
                year = year - date_year
                month = (month - 1) - date_month
            day = 32 - (date_day - day)
        work_year  =year
        work_month = month
        work_date  = day

        try:
            old_grade = data_new['old_grade']
        except Exception as e:
            old_grade = ''
        try:
            star_date_kpi = data_new['star_date_kpi']
        except Exception as e:
            star_date_kpi = ''
        try:
            group_kpi = data_new['group_kpi']
        except Exception as e:
            group_kpi = ''
        try:
            structure_salary = data_new['structure_salary']
        except Exception as e:
            structure_salary = ''

        type_action = "ADD"

        sqlIn_be = "INSERT INTO employee_kpi(year,term,companyid,em_id_leader,structure_salary,employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,group_kpi,star_date_kpi,status,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_be,(data_new['year'],data_new['term'],data_new['companyid'],result_test[0]['employeeid'],structure_salary,employeeid,data_new['name'],data_new['surname'],data_new['org_name'],data_new['position'],work_date,work_month,work_year,old_grade,group_kpi,star_date_kpi,data_new['status'],data_new['createby']))

        sqlIn_be2 = "INSERT INTO employee_kpi_log(year,term,companyid,em_id_leader,structure_salary,employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,group_kpi,star_date_kpi,status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_be2,(data_new['year'],data_new['term'],data_new['companyid'],result_test[0]['employeeid'],structure_salary,employeeid,data_new['name'],data_new['surname'],data_new['org_name'],data_new['position'],work_date,work_month,work_year,old_grade,group_kpi,star_date_kpi,data_new['status'],data_new['createby'],type_action))

        return "Success"
    except Exception as e:
        logserver(e)
        print str(e)
        return "fail"
@app.route('/Add_emp_kpi_user', methods=['POST'])
@connect_sql()
def Add_emp_kpi_user(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        employeeid = str(data_new['employeeid'])
        result_token = CheckTokenAssessor_kpi(data_new['createby'],data_new['token'])
        if result_token!='pass':
            return 'token fail'

        try:
            sql44 = "SELECT name FROM employee_kpi WHERE employeeid=%s AND year=%s AND term=%s"
            cursor.execute(sql44,(employeeid,data_new['year'],data_new['term']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            name = result[0]['name']
            return "employee is duplicate"
        except Exception as e:
            pass
        print data_new['companyid']
        sql44_ = "SELECT employeeid FROM assessor_kpi WHERE employeeid=%s AND companyid=%s  AND type='main'"
        cursor.execute(sql44_,(data_new['createby'],data_new['companyid']))
        columns = [column[0] for column in cursor.description]
        result_test = toJson(cursor.fetchall(),columns)
        print result_test[0]

        if not result_test:
            return "no org_name"

        now = datetime.now()
        n = data_new['start_work']
        date = n.split("-")
        date_day = int(date[0])
        date_month = int(date[1])
        date_year = int(date[2])
        year = now.year
        month = now.month
        day = now.day
        if date_day <= day :
            if date_month <= month :
                year = year - date_year
                month = month - date_month
            else :
                year = (year - 1) - date_year
                month = 12 - (date_month - month)
            day = day - date_day
        else :
            if date_month >= month :
                year = (year - 1) - date_year
                month = 11 - (date_month - month)
            else:
                year = year - date_year
                month = (month - 1) - date_month
            day = 32 - (date_day - day)
        work_year  =year
        work_month = month
        work_date  = day

        try:
            old_grade = data_new['old_grade']
        except Exception as e:
            old_grade = ''
        try:
            star_date_kpi = data_new['star_date_kpi']
        except Exception as e:
            star_date_kpi = ''
        try:
            group_kpi = data_new['group_kpi']
        except Exception as e:
            group_kpi = ''
        try:
            structure_salary = data_new['structure_salary']
        except Exception as e:
            structure_salary = ''

        # sqlIn_be = "INSERT INTO employee_kpi_approve(year,term,companyid,em_id_leader,structure_salary,employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,group_kpi,star_date_kpi,status,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # cursor.execute(sqlIn_be,(data_new['year'],data_new['term'],data_new['companyid'],result_test[0]['employeeid'],structure_salary,employeeid,data_new['name'],data_new['surname'],data_new['org_name'],data_new['position'],work_date,work_month,work_year,old_grade,group_kpi,star_date_kpi,data_new['status'],data_new['createby']))

        if(str(data_new['type'])=='main'):

            type_action = "ADD"
            print result_test[0]['employeeid']
            sqlIn_be = "INSERT INTO employee_kpi(year,term,companyid,em_id_leader,structure_salary,employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,group_kpi,star_date_kpi,status,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_be,(data_new['year'],data_new['term'],data_new['companyid'],result_test[0]['employeeid'],structure_salary,employeeid,data_new['name'],data_new['surname'],data_new['org_name'],data_new['position'],work_date,work_month,work_year,old_grade,group_kpi,star_date_kpi,data_new['status'],data_new['createby']))

            sqlIn_be2 = "INSERT INTO employee_kpi_log(year,term,companyid,em_id_leader,structure_salary,employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,group_kpi,star_date_kpi,status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_be2,(data_new['year'],data_new['term'],data_new['companyid'],result_test[0]['employeeid'],structure_salary,employeeid,data_new['name'],data_new['surname'],data_new['org_name'],data_new['position'],work_date,work_month,work_year,old_grade,group_kpi,star_date_kpi,data_new['status'],data_new['createby'],type_action))
        else:
            sqlIn_be = "INSERT INTO employee_kpi_approve(year,term,companyid,em_id_leader,structure_salary,employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,group_kpi,star_date_kpi,status,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_be,(data_new['year'],data_new['term'],data_new['companyid'],result_test[0]['employeeid'],structure_salary,employeeid,data_new['name'],data_new['surname'],data_new['org_name'],data_new['position'],work_date,work_month,work_year,old_grade,group_kpi,star_date_kpi,data_new['status'],data_new['createby']))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/UpdateApprove_kpi', methods=['POST'])
@connect_sql()
def UpdateApprove_kpi(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        i=0
        for i in xrange(len(data_new['employee'])):

            sqlUp_main = "UPDATE employee_kpi_approve SET validstatus=2 WHERE employeeid=%s AND year=%s AND term=%s"
            cursor.execute(sqlUp_main,(data_new['employee'][i]['employeeid'],data_new['employee'][i]['year'],data_new['employee'][i]['term']))

            sql = "SELECT * FROM employee_kpi_approve WHERE employeeid=%s AND year=%s AND term=%s"
            cursor.execute(sql,(data_new['employee'][i]['employeeid'],data_new['employee'][i]['year'],data_new['employee'][i]['term']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

            type_action = "ADD"

            sqlIn_be = "INSERT INTO employee_kpi(year,term,companyid,em_id_leader,structure_salary,employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,group_kpi,star_date_kpi,status,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_be,(result[0]['year'],result[0]['term'],result[0]['companyid'],result[0]['createby'],result[0]['structure_salary'],result[0]['employeeid'],result[0]['name'],result[0]['surname'],result[0]['org_name'],result[0]['position'],result[0]['work_date'],result[0]['work_month'],result[0]['work_year'],result[0]['old_grade'],result[0]['group_kpi'],result[0]['star_date_kpi'],result[0]['status'],data_new['createby']))

            sqlIn_be2 = "INSERT INTO employee_kpi_log(year,term,companyid,em_id_leader,structure_salary,employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,group_kpi,star_date_kpi,status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_be2,(result[0]['year'],result[0]['term'],result[0]['companyid'],result[0]['createby'],result[0]['structure_salary'],result[0]['employeeid'],result[0]['name'],result[0]['surname'],result[0]['org_name'],result[0]['position'],result[0]['work_date'],result[0]['work_month'],result[0]['work_year'],result[0]['old_grade'],result[0]['group_kpi'],result[0]['star_date_kpi'],result[0]['status'],data_new['createby'],type_action))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Update_Not_Approve_kpi', methods=['POST'])
@connect_sql()
def Update_Not_Approve_kpi(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        i=0
        for i in xrange(len(data_new['employee'])):

            sqlUp_main = "UPDATE employee_kpi_approve SET validstatus=3 WHERE employeeid=%s AND year=%s term=%s"
            cursor.execute(sqlUp_main,(data_new['employee'][i]['employeeid'],data_new['employee'][i]['year'],data_new['employee'][i]['term']))

            try:
                sqlUp = "DELETE FROM employee_kpi WHERE  WHERE employeeid=%s AND year=%s term=%s"
                cursor.execute(sqlUp,(data_new['employee'][i]['employeeid'],data_new['employee'][i]['year'],data_new['employee'][i]['term']))
            except Exception as e:
                pass

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryApprove_kpi', methods=['POST'])
@connect_sql()
def QryApprove_kpi(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT employee_kpi_approve.term,employee_kpi_approve.year,employee_kpi_approve.employeeid,employee_kpi_approve.name,employee_kpi_approve.surname,assessor_kpi.name_asp,assessor_kpi.surname_asp,employee_kpi_approve.validstatus FROM employee_kpi_approve\
                                LEFT JOIN assessor_kpi ON employee_kpi_approve.em_id_leader = assessor_kpi.employeeid\
        WHERE employee_kpi_approve.em_id_leader =%s AND employee_kpi_approve.validstatus=1 "
        cursor.execute(sql,(data_new['em_id_leader']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryApprove_kpi_result', methods=['POST'])
@connect_sql()
def QryApprove_kpi_result(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT employee_kpi_approve.term,employee_kpi_approve.year,employee_kpi_approve.employeeid,employee_kpi_approve.name,employee_kpi_approve.surname,assessor_kpi.name_asp,assessor_kpi.surname_asp,employee_kpi_approve.validstatus FROM employee_kpi_approve\
                                LEFT JOIN assessor_kpi ON employee_kpi_approve.em_id_leader = assessor_kpi.employeeid\
        WHERE employee_kpi_approve.em_id_leader =%s AND employee_kpi_approve.validstatus IN (2,3)"
        cursor.execute(sql,(data_new['em_id_leader']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryApprove_kpi_status', methods=['POST'])
@connect_sql()
def QryApprove_kpi_status(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT employee_kpi_approve.term,employee_kpi_approve.year,employee_kpi_approve.employeeid,employee_kpi_approve.name,employee_kpi_approve.surname,assessor_kpi.name_asp,assessor_kpi.surname_asp,employee_kpi_approve.validstatus FROM employee_kpi_approve\
                                LEFT JOIN assessor_kpi ON employee_kpi_approve.createby = assessor_kpi.employeeid\
        WHERE employee_kpi_approve.createby = %s"
        cursor.execute(sql,(data_new['createby']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Edit_emp_kpi', methods=['POST'])
@connect_sql()
def Edit_emp_kpi(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        employeeid = data_new['employeeid']

        sql = "SELECT * FROM employee_kpi WHERE employeeid=%s AND year=%s AND term=%s"
        cursor.execute(sql,(data_new['employeeid'],data_new['old_year'],data_new['old_term']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sql44 = "SELECT employeeid FROM assessor_kpi WHERE companyid=%s AND org_name_id=%s AND type='main'"
        cursor.execute(sql44,(data_new['companyid'],data_new['org_name']))
        columns = [column[0] for column in cursor.description]
        result_test = toJson(cursor.fetchall(),columns)

        try:
            old_grade = data_new['old_grade']
        except Exception as e:
            old_grade = ''
        try:
            star_date_kpi = data_new['star_date_kpi']
        except Exception as e:
            star_date_kpi = ''
        try:
            group_kpi = data_new['group_kpi']
        except Exception as e:
            group_kpi = ''
        try:
            structure_salary = data_new['structure_salary']
        except Exception as e:
            structure_salary = ''

        type_action = "Edit"

        sqlIn_be2 = "INSERT INTO employee_kpi_log(year,term,companyid,em_id_leader,structure_salary,employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,group_kpi,star_date_kpi,status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_be2,(result[0]['year'],result[0]['term'],result[0]['companyid'],result_test[0]['employeeid'],result[0]['structure_salary'],employeeid,result[0]['name'],result[0]['surname'],result[0]['org_name'],result[0]['position'],result[0]['work_date'],result[0]['work_month'],result[0]['work_year'],result[0]['old_grade'],result[0]['group_kpi'],result[0]['star_date_kpi'],result[0]['status'],result[0]['createby'],type_action))

        sqlI9de = "DELETE FROM employee_kpi WHERE employeeid=%s AND year=%s AND term=%s"
        cursor.execute(sqlI9de,(data_new['employeeid'],data_new['old_year'],data_new['old_term']))

        sqlIn_be = "INSERT INTO employee_kpi(year,term,companyid,em_id_leader,structure_salary,employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,group_kpi,star_date_kpi,status,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_be,(data_new['year'],data_new['term'],data_new['companyid'],result_test[0]['employeeid'],data_new['structure_salary'],employeeid,data_new['name'],data_new['surname'],data_new['org_name'],data_new['position'],result[0]['work_date'],result[0]['work_month'],result[0]['work_year'],old_grade,group_kpi,star_date_kpi,data_new['status'],data_new['createby']))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Delete_emp_kpi', methods=['POST'])
@connect_sql()
def Delete_emp_kpi(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        employeeid = data_new['employeeid']

        sql = "SELECT * FROM employee_kpi WHERE employeeid=%s AND year=%s AND term=%s"
        cursor.execute(sql,(data_new['employeeid'],data_new['year'],data_new['term']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Delete"

        sqlIn_be2 = "INSERT INTO employee_kpi_log(year,term,companyid,em_id_leader,structure_salary,employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,group_kpi,star_date_kpi,status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_be2,(result[0]['year'],result[0]['term'],result[0]['companyid'],result[0]['employeeid'],result[0]['structure_salary'],employeeid,result[0]['name'],result[0]['surname'],result[0]['org_name'],result[0]['position'],result[0]['work_date'],result[0]['work_month'],result[0]['work_year'],result[0]['old_grade'],result[0]['group_kpi'],result[0]['star_date_kpi'],result[0]['status'],result[0]['createby'],type_action))

        sqlI9de = "DELETE FROM employee_kpi WHERE employeeid=%s AND year=%s AND term=%s"
        cursor.execute(sqlI9de,(data_new['employeeid'],data_new['year'],data_new['term']))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Update_grade_hr_board', methods=['POST'])
@connect_sql()
def Update_grade_hr_board(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        comment_hr = data_new['comment_hr']
        permission_hr = str(data_new['permission'])
        if permission_hr!="HrBoard":
            return "hr no permission"
        sql = "SELECT employeeid,grade,comment_hr FROM employee_kpi WHERE employeeid=%s AND year=%s AND term=%s"
        cursor.execute(sql,(data_new['employeeid'],data_new['year'],data_new['term']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        grade_ = str(result[0]['grade'])
        if grade_ is None:
            type_action = "Edit"
            commet_hr_edit = str(result[0]['comment_hr'])
            sqlIn_be2 = "INSERT INTO answer_kpi_hr_log(year,term,employeeid,grade,comment_hr,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_be2,(data_new['year'],data_new['term'],[0]['employeeid'],grade_,commet_hr_edit,result[0]['createby'],type_action))
        else:
            type_action = "Insert"
            sqlIn_be1 = "INSERT INTO answer_kpi_hr_log(year,term,employeeid,grade,comment_hr,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_be1,(data_new['year'],data_new['term'],data_new['employeeid'],data_new['grade'],comment_hr,data_new['createby'],type_action))

        sqlUp = "UPDATE employee_kpi SET grade=%s,pass_hr=%s,comment_hr=%s WHERE employeeid=%s AND year=%s AND term=%s"
        cursor.execute(sqlUp,(data_new['grade'],data_new['pass_hr'],comment_hr,data_new['employeeid'],data_new['year'],data_new['term']))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Update_grade_hr_hall', methods=['POST'])
@connect_sql()
def Update_grade_hr_hall(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        comment_hr = data_new['comment_hr']
        permission_hr = str(data_new['permission'])
        if permission_hr!="HrHall":
            return "hr no permission"
        sql = "SELECT employeeid,grade,comment_hr FROM employee_kpi WHERE employeeid=%s AND year=%s AND term=%s"
        cursor.execute(sql,(data_new['employeeid'],data_new['year'],data_new['term']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        grade_ = str(result[0]['grade'])
        if grade_ is None:
            type_action = "Edit"
            commet_hr_edit = str(result[0]['comment_hr'])
            sqlIn_be2 = "INSERT INTO answer_kpi_hr_log(year,term,employeeid,grade,comment_hr,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_be2,(data_new['year'],data_new['term'],result[0]['employeeid'],grade_,commet_hr_edit,result[0]['createby'],type_action))
        else:
            type_action = "Insert"
            sqlIn_be1 = "INSERT INTO answer_kpi_hr_log(year,term,employeeid,grade,comment_hr,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_be1,(data_new['year'],data_new['term'],data_new['employeeid'],data_new['grade'],comment_hr,data_new['createby'],type_action))

        sqlUp = "UPDATE employee_kpi SET grade=%s,pass_hr=%s,comment_hr=%s WHERE employeeid=%s AND year=%s AND term=%s"
        cursor.execute(sqlUp,(data_new['grade'],data_new['pass_hr'],comment_hr,data_new['employeeid'],data_new['year'],data_new['term']))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qry_board_kpi', methods=['POST'])
@connect_sql()
def Qry_board_kpi(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        year_term = "WHERE employeeid="+data_new['employeeid']+""
        try:
            year_term = "WHERE employeeid="+data_new['employeeid']+" AND year="+data_new['year']+" AND term="+data_new['term']+""
        except Exception as e:
            pass

        sql = "SELECT createby,year,term,employeeid,employeeid_board,name_kpi,surname_kpi,org_name_kpi,grade_board,comment,grade FROM employee_kpi "+year_term+""
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qry_em_board_kpi', methods=['POST'])
@connect_sql()
def Qry_em_board_kpi(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT term,year,employeeid,employeeid_board,name_kpi,surname_kpi,position_kpi FROM board_kpi WHERE employeeid=%s AND year=%s AND term=%s AND validstatus=1"
        cursor.execute(sql,(data_new['employeeid'],data_new['year'],data_new['term']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qry_user_kpi_no_emid_leader', methods=['POST'])
@connect_sql()
def Qry_user_kpi_no_emid_leader(cursor):
    try:
        # dataInput = request.json
        # source = dataInput['source']
        # data_new = source
        sql = "SELECT employee_kpi.createby,employee_kpi.comment_cancel,employee_kpi.year,employee_kpi.term,employee_kpi.employeeid,employee_kpi.name,company.company_short_name,employee_kpi.surname,org_name.org_name_detail,position.position_detail,employee_kpi.work_date,employee_kpi.work_month,employee_kpi.work_year,employee_kpi.old_grade,employee_kpi.grade,employee_kpi.comment_hr,employee_kpi.group_kpi,employee_kpi.star_date_kpi,employee_kpi.status FROM employee_kpi\
                                                                                        INNER JOIN company ON employee_kpi.companyid = company.companyid\
                                                                                        INNER JOIN org_name ON employee_kpi.org_name = org_name.org_name_id\
                                                                                        INNER JOIN position ON employee_kpi.position = position.position_id\
        WHERE employee_kpi.em_id_leader IS NULL"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/update_user_kpi_no_emid_leader', methods=['POST'])
@connect_sql()
def update_user_kpi_no_emid_leader(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        if str(data_new['type'])=='main':
            try:
                sql_check_2 = "SELECT employeeid FROM assessor_kpi WHERE employeeid=%s AND companyid=%s AND org_name_id=%s"
                cursor.execute(sql_check_2,(data_new['em_id_leader'],data_new['companyid'],data_new['org_name_id']))
                columns = [column[0] for column in cursor.description]
                result_check_2 = toJson(cursor.fetchall(),columns)
                name_check_2 = result_check_2[0]['employeeid']
            except Exception as e:
                try:
                    sql44 = "SELECT name_asp FROM assessor_kpi WHERE companyid=%s AND org_name_id=%s AND type='main'"
                    cursor.execute(sql44,(data_new['companyid'],data_new['org_name_id']))
                    columns = [column[0] for column in cursor.description]
                    result_test = toJson(cursor.fetchall(),columns)
                    name_test = result_test[0]['name_asp']
                    return "main more one"
                except Exception as e:
                    try:
                        sql44 = "SELECT name_asp FROM assessor_kpi WHERE companyid=%s AND employeeid=%s AND org_name_id=%s"
                        cursor.execute(sql44,(data_new['companyid'],data_new['em_id_leader'],data_new['org_name_id']))
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
                        sql = "INSERT INTO assessor_kpi (assessor_kpi_id,employeeid,companyid,name_asp,surname_asp,org_name_id,email_asp,createby,type) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        cursor.execute(sql,(assessor_kpi_id_last,data_new['em_id_leader'],data_new['companyid'],data_new['name_asp'],data_new['surname_asp'],data_new['org_name_id'],data_new['email_asp'],data_new['createby'],data_new['type']))
        else:
            try:
                sql44 = "SELECT name_asp FROM assessor_kpi WHERE companyid=%s AND employeeid=%s AND org_name_id=%s"
                cursor.execute(sql44,(data_new['companyid'],data_new['em_id_leader'],data_new['org_name_id']))
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
                cursor.execute(sql,(assessor_kpi_id_last,data_new['em_id_leader'],data_new['companyid'],data_new['name_asp'],data_new['surname_asp'],data_new['org_name_id'],data_new['email_asp'],data_new['createby'],type))


        sqlUp_main = "UPDATE employee_kpi SET em_id_leader=%s,validstatus=1 WHERE employeeid=%s AND year=%s AND term=%s"
        cursor.execute(sqlUp_main,(data_new['em_id_leader'],data_new['employeeid'],data_new['year'],data_new['term']))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qry_user_kpi', methods=['POST'])
@connect_sql()
def Qry_user_kpi(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT employee_kpi.createby,employee_kpi.comment_cancel,employee_kpi.year,employee_kpi.term,employee_kpi.employeeid,employee_kpi.name,company.company_short_name,employee_kpi.surname,org_name.org_name_detail,position.position_detail,employee_kpi.work_date,employee_kpi.work_month,employee_kpi.work_year,employee_kpi.old_grade,employee_kpi.grade,employee_kpi.comment_hr,employee_kpi.group_kpi,employee_kpi.star_date_kpi,employee_kpi.status FROM employee_kpi\
                                                                                        INNER JOIN company ON employee_kpi.companyid = company.companyid\
                                                                                        INNER JOIN org_name ON employee_kpi.org_name = org_name.org_name_id\
                                                                                        INNER JOIN position ON employee_kpi.position = position.position_id"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qry_user_kpi_board', methods=['POST'])
@connect_sql()
def Qry_user_kpi_board(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        # year_term = "WHERE employee_kpi.em_id_leader="+'"'+str(data_new['em_id_leader'])+'"'

        if (str(data_new['type'])=='main')and(str(data_new['companyid'])!='23'):

            try:
                year_term = "WHERE employee_kpi.companyid="+"'"+str(data_new['companyid'])+"'"+' AND employee_kpi.year='+'"'+str(data_new['year'])+'"'+'AND employee_kpi.term='+'"'+str(data_new['term'])+'"'+' OR employee_kpi.em_id_leader='+'"'+str(data_new['em_id_leader'])+'"'
            except Exception as e:
                year_term = "WHERE employee_kpi.companyid="+"'"+str(data_new['companyid'])+"'"+' OR employee_kpi.em_id_leader='+'"'+str(data_new['em_id_leader'])+'"'

            sql = "SELECT employee_kpi.validstatus,employee_kpi.em_id_leader,employee_kpi.newKpiDescriptions_GM,employee_kpi.specialMoney_GM,employee_kpi.positionChange_GM,employee_kpi.status_GM,employee_kpi.old_grade_GM,employee_kpi.createby,employee_kpi.comment_cancel,employee_kpi.year,employee_kpi.term,employee_kpi.employeeid,employee_kpi.name,employee_kpi.companyid AS company_short_name,employee_kpi.surname,org_name.org_name_detail,position.position_detail,employee_kpi.work_date,employee_kpi.work_month,employee_kpi.work_year,employee_kpi.old_grade,employee_kpi.grade,employee_kpi.comment_hr,employee_kpi.group_kpi,employee_kpi.star_date_kpi,employee_kpi.status FROM employee_kpi\
                                                                                            INNER JOIN org_name ON employee_kpi.org_name = org_name.org_name_id\
                                                                                            INNER JOIN position ON employee_kpi.position = position.position_id\
            "+year_term+" GROUP BY employee_kpi.employeeid"
            cursor.execute(sql)
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            for i1 in result:
                sql2 = "SELECT company_short_name FROM company WHERE companyid=%s"
                cursor.execute(sql2,(i1['company_short_name']))
                columns = [column[0] for column in cursor.description]
                data2 = toJson(cursor.fetchall(),columns)
                i1['company_short_name'] = data2[0]['company_short_name']
            return jsonify(result)

        elif (str(data_new['type'])=='main')and(str(data_new['companyid'])=='23'):
            try:
                year_term = "WHERE employee_kpi.companyid="+"'"+str(data_new['companyid'])+"'"+' AND employee_kpi.org_name LIKE'+'"'+'%'+str(data_new['org_name_id'])+'%'+'"'+' AND employee_kpi.year='+'"'+str(data_new['year'])+'"'+'AND employee_kpi.term='+'"'+str(data_new['term'])+'"'+' OR employee_kpi.em_id_leader='+'"'+str(data_new['em_id_leader'])+'"'
            except Exception as e:
                year_term = "WHERE employee_kpi.companyid="+"'"+str(data_new['companyid'])+"'"+' AND employee_kpi.org_name='+'"'+str(data_new['org_name_id'])+'"'+' OR employee_kpi.em_id_leader='+'"'+str(data_new['em_id_leader'])+'"'
            sql = "SELECT employee_kpi.validstatus,employee_kpi.em_id_leader,employee_kpi.newKpiDescriptions_GM,employee_kpi.specialMoney_GM,employee_kpi.positionChange_GM,employee_kpi.status_GM,employee_kpi.old_grade_GM,employee_kpi.createby,employee_kpi.comment_cancel,employee_kpi.year,employee_kpi.term,employee_kpi.employeeid,employee_kpi.name,employee_kpi.companyid AS company_short_name,employee_kpi.surname,org_name.org_name_detail,position.position_detail,employee_kpi.work_date,employee_kpi.work_month,employee_kpi.work_year,employee_kpi.old_grade,employee_kpi.grade,employee_kpi.comment_hr,employee_kpi.group_kpi,employee_kpi.star_date_kpi,employee_kpi.status FROM employee_kpi\
                                                                                            INNER JOIN org_name ON employee_kpi.org_name = org_name.org_name_id\
                                                                                            INNER JOIN position ON employee_kpi.position = position.position_id\
            "+year_term+" GROUP BY employee_kpi.employeeid"
            cursor.execute(sql)
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            for i1 in result:
                sql2 = "SELECT company_short_name FROM company WHERE companyid=%s"
                cursor.execute(sql2,(i1['company_short_name']))
                columns = [column[0] for column in cursor.description]
                data2 = toJson(cursor.fetchall(),columns)
                i1['company_short_name'] = data2[0]['company_short_name']
            return jsonify(result)

        else:
            try:
                year_term = "WHERE employee_kpi.em_id_leader="+'"'+str(data_new['em_id_leader'])+'"'+' AND employee_kpi.year='+'"'+str(data_new['year'])+'"'+'AND employee_kpi.term='+'"'+str(data_new['term'])+'"'
            except Exception as e:
                year_term = "WHERE employee_kpi.em_id_leader="+'"'+str(data_new['em_id_leader'])+'"'

            sql = "SELECT employee_kpi.validstatus,employee_kpi.em_id_leader,employee_kpi.newKpiDescriptions_GM,employee_kpi.specialMoney_GM,employee_kpi.positionChange_GM,employee_kpi.status_GM,employee_kpi.old_grade_GM,employee_kpi.createby,employee_kpi.comment_cancel,employee_kpi.year,employee_kpi.term,employee_kpi.employeeid,employee_kpi.name,employee_kpi.companyid AS company_short_name,employee_kpi.surname,org_name.org_name_detail,position.position_detail,employee_kpi.work_date,employee_kpi.work_month,employee_kpi.work_year,employee_kpi.old_grade,employee_kpi.grade,employee_kpi.comment_hr,employee_kpi.group_kpi,employee_kpi.star_date_kpi,employee_kpi.status FROM employee_kpi\
                                                                                            INNER JOIN org_name ON employee_kpi.org_name = org_name.org_name_id\
                                                                                            INNER JOIN position ON employee_kpi.position = position.position_id\
            "+year_term+" GROUP BY employee_kpi.employeeid"
            cursor.execute(sql)
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            for i1 in result:
                sql2 = "SELECT company_short_name FROM company WHERE companyid=%s"
                cursor.execute(sql2,(i1['company_short_name']))
                columns = [column[0] for column in cursor.description]
                data2 = toJson(cursor.fetchall(),columns)
                i1['company_short_name'] = data2[0]['company_short_name']
            return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Add_board_kpi', methods=['POST'])
@connect_sql()
def Add_board_kpi(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        employeeid = str(data_new['employeeid'])
        check_board = str(data_new['employeeid_board'])
        if employeeid==check_board:
            return "employee is board"

        type_action = "ADD"

        try:
            sql44 = "SELECT employeeid FROM board_kpi WHERE employeeid=%s AND employeeid_board=%s AND year=%s AND term=%s AND validstatus=1"
            cursor.execute(sql44,(employeeid,data_new['employeeid_board'],data_new['year'],data_new['term']))
            columns = [column[0] for column in cursor.description]
            result_check_em_board = toJson(cursor.fetchall(),columns)
            check_em_board = result_check_em_board[0]['employeeid']
            return "employee is duplicate"
        except Exception as e:
            pass
        try:
            permission = "board"
            # for i in xrange(len(data_new['emp_board'])):
            sql = "SELECT username FROM Admin WHERE employeeid=%s"
            cursor.execute(sql,(data_new['employeeid_board']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            check_email = result[0]['username']
        except Exception as e:
            permission = "board"
            # for i in xrange(len(data_new['emp_board'])):
            name___ = data_new['name_kpi']+' '+data_new['surname_kpi']
            sqlIn_bet2 = "INSERT INTO Admin(employeeid,username,name,permission,createby) VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_bet2,(data_new['employeeid_board'],data_new['username'],name___,permission,data_new['createby']))

        # for i in xrange(len(data_new['emp_board'])):
        sqlIn_be = "INSERT INTO board_kpi(year,term,employeeid,employeeid_board,name_kpi,surname_kpi,position_kpi,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_be,(data_new['year'],data_new['term'],employeeid,data_new['employeeid_board'],data_new['name_kpi'],data_new['surname_kpi'],data_new['position_kpi'],data_new['createby']))

        # for i in xrange(len(data_new['emp_board'])):
        sqlIn_be2 = "INSERT INTO board_kpi_log(year,term,employeeid,employeeid_board,name_kpi,surname_kpi,position_kpi,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_be2,(data_new['year'],data_new['term'],employeeid,data_new['employeeid_board'],data_new['name_kpi'],data_new['surname_kpi'],data_new['position_kpi'],data_new['createby'],type_action))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/board_qry', methods=['POST'])
@connect_sql()
def board_qry(cursor):
    try:
        sql = "SELECT year,term,employeeid_board,name,group_kpi FROM board_kpi_v2 WHERE validstatus=1 "
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/board_qry_search', methods=['POST'])
@connect_sql()
def board_qry_search(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT year,term,employeeid_board,name,group_kpi FROM board_kpi_v2 WHERE validstatus=1 AND year=%s AND term=%s "
        cursor.execute(sql,(data_new['year'],data_new['term']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Add_board_kpi_no_result', methods=['POST'])
@connect_sql()
def Add_board_kpi_no_result(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        employeeid = data_new['employeeid_board']

        nameKpi__ = str(data_new['name_kpi'])+" "+str(data_new['surname_kpi'])

        try:
            sql_check_board = "SELECT year,term,employeeid_board FROM board_kpi_v2 WHERE employeeid_board=%s AND group_kpi=%s AND validstatus=1 AND year=%s AND term=%s "
            cursor.execute(sql_check_board,(data_new['employeeid_board'],data_new['group_kpi_id'],data_new['year'],data_new['term']))
            columns = [column[0] for column in cursor.description]
            result_check_board = toJson(cursor.fetchall(),columns)
            test_check_board = result_check_board[0]['employeeid_board']
            return "employee board is duplicate"
        except Exception as e:
            pass

        sql_be = "INSERT INTO board_kpi_v2(year,term,employeeid_board,name,group_kpi,createby) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_be,(data_new['year'],data_new['term'],data_new['employeeid_board'],nameKpi__,data_new['group_kpi_id'],data_new['createby']))

        try:
            permission = data_new['group_kpi_id']
            # for i in xrange(len(data_new['emp_board'])):
            sql_test_admin = "SELECT username FROM Admin WHERE employeeid=%s"
            cursor.execute(sql_test_admin,(employeeid))
            columns = [column[0] for column in cursor.description]
            result_test_admin = toJson(cursor.fetchall(),columns)
            check_email = result_test_admin[i]['username']
        except Exception as e:
            permission = data_new['group_kpi_id']
            sql = "INSERT INTO Admin (employeeid,username,name,permission,createby) VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(sql,(data_new['employeeid_board'],data_new['username'],nameKpi__,permission,data_new['createby']))

        group_kpi_id = "WHERE year="+data_new['year']+" AND term="+data_new['term']+""
        try:
            group_ = str(data_new['group_kpi_id'])
            group_kpi_id = 'WHERE group_kpi='+'"'+group_+'"'+'AND year='+'"'+data_new['year']+'"'+'AND term='+'"'+data_new['term']+'"'
        except Exception as e:
            pass
        try:
            sql_emp_kpi = "SELECT employee_kpi.year,employee_kpi.term,employee_kpi.employeeid FROM employee_kpi INNER JOIN board_kpi ON employee_kpi.employeeid = board_kpi.employeeid "+group_kpi_id+" AND employee_kpi.grade IS NULL AND board_kpi.validstatus=1 GROUP BY board_kpi.employeeid"
            cursor.execute(sql_emp_kpi)
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            check_emid = result[0]['employeeid']
        except Exception as e:
            sql_emp_kpi = "SELECT year,term,employeeid FROM employee_kpi "+group_kpi_id+" "
            cursor.execute(sql_emp_kpi)
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)

        type_action = "ADD"

        for i in xrange(len(result)):
            check_em_id = str(result[i]['employeeid'])
            check_em_board = str(data_new['employeeid_board'])
            if check_em_id==check_em_board:
                pass
            else:
                sqlIn_bet = "INSERT INTO board_kpi(year,term,employeeid,employeeid_board,name_kpi,surname_kpi,position_kpi,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn_bet,(result[i]['year'],result[i]['term'],result[i]['employeeid'],data_new['employeeid_board'],data_new['name_kpi'],data_new['surname_kpi'],data_new['position_kpi'],data_new['createby']))

        for i in xrange(len(result)):
            check_em_id = str(result[i]['employeeid'])
            check_em_board = str(data_new['employeeid_board'])
            if check_em_id==check_em_board:
                type_action = "Copy_board"
                sqlIn_be_2 = "INSERT INTO board_kpi_log(year,term,employeeid,employeeid_board,name_kpi,surname_kpi,position_kpi,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn_be_2,(result[i]['year'],result[i]['term'],result[i]['employeeid'],data_new['employeeid_board'],data_new['name_kpi'],data_new['surname_kpi'],data_new['position_kpi'],data_new['createby'],type_action))
            else:
                sqlIn_be_2 = "INSERT INTO board_kpi_log(year,term,employeeid,employeeid_board,name_kpi,surname_kpi,position_kpi,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn_be_2,(result[i]['year'],result[i]['term'],result[i]['employeeid'],data_new['employeeid_board'],data_new['name_kpi'],data_new['surname_kpi'],data_new['position_kpi'],data_new['createby'],type_action))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Delete_board_kpi_no_result', methods=['POST'])
@connect_sql()
def Delete_board_kpi_no_result(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sqlUp = "UPDATE board_kpi_v2 SET validstatus=0 WHERE employeeid_board=%s AND group_kpi=%s AND year=%s AND term=%s"
        cursor.execute(sqlUp,(data_new['employeeid_board'],data_new['group_kpi'],data_new['year'],data_new['term']))

        try:
            sqlDe = "DELETE FROM Admin WHERE employeeid=%s AND permission='board'"
            cursor.execute(sqlDe,(data_new['employeeid_board']))
        except Exception as e:
            pass

        sqlUp2 = "UPDATE board_kpi SET validstatus=0 WHERE employeeid_board=%s AND grade_board IS NULL OR pass_board IS NULL AND year=%s AND term=%s "
        cursor.execute(sqlUp2,(data_new['employeeid_board'],data_new['year'],data_new['term']))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Delete_board_kpi', methods=['POST'])
@connect_sql()
def Delete_board_kpi(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT * FROM board_kpi WHERE employeeid=%s AND employeeid_board=%s AND validstatus=1 AND year=%s AND term=%s"
        cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_board'],data_new['year'],data_new['term']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Delete"

        sqlIn_be2 = "INSERT INTO board_kpi_log(year,term,employeeid,employeeid_board,name_kpi,surname_kpi,position_kpi,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_be2,(data_new['year'],data_new['term'],result[0]['employeeid'],result[0]['employeeid_board'],result[0]['name_kpi'],result[0]['surname_kpi'],result[0]['position_kpi'],data_new['createby'],type_action))

        sqlde = "UPDATE board_kpi SET validstatus=0 WHERE employeeid=%s AND employeeid_board=%s AND year=%s AND term=%s"
        cursor.execute(sqlde,(data_new['employeeid'],data_new['employeeid_board'],data_new['year'],data_new['term']))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Update_board_kpi', methods=['POST'])
@connect_sql()
def Update_board_kpi(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        employeeid__ = str(data_new['employeeid'])
        check_board = str(data_new['employeeid_board'])
        if employeeid__==check_board:
            return "employee is board"
        sql = "SELECT employeeid,employeeid_board,grade_board,comment FROM board_kpi WHERE employeeid=%s AND employeeid_board=%s AND year=%s AND term=%s AND validstatus=1"
        cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_board'],data_new['year'],data_new['term']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        # print (result)
        # try:
        #     grade_board = str(result[0]['grade_board'])
        # except Exception as e:
        #     grade_board = None
        # grade_board = str(result[0]['grade_board'])
        if result is None:
            # grade_board = ''
            type_action = "Edit"
            sqlIn_be2 = "INSERT INTO answer_kpi_log(year,term,employeeid,employeeid_board,grade_board,comment,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_be2,(data_new['year'],data_new['term'],result[0]['employeeid'],result[0]['employeeid_board'],result[0]['grade_board'],result[0]['comment'],data_new['createby'],type_action))
        else:
            type_action = "Insert"
            sqlIn_be1 = "INSERT INTO answer_kpi_log(year,term,employeeid,employeeid_board,grade_board,comment,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_be1,(data_new['year'],data_new['term'],data_new['employeeid'],data_new['employeeid_board'],data_new['grade_board'],data_new['comment'],data_new['createby'],type_action))
        try:
            comment_board = str(data_new['comment'])
        except Exception as e:
            comment_board = ''

        sqlUp = "UPDATE board_kpi SET grade_board=%s,pass_board=%s,comment=%s WHERE employeeid=%s AND employeeid_board=%s AND year=%s AND term=%s AND validstatus=1"
        cursor.execute(sqlUp,(data_new['grade_board'],data_new['pass_board'],comment_board,data_new['employeeid'],data_new['employeeid_board'],data_new['year'],data_new['term']))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
# @app.route('/upload_user_kpi_one', methods=['POST'])
# @connect_sql()
# def upload_user_kpi_one(cursor):
#     try:
#         employeeid = request.form['employeeid']
#         Type = 'kpi'
#         try:
#             sqlDe = "DELETE FROM employee_upload WHERE employeeid=%s"
#             cursor.execute(sqlDe,(request.form['employeeid']))
#         except Exception as e:
#             pass
#         path = 'uploads/'+employeeid+'/'+'kpi'
#         path2 = employeeid+'/'+'kpi'
#         if not os.path.exists(path):
#             os.makedirs(path)
#         if request.method == 'POST':
#             file = request.files['file']
#         if file:
#             file.save(os.path.join(path, employeeid + 'kpi.png'))
#             PathFile = path2+'/'+employeeid + 'kpi.png'
#             fileName = employeeid + 'kpi.png'
#         else:
#             return 'file is not allowed'
#
#         sql = "INSERT INTO employee_upload_kpi(employeeid,FileName,Type,PathFile,createby) VALUES (%s,%s,%s,%s,%s)"
#         cursor.execute(sql,(employeeid,fileName,Type,PathFile,request.form['createby']))
#
#         return "success"
#     except Exception as e:
#         logserver(e)
#         return "fail"
# @app.route('/Qry_upload_kpi_one', methods=['POST'])
# @connect_sql()
# def Qry_upload_kpi_one(cursor):
#     try:
#         dataInput = request.json
#         source = dataInput['source']
#         data_new = source
#
#         sql = "SELECT employeeid,FileName,Type,PathFile FROM employee_upload_kpi WHERE employeeid=%s "
#         cursor.execute(sql,(data_new['employeeid']))
#         columns = [column[0] for column in cursor.description]
#         result = toJson(cursor.fetchall(),columns)
#         for item_ in result:
#             img_base64 = []
#             item_['PathFile'] = '../app/uploads/'+str(item_['PathFile'])
#             tranImage = item_['PathFile']
#             with open(tranImage, 'rb') as image_file:
#                 encoded_Image = base64.b64encode(image_file.read())
#             item_['img_base64'] = encoded_Image
#         return jsonify(result)
#     except Exception as e:
#         logserver(e)
#         return "fail"
@app.route('/Export_kpi', methods=['POST'])
@connect_sql()
def Export_kpi(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        try:
            sql = "SELECT employee_kpi.year,employee_kpi.term,employee_kpi.employeeid,employee_kpi.name,employee_kpi.surname,org_name.org_name_detail AS org_name,position.position_detail AS position,employee_kpi.work_date,employee_kpi.work_month,employee_kpi.work_year,employee_kpi.old_grade,employee_kpi.grade,employee_kpi.comment_hr,employee_kpi.group_kpi,employee_kpi.star_date_kpi,employee_kpi.status FROM employee_kpi\
                                                                                INNER JOIN org_name ON employee_kpi.org_name = org_name.org_name_id\
                                                                                INNER JOIN position ON employee_kpi.position = position.position_id\
            WHERE employee_kpi.year=%s AND employee_kpi.term=%s AND employee_kpi.grade IS NOT NULL"
            cursor.execute(sql,(data_new['year'],data_new['term']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            for i1 in result:
                kpi_ful = []
                sql2 = "SELECT name_kpi,surname_kpi,grade_board,pass_board,comment FROM board_kpi WHERE employeeid=%s AND validstatus=1 AND year=%s AND term=%s"
                cursor.execute(sql2,(i1['employeeid'],data_new['year'],data_new['term']))
                columns = [column[0] for column in cursor.description]
                data2 = toJson(cursor.fetchall(),columns)
                for i2 in data2 :
                    kpi_ful.append(i2)
                i1['kpi_ful'] = kpi_ful
        except Exception as e:
            logserver(e)
            return "No_Data"
        isSuccess = True
        reasonCode = 200
        reasonText = ""
        now = datetime.now()
        datetimeStr = now.strftime('%Y%m%d_%H%M%S%f')
        filename_tmp = secure_filename('{}_{}'.format(datetimeStr, 'Template_kpi.xlsx'))

        wb = load_workbook('../app/Template/Template_kpi.xlsx')
        if len(result) > 0:

            sheet = wb['Sheet1']
            sheet['C'+str(2)] = data_new['year'] + '/' + data_new['term']
            offset = 4
            i = 0
            for i in xrange(len(result)):
                sheet['A'+str(offset + i)] = i+1
                sheet['B'+str(offset + i)] = result[i]['employeeid']
                sheet['C'+str(offset + i)] = result[i]['name']
                sheet['D'+str(offset + i)] = result[i]['surname']
                sheet['E'+str(offset + i)] = result[i]['org_name']
                sheet['F'+str(offset + i)] = result[i]['position']
                sheet['G'+str(offset + i)] = result[i]['work_date']
                sheet['H'+str(offset + i)] = result[i]['work_month']
                sheet['I'+str(offset + i)] = result[i]['work_year']
                sheet['J'+str(offset + i)] = result[i]['star_date_kpi']
                sheet['K'+str(offset + i)] = result[i]['group_kpi']
                sheet['L'+str(offset + i)] = result[i]['old_grade']
                sheet['M'+str(offset + i)] = result[i]['status']
                sheet['N'+str(offset + i)] = result[i]['grade']
                try:
                    sheet['O'+str(offset + i)] = result[i]['kpi_ful'][0]['name_kpi']+' '+result[i]['kpi_ful'][0]['surname_kpi']
                    sheet['P'+str(offset + i)] = result[i]['kpi_ful'][0]['grade_board']
                    sheet['Q'+str(offset + i)] = result[i]['kpi_ful'][0]['comment']
                except Exception as e:
                    pass
                try:
                    sheet['R'+str(offset + i)] = result[i]['kpi_ful'][1]['name_kpi']+' '+result[i]['kpi_ful'][1]['surname_kpi']
                    sheet['S'+str(offset + i)] = result[i]['kpi_ful'][1]['grade_board']
                    sheet['T'+str(offset + i)] = result[i]['kpi_ful'][1]['comment']
                except Exception as e:
                    pass
                try:
                    sheet['U'+str(offset + i)] = result[i]['kpi_ful'][2]['name_kpi']+' '+result[i]['kpi_ful'][2]['surname_kpi']
                    sheet['V'+str(offset + i)] = result[i]['kpi_ful'][2]['grade_board']
                    sheet['W'+str(offset + i)] = result[i]['kpi_ful'][2]['comment']
                except Exception as e:
                    pass
                try:
                    sheet['X'+str(offset + i)] = result[i]['kpi_ful'][3]['name_kpi']+' '+result[i]['kpi_ful'][3]['surname_kpi']
                    sheet['Y'+str(offset + i)] = result[i]['kpi_ful'][3]['grade_board']
                    sheet['Z'+str(offset + i)] = result[i]['kpi_ful'][3]['comment']
                except Exception as e:
                    pass
                try:
                    sheet['AA'+str(offset + i)] = result[i]['kpi_ful'][4]['name_kpi']+' '+result[i]['kpi_ful'][4]['surname_kpi']
                    sheet['AB'+str(offset + i)] = result[i]['kpi_ful'][4]['grade_board']
                    sheet['AC'+str(offset + i)] = result[i]['kpi_ful'][4]['comment']
                except Exception as e:
                    pass
                try:
                    sheet['AD'+str(offset + i)] = result[i]['kpi_ful'][5]['name_kpi']+' '+result[i]['kpi_ful'][5]['surname_kpi']
                    sheet['AE'+str(offset + i)] = result[i]['kpi_ful'][5]['grade_board']
                    sheet['AF'+str(offset + i)] = result[i]['kpi_ful'][5]['comment']
                except Exception as e:
                    pass
                try:
                    sheet['AG'+str(offset + i)] = result[i]['kpi_ful'][6]['name_kpi']+' '+result[i]['kpi_ful'][6]['surname_kpi']
                    sheet['AH'+str(offset + i)] = result[i]['kpi_ful'][6]['grade_board']
                    sheet['AI'+str(offset + i)] = result[i]['kpi_ful'][6]['comment']
                except Exception as e:
                    pass
                try:
                    sheet['AJ'+str(offset + i)] = result[i]['kpi_ful'][7]['name_kpi']+' '+result[i]['kpi_ful'][7]['surname_kpi']
                    sheet['AK'+str(offset + i)] = result[i]['kpi_ful'][7]['grade_board']
                    sheet['AL'+str(offset + i)] = result[i]['kpi_ful'][7]['comment']
                except Exception as e:
                    pass
                try:
                    sheet['AM'+str(offset + i)] = result[i]['kpi_ful'][8]['name_kpi']+' '+result[i]['kpi_ful'][8]['surname_kpi']
                    sheet['AN'+str(offset + i)] = result[i]['kpi_ful'][8]['grade_board']
                    sheet['AO'+str(offset + i)] = result[i]['kpi_ful'][8]['comment']
                except Exception as e:
                    pass
                try:
                    sheet['AP'+str(offset + i)] = result[i]['kpi_ful'][9]['name_kpi']+' '+result[i]['kpi_ful'][9]['surname_kpi']
                    sheet['AQ'+str(offset + i)] = result[i]['kpi_ful'][9]['grade_board']
                    sheet['AR'+str(offset + i)] = result[i]['kpi_ful'][9]['comment']
                except Exception as e:
                    pass
                sheet['AS'+str(offset + i)] = result[i]['comment_hr']
                i = i + 1
        wb.save(filename_tmp)
        with open(filename_tmp, "rb") as f:
            encoded_string = base64.b64encode(f.read())
        os.remove(filename_tmp)
        displayColumns = ['isSuccess','reasonCode','reasonText','excel_base64']
        displayData = [(isSuccess,reasonCode,reasonText,encoded_string)]
        return jsonify(toDict(displayData,displayColumns))
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Export_kpi_hr', methods=['POST'])
@connect_sql()
def Export_kpi_hr(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        print data_new['companyid']
        if (str(data_new['type'])=='main')and(str(data_new['companyid'])!='23'):
            try:
                sql = "SELECT employee_kpi.comment_cancel,employee_kpi.positionChange_bet,employee_kpi.date_bet,employee_kpi.comment_pass,employee_kpi.Pass,employee_kpi.grade,employee_kpi.name,employee_kpi.surname,employee_kpi.work_date,employee_kpi.work_month,employee_kpi.work_year,employee_kpi.old_grade,employee_kpi.gradeCompareWithPoint,employee_kpi.structure_salary,employee_kpi.status,employee_kpi.em_id_leader,employee_kpi.specialMoney,employee_kpi.positionChange,position.position_detail,org_name.org_name_detail,employee_kpi.employeeid,employee_kpi.companyid,employee_kpi.totalGradePercent FROM employee_kpi\
                                                                                    INNER JOIN org_name ON employee_kpi.org_name = org_name.org_name_id\
                                                                                    INNER JOIN position ON employee_kpi.position = position.position_id\
                WHERE employee_kpi.year=%s AND employee_kpi.term=%s AND employee_kpi.companyid=%s GROUP BY employee_kpi.employeeid "
                cursor.execute(sql,(data_new['year'],data_new['term'],data_new['companyid']))
                columns = [column[0] for column in cursor.description]
                result = toJson(cursor.fetchall(),columns)
                for i1 in result:
                    kpi_ful = []
                    sql2 = "SELECT name_asp,surname_asp FROM assessor_kpi WHERE employeeid=%s"
                    cursor.execute(sql2,(i1['em_id_leader']))
                    columns = [column[0] for column in cursor.description]
                    data2 = toJson(cursor.fetchall(),columns)
                    for i2 in data2 :
                        kpi_ful.append(i2)
                    i1['name_leader'] = kpi_ful
                for i3 in result:
                    kpi_ful2 = []
                    try:
                        sql3 = "SELECT employee.start_work,employee.EndWork_probation,employee.nickname_employee,section.sect_detail,cost_center_name.cost_detail FROM employee\
                                                                           INNER JOIN section ON employee.section_id = section.sect_id\
                                                                           INNER JOIN cost_center_name ON employee.cost_center_name_id = cost_center_name.cost_center_name_id\
                        WHERE employee.employeeid=%s "
                        cursor.execute(sql3,(i3['employeeid']))
                        columns = [column[0] for column in cursor.description]
                        data3 = toJson(cursor.fetchall(),columns)
                    except Exception as e:
                        data3 = ['']
                    for i4 in data3 :
                        kpi_ful2.append(i4)
                    i3['sec_cost_center'] = kpi_ful2
                for item in result:
                    try:
                        sql5 = "SELECT position_detail FROM position WHERE position_id=%s"
                        cursor.execute(sql5,(item['positionChange']))
                        columns = [column[0] for column in cursor.description]
                        data5 = toJson(cursor.fetchall(),columns)
                        item['positionChange'] = data5[0]['position_detail']
                    except Exception as e:
                        item['positionChange'] = item['positionChange']
                    if item['specialMoney'] is None:
                        item['specialMoney']=''
                for item2 in result:
                    sql2_ = "SELECT company_short_name FROM company WHERE companyid=%s"
                    cursor.execute(sql2_,(item2['companyid']))
                    columns = [column[0] for column in cursor.description]
                    data2_ = toJson(cursor.fetchall(),columns)
                    item2['companyid'] = data2_[0]['company_short_name']
            except Exception as e:
                logserver(e)
                return "No_Data"
        else:
            try:
                sql = "SELECT employee_kpi.comment_cancel,employee_kpi.positionChange_bet,employee_kpi.date_bet,employee_kpi.comment_pass,employee_kpi.Pass,employee_kpi.grade,employee_kpi.name,employee_kpi.surname,employee_kpi.work_date,employee_kpi.work_month,employee_kpi.work_year,employee_kpi.old_grade,employee_kpi.gradeCompareWithPoint,employee_kpi.structure_salary,employee_kpi.status,employee_kpi.em_id_leader,employee_kpi.specialMoney,employee_kpi.positionChange,position.position_detail,org_name.org_name_detail,employee_kpi.employeeid,employee_kpi.companyid,employee_kpi.totalGradePercent FROM employee_kpi\
                                                                                    INNER JOIN org_name ON employee_kpi.org_name = org_name.org_name_id\
                                                                                    INNER JOIN position ON employee_kpi.position = position.position_id\
                WHERE employee_kpi.year=%s AND employee_kpi.term=%s GROUP BY employee_kpi.employeeid"
                cursor.execute(sql,(data_new['year'],data_new['term']))
                columns = [column[0] for column in cursor.description]
                result = toJson(cursor.fetchall(),columns)
                for i1 in result:
                    try:
                        kpi_ful = []
                        sql2 = "SELECT name_asp,surname_asp FROM assessor_kpi WHERE employeeid=%s"
                        cursor.execute(sql2,(i1['em_id_leader']))
                        columns = [column[0] for column in cursor.description]
                        data2 = toJson(cursor.fetchall(),columns)
                        for i2 in data2 :
                            kpi_ful.append(i2)
                        i1['name_leader'] = kpi_ful
                    except Exception as e:
                        kpi_ful = []
                        i1['name_leader'] = kpi_ful
                for i3 in result:
                    kpi_ful2 = []
                    try:
                        sql3 = "SELECT employee.start_work,employee.EndWork_probation,employee.nickname_employee,section.sect_detail,cost_center_name.cost_detail FROM employee\
                                                                           INNER JOIN section ON employee.section_id = section.sect_id\
                                                                           INNER JOIN cost_center_name ON employee.cost_center_name_id = cost_center_name.cost_center_name_id\
                        WHERE employee.employeeid=%s "
                        cursor.execute(sql3,(i3['employeeid']))
                        columns = [column[0] for column in cursor.description]
                        data3 = toJson(cursor.fetchall(),columns)
                    except Exception as e:
                        data3 = ['']
                    for i4 in data3 :
                        kpi_ful2.append(i4)
                    i3['sec_cost_center'] = kpi_ful2
                for item in result:
                    try:
                        sql5 = "SELECT position_detail FROM position WHERE position_id=%s"
                        cursor.execute(sql5,(item['positionChange']))
                        columns = [column[0] for column in cursor.description]
                        data5 = toJson(cursor.fetchall(),columns)
                        item['positionChange'] = data5[0]['position_detail']
                    except Exception as e:
                        item['positionChange'] = item['positionChange']
                    if item['specialMoney'] is None:
                        item['specialMoney']=''
                for item2 in result:
                    sql2_ = "SELECT company_short_name FROM company WHERE companyid=%s"
                    cursor.execute(sql2_,(item2['companyid']))
                    columns = [column[0] for column in cursor.description]
                    data2_ = toJson(cursor.fetchall(),columns)
                    item2['companyid'] = data2_[0]['company_short_name']
            except Exception as e:
                logserver(e)
                return "No_Data"
        isSuccess = True
        reasonCode = 200
        reasonText = ""
        now = datetime.now()
        datetimeStr = now.strftime('%Y%m%d_%H%M%S%f')
        filename_tmp = secure_filename('{}_{}'.format(datetimeStr, 'Template_kpi.xlsx'))

        wb = load_workbook('../app/Template/Template_kpi_.xlsx')
        if len(result) > 0:

            sheet = wb['Sheet1']
            sheet['C'+str(2)] = data_new['year'] + '/' + data_new['term']
            offset = 4
            i = 0
            for i in xrange(len(result)):
                sheet['A'+str(offset + i)] = result[i]['companyid']
                sheet['B'+str(offset + i)] = result[i]['employeeid']
                sheet['C'+str(offset + i)] = result[i]['name']
                sheet['D'+str(offset + i)] = result[i]['surname']
                try:
                    sheet['E'+str(offset + i)] = result[i]['sec_cost_center'][0]['nickname_employee']
                except Exception as e:
                    pass
                sheet['F'+str(offset + i)] = result[i]['position_detail']
                try:
                    sheet['G'+str(offset + i)] = result[i]['sec_cost_center'][0]['sect_detail']
                except Exception as e:
                    pass
                sheet['H'+str(offset + i)] = result[i]['org_name_detail']
                try:
                    sheet['I'+str(offset + i)] = result[i]['sec_cost_center'][0]['cost_detail']
                except Exception as e:
                    pass
                try:
                    sheet['J'+str(offset + i)] = result[i]['name_leader'][0]['name_asp']+' '+result[i]['name_leader'][0]['surname_asp']
                except Exception as e:
                    pass
                try:
                    sheet['K'+str(offset + i)] = result[i]['sec_cost_center'][0]['start_work']
                except Exception as e:
                    pass
                try:
                    sheet['L'+str(offset + i)] = result[i]['sec_cost_center'][0]['EndWork_probation']
                except Exception as e:
                    pass
                sheet['M'+str(offset + i)] = result[i]['work_year']
                sheet['N'+str(offset + i)] = result[i]['work_month']
                sheet['O'+str(offset + i)] = result[i]['work_date']
                sheet['P'+str(offset + i)] = result[i]['gradeCompareWithPoint']
                sheet['Q'+str(offset + i)] = result[i]['structure_salary']
                sheet['R'+str(offset + i)] = result[i]['totalGradePercent']
                sheet['S'+str(offset + i)] = result[i]['old_grade']
                sheet['T'+str(offset + i)] = result[i]['grade']
                sheet['U'+str(offset + i)] = result[i]['status']
                sheet['V'+str(offset + i)] = result[i]['positionChange']
                sheet['W'+str(offset + i)] = result[i]['specialMoney']
                sheet['X'+str(offset + i)] = result[i]['Pass']
                sheet['Y'+str(offset + i)] = result[i]['comment_pass']
                sheet['Z'+str(offset + i)] = result[i]['date_bet']
                sheet['AA'+str(offset + i)] = result[i]['positionChange_bet']
                sheet['AB'+str(offset + i)] = result[i]['comment_cancel']
                i = i + 1
        wb.save(filename_tmp)
        with open(filename_tmp, "rb") as f:
            encoded_string = base64.b64encode(f.read())
        os.remove(filename_tmp)
        displayColumns = ['isSuccess','reasonCode','reasonText','excel_base64']
        displayData = [(isSuccess,reasonCode,reasonText,encoded_string)]
        return jsonify(toDict(displayData,displayColumns))
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/userGetKpiFile/<path>', methods=['GET'])
def userGetKpiFile(path):
    return send_from_directory('../uploads/', path)
