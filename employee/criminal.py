#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/QryCriminal', methods=['POST'])
@connect_sql()
def QryCriminal(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql ="""SELECT Personal.*,Address.AddressType, Address.HouseNo, Address.Street, Address.DISTRICT_ID, Address.AMPHUR_ID, Address.PROVINCE_ID, Address.PostCode, Address.Tel, Address.Fax,homeTable.AddressType as homeAddress, homeTable.HouseNo as homeHouseNo, homeTable.Street as homeStreet,
        homeTable.DISTRICT_ID as homeDistrict, homeTable.AMPHUR_ID as homeAmphur, homeTable.PROVINCE_ID as homeProvince, homeTable.PostCode as homePostCode, homeTable.Tel as homeTel, homeTable.Fax as homeFax,
        Family.Name as fatherName, Family.Surname as fatherSurname,motherTable.Name as motherName, motherTable.Surname as motherSurname
        FROM Personal
        LEFT JOIN Address ON Address.ID_CardNo = Personal.ID_CardNo
        LEFT JOIN Family ON Family.ID_CardNo = Personal.ID_CardNo
        LEFT JOIN (SELECT * FROM Address WHERE AddressType = 'Home') AS homeTable ON homeTable.ID_CardNo = Personal.ID_CardNo
        LEFT JOIN (SELECT * FROM Family WHERE MemberType = 'Mother') AS motherTable ON motherTable.ID_CardNo = Personal.ID_CardNo
        WHERE Address.AddressType = 'Present' and Family.MemberType = 'Father' AND Personal.ID_CardNo = %s """
        cursor.execute(sql,data_new['ID_CardNo'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryEmployeeList', methods=['POST'])
@connect_sql()
def QryEmployeeList(cursor):
    try:
        sql = "SELECT NameTh,SurnameTh,NicknameTh,ID_CardNo FROM Personal"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryAllEmployeeCrimeList', methods=['POST'])
@connect_sql()
def QryAllEmployeeCrimeList(cursor):
    try:
        sql4 ="""SELECT Personal.*,Address.AddressType, Address.HouseNo, Address.Street, Address.DISTRICT_ID, Address.AMPHUR_ID, Address.PROVINCE_ID, Address.PostCode, Address.Tel, Address.Fax,homeTable.AddressType as homeAddress, homeTable.HouseNo as homeHouseNo, homeTable.Street as homeStreet,
        homeTable.DISTRICT_ID as homeDistrict, homeTable.AMPHUR_ID as homeAmphur, homeTable.PROVINCE_ID as homeProvince, homeTable.PostCode as homePostCode, homeTable.Tel as homeTel, homeTable.Fax as homeFax,
        Family.Name as fatherName, Family.Surname as fatherSurname,motherTable.Name as motherName, motherTable.Surname as motherSurname
        FROM Personal
        LEFT JOIN Address ON Address.ID_CardNo = Personal.ID_CardNo
        LEFT JOIN Family ON Family.ID_CardNo = Personal.ID_CardNo
        LEFT JOIN (SELECT * FROM Address WHERE AddressType = 'Home') AS homeTable ON homeTable.ID_CardNo = Personal.ID_CardNo
        LEFT JOIN (SELECT * FROM Family WHERE MemberType = 'Mother') AS motherTable ON motherTable.ID_CardNo = Personal.ID_CardNo
        WHERE Address.AddressType = 'Present' and Family.MemberType = 'Father'"""
        cursor.execute(sql4)
        columns = [column[0] for column in cursor.description]
        result4 = toJson(cursor.fetchall(),columns)
        return jsonify(result4)
    except Exception as e:
        logserver(e)
        return "fail"
