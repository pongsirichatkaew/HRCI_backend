#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/Insertquota', methods=['POST'])
@connect_sql()
def Insertquota(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sqlQry = "SELECT quota_id FROM quota ORDER BY quota_id DESC LIMIT 1"
        cursor.execute(sqlQry)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        quota_id_last=result[0]['quota_id']+1

        sql = "INSERT INTO quota (quota_id,year,companyid,position_id,member,createby) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(quota_id_last,data_new['year'],data_new['companyid'],data_new['position_id'],data_new['member'],data_new['createby']))

        type_action = "ADD"

        sql_log = "INSERT INTO quota_log (quota_id,year,companyid,position_id,member,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(quota_id_last,data_new['year'],data_new['companyid'],data_new['position_id'],data_new['member'],data_new['createby'],type_action))

        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Editquota', methods=['POST'])
@connect_sql()
def Editquota(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT quota_id,year,position_id,companyid,member FROM quota WHERE quota_id=%s"
        cursor.execute(sql,(data_new['quota_id']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Edit"

        sql_log = "INSERT INTO quota_log (quota_id,year,companyid,position_id,member,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(result[0]['quota_id'],result[0]['year'],result[0]['companyid'],result[0]['position_id'],result[0]['member'],data_new['createby'],type_action))

        sqlUp = "DELETE FROM quota WHERE quota_id=%s"
        cursor.execute(sqlUp,(data_new['quota_id']))

        sqlIn = "INSERT INTO quota (quota_id,year,companyid,position_id,member,createby) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn,(result[0]['quota_id'],,data_new['year']data_new['companyid'],data_new['position_id'],data_new['member'],data_new['createby']))

        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qryquota', methods=['POST'])
@connect_sql()
def Qryquota(cursor):
    try:
        sql = "SELECT quota.quota_id,quota.year,company.companyid,company.company_short_name,position.position_detail,quota.position_id,quota.member FROM quota LEFT JOIN company ON company.companyid = quota.companyid\
                                                                                                                                   LEFT JOIN position ON position.position_id = quota.position_id"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Deletequota', methods=['POST'])
@connect_sql()
def Deletequota(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT quota_id,year,position_id,companyid,member FROM quota WHERE quota_id=%s"
        cursor.execute(sql,(data_new['quota_id']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Delete"

        sql_log = "INSERT INTO quota_log (quota_id,year,companyid,position_id,member,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(result[0]['quota_id'],result[0]['year'],result[0]['companyid'],result[0]['position_id'],result[0]['member'],data_new['createby'],type_action))

        sqlUp = "DELETE FROM quota WHERE quota_id=%s"
        cursor.execute(sqlUp,(data_new['quota_id']))

        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
