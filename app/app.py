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
from status.assessor_probation import*
from status.signature_crime import*
from status.employee_Deputy_Manager_Hr import*
from status.employee_Deputy_Manager_PayRoll import*
from status.Status import *
from employee.Employee import *
from employee.criminal import *
from employee.Contract import *
from employee.probation import *
from employee.kpi import *
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

    section_ = ['iostest','test2','iostest3','iostest4']
    org_name = ['','b','c','']
    new_section_ = []
    new_org_name = []
    for i in xrange(len(section_)):
        if section_[i].startswith("ios"):
            last = section_[i].replace(section_[i],"")
            new_section_.append(last)
            if org_name[i]=="":
              new_org_name.append(section_[i])
            else:
              new_org_name.append(org_name[i])
        else:
            last = section_[i]
            new_section_.append(last)
            new_org_name.append(org_name[i])
    print("------------------------------------------------")
    print(section_)
    print(new_section_)
    print("=================================================")
    print(org_name)
    print(new_org_name)
    testA = ['aa','bb','cc','dd','aaa']
    check_string = ('aaa','bb')
    for k in testA:
      if k.startswith(check_string):
          print(k)
    return "success"
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
        for item in _output2:
            sum_permisssion = []
            sql2 = "SELECT permission FROM Admin WHERE username=%s"
            cursor.execute(sql2,_output[0]['username'])
            data2 = cursor.fetchall()
            columns2 = [column[0] for column in cursor.description]
            _output_per = toJson(data2, columns2)
            for i2 in _output_per :
                sum_permisssion.append(i2)
            item['permission'] = sum_permisssion
        sql3 = "SELECT * FROM assessor_pro WHERE email_asp=%s"
        cursor.execute(sql3,_output[0]['username'])
        data3 = cursor.fetchall()
        columns3 = [column[0] for column in cursor.description]
        _output3 = toJson(data3, columns3)
        for item2 in _output3:
            sum_permisssion2 = []
            sql2_ = "SELECT tier_approve FROM assessor_pro WHERE email_asp=%s GROUP BY tier_approve"
            cursor.execute(sql2_,_output[0]['username'])
            data3 = cursor.fetchall()
            columns3 = [column[0] for column in cursor.description]
            _output_per2 = toJson(data3, columns3)
            for i3 in _output_per2 :
                sum_permisssion2.append(i3)
            item2['tier_approve'] = sum_permisssion2
        connection.commit()
        connection.close()
        result={}
        result['message'] = 'login success'
        result['userid'] = _output[0]['userid']
        result['name'] = _output[0]['name']
        result['username'] = _output[0]['username']
        try:
            result['permission'] = _output2[0]['permission']
        except Exception as e:
            new_arr = []
            user = ['user']
            key_ = ['permission']
            last_user = dict(zip(key_,user))
            new_arr.append(last_user)
            result['permission'] = new_arr
        try:
            result['permission2'] = _output3[0]['tier_approve']
        except Exception as e:
            result['permission2'] = ''
        return jsonify(result)
    except Exception as e:
        logserver(e)
        result2={}
        result2['message'] = 'login fail'
        return jsonify(result2)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',threaded=True,port=5000)
