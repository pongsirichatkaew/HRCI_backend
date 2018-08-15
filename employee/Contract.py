#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/QryContract', methods=['POST'])
@connect_sql()
def QryContract(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        employeeid = ['employeeid']
        sql = "SELECT * FROM employee INNER JOIN company ON employee.company_id = company.companyid\
                                      INNER JOIN section ON employee.section_id = section.sect_id\
                                      INNER JOIN position ON employee.position_id = position.position_id\
                                      INNER JOIN Address ON employee.citizenid = Address.ID_CardNo\
                                      INNER JOIN Personal ON employee.citizenid = Personal.ID_CardNo\
        WHERE employeeid=%s"
        cursor.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        sql2 = "SELECT employee_MD.name_md,employee_MD.surname_md,employee_MD.position FROM employee_MD  INNER JOIN company ON employee_MD.company_id = company.companyid\
        WHERE companyid=%s"
        cursor.execute(sql2,result[0]['company_id'])
        columns2 = [column[0] for column in cursor.description]
        result2 = toJson(cursor.fetchall(),columns2)

        sql3 = "SELECT contract_id,Start_contract,End_contract,salary_thai FROM Contract WHERE ID_CardNo=%s"
        cursor.execute(sql3,result[0]['citizenid'])
        columns3 = [column[0] for column in cursor.description]
        result3 = toJson(cursor.fetchall(),columns3)
        tranCon_id = result3[0]['contract_id']
        if   tranCon_id<=9:
             tranCon=str(tranCon_id)
             codesumlast="000"+tranCon
        elif tranCon_id<=99:
             tranCon=str(tranCon_id)
             codesumlast="00"+tranCon
        elif tranCon_id<=999:
             tranCon=str(tranCon_id)
             codesumlast="0"+tranCon
        else:
             codesumlast=str(tranCon_id)

        # arr={}
        # arr["result"] = result
        # arr["result2"] = result2
        # arr["result3"] = codesumlast
        result[0]['name_md'] = result2[0]['name_md']
        result[0]['surname_md'] = result2[0]['surname_md']
        result[0]['position'] = result2[0]['position']
        return jsonify(result)
    except Exception as e:
        logserver(e)
@app.route('/QryListContract', methods=['POST'])
@connect_sql()
def QryListContract(cursor):
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        sql = "SELECT * FROM employee INNER JOIN company ON employee.company_id = company.companyid\
                                      INNER JOIN section ON employee.section_id = section.sect_id\
                                      INNER JOIN position ON employee.position_id = position.position_id\
                                      INNER JOIN org_name ON employee.org_name_id = org_name.org_name_id\
                                      INNER JOIN cost_center_name ON employee.cost_center_name_id = cost_center_name.cost_center_name_id\
        "
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        connection.close()
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
