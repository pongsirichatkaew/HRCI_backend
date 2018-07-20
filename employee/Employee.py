#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/QryEmployee', methods=['POST'])
def QryEmployee():
    try:
        connection = mysql3.connect()
        cursor = connection.cursor()
        data = request.json
        citizenid = data['citizenid']
        EmploymentAppNo = data['EmploymentAppNo']
        sql = "SELECT EmploymentAppNo,AppliedPosition1,AppliedPosition2,StartExpectedSalary,EndExpectedSalary,NameTh,SurnameTh,Mobile,Email,date FROM Personal WHERE ID_CardNo=%s AND EmploymentAppNo=%s"
        cursor.execute(sql,(citizenid,EmploymentAppNo))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        connection.close()

        # connection = mysql.connect()
        # cursor = connection.cursor()
        # sqlIn = "INSERT INTO employee (employeeid,citizenid,name_th,name_eng,surname_th,surname_eng,nickname_employee,address_employee,salary,email,,phone_company,position_id,section_id,org_name_id,cost_center_name_id,company_id,start_work) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # cursor.execute(sqlIn,(status_detail,path_color))
        # connection.commit()
        # connection.close()
        # return "success"

        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
