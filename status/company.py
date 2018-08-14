#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/InsertCompany', methods=['POST'])
@connect_sql()
def InsertCompany(cursor):
    try:
        data = request.json
        source = data['source']
        new_data = source
        companyid = new_data['companyid']
        acronym = new_data['acronym']
        companyname = new_data['companyname']
        company_short_name = new_data['company_short_name']
        address_company = new_data['address_company']
        validstatus = new_data['validstatus']
        email = new_data['email']
        phone = new_data['phone']
        imageName = new_data['imageName']
        sql = "INSERT INTO company (companyid,acronym,companyname,company_short_name,email,address_company,phone,validstatus,imageName) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(companyid,acronym,companyname,company_short_name,email,address_company,phone,validstatus,imageName))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditCompany', methods=['POST'])
@connect_sql()
def EditCompany(cursor):
    try:
        data = request.json
        source = data['source']
        new_data = source
        id = new_data['id']
        companyid = new_data['companyid']
        acronym = new_data['acronym']
        companyname = new_data['companyname']
        company_short_name = new_data['company_short_name']
        email = new_data['email']
        phone = new_data['phone']
        address_company = new_data['address_company']
        validstatus = new_data['validstatus']
        imageName = new_data['imageName']
        sqlUp = "UPDATE company SET companyid=%s,acronym=%s,companyname=%s,company_short_name=%s,email=%s,address_company=%s,phone=%s,validstatus=%s,imageName=%s WHERE id=%s"
        cursor.execute(sqlUp,(companyid,acronym,companyname,company_short_name,email,address_company,phone,validstatus,imageName,id))
        # sqlIn = "INSERT INTO company (companyid,companyname,company_short_name,email,address_company,path_logo) VALUES (%s,%s,%s,%s,%s,%s)"
        # cursor.execute(sqlIn,(companyid,companyname,company_short_name,email,address_company,path_logo))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryCompany', methods=['POST'])
@connect_sql()
def QryCompany(cursor):
    try:
        sql = "SELECT id,companyid,companyname,company_short_name,email,address_company,imageName,phone,validstatus,acronym FROM company"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
