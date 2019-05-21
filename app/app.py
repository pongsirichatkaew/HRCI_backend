#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *
from status.section import *
from status.quota import *
from status.org_name import *
from status.cost_center_name import *
from status.position import *
from status.company import *
from status.question_pro import *
from status.Admin import *
from status.employee_ga import *
from status.employee_MD import*
from status.assessor_probation import*
from status.assessor_quota import*
from status.assessor_kpi import*
from status.signature_crime import*
from status.employee_Deputy_Manager_Hr import*
from status.employee_Deputy_Manager_PayRoll import*
from status.Status import *
from status.mail_setting import *
from status.mail_hr import *
from employee.Employee import *
from employee.criminal import *
from employee.Contract import *
from employee.probation import *
from employee.kpi import *
from employee.kpi_user import *
from employee.request_employee import *
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
    result_token = CheckTokenAssessor(data_new['createby'],data_new['token'])
    if result_token!='pass':
        return 'token fail'
    return "success"
@app.route('/login', methods=['POST'])
def login():
    try:
        _data = request.json
        source = _data['source']
        data_new = source
        username = data_new['username']
        password = data_new['password']
        Gen_token = uuid.uuid4().hex
        connection = mysql2.connect()
        cursor = connection.cursor()
        sql = "SELECT * FROM user WHERE username = %s and password = %s ORDER BY id ASC LIMIT 1"
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

        sqlUp_token = "UPDATE Admin SET token=%s,time_token=now() WHERE username=%s"
        cursor.execute(sqlUp_token,(Gen_token,_output[0]['username']))

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

        sql5 = "SELECT * FROM assessor_quota WHERE email_asp=%s"
        cursor.execute(sql5,_output[0]['username'])
        data5 = cursor.fetchall()
        columns5 = [column[0] for column in cursor.description]
        _output5 = toJson(data5, columns5)
        for item5 in _output5:
            sum_permisssion5 = []
            sql5_ = "SELECT tier_approve FROM assessor_quota WHERE email_asp=%s GROUP BY tier_approve"
            cursor.execute(sql5_,_output[0]['username'])
            data5 = cursor.fetchall()
            columns5 = [column[0] for column in cursor.description]
            _output_per5 = toJson(data5, columns5)
            for i5 in _output_per5 :
                sum_permisssion5.append(i5)
            item5['tier_approve'] = sum_permisssion5

        sql4 = "SELECT * FROM assessor_kpi WHERE email_asp=%s"
        cursor.execute(sql4,_output[0]['username'])
        data4 = cursor.fetchall()
        columns4 = [column[0] for column in cursor.description]
        _output4 = toJson(data4, columns4)
        for item4 in _output4:
            sum_permisssion4 = []
            sql4_ = "SELECT type,companyid,org_name_id,status FROM assessor_kpi WHERE email_asp=%s AND status='active' GROUP BY type"
            cursor.execute(sql4_,_output[0]['username'])
            data4 = cursor.fetchall()
            columns4 = [column[0] for column in cursor.description]
            _output_per4 = toJson(data4, columns4)
            for i4 in _output_per4 :
                sum_permisssion4.append(i4)
            item4['type'] = sum_permisssion4
        # connection.commit()
        # connection.close()
        result={}
        result['message'] = 'login success'
        result['userid'] = _output[0]['userid']
        result['name'] = _output[0]['name']
        result['username'] = _output[0]['username']
        result['token'] = Gen_token
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
            sqlUp_token2 = "UPDATE assessor_pro SET token=%s,time_token=now() WHERE email_asp=%s"
            cursor.execute(sqlUp_token2,(Gen_token,_output[0]['username']))
        except Exception as e:
            result['permission2'] = ''
        try:
            result['permission4'] = _output4[0]['type']
            sqlUp_token4 = "UPDATE assessor_kpi SET token=%s,time_token=now() WHERE email_asp=%s"
            cursor.execute(sqlUp_token4,(Gen_token,_output[0]['username']))
        except Exception as e:
            result['permission4'] = ''
        try:
            result['permission3'] = _output5[0]['tier_approve']
            sqlUp_token5 = "UPDATE assessor_quota SET token=%s,time_token=now() WHERE email_asp=%s"
            cursor.execute(sqlUp_token5,(Gen_token,_output[0]['username']))
        except Exception as e:
            result['permission3'] = ''
        connection.commit()
        connection.close()
        return jsonify(result)
    except Exception as e:
        logserver(e)
        result2={}
        result2['message'] = 'login fail'
        return jsonify(result2)

if __name__ == '__main__':
    # context = ('ssl/inet.crt', 'ssl/inet.key')
    # app.run(debug=True,host='0.0.0.0',ssl_context=context,threaded=True,port=5000)
    app.run(debug=True,host='0.0.0.0',threaded=True,port=5000)
