#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *
@app.route('/Add_project', methods=['POST'])
@connect_sql()
def Add_project(cursor):
    try:
        sql = "SELECT employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,grade,comment_hr,group_kpi,star_date_kpi,status FROM employee_kpi "
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
