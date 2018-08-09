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
        # sql = "SELECT Name,Surname,MemberType,EmploymentAppNo FROM Family WHERE (MemberType ='Father'OR MemberType ='Mother') AND EmploymentAppNo"
        # cursor4.execute(sql)
        # columns = [column[0] for column in cursor4.description]
        # result = toJson(cursor4.fetchall(),columns)
        #
        # sql2 = "SELECT NameTh,SurnameTh,ID_CardNo,Birthdate,EmploymentAppNo FROM Personal"
        # cursor4.execute(sql2)
        # columns = [column[0] for column in cursor4.description]
        # result2 = toJson(cursor4.fetchall(),columns)
        #
        # sql3 = "SELECT AddressType,HouseNo,Street,DISTRICT_ID,AMPHUR_ID,PROVINCE_ID,PostCode,EmploymentAppNo FROM Address WHERE (AddressType ='Present'OR AddressType ='Home')"
        # cursor4.execute(sql3)
        # columns = [column[0] for column in cursor4.description]
        # result3 = toJson(cursor4.fetchall(),columns)
        # arr={}
        # arr["result"] = result
        # arr["result2"] = result2
        # arr["result3"] = result3
        sql4 ="""SELECT Personal.*,Address.AddressType, Address.HouseNo, Address.Street, Address.DISTRICT_ID, Address.AMPHUR_ID, Address.PROVINCE_ID, Address.PostCode, Address.Tel, Address.Fax,homeTable.AddressType as homeAddress, homeTable.HouseNo as homeHouseNo, homeTable.Street as homeStreet,
        homeTable.DISTRICT_ID as homeDistrict, homeTable.AMPHUR_ID as homeAmphur, homeTable.PROVINCE_ID as homeProvince, homeTable.PostCode as homePostCode, homeTable.Tel as homeTel, homeTable.Fax as homeFax,
        Family.Name as fatherName, Family.Surname as fatherSurname,motherTable.Name as motherName, motherTable.Surname as motherSurname
        FROM Personal
        LEFT JOIN Address ON Address.EmploymentAppNo = Personal.EmploymentAppNo
        LEFT JOIN Family ON Family.EmploymentAppNo = Personal.EmploymentAppNo
        LEFT JOIN (SELECT * FROM Address WHERE AddressType = 'Home') AS homeTable ON homeTable.EmploymentAppNo = Personal.EmploymentAppNo
        LEFT JOIN (SELECT * FROM Family WHERE MemberType = 'Mother') AS motherTable ON motherTable.EmploymentAppNo = Personal.EmploymentAppNo
        WHERE Address.AddressType = 'Present' and Family.MemberType = 'Father'"""
        cursor4.execute(sql4)
        columns = [column[0] for column in cursor4.description]
        result4 = toJson(cursor4.fetchall(),columns)
        return jsonify(result4)
    except Exception as e:
        logserver(e)
        return "fail"
