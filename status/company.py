#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/InsertCompany', methods=['POST'])
@connect_sql()
def InsertCompany(cursor):
    try:
        data = request.json
        source = data['source']
        data_new = source

        sqlQry = "SELECT companyid FROM company ORDER BY companyid DESC LIMIT 1"
        cursor.execute(sqlQry)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        companyid_last=result[0]['companyid']+1

        sql = "INSERT INTO company(acronym,companyid,companyname,company_short_name,phone,email,address_company,imageName) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(data_new['acronym'],companyid_last,data_new['companyname'],data_new['company_short_name'],data_new['phone'],data_new['email'],data_new['address_company'],data_new['imageName']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
        # dataInput = request.json
        # sqlQry = "SELECT companyid FROM company ORDER BY companyid DESC LIMIT 1"
        # cursor3.execute(sqlQry)
        # columns = [column[0] for column in cursor3.description]
        # result = toJson(cursor3.fetchall(),columns)
        # company_id_last=result[0]['companyid']+1

        # currentTime = datetime.datetime.today().strftime('%Y%m%d%H%M%S%f')
        # path = 'uploads/users/' + request.form['userId']
        # if not os.path.exists(path):
        #     os.makedirs(path)
        # if request.method == 'POST':
        #     file = request.files['file']
        # if file:
    	#   file.save(os.path.join(path, currentTime + '_profile_img.png'))
        #   userLogSaveFile(request.form['userId'], currentTime + '_profile_img.png')
        # else:
        #   return 'file is not allowed'

        # sql = "INSERT INTO company (companyid,acronym,companyname,company_short_name,email,address_company,phone,imageName) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        # cursor.execute(sql,(company_id_last,result['acronym'],result['companyname'],result['company_short_name'],result['email'],result['address_company'],result['phone'],imageName))
    #     return "success"
    # except Exception as e:
    #     logserver(e)
    #     return "fail"
@app.route('/EditCompany', methods=['POST'])
@connect_sql()
def EditCompany(cursor):
    try:
        data = request.json
        source = data['source']
        data_new = source

        sqlUp = "UPDATE company SET validstatus= 0 WHERE companyid=%s"
        cursor.execute(sqlUp,(data_new['companyid']))

        sqlIn = "INSERT INTO company(acronym,companyid,companyname,company_short_name,phone,email,address_company,imageName) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn,(data_new['acronym'],data_new['companyid'],data_new['companyname'],data_new['company_short_name'],data_new['phone'],data_new['email'],data_new['address_company'],data_new['imageName']))
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

        sql_OldTimeCompany = "UPDATE company SET validstatus=0 WHERE companyid=%s"
        cursor.execute(sql_OldTimeCompany,(data_new['companyid']))

        sql_NewTimeCompany = "INSERT INTO company(acronym,companyid,companyname,company_short_name,phone,email,address_company,imageName,validstatus) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_NewTimeCompany,(data_new['acronym'],data_new['companyid'],data_new['companyname'],data_new['company_short_name'],data_new['phone'],data_new['email'],data_new['address_company'],data_new['imageName'],0))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
