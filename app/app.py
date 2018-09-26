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
    # def uploadmutifile():
    # path = "uploads/"
    #     try:
    #         file = request.files.getlist('file')
    #         for idx, fileList in enumerate(file):
    #             fileName = fileList.filename
    #             fileType = fileName.split('.')[-1]
    #             fileList.filename = 'U' + "test" + '' + request.form['source_id']  + '' + str(idx + 1) + '.' + fileType
    #             try:
    #                 os.remove(os.path.join(path, fileList.filename))
    #             except OSError:
    #                 pass
    #             if file and allowed_file(fileList.filename):
    #                 fileList.save(os.path.join(path, fileList.filename))
    #             else:
    #                 return jsonify({"status": "file is not allowed"})
    #         return jsonify({"status": "success"})
    #     except Exception as e:
    #         current_app.logger.info("Error in file: " + str(e))
    #         return jsonify({"status": "Error in file upload"})
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
