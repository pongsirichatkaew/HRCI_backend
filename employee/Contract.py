#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/QryContract', methods=['POST'])
@connect_sql()
def QryContract(cursor):
    try:
        dataInput = request.json
        sql = "SELECT * FROM employee INNER JOIN company ON company.companyid = employee.companyid\
                                      INNER JOIN Address ON Address.ID_CardNo = employee.ID_CardNo\
               WHERE employee.employeeid=%s"
        cursor.execute(sql,dataInput['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
