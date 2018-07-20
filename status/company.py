#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/InsertCompany', methods=['POST'])
@connect_sql()
def InsertCompany(cursor):
    try:
        data = request.json
        companyid = data['companyid']
        companyname = data['companyname']
        company_short_name = data['company_short_name']
        address_company = data['address_company']
        path_logo = data['path_logo']
        email = data['email']
        sql = "INSERT INTO company (companyid,companyname,company_short_name,email,address_company,path_logo) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(companyid,companyname,company_short_name,email,address_company,path_logo))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditCompany', methods=['POST'])
@connect_sql()
def EditCompany(cursor):
    try:
        data = request.json
        id = data['id']
        companyid = data['companyid']
        companyname = data['companyname']
        company_short_name = data['company_short_name']
        email = data['email']
        address_company = data['address_company']
        path_logo = data['path_logo']
        sqlUp = "UPDATE company SET validstatus = '0' WHERE id=%s"
        cursor.execute(sqlUp,(data['id']))
        sqlIn = "INSERT INTO company (companyid,companyname,company_short_name,email,address_company,path_logo) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn,(companyid,companyname,company_short_name,email,address_company,path_logo))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryCompany', methods=['POST'])
@connect_sql()
def QryCompany(cursor):
    try:
        sql = "SELECT id,companyid,companyname,company_short_name,email,address_company,path_logo FROM company WHERE validstatus=1"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
