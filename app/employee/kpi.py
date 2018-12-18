#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *
@app.route('/QryEmployee_kpi', methods=['POST'])
@connect_sql()
def QryEmployee_kpi():
    try:
        group_kpi_id = ""
        try:
            dataInput = request.json
            source = dataInput['source']
            data_new = source
            org_name = 'WHERE group_kpi='+str(data_new['group_kpi_id'])
        except Exception as e:
            pass
        sql = "SELECT employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,grade,group_kpi FROM employee_kpi "+group_kpi_id+" "
        cursor.execute(sql)
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

        sql = "SELECT employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,grade,group_kpi FROM employee_kpi WHERE employeeid=%s "
        cursor.execute(sql,(data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sql2 = "SELECT employeeid_board,name_kpi,surname_kpi,org_name_kpi,grade_board,comment FROM board_kpi WHERE employeeid=%s"
        cursor.execute(sql2,(data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        result2 = toJson(cursor.fetchall(),columns)

        try:
            encoded_Image=str("http://intranet.inet.co.th/assets/upload/staff/"+str(data_new['employeeid'])+".jpg")
            open_path_ = urllib.urlopen(encoded_Image)
            htmlSource = open_path_.read()
            open_path_.close()
            test= htmlSource.decode('utf-8')
            encoded_Image=str("http://intranet.inet.co.th/assets/upload/staff/"+str(data_new['employeeid'])+"s.jpg")
        except Exception as e:
            encoded_Image=str("http://intranet.inet.co.th/assets/upload/staff/"+str(data_new['employeeid'])+".jpg")

        sum={}
        sum["employee"] = result
        sum["board"] = result2
        sum["image"] = encoded_Image

        return jsonify(result)
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
        employeeid = data_new['employeeid']

        type_action = "ADD"

        sqlIn_be = "INSERT INTO employee_kpi(employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,group_kpi,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_be,(employeeid,data_new['name'],data_new['surname'],data_new['org_name'],data_new['position'],data_new['work_date'],data_new['work_month'],data_new['work_year'],data_new['old_grade'],data_new['group_kpi'],data_new['createby']))

        sqlIn_be = "INSERT INTO employee_kpi_log(employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,group_kpi,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_be,(employeeid,data_new['name'],data_new['surname'],data_new['org_name'],data_new['position'],data_new['work_date'],data_new['work_month'],data_new['work_year'],data_new['old_grade'],data_new['group_kpi'],data_new['createby'],type_action))

        return "Success"
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

        sql = "SELECT * FROM employee_kpi WHERE employeeid=%s"
        cursor.execute(sql,(data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Edit"

        sql_be = "INSERT INTO employee_kpi_log(employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,group_kpi,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_be,(data_new['employeeid'],result[0]['name'],result[0]['surname'],result[0]['org_name'],result[0]['position'],result[0]['work_date'],result[0]['work_month'],result[0]['work_year'],result[0]['work_date'],result[0]['old_grade'],data_new['createby'],type_action))

        sqlI9de = "DELETE FROM employee_kpi WHERE employeeid=%s"
        cursor.execute(sqlI9de,data_new['employeeid'])

        sqlIn_be = "INSERT INTO employee_kpi(employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,group_kpi_kpi,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_be,(employeeid,data_new['name'],data_new['surname'],data_new['org_name'],data_new['position'],data_new['work_date'],data_new['work_month'],data_new['work_year'],data_new['old_grade'],data_new['group_kpi'],data_new['createby']))

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

        sql = "SELECT * FROM employee_kpi WHERE employeeid=%s"
        cursor.execute(sql,(data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Delete"

        sql_be = "INSERT INTO employee_kpi_log(employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,group_kpi,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_be,(data_new['employeeid'],result[0]['name'],result[0]['surname'],result[0]['org_name'],result[0]['position'],result[0]['work_date'],result[0]['work_month'],result[0]['work_year'],result[0]['old_grade'],result[0]['group_kpi'],data_new['createby'],type_action))

        sqlI9de = "DELETE FROM employee_kpi WHERE employeeid=%s"
        cursor.execute(sqlI9de,data_new['employeeid'])

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Update_grade_hr', methods=['POST'])
@connect_sql()
def Update_grade_hr(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT employeeid,grade FROM employee_kpi WHERE employeeid=%s"
        cursor.execute(sql,(data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        grade_board = str(result[0]['grade'])
        if grade_board != "":
            type_action = "Edit"
            sqlIn_be2 = "INSERT INTO answer_kpi_hr_log(employeeid,grade,createby,type_action) VALUES (%s,%s,%s,%s)"
            cursor.execute(sqlIn_be2,(result[0]['employeeid'],result[0]['grade'],result[0]['createby'],type_action))
        else:
            type_action = "Insert"
            sqlIn_be1 = "INSERT INTO answer_kpi_hr_log(employeeid,grade,createby,type_action) VALUES (%s,%s,%s,%s)"
            cursor.execute(sqlIn_be1,(data_new['employeeid'],data_new['grade'],data_new['createby'],type_action))
        sqlUp = "UPDATE employee_kpi SET grade=$ WHERE employeeid=%s"
        cursor.execute(sqlUp,(data_new['grade'],data_new['employeeid']))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
# @app.route('/Qry_board_kpi', methods=['POST'])
# @connect_sql()
# def Qry_board_kpi():
#     try:
#         dataInput = request.json
#         source = dataInput['source']
#         data_new = source
#         sql = "SELECT employeeid,employeeid_board,name_kpi,surname_kpi,org_name_kpi,grade_board,comment,grade FROM employee_kpi WHERE employeeid=%s"
#         cursor.execute(sql,(data_new['employeeid']))
#         columns = [column[0] for column in cursor.description]
#         result = toJson(cursor.fetchall(),columns)
#         return jsonify(result)
#     except Exception as e:
#         logserver(e)
#         return "fail"
@app.route('/Add_board_kpi', methods=['POST'])
@connect_sql()
def Add_board_kpi(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        employeeid = data_new['employeeid']

        type_action = "ADD"

        for i in xrange(len(data_new['emp_board'])):
            sqlIn_be = "INSERT INTO board_kpi(employeeid,employeeid_board,name_kpi,surname_kpi,org_name,createby) VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_be,(employeeid,data_new['emp_board'][i]['employeeid_board'],data_new['emp_board'][i]['name_kpi'],data_new['emp_board'][i]['surname_kpi'],data_new['emp_board'][i]['org_name_kpi'],data_new['createby']))

        for i in xrange(len(data_new['emp_board'])):
            sqlIn_be2 = "INSERT INTO board_kpi_log(employeeid,employeeid_board,name_kpi,surname_kpi,org_name,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_be2,(employeeid,data_new['emp_board'][i]['employeeid_board'],data_new['emp_board'][i]['name_kpi'],data_new['emp_board'][i]['surname_kpi'],data_new['emp_board'][i]['org_name_kpi'],data_new['createby'],type_action))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Edit_board_kpi', methods=['POST'])
@connect_sql()
def Edit_board_kpi(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT * FROM board_kpi WHERE employeeid=%s AND employeeid_board=%s"
        cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_board']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Edit"

        sqlIn_be2 = "INSERT INTO board_kpi_log(employeeid,employeeid_board,name_kpi,surname_kpi,org_name,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_be2,(employeeid,result[0]['employeeid_board'],result[0]['name_kpi'],result[0]['surname_kpi'],result[0]['org_name_kpi'],data_new['createby'],type_action))

        sqlde = "DELETE FROM board_kpi WHERE employeeid=%s AND employeeid_board=%s"
        cursor.execute(sqlde,(data_new['employeeid'],data_new['employeeid_board']))

        sqlIn_be = "INSERT INTO board_kpi(employeeid,employeeid_board,name_kpi,surname_kpi,org_name,createby) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_be,(employeeid,data_new['employeeid_board'],data_new['name_kpi'],data_new['surname_kpi'],data_new['org_name_kpi'],data_new['createby']))
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
        sql = "SELECT * FROM board_kpi WHERE employeeid=%s AND employeeid_board=%s"
        cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_board']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Delete"

        sqlIn_be2 = "INSERT INTO board_kpi_log(employeeid,employeeid_board,name_kpi,surname_kpi,org_name,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_be2,(employeeid,result[0]['employeeid_board'],result[0]['name_kpi'],result[0]['surname_kpi'],result[0]['org_name_kpi'],data_new['createby'],type_action))

        sqlde = "DELETE FROM board_kpi WHERE employeeid=%s AND employeeid_board=%s"
        cursor.execute(sqlde,(data_new['employeeid'],data_new['employeeid_board']))

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
        sql = "SELECT employeeid,employeeid_board,grade_board,comment FROM board_kpi WHERE employeeid=%s AND employeeid_board=%s"
        cursor.execute(sql,(data_new['employeeid'],data_new['employeeid_board']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        grade_board = str(result[0]['grade_board'])
        if grade_board != "":
            type_action = "Edit"
            sqlIn_be2 = "INSERT INTO answer_kpi_log(employeeid,employeeid_board,grade_board,comment,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_be2,(result[0]['employeeid'],result[0]['employeeid_board'],result[0]['grade_board'],result[0]['comment'],data_new['createby'],type_action))
        else:
            type_action = "Insert"
            sqlIn_be1 = "INSERT INTO answer_kpi_log(employeeid,employeeid_board,grade_board,comment,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_be1,(data_new['employeeid'],data_new['employeeid_board'],data_new['grade_board'],data_new['comment'],data_new['createby'],type_action))
        sqlUp = "UPDATE board_kpi SET grade_board=$,comment=$s WHERE employeeid=%s AND employeeid_board=%s"
        cursor.execute(sqlUp,(data_new['grade_board'],data_new['comment'],data_new['employeeid'],data_new['employeeid_board']))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/upload_user_kpi', methods=['POST'])
@connect_sql()
def upload_user_kpi(cursor):
    try:
        try:
            sqlDe = "DELETE FROM employee_upload WHERE employeeid=%s"
            cursor.execute(sqlDe,(request.form['employeeid']))
        except Exception as e:
            pass

        Type = 'kpi'
        employeeid = request.form['employeeid']
        path = '../uploads/'+employeeid+'/'+'kpi'+'/'
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
                sql = "INSERT INTO employee_upload_kpi(employeeid,FileName,Type,PathFile,createby) VALUES (%s,%s,%s,%s,%s)"
                cursor.execute(sql,(employeeid,fileName,Type,PathFile,request.form['createby']))
            else:
                return "file is not allowed"
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qry_upload_file_kpi', methods=['POST'])
@connect_sql()
def Qry_upload_file_kpi(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT employeeid,FileName,Type,PathFile FROM employee_upload_kpi WHERE employeeid=%s "
        cursor.execute(sql,(data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        for item_ in result:
            item_['PathFile'] = '../uploads/'+str(item_['PathFile'])
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
