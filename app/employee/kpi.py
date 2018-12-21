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
            group_ = str(data_new['group_kpi_id'])
            group_kpi_id = 'WHERE group_kpi='+'"'+group_+'"'
        except Exception as e:
            pass
        try:
            dataInput = request.json
            source = dataInput['source']
            data_new = source
            group_2 = str(data_new['group_kpi_id2'])
            group_kpi_id = 'WHERE group_kpi IN ('+'"'+group_+'"'+','+'"'+group_2+'"'+')'
        except Exception as e:
            pass
        sql = "SELECT employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,grade,group_kpi,star_date_kpi,status FROM employee_kpi "+group_kpi_id+" "
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

        sql = "SELECT employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,grade,group_kpi,star_date_kpi,status FROM employee_kpi WHERE employeeid=%s "
        cursor.execute(sql,(data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sql2 = "SELECT employeeid_board,name_kpi,surname_kpi,position_kpi,grade_board,comment FROM board_kpi WHERE employeeid=%s"
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
        employeeid = data_new['employeeid']

        try:
            sql44 = "SELECT employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,grade,group_kpi,star_date_kpi FROM employee_kpi WHERE employeeid=%s"
            cursor.execute(sql44,(employeeid))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            name = result[0]['name']
            return "employee is duplicate"
        except Exception as e:
            pass

        type_action = "ADD"

        sqlIn_be = "INSERT INTO employee_kpi(employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,group_kpi,star_date_kpi,status,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_be,(employeeid,data_new['name'],data_new['surname'],data_new['org_name'],data_new['position'],data_new['work_date'],data_new['work_month'],data_new['work_year'],data_new['old_grade'],data_new['group_kpi'],data_new['star_date_kpi'],data_new['status'],data_new['createby']))

        sqlIn_be = "INSERT INTO employee_kpi_log(employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,group_kpi,star_date_kpi,status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_be,(employeeid,data_new['name'],data_new['surname'],data_new['org_name'],data_new['position'],data_new['work_date'],data_new['work_month'],data_new['work_year'],data_new['old_grade'],data_new['group_kpi'],data_new['star_date_kpi'],data_new['status'],data_new['createby'],type_action))

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

        sql_be = "INSERT INTO employee_kpi_log(employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,group_kpi,star_date_kpi,status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_be,(data_new['employeeid'],result[0]['name'],result[0]['surname'],result[0]['org_name'],result[0]['position'],result[0]['work_date'],result[0]['work_month'],result[0]['work_year'],result[0]['old_grade'],result[0]['group_kpi'],result[0]['star_date_kpi'],result[0]['status'],data_new['createby'],type_action))

        sqlI9de = "DELETE FROM employee_kpi WHERE employeeid=%s"
        cursor.execute(sqlI9de,data_new['employeeid'])

        sqlIn_be = "INSERT INTO employee_kpi(employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,group_kpi,star_date_kpi,status,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_be,(employeeid,data_new['name'],data_new['surname'],data_new['org_name'],data_new['position'],data_new['work_date'],data_new['work_month'],data_new['work_year'],data_new['old_grade'],data_new['group_kpi'],data_new['star_date_kpi'],data_new['status'],data_new['createby']))

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

        sql_be = "INSERT INTO employee_kpi_log(employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,group_kpi,star_date_kpi,status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_be,(result[0]['employeeid'],result[0]['name'],result[0]['surname'],result[0]['org_name'],result[0]['position'],result[0]['work_date'],result[0]['work_month'],result[0]['work_year'],result[0]['old_grade'],result[0]['group_kpi'],result[0]['star_date_kpi'],result[0]['status'],data_new['createby'],type_action))

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
        if grade_board is None:
            type_action = "Edit"
            sqlIn_be2 = "INSERT INTO answer_kpi_hr_log(employeeid,grade,createby,type_action) VALUES (%s,%s,%s,%s)"
            cursor.execute(sqlIn_be2,(result[0]['employeeid'],result[0]['grade'],result[0]['createby'],type_action))
        else:
            type_action = "Insert"
            sqlIn_be1 = "INSERT INTO answer_kpi_hr_log(employeeid,grade,createby,type_action) VALUES (%s,%s,%s,%s)"
            cursor.execute(sqlIn_be1,(data_new['employeeid'],data_new['grade'],data_new['createby'],type_action))
        sqlUp = "UPDATE employee_kpi SET grade=%s WHERE employeeid=%s"
        cursor.execute(sqlUp,(data_new['grade'],data_new['employeeid']))

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
        sql = "SELECT employeeid,employeeid_board,name_kpi,surname_kpi,org_name_kpi,grade_board,comment,grade FROM employee_kpi WHERE employeeid=%s"
        cursor.execute(sql,(data_new['employeeid']))
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
        sql = "SELECT employeeid,employeeid_board,name_kpi,surname_kpi,position_kpi FROM board_kpi WHERE employeeid=%s"
        cursor.execute(sql,(data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
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
        employeeid = data_new['employeeid']

        type_action = "ADD"

        for i in xrange(len(data_new['emp_board'])):
            sqlIn_be = "INSERT INTO board_kpi(employeeid,employeeid_board,name_kpi,surname_kpi,position_kpi,createby) VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_be,(employeeid,data_new['emp_board'][i]['employeeid_board'],data_new['emp_board'][i]['name_kpi'],data_new['emp_board'][i]['surname_kpi'],data_new['emp_board'][i]['position_kpi'],data_new['createby']))

        for i in xrange(len(data_new['emp_board'])):
            sqlIn_be2 = "INSERT INTO board_kpi_log(employeeid,employeeid_board,name_kpi,surname_kpi,position_kpi,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_be2,(employeeid,data_new['emp_board'][i]['employeeid_board'],data_new['emp_board'][i]['name_kpi'],data_new['emp_board'][i]['surname_kpi'],data_new['emp_board'][i]['position_kpi'],data_new['createby'],type_action))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qry_board_kpi_v2', methods=['POST'])
@connect_sql()
def Qry_board_kpi_v2(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT employeeid_board,name,group_kpi FROM employee_kpi WHERE validstatus=1 "
        cursor.execute(sql,(data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Add_board_kpi_v2', methods=['POST'])
@connect_sql()
def Add_board_kpi_v2(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        employeeid = data_new['employeeid_board']

        nameKpi__ = str(data_new['name_kpi'])+" "+str(data_new['surname_kpi'])

        sql_be = "INSERT INTO board_kpi_v2(employeeid_board,name,group_kpi,createby) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql_be,(data_new['employeeid_board'],nameKpi__,data_new['group_kpi_id'],data_new['createby']))

        sql = "INSERT INTO Admin (employeeid,username,name,permission,position,createby) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(data_new['employeeid_board'],data_new['username'],nameKpi__,data_new['group_kpi_id'],data_new['createby']))

        group_kpi_id = ""
        try:
            dataInput = request.json
            source = dataInput['source']
            data_new = source
            group_ = str(data_new['group_kpi_id'])
            group_kpi_id = 'WHERE group_kpi='+'"'+group_+'"'
        except Exception as e:
            pass
        try:
            dataInput = request.json
            source = dataInput['source']
            data_new = source
            group_2 = str(data_new['group_kpi_id2'])
            group_kpi_id = 'WHERE group_kpi IN ('+'"'+group_+'"'+','+'"'+group_2+'"'+')'
        except Exception as e:
            pass
        sql_emp_kpi = "SELECT employeeid FROM employee_kpi "+group_kpi_id+" "
        cursor.execute(sql_emp_kpi)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "ADD"

        for i in xrange(len(result)):
            sqlIn_be = "INSERT INTO board_kpi(employeeid,employeeid_board,name_kpi,surname_kpi,position_kpi,createby) VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_be,(result[i]['employeeid'],data_new['employeeid_board'],data_new['name_kpi'],data_new['surname_kpi'],data_new['position_kpi'],data_new['createby']))

        for i in xrange(len(result)):
            sqlIn_be = "INSERT INTO board_kpi_log(employeeid,employeeid_board,name_kpi,surname_kpi,position_kpi,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_be,(result[i]['employeeid'],data_new['employeeid_board'],data_new['name_kpi'],data_new['surname_kpi'],data_new['position_kpi'],data_new['createby'],type_action))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Delete_board_kpi_v2', methods=['POST'])
@connect_sql()
def Delete_board_kpi_v2(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sqlUp = "UPDATE board_kpi_v2 SET validstatus=0 WHERE employeeid_board=%s"
        cursor.execute(sqlUp,(data_new['employeeid_board']))

        sqlDe = "DELETE FROM Admin WHERE employeeid=%s"
        cursor.execute(sqlDe,(data_new['employeeid_board']))

        sql_be = "INSERT INTO board_kpi_v2(employeeid_board,name,group_kpi,createby) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql_be,(data_new['employeeid_board'],data_new['name'],data_new['group_kpi'],data_new['createby']))

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

        sqlIn_be2 = "INSERT INTO board_kpi_log(employeeid,employeeid_board,name_kpi,surname_kpi,position_kpi,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_be2,(employeeid,result[0]['employeeid_board'],result[0]['name_kpi'],result[0]['surname_kpi'],result[0]['position_kpi'],data_new['createby'],type_action))

        sqlde = "DELETE FROM board_kpi WHERE employeeid=%s AND employeeid_board=%s"
        cursor.execute(sqlde,(data_new['employeeid'],data_new['employeeid_board']))

        sqlIn_be = "INSERT INTO board_kpi(employeeid,employeeid_board,name_kpi,surname_kpi,position_kpi,createby) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_be,(employeeid,data_new['employeeid_board'],data_new['name_kpi'],data_new['surname_kpi'],data_new['position_kpi'],data_new['createby']))
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

        sqlIn_be2 = "INSERT INTO board_kpi_log(employeeid,employeeid_board,name_kpi,surname_kpi,position_kpi,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_be2,(result[0]['employeeid'],result[0]['employeeid_board'],result[0]['name_kpi'],result[0]['surname_kpi'],result[0]['position_kpi'],data_new['createby'],type_action))

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
            sqlIn_be2 = "INSERT INTO answer_kpi_log(employeeid,employeeid_board,grade_board,comment,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_be2,(result[0]['employeeid'],result[0]['employeeid_board'],result[0]['grade_board'],result[0]['comment'],data_new['createby'],type_action))
        else:
            type_action = "Insert"
            sqlIn_be1 = "INSERT INTO answer_kpi_log(employeeid,employeeid_board,grade_board,comment,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_be1,(data_new['employeeid'],data_new['employeeid_board'],data_new['grade_board'],data_new['comment'],data_new['createby'],type_action))
        sqlUp = "UPDATE board_kpi SET grade_board=%s,comment=%s WHERE employeeid=%s AND employeeid_board=%s"
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
            fileList.filename = 'kpi' + '' + '' + str(idx + 1) + '.' + fileType
            try:
                os.remove(os.path.join(path, fileList.filename))
            except OSError:
                pass
            if file and allowed_file(fileList.filename):
                fileList.save(os.path.join(path, fileList.filename))
                PathFile = employeeid+'/'+'kpi'+'/'+str(fileList.filename)
                sql = "INSERT INTO employee_upload_kpi(employeeid,FileName,Type,PathFile,createby) VALUES (%s,%s,%s,%s,%s)"
                cursor.execute(sql,(employeeid,fileName,Type,PathFile,request.form['createby']))
            else:
                return "file is not allowed"
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/upload_user_kpi_one', methods=['POST'])
@connect_sql()
def upload_user_kpi_one(cursor):
    try:
        employeeid = request.form['employeeid']
        Type = 'kpi'
        try:
            sqlDe = "DELETE FROM employee_upload WHERE employeeid=%s"
            cursor.execute(sqlDe,(request.form['employeeid']))
        except Exception as e:
            pass
        path = 'uploads/'+employeeid+'/'+'kpi'+'/'
        path2 = employeeid+'/'+'kpi'+'/'
        if not os.path.exists(path):
            os.makedirs(path)
        if request.method == 'POST':
            file = request.files['file']
        if file:
            file.save(os.path.join(path, employeeid + 'kpi.png'))
            PathFile = path2+'/'+employeeid + 'kpi.png'
            fileName = employeeid + 'kpi.png'
        else:
            return 'file is not allowed'

        sql = "INSERT INTO employee_upload_kpi(employeeid,FileName,Type,PathFile,createby) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sql,(employeeid,fileName,Type,PathFile,request.form['createby']))

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
            # item_['PathFile'] = str(item_['PathFile'])
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qry_upload_kpi_one', methods=['POST'])
@connect_sql()
def Qry_upload_kpi_one(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT employeeid,FileName,Type,PathFile FROM employee_upload_kpi WHERE employeeid=%s "
        cursor.execute(sql,(data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        for item_ in result:
            img_base64 = []
            item_['PathFile'] = '../uploads/'+str(item_['PathFile'])
            tranImage = item_['PathFile']
            with open(tranImage, 'rb') as image_file:
                encoded_Image = base64.b64encode(image_file.read())
            item_['img_base64'] = encoded_Image
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryAdmin_business', methods=['POST'])
@connect_sql()
def QryAdmin_business(cursor):
    try:
        sql = "SELECT id,employeeid,username,name,permission,position FROM Admin WHERE permission='สายงานธุรกิจ'"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        for item_ in result:
            surname = []
            user_s = item_['name'].split(" ")
            name_t = user_s[0]
            surname_t = user_s[1]
            item_['name'] = name_t
            item_['surname'] = surname_t
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryAdmin_Engineer', methods=['POST'])
@connect_sql()
def QryAdmin_Engineer(cursor):
    try:
        sql2 = "SELECT id,employeeid,username,name,permission,position FROM Admin WHERE permission='สายงาน Engineer'"
        cursor.execute(sql2)
        columns = [column[0] for column in cursor.description]
        result2 = toJson(cursor.fetchall(),columns)
        for item_ in result2:
            surname = []
            user_s = item_['name'].split(" ")
            name_t = user_s[0]
            surname_t = user_s[1]
            item_['name'] = name_t
            item_['surname'] = surname_t
        return jsonify(result2)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryAdmin_Support', methods=['POST'])
@connect_sql()
def QryAdmin_Support(cursor):
    try:
        sql3 = "SELECT id,employeeid,username,name,permission,position FROM Admin WHERE permission='สายงาน Support'"
        cursor.execute(sql3)
        columns = [column[0] for column in cursor.description]
        result3 = toJson(cursor.fetchall(),columns)
        for item_ in result3:
            surname = []
            user_s = item_['name'].split(" ")
            name_t = user_s[0]
            surname_t = user_s[1]
            item_['name'] = name_t
            item_['surname'] = surname_t
        return jsonify(result3)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Export_kpi', methods=['POST'])
@connect_sql()
def Export_kpi(cursor):
    try:
        try:
            sql = "SELECT employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,grade,group_kpi,star_date_kpi,status FROM employee_kpi"
            cursor.execute(sql)
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            for i1 in result:
                kpi_ful = []
                sql2 = "SELECT name_kpi,surname_kpi,grade_board,comment FROM board_kpi WHERE employeeid=%s"
                cursor.execute(sql2,(i1['employeeid']))
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

        wb = load_workbook('../Template/Template_kpi.xlsx')
        if len(result) > 0:

            sheet = wb['Sheet1']
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
