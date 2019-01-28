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

        sql = "INSERT INTO company_em (typeEm_id,typeEm_first,typeEm_year,typeEm_max,typeEm_detail,company_id,createby) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(typeEm_id_last,data_new['typeEm_first'],data_new['typeEm_year'],data_new['typeEm_max'],data_new['typeEm_detail'],data_new['company_id'],data_new['createby']))

        type_action = "ADD"

        sql_log = "INSERT INTO company_em_log (typeEm_id,typeEm_first,typeEm_year,typeEm_max,typeEm_detail,company_id,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(typeEm_id_last,data_new['typeEm_first'],data_new['typeEm_year'],data_new['typeEm_max'],data_new['typeEm_detail'],data_new['company_id'],data_new['createby'],type_action))

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

        sql_log = "INSERT INTO company_em_log (typeEm_id,typeEm_first,typeEm_year,typeEm_max,typeEm_detail,company_id,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(data_new['typeEm_id'],data_new['typeEm_first'],data_new['typeEm_year'],data_new['typeEm_max'],data_new['typeEm_detail'],data_new['company_id'],data_new['createby'],type_action))

        sqlUp = "DELETE FROM company_em WHERE typeEm_id=%s"
        cursor.execute(sqlUp,(data_new['typeEm_id']))

        sqlIn = "INSERT INTO company_em (typeEm_id,typeEm_first,typeEm_year,typeEm_max,typeEm_detail,company_id,createby) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn,(result[0]['typeEm_id'],data_new['typeEm_first'],data_new['typeEm_year'],data_new['typeEm_max'],data_new['typeEm_detail'],data_new['company_id'],data_new['createby']))

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

        sql_log = "INSERT INTO company_em_log (typeEm_id,typeEm_first,typeEm_year,typeEm_max,typeEm_detail,company_id,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(data_new['typeEm_id'],data_new['typeEm_first'],data_new['typeEm_year'],data_new['typeEm_max'],data_new['typeEm_detail'],data_new['company_id'],data_new['createby'],type_action))

        sqlUp = "DELETE FROM company_em WHERE typeEm_id=%s"
        cursor.execute(sqlUp,(data_new['typeEm_id']))

        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/userGetFile/<path>/<fileName>', methods=['GET'])
def userGetFile(path, fileName):
    # current_app.logger.info('userGetFile')
    # current_app.logger.info(path)
    # current_app.logger.info(fileName)
    return send_from_directory('../uploads/' + path, fileName)
    # return "ssss"
