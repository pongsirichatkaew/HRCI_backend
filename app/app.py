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
from mobile.kpi_mobile import *
from apiAlertOnechat import *

@app.route('/hello', methods=['GET'])
def hello():
    return 'Hello pm2.5 , Im updated at 30/08/2019 18:30'
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
        #login with intranet
        try:
            connection = mysql2.connect()
            cursor = connection.cursor()
            sql_employee = "SELECT code FROM hrci WHERE email = %s AND workstatus='Active' ORDER BY id ASC LIMIT 1"
            cursor.execute(sql_employee,(username))
            data = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            check_employeeid = toJson(data, columns)
            sql = "SELECT * FROM user WHERE username = %s and password = %s and userid=%s ORDER BY id ASC LIMIT 1"
            cursor.execute(sql,(username, hashlib.sha512(password).hexdigest(),check_employeeid[0]['code']))
            data = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            _output = toJson(data, columns)
            connection.commit()
            connection.close()
            username = _output[0]['username']
            name = _output[0]['name']
            code = _output[0]['userid']
        #login with oneid
        except Exception as e:
            payload =   {
                            "grant_type":"password",
                            "client_id":"151",
                            "client_secret":"lJO7R2FwahEp5fppIDvh7M1OLARBjHXmfOrHr1z1",
                            "username":username,
                            "password":password
                        }
            response = callServer("https://one.th/api/oauth/getpwd",payload)

            if response['status'] == 'success':
                response = response['response'].json()

                if 'result' in response :
                    if response['result'] == 'Fail':
                        return jsonify({'status':'fail','message':"Wrong Username / Password"})

                    if 'token_type' in response and 'access_token' in response:
                        accessTokenOneID = response['token_type']+' '+response['access_token']
                        refresh_token = response['refresh_token']
                        access_token = response['access_token']
                    else:
                        print '##################### access_token not found ##################'
                        return jsonify({'status':'fail','message':"access_token not found"})
                else:
                    print '##################### No result from oneid ##################'

                    return jsonify({'status':'fail','message':"No result from oneid"})

                authenticationOneID = getAuthorizationAPI("https://one.th/api/account_and_biz_detail",accessTokenOneID)
                if authenticationOneID['status'] == 'success':
                    authenticationOneID = authenticationOneID['response'].json()
                    onemail = authenticationOneID['thai_email2']
                    connection = mysql2.connect()
                    cursor = connection.cursor()
                    sql_employee = "SELECT * FROM hrci WHERE onemail = %s AND workstatus='Active' ORDER BY id ASC LIMIT 1"
                    cursor.execute(sql_employee,onemail)
                    data = cursor.fetchall()
                    columns = [column[0] for column in cursor.description]
                    check_employeeid = toJson(data, columns)
                    username = check_employeeid[0]['email']
                    name = check_employeeid[0]['engname']
                    code = check_employeeid[0]['code']
        # _output = []
        # _output.append({})
        # _output[0]['userid']='61330'
        # _output[0]['name']='Korakot'
        # _output[0]['username']='korakot.bu@inet.co.th'
        connection = mysql.connect()
        cursor = connection.cursor()
        sql2 = "SELECT * FROM Admin WHERE username=%s"
        cursor.execute(sql2,username)
        data2 = cursor.fetchall()
        columns2 = [column[0] for column in cursor.description]
        _output2 = toJson(data2, columns2)
        for item in _output2:
            sum_permisssion = []
            sql2 = "SELECT permission FROM Admin WHERE username=%s"
            cursor.execute(sql2,username)
            data2 = cursor.fetchall()
            columns2 = [column[0] for column in cursor.description]
            _output_per = toJson(data2, columns2)
            for i2 in _output_per :
                sum_permisssion.append(i2)
            item['permission'] = sum_permisssion

        sqlUp_token = "UPDATE Admin SET token=%s,time_token=now() WHERE username=%s"
        cursor.execute(sqlUp_token,(Gen_token,username))

        sql3 = "SELECT * FROM assessor_pro WHERE email_asp=%s"
        cursor.execute(sql3,username)
        data3 = cursor.fetchall()
        columns3 = [column[0] for column in cursor.description]
        _output3 = toJson(data3, columns3)
        for item2 in _output3:
            sum_permisssion2 = []
            sql2_ = "SELECT tier_approve FROM assessor_pro WHERE email_asp=%s GROUP BY tier_approve"
            cursor.execute(sql2_,username)
            data3 = cursor.fetchall()
            columns3 = [column[0] for column in cursor.description]
            _output_per2 = toJson(data3, columns3)
            for i3 in _output_per2 :
                sum_permisssion2.append(i3)
            item2['tier_approve'] = sum_permisssion2

        sql5 = "SELECT * FROM assessor_quota WHERE email_asp=%s"
        cursor.execute(sql5,username)
        data5 = cursor.fetchall()
        columns5 = [column[0] for column in cursor.description]
        _output5 = toJson(data5, columns5)
        for item5 in _output5:
            sum_permisssion5 = []
            sql5_ = "SELECT tier_approve FROM assessor_quota WHERE email_asp=%s GROUP BY tier_approve"
            cursor.execute(sql5_,username)
            data5 = cursor.fetchall()
            columns5 = [column[0] for column in cursor.description]
            _output_per5 = toJson(data5, columns5)
            for i5 in _output_per5 :
                sum_permisssion5.append(i5)
            item5['tier_approve'] = sum_permisssion5

        sql4 = "SELECT * FROM assessor_kpi WHERE email_asp=%s"
        cursor.execute(sql4,username)
        data4 = cursor.fetchall()
        columns4 = [column[0] for column in cursor.description]
        _output4 = toJson(data4, columns4)
        for item4 in _output4:
            sum_permisssion4 = []
            sql4_ = "SELECT type,companyid,org_name_id,status FROM assessor_kpi WHERE email_asp=%s  GROUP BY type"
            cursor.execute(sql4_,username)
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
        result['userid'] = code
        result['name'] = name
        result['username'] = username
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
            cursor.execute(sqlUp_token2,(Gen_token,username))
        except Exception as e:
            result['permission2'] = ''
        try:
            result['permission4'] = _output4[0]['type']
            sqlUp_token4 = "UPDATE assessor_kpi SET token=%s,time_token=now() WHERE email_asp=%s"
            cursor.execute(sqlUp_token4,(Gen_token,username))
        except Exception as e:
            result['permission4'] = ''
        try:
            result['permission3'] = _output5[0]['tier_approve']
            sqlUp_token5 = "UPDATE assessor_quota SET token=%s,time_token=now() WHERE email_asp=%s"
            cursor.execute(sqlUp_token5,(Gen_token,username))
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

def callServer(path, data):
    url = path
    payload = data
    try:
        response = requests.request("POST", url=url, json=payload, verify=False, stream=True, timeout=99)
        return {'status': 'success','response': response}
    except requests.HTTPError:
        current_app.logger.info("HTTP error occurred.")
        return {'status': 'HTTPError','message': "HTTP error occurred."}
    except requests.Timeout:
        current_app.logger.info("Request timed out.")
        return {'status': 'Timeout','message': 'Request timed out'}
    except requests.ConnectionError:
        current_app.logger.info("API Connection error occurred.")
        return {'status': 'ConnectionError','message': 'API Connection error occurred.'}
    except Exception as ex:
        current_app.logger.info("An unexpected error: " + ex.__str__())
        return {'status': 'fail','message': 'An unexpected error: ' + ex.__str__()}

def getAuthorizationAPI(path, data):
    url = path
    payload = data
    try:
        response = requests.get(url, headers={'Authorization': payload}, verify=False, stream=True, timeout=99)
        return {'status': 'success','response': response}
    except requests.HTTPError:
        current_app.logger.info("HTTP error occurred.")
        return {'status': 'HTTPError','message': "HTTP error occurred."}
    except requests.Timeout:
        current_app.logger.info("Request timed out.")
        return {'status': 'Timeout','message': 'Request timed out'}
    except requests.ConnectionError:
        current_app.logger.info("API Connection error occurred.")
        return {'status': 'ConnectionError','message': 'API Connection error occurred.'}
    except Exception as ex:
        current_app.logger.info("An unexpected error: " + ex.__str__())
        return {'status': 'fail','message': 'An unexpected error: ' + ex.__str__()}

if __name__ == '__main__':
    context = ('ssl/inet.crt', 'ssl/inet.key')
    app.run(debug=True,host='0.0.0.0',ssl_context=context,threaded=True,port=5000)
    # app.run(debug=True,host='0.0.0.0',threaded=True,port=8888)
