#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/QryCriminal', methods=['POST'])
@connect_sql4()
def QryCriminal(cursor4):
    try:
        dataInput = request.json
        # sql = "SELECT Personal.NameTh,Personal.SurnameTh,Personal.ID_CardNo,Personal.Birthdate, \
        #  Family.MemberType = (SELECT MemberType FROM Family WHERE MemberType ='Father'), \
        #   Family.Name,Family.Surname,Address.AddressType,Address.HouseNo,Address.Street,Address.DISTRICT_ID,Address.AMPHUR_ID,Address.PROVINCE_ID,Address.PostCode FROM Personal INNER JOIN Address ON Address.ID_CardNo = Personal.ID_CardNo\
        #                                                     INNER JOIN Family ON Family.ID_CardNo = Personal.ID_CardNo \
        # "
        # cursor4.execute(sql)
        # columns = [column[0] for column in cursor4.description]
        # result = toJson(cursor4.fetchall(),columns)
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

        return jsonify(result,result2,result3)
    except Exception as e:
        logserver(e)
        return "fail"
