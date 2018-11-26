#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *
from status.section import *
from status.org_name import *
from status.cost_center_name import *
from status.position import *
from status.company import *
from status.question_pro import *
from status.Admin import *
from status.employee_ga import *
from status.employee_MD import*
from status.signature_crime import*
from status.employee_Deputy_Manager_Hr import*
from status.employee_Deputy_Manager_PayRoll import*
from status.Status import *
from employee.Employee import *
from employee.criminal import *
from employee.Contract import *
from employee.probation import *
from Appform.appform import *

@app.route('/hello', methods=['GET'])
def hello():
    return 'hello'
@app.route('/TestgenEM', methods=['POST'])
@connect_sql()
def TestgenEM(cursor):
    dataInput = request.json
    source = dataInput['source']
    data_new = source

    sql = """SELECT employee.id,employee.employeeid,employee.name_th,employee.surname_th,employee.name_eng,employee.surname_eng,employee.salary,position.position_detail,section.sect_detail,org_name.org_name_detail,\
    cost_center_name.cost_detail,company.companyname,employee.start_work,employee_ga.phone_depreciate,\
    employee_ga.notebook_depreciate,employee_ga.limit_phone,employee_ga.chair_table,employee_ga.pc,\
    employee_ga.notebook,employee_ga.office_equipment,employee_ga.ms,employee_ga.car_ticket,\
    employee_ga.band_car,employee_ga.color,employee_ga.regis_car_number,employee_ga.other,employee_ga.description FROM employee \
		                              LEFT JOIN company ON company.companyid = employee.company_id \
                                      LEFT JOIN position ON position.position_id = employee.position_id \
                                      LEFT JOIN section ON section.sect_id = employee.section_id \
                                      LEFT JOIN org_name ON org_name.org_name_id = employee.org_name_id \
                                      LEFT JOIN cost_center_name ON cost_center_name.cost_center_name_id = employee.cost_center_name_id \
		                              LEFT JOIN employee_ga ON employee_ga.employeeid = employee.employeeid \
                                      LEFT JOIN status ON status.status_id = employee.validstatus \
    WHERE employee.validstatus=1 AND position.validstatus=1 AND section.validstatus=1 AND org_name.validstatus=1 AND status.validstatus=1 AND cost_center_name.validstatus=1 AND status.validstatus=1 AND employee_ga.validstatus=1"""
    cursor.execute(sql)
    columns = [column[0] for column in cursor.description]
    result = toJson(cursor.fetchall(),columns)
    for item_ in result:
        item_['salary'] = base64.b64decode(item_['salary'])
    return jsonify(result)
@app.route('/login', methods=['POST'])
def login():
    try:
        _data = request.json
        source = _data['source']
        data_new = source
        username = data_new['username']
        password = data_new['password']
        connection = mysql2.connect()
        cursor = connection.cursor()
        sql = "SELECT * FROM user WHERE username = %s and password = %s"
        cursor.execute(sql,(username, hashlib.sha512(password).hexdigest()))
        data = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        _output = toJson(data, columns)
        connection.commit()
        connection.close()

        connection = mysql.connect()
        cursor = connection.cursor()
        sql2 = "SELECT * FROM Admin WHERE username=%s"
        cursor.execute(sql2,_output[0]['username'])
        data2 = cursor.fetchall()
        columns2 = [column[0] for column in cursor.description]
        _output2 = toJson(data2, columns2)
        connection.commit()
        connection.close()
        result={}
        result['message'] = 'login success'
        result['userid'] = _output[0]['userid']
        result['name'] = _output[0]['name']
        result['username'] = _output[0]['username']
        result['permission'] = _output2[0]['permission']
        return jsonify(result)
    except Exception as e:
        logserver(e)
        result2={}
        result2['message'] = 'login fail'
        return jsonify(result2)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',threaded=True,port=5000)
