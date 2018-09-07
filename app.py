from dbConfig import *
from status.section import *
from status.org_name import *
from status.cost_center_name import *
from status.position import *
from status.company import *
from status.Admin import *
from status.employee_MD import*
from status.signature_crime import*
from status.employee_Deputy_Manager_Hr import*
from status.employee_Deputy_Manager_PayRoll import*
from status.Status import *
from employee.Employee import *
from employee.criminal import *
from employee.Contract import *
from Appform.appform import *

@app.route('/hello', methods=['GET'])
def hello():
    return 'hello'
@app.route('/TestgenEM', methods=['POST'])
def TestgenEM():
    try:
        connection = mysql4.connect()
        cursor = connection.cursor()
        dataInput = request.json
        sql = "SELECT employeeid FROM test_employeeid WHERE companyid=%s ORDER BY employeeid DESC LIMIT 1"
        cursor.execute(sql,dataInput['companyid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sql2 = "SELECT first_com FROM test_company WHERE companyid=%s"
        cursor.execute(sql2,dataInput['companyid'])
        columns2 = [column[0] for column in cursor.description]
        result2 = toJson(cursor.fetchall(),columns2)
        connection.commit()
        connection.close()
        now = datetime.now()
        date = str(int(now.year)+543)
        form_employee = date[2:]
        type = result[0]['employeeid']
        codelast = int(str(type[-3:]))+1
        if   codelast<=9:
             codelast=str(codelast)
             codesumlast="00"+codelast
        elif codelast<=99:
             codelast=str(codelast)
             codesumlast="0"+codelast
        else:
             codesumlast=str(codelast)
        first_character = "OLS"
        sumone = str(result2[0]['first_com'])+form_employee+codesumlast
        return jsonify(sumone)
    except Exception as e:
        logserver(e)
        return "fail"
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
