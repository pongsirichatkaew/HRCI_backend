#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/InsertBenefits', methods=['POST'])
@connect_sql()
def InsertBenefits(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sqlQry = "SELECT benefits_id FROM benefits ORDER BY benefits_id DESC LIMIT 1"
        cursor.execute(sqlQry)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        benefits_id_last=result[0]['benefits_id']+1

        sql = "INSERT INTO benefits (benefits_id,benefits_detail,createby) VALUES (%s,%s,%s)"
        cursor.execute(sql,(benefits_id_last,data_new['benefits_detail'],data_new['createby']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditBenefits', methods=['POST'])
@connect_sql()
def EditBenefits(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT benefits_id FROM benefits WHERE benefits_id=%s"
        cursor.execute(sql,(data_new['benefits_id']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sqlUp = "UPDATE benefits SET validstatus=0 WHERE benefits_id=%s"
        cursor.execute(sqlUp,(data_new['benefits_id']))

        sqlIn = "INSERT INTO benefits (benefits_id,benefits_detail,createby) VALUES (%s,%s,%s)"
        cursor.execute(sqlIn,(result[0]['benefits_id'],data_new['benefits_detail'],data_new['createby']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/DeleteBenefits', methods=['POST'])
@connect_sql()
def DeleteBenefits(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql_OldTimeBenefits = "UPDATE benefits SET validstatus=0 WHERE benefits_id=%s"
        cursor.execute(sql_OldTimePosition,(data_new['benefits_id']))

        sql_NewTimeBenefits = "INSERT INTO benefits (benefits_id,benefits_detail,validstatus,createby) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql_NewTimePosition,(data_new['benefits_id'],data_new['benefits_detail'],0,data_new['createby']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryBenefits', methods=['POST'])
@connect_sql()
def QryBenefits(cursor):
    try:
        sql = "SELECT benefits_id,benefits_detail FROM benefits WHERE validstatus=1"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/test_test', methods=['POST'])
@connect_sql()
def test_test(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        start_date_ = data_new['Start_contract']
        split_str_date = start_date_.split("-")
        str_date_year = split_str_date[2]

        now_contract = datetime.now()
        date_contract = now_contract.year
        return jsonify(str_date_year)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryEmployee_ga', methods=['POST'])
@connect_sql()
def QryEmployee_ga(cursor):
    try:
        sql = "SELECT column_name FROM information_schema.columns WHERE table_schema = 'HRCI_Management' AND table_name = 'employee_ga' ;"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        string =""
        for item_ in result:
            # print item_['column_name']
            if item_['column_name'] in ['id','employeeid','citizenid','createby','create_at','validstatus']:
                pass
            else:
                print item_['column_name']
                if string=="":
                    string+=item_['column_name']
                else:
                    string+=","+item_['column_name']
        string_last= string.split(",")
        # create_key ตามค่าว่าง
        length_string = [ 'column_name' for i in range(len(string.split(",")))]
        json_result = zip(length_string,string_last)
        # แปลงข้อมูล เป็น dict ครอบด้วย list
        json_result_list = [ {x: y} for x, y in zip(length_string,string_last)]
        return jsonify(json_result_list)
    except Exception as e:
        logserver(e)
        return "fail"
