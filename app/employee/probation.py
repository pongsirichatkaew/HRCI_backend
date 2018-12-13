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
        sqlUp = "UPDATE Emp_probation SET validstatus=%s WHERE employeeid=%s"
        cursor.execute(sqlUp,(data_new['validstatus'],data_new['employeeid']))
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryEmployee_probation', methods=['POST'])
def QryEmployee_probation():
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        sql = "SELECT Emp_probation.name_th,Emp_probation.employeeid,Emp_probation.surname_th,Emp_probation.citizenid,Emp_probation.start_work,company.company_short_name,position.position_detail,section.sect_detail,org_name.org_name_detail,cost_center_name.cost_detail,status.status_detail,status.path_color,status.font_color FROM Emp_probation LEFT JOIN company ON company.companyid = Emp_probation.company_id\
                                      LEFT JOIN position ON position.position_id = Emp_probation.position_id\
                                      LEFT JOIN section ON section.sect_id = Emp_probation.section_id\
                                      LEFT JOIN org_name ON org_name.org_name_id = Emp_probation.org_name_id\
                                      LEFT JOIN cost_center_name ON cost_center_name.cost_center_name_id = Emp_probation.cost_center_name_id\
                                      LEFT JOIN status ON status.status_id = Emp_probation.validstatus"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
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
        sql = "SELECT Emp_probation.name_th,Emp_probation.employeeid,Emp_probation.surname_th,Emp_probation.citizenid,Emp_probation.start_work,Emp_probation.EndWork_probation,position.position_detail,section.sect_detail,org_name.org_name_detail,cost_center_name.cost_detail,company.imageName FROM Emp_probation LEFT JOIN position ON position.position_id = Emp_probation.position_id\
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

            question = []
            sql1pro = "SELECT question_pro_id,pro_values,type_check,group_q FROM employee_pro WHERE employeeid = %s AND validstatus=1 ORDER BY question_pro_id ASC"
            cursor.execute(sql1pro,(data_new['employeeid']))
            print(sql1pro)
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
        path = '../uploads/'+employeeid+'/'
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
                PathFile = employeeid+'/'+str(fileList.filename)                
                sql = "INSERT INTO employee_upload(ID_CardNo,Type,PathFile,createby) VALUES (%s,%s,%s,%s)"
                cursor.execute(sql,(ID_CardNo,Type,PathFile,request.form['createby']))
            else:
                return "file is not allowed"
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
