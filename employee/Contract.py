#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/QryContract', methods=['POST'])
@connect_sql()
def QryContract(cursor):
    try:
        sql = "SELECT * FROM employee INNER JOIN company ON employee.company_id = company.companyid\
                                      INNER JOIN section ON employee.section_id = section.sect_id\
                                      INNER JOIN position ON employee.position_id = position.position_id\
        "
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        sql2 = "SELECT * FROM employee_MD  INNER JOIN company ON employee.position_id = employee_MD.position_id\
        WHERE companyid=%s"
        cursor.execute(sql2,result['company'])
        columns2 = [column[0] for column in cursor.description]
        result2 = toJson(cursor.fetchall(),columns2)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
