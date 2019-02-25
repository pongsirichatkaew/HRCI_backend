#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/InsertCompany', methods=['POST'])
@connect_sql()
def InsertCompany(cursor):
    try:
        sqlQry = "SELECT companyid FROM company ORDER BY companyid DESC LIMIT 1"
        cursor.execute(sqlQry)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        companyid_last=str(result[0]['companyid']+1)

        currentTime = datetime.today().strftime('%Y%m%d%H%M%S%f')
        path = 'uploads/' + companyid_last
        path2 = companyid_last
        if not os.path.exists(path):
            os.makedirs(path)
        if request.method == 'POST':
            file = request.files['file']
        if file:
            file.save(os.path.join(path, currentTime + '_company_img.png'))
            path_image = path2+'/'+currentTime+'_company_img.png'
        else:
            return 'file is not allowed'

        sql = "INSERT INTO company(acronym,companyid,companyname,company_short_name,phone,email,address_company,imageName,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(request.form['acronym'],companyid_last,request.form['companyname'],request.form['company_short_name'],request.form['phone'],request.form['email'],request.form['address_company'],path_image,request.form['createby']))

        type_action = "ADD"

        sql_log = "INSERT INTO company_log(acronym,companyid,companyname,company_short_name,phone,email,address_company,imageName,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(request.form['acronym'],companyid_last,request.form['companyname'],request.form['company_short_name'],request.form['phone'],request.form['email'],request.form['address_company'],path_image,request.form['createby'],type_action))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditCompany', methods=['POST'])
@connect_sql()
def EditCompany(cursor):
    try:
        sql_se = "SELECT * FROM company WHERE companyid=%s"
        cursor.execute(sql_se,(request.form['companyid']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        currentTime = datetime.today().strftime('%Y%m%d%H%M%S%f')
        path = 'uploads/' + request.form['companyid']
        path2 = request.form['companyid']
        if not os.path.exists(path):
            os.makedirs(path)
        if request.method == 'POST':
            file = request.files['file']
        if file:
            file.save(os.path.join(path, currentTime + '_company_img.png'))
            path_image = path2+'/'+currentTime+'_company_img.png'
        else:
            return 'file is not allowed'

        type_action= "Edit"

        sql_log = "INSERT INTO company_log(acronym,companyid,companyname,company_short_name,phone,email,address_company,imageName,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(result[0]['acronym'],result[0]['companyid'],result[0]['companyname'],result[0]['company_short_name'],result[0]['phone'],result[0]['email'],result[0]['address_company'],result[0]['imageName'],request.form['createby'],type_action))

        sqlDe = "DELETE FROM company WHERE companyid=%s"
        cursor.execute(sqlDe,(request.form['companyid']))

        sql = "INSERT INTO company(acronym,companyid,companyname,company_short_name,phone,email,address_company,imageName,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(request.form['acronym'],request.form['companyid'],request.form['companyname'],request.form['company_short_name'],request.form['phone'],request.form['email'],request.form['address_company'],path_image,request.form['createby']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditCompany_data', methods=['POST'])
@connect_sql()
def EditCompany_data(cursor):
    try:
        data = request.json
        source = data['source']
        data_new = source

        sql = "SELECT * FROM company WHERE companyid=%s"
        cursor.execute(sql,data_new['companyid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action= "Edit_data"

        sql_log = "INSERT INTO company_log(acronym,companyid,companyname,company_short_name,phone,email,address_company,imageName,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(result[0]['acronym'],result[0]['companyid'],result[0]['companyname'],result[0]['company_short_name'],result[0]['phone'],result[0]['email'],result[0]['address_company'],result[0]['imageName'],data_new['createby'],type_action))

        sqlDe = "DELETE FROM company WHERE companyid=%s"
        cursor.execute(sqlDe,(data_new['companyid']))

        sql = "INSERT INTO company(acronym,companyid,companyname,company_short_name,phone,email,address_company,imageName,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(data_new['acronym'],data_new['companyid'],data_new['companyname'],data_new['company_short_name'],data_new['phone'],data_new['email'],data_new['address_company'],result[0]['imageName'],data_new['createby']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryCompany', methods=['POST'])
@connect_sql()
def QryCompany(cursor):
    try:
        sql = "SELECT id,companyid,companyname,company_short_name,email,address_company,imageName,phone,acronym FROM company"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/DeleteCompany', methods=['POST'])
@connect_sql()
def DeleteCompany(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT * FROM company WHERE companyid=%s"
        cursor.execute(sql,data_new['companyid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action= "Delete"

        sql_log = "INSERT INTO company_log(acronym,companyid,companyname,company_short_name,phone,email,address_company,imageName,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(result[0]['acronym'],result[0]['companyid'],result[0]['companyname'],result[0]['company_short_name'],result[0]['phone'],result[0]['email'],result[0]['address_company'],result[0]['imageName'],data_new['createby'],type_action))

        sqlDe = "DELETE FROM company WHERE companyid=%s"
        cursor.execute(sqlDe,(data_new['companyid']))

        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryCompanyname', methods=['POST'])
@connect_sql()
def QryCompanyname(cursor):
    try:
        sql = "SELECT companyid,companyname FROM company"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Insert_typeEm', methods=['POST'])
@connect_sql()
def Insert_typeEm(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        try:
            sqlQry = "SELECT typeEm_id FROM company_em ORDER BY typeEm_id DESC LIMIT 1"
            cursor.execute(sqlQry)
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            typeEm_id_last=result[0]['typeEm_id']+1
        except Exception as e:
            typeEm_id_last = 1

        sql = "INSERT INTO company_em (typeEm_id,typeEm_first,typeEm_year,typeEm_max,typeEm_detail,company_id,email,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(typeEm_id_last,data_new['typeEm_first'],data_new['typeEm_year'],data_new['typeEm_max'],data_new['typeEm_detail'],data_new['company_id'],data_new['email'],data_new['createby']))

        type_action = "ADD"

        sql_log = "INSERT INTO company_em_log (typeEm_id,typeEm_first,typeEm_year,typeEm_max,typeEm_detail,company_id,email,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(typeEm_id_last,data_new['typeEm_first'],data_new['typeEm_year'],data_new['typeEm_max'],data_new['typeEm_detail'],data_new['company_id'],data_new['email'],data_new['createby'],type_action))

        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Edit_typeEm', methods=['POST'])
@connect_sql()
def Edit_typeEm(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT * FROM company_em WHERE typeEm_id=%s"
        cursor.execute(sql,(data_new['typeEm_id']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Edit"

        sql_log = "INSERT INTO company_em_log (typeEm_id,typeEm_first,typeEm_year,typeEm_max,typeEm_detail,company_id,email,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(data_new['typeEm_id'],data_new['typeEm_first'],data_new['typeEm_year'],data_new['typeEm_max'],data_new['typeEm_detail'],data_new['company_id'],data_new['email'],data_new['createby'],type_action))

        sqlUp = "DELETE FROM company_em WHERE typeEm_id=%s"
        cursor.execute(sqlUp,(data_new['typeEm_id']))

        sqlIn = "INSERT INTO company_em (typeEm_id,typeEm_first,typeEm_year,typeEm_max,typeEm_detail,company_id,email,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn,(result[0]['typeEm_id'],data_new['typeEm_first'],data_new['typeEm_year'],data_new['typeEm_max'],data_new['typeEm_detail'],data_new['company_id'],data_new['email'],data_new['createby']))

        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qry_typeEm', methods=['POST'])
@connect_sql()
def Qry_typeEm(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT * FROM company_em WHERE company_id=%s"
        cursor.execute(sql,(data_new['company_id']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qry_Edit_Type_Employee', methods=['POST'])
@connect_sql()
def Qry_Edit_Type_Employee(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT * FROM company_em WHERE typeEm_id=%s"
        cursor.execute(sql,(data_new['typeEm_id']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Delete_typeEm', methods=['POST'])
@connect_sql()
def Delete_typeEm(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT * FROM company_em WHERE typeEm_id=%s"
        cursor.execute(sql,(data_new['typeEm_id']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Delete"

        sql_log = "INSERT INTO company_em_log (typeEm_id,typeEm_first,typeEm_year,typeEm_max,typeEm_detail,company_id,createby,email,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(data_new['typeEm_id'],data_new['typeEm_first'],data_new['typeEm_year'],data_new['typeEm_max'],data_new['typeEm_detail'],data_new['company_id'],data_new['email'],data_new['createby'],type_action))

        sqlUp = "DELETE FROM company_em WHERE typeEm_id=%s"
        cursor.execute(sqlUp,(data_new['typeEm_id']))

        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/gen_employeeid', methods=['POST'])
def gen_employeeid():
    dataInput = request.json
    source = dataInput['source']
    data_new = source

    connection = mysql.connect()
    cursor = connection.cursor()
    sql_type_em = "SELECT * FROM company_em WHERE company_id=%s AND typeEm_detail=%s"
    cursor.execute(sql_type_em,(data_new['company_id'],data_new['typeEm_detail']))
    columns = [column[0] for column in cursor.description]
    result_type_em = toJson(cursor.fetchall(),columns)
    max_all = str(len(result_type_em[0]['typeEm_max']))
    first_character =  result_type_em[0]['typeEm_first']
    type_year = result_type_em[0]['typeEm_year']
    start_date_ = data_new['Start_contract']
    split_str_date = start_date_.split("-")
    year_last = split_str_date[2]
    str_date_year = split_str_date[2]
    if type_year=='christ':
        str_date_year = str_date_year[2:]
    else:
        new_star = str(int(str_date_year)+543)
        str_date_year = new_star[2:]
    sql = "SELECT RIGHT(employeeid,{}) AS max_employeeid FROM employee WHERE company_id={} AND type_em='{}' AND start_work LIKE '%-%-{}' ORDER BY employeeid DESC LIMIT 1".format(max_all,data_new['company_id'],data_new['typeEm_detail'],year_last)
    cursor.execute(sql)
    columns = [column[0] for column in cursor.description]
    result = toJson(cursor.fetchall(),columns)
    connection.commit()
    connection.close()
    max = int(max_all)-1
    try:
        number = str(int(result[0]['max_employeeid'])+1)
    except Exception as e:
        number = '1'
    for i in range(max):
        last_em = "0"*(max-i)+str(number)
        if len(last_em)==(max+1):
            break
        if len(last_em)>max+1:
            last_em = last_em[1:]
    last_em_last = first_character+str_date_year+last_em
    last = []
    last.append(last_em_last)
    keyEm = ['employeeid']
    resultEm = dict(zip(keyEm,last))

    connection = mysql3.connect()
    cursor = connection.cursor()
    sqlAppform = "SELECT NameEn,SurnameEn FROM Personal WHERE EmploymentAppNo=%s"
    cursor.execute(sqlAppform,data_new['EmploymentAppNo'])
    columns = [column[0] for column in cursor.description]
    resultAppform = toJson(cursor.fetchall(),columns)
    connection.commit()
    connection.close()
    for item in resultAppform:
        prefix = ['Mr.', 'MS.', 'Mrs.','Acting Sub Lt.','Acting Sub Ly.']
        for i in xrange(len(prefix)):
    	    Name_e = item['NameEn'].split(prefix[i])
            if len(Name_e)==2:
                Name_ea = Name_e[1].lower()
            Surname_e = item['SurnameEn'].lower()
            two = Surname_e[:2]
    new_email = Name_ea+'.'+two+result_type_em[0]['email']
    last_email = []
    last_email.append(new_email)
    keyEmail = ['email']
    result_mail = dict(zip(keyEmail,last_email))
    sumall = dict(resultEm.items() + result_mail.items())
    all_result = []
    all_result.append(sumall)
    return jsonify(all_result)
@app.route('/userGetFile/<path>/<fileName>', methods=['GET'])
def userGetFile(path, fileName):
    # current_app.logger.info('userGetFile')
    # current_app.logger.info(path)
    # current_app.logger.info(fileName)
    return send_from_directory('../uploads/' + path, fileName)
    # return "ssss"
