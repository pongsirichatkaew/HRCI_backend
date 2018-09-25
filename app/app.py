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
@connect_sql()
def TestgenEM(cursor):
    # try:
    # dataInput = request.json
    # companyid__ = int(dataInput['company_id'])
    # if companyid__==1:
    #     now = datetime.now()
    #     date_n = str(int(now.year))
    #     form_employee = date_n
    # elif companyid__==21:
    #     now = datetime.now()
    #     date_n = str(int(now.year))
    #     form_employee = date_n[2:]
    # else:
    #     now = datetime.now()
    #     date_n = str(int(now.year)+543)
    #     form_employee = date_n[2:]
    # sqlcompafirst = "SELECT acronym FROM company WHERE companyid=%s"
    # cursor.execute(sqlcompafirst,dataInput['company_id'])
    # columnscompafirst = [column[0] for column in cursor.description]
    # resultcompafirst = toJson(cursor.fetchall(),columnscompafirst)
    # coun_length =len(resultcompafirst[0]['acronym'])
    # coun_company = str(resultcompafirst[0]['acronym'])
    # try:
    #     sqlEmployee = "SELECT employeeid FROM employee WHERE company_id=%s ORDER BY employeeid DESC LIMIT 1"
    #     cursor.execute(sqlEmployee,dataInput['company_id'])
    #     columnsEmployee = [column[0] for column in cursor.description]
    #     resultEmployee = toJson(cursor.fetchall(),columnsEmployee)
    #     Emp_last = resultEmployee[0]['employeeid']
    #     if companyid__!=1:
    #         form_employee2 = Emp_last[coun_length:]
    #         form_employee3 = form_employee2[:-3]
    #         if form_employee3==form_employee:
    #             Emp_last = resultEmployee[0]['employeeid']
    #         else:
    #             Emp_last = coun_company+"000"
    #     else:
    #         form_employee2 = Emp_last[coun_length:]
    #         form_employee3 = form_employee2[:-4]
    #         if form_employee3==form_employee:
    #             Emp_last = resultEmployee[0]['employeeid']
    #         else:
    #             Emp_last = coun_company+"000"
    # except Exception as e:
    #     if companyid__!=1:
    #         Emp_last = coun_company+"000"
    #     else:
    #        Emp_last = coun_company+"000"
    # type = Emp_last
    # if  coun_length==0:
    #     coun_length=2
    # elif coun_length==1:
    #     coun_length=3
    # else:
    #     coun_length=coun_length+2
    # if companyid__!=1:
    #     codelast = int(str(type[coun_length:]))+1
    # else:
    #     codelast = str(int(str(type[coun_length:]))+1)
    #     codelast = codelast[2:]
    #     if codelast=="":
    #        codelast=1
    #     else:
    #         codelast=codelast
    # if companyid__!=1:
    #     if  codelast<=9:
    #         codelast=str(codelast)
    #         codesumlast="00"+codelast
    #     elif codelast<=99:
    #         codelast=str(codelast)
    #         codesumlast="0"+codelast
    #     else:
    #         codesumlast=str(codelast)
    # else:
    #     if  codelast<=9:
    #         codelast=str(codelast)
    #         codesumlast="000"+codelast
    #     elif codelast<=99:
    #         codelast=str(codelast)
    #         codesumlast="00"+codelast
    #     elif codelast<=999:
    #         codelast=str(codelast)
    #         codesumlast="0"+codelast
    #     else:
    #         codesumlast=str(codelast)
    # first_character = resultcompafirst[0]['acronym']
    # if companyid__==1:
    #     employeeid = first_character+form_employee+codesumlast
    # elif companyid__==21:
    #     employeeid = first_character+form_employee+codesumlast
    # else:
    #     employeeid = first_character+form_employee+codesumlast
    # return jsonify(employeeid)
    # except Exception as e:
    #     logserver(e)
    #     return "fail"
    dataInput = request.json
    source = dataInput['source']
    data_new = source
    now_contract = datetime.now()
    date_contract = str(int(now_contract.year)+543)
    date_sub_contract = date_contract[2:]
    try:
        sql_contract_id = "SELECT contract_id,year FROM Contract WHERE companyid=%s AND validstatus =1 AND year=%s ORDER BY contract_id DESC LIMIT 1"
        cursor.execute(sql_contract_id,(data_new['company_id'],date_contract))
        columns = [column[0] for column in cursor.description]
        resultsql_contract_id = toJson(cursor.fetchall(),columns)
        year_contract = resultsql_contract_id[0]['year']
        contract_id_ = resultsql_contract_id[0]['contract_id']
        year_sub_con = year_contract[2:]
        if year_sub_con==date_sub_contract:
            contract_id_ = resultsql_contract_id[0]['contract_id']
        else:
            contract_id_ = 0
    except Exception as e:
        contract_id_ = 0
    contract_id_last = int(contract_id_)+1
    return jsonify(contract_id_last)
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
        sql2 = "SELECT * FROM Admin WHERE username=%s AND validstatus=1"
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
