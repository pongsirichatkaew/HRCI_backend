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
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditCompany', methods=['POST'])
@connect_sql()
def EditCompany(cursor):
    try:
        sqlUp = "UPDATE company SET validstatus=0,createby=%s WHERE companyid=%s"
        cursor.execute(sqlUp,(request.form['createby'],request.form['companyid']))

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

        sql = "SELECT imageName FROM company WHERE companyid=%s"
        cursor.execute(sql,data_new['companyid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sqlUp = "UPDATE company SET validstatus=0,createby=%s WHERE companyid=%s"
        cursor.execute(sqlUp,(data_new['createby'],data_new['companyid']))

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
        sql = "SELECT id,companyid,companyname,company_short_name,email,address_company,imageName,phone,validstatus,acronym FROM company WHERE validstatus =1"
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

        sql_OldTimeCompany = "UPDATE company SET validstatus=0,createby=%s WHERE companyid=%s"
        cursor.execute(sql_OldTimeCompany,(data_new['createby'],data_new['companyid']))

        sql_NewTimeCompany = "INSERT INTO company(acronym,companyid,companyname,company_short_name,phone,email,address_company,imageName,createby,validstatus) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_NewTimeCompany,(data_new['acronym'],data_new['companyid'],data_new['companyname'],data_new['company_short_name'],data_new['phone'],data_new['email'],data_new['address_company'],data_new['imageName'],data_new['createby'],0))
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
