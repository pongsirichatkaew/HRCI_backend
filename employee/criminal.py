#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/QryCriminal', methods=['POST'])
@connect_sql4()
def QryCriminal(cursor4):
    try:
        dataInput = request.json
        # source = dataInput['source']
        # data_new = source
        sql = "SELECT Name,Surname,MemberType FROM Family WHERE (MemberType ='Father'OR MemberType ='Mother')AND EmploymentAppNo=%s"
        cursor4.execute(sql,dataInput['EmploymentAppNo'])
        columns = [column[0] for column in cursor4.description]
        result = toJson(cursor4.fetchall(),columns)

        sql2 = "SELECT NameTh,SurnameTh,ID_CardNo,Birthdate FROM Personal WHERE EmploymentAppNo=%s"
        cursor4.execute(sql2,dataInput['EmploymentAppNo'])
        columns = [column[0] for column in cursor4.description]
        result2 = toJson(cursor4.fetchall(),columns)

        sql3 = "SELECT AddressType,HouseNo,Street,DISTRICT_ID,AMPHUR_ID,PROVINCE_ID,PostCode FROM Address WHERE (AddressType ='Present'OR AddressType ='Home') AND EmploymentAppNo=%s"
        cursor4.execute(sql3,dataInput['EmploymentAppNo'])
        columns = [column[0] for column in cursor4.description]
        result3 = toJson(cursor4.fetchall(),columns)
        arr={}
        arr["result"] = result
        arr["result2"] = result2
        arr["result3"] = result3

        return jsonify(arr)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryEmployeeList', methods=['POST'])
@connect_sql4()
def QryEmployeeList(cursor):
    try:
        sql = "SELECT EmploymentAppNo,NameTh,SurnameTh,NicknameTh FROM Personal"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryAllEmployeeCrimeList', methods=['POST'])
@connect_sql4()
def QryAllEmployeeCrimeList(cursor4):
    try:
        sql = "SELECT Name,Surname,MemberType FROM Family WHERE (MemberType ='Father'OR MemberType ='Mother')"
        cursor4.execute(sql)
        columns = [column[0] for column in cursor4.description]
        result = toJson(cursor4.fetchall(),columns)

        sql2 = "SELECT NameTh,SurnameTh,ID_CardNo,Birthdate FROM Personal"
        cursor4.execute(sql2)
        columns = [column[0] for column in cursor4.description]
        result2 = toJson(cursor4.fetchall(),columns)

        sql3 = "SELECT AddressType,HouseNo,Street,DISTRICT_ID,AMPHUR_ID,PROVINCE_ID,PostCode FROM Address WHERE (AddressType ='Present'OR AddressType ='Home')"
        cursor4.execute(sql3)
        columns = [column[0] for column in cursor4.description]
        result3 = toJson(cursor4.fetchall(),columns)
        arr={}
        arr["result"] = result
        arr["result2"] = result2
        arr["result3"] = result3

        return jsonify(arr)
    except Exception as e:
        logserver(e)
        return "fail"
