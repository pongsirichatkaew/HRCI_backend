#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/QryContract', methods=['POST'])
@connect_sql()
def QryContract(cursor):
    try:
        dataInput = request.json
        sql = "SELECT * FROM employee INNER JOIN company ON employee.company_id = company.companyid\
                                      INNER JOIN section ON employee.section_id = section.sect_id\
                                      INNER JOIN position ON employee.position_id = position.position_id\
        WHERE employeeid=%s"
        cursor.execute(sql,dataInput['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        sql2 = "SELECT employee_MD.name_md,employee_MD.surname_md,employee_MD.position FROM employee_MD  INNER JOIN company ON employee_MD.company_id = company.companyid\
        WHERE companyid=%s"
        cursor.execute(sql2,result[0]['company_id'])
        columns2 = [column[0] for column in cursor.description]
        result2 = toJson(cursor.fetchall(),columns2)
        arr={}
        arr["result"] = result
        arr["result2"] = result2
        return jsonify(arr)
    except Exception as e:
        logserver(e)
        return "fail"
