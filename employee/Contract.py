#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/QryContract', methods=['POST'])
def connect_sql():
def QryContract(cursor):
    try:
        sql = "SELECT * FROM employee \
        INNER JOIN company ON employee.companyid = company.companyid\
        INNER JOIN section "
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
