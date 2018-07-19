from dbConfig import *
from test import *
from status import *

@app.route('/hello', methods=['GET'])
def hello():
    return 'hello'

@app.route('/login', methods=['POST'])
@connect_sql2()
def login(cursor):
    _data = request.json
    username = _data['username']
    password = _data['password']
    sql = "SELECT * FROM user WHERE username = %s and password = %s"
    conn = mysql2.connect()
    cursor = conn.cursor()
    cursor.execute(sql, (username, hashlib.sha512(password).hexdigest()))
    data = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    _output = toJson(data, columns)

    result = {}
    if len(_output) != 0:
        result['message'] = 'login success'
        result['userid'] = _output[0]['userid']
        result['username'] = _output[0]['username']
    else:
        result['message'] = 'login fail'
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',threaded=True,port=5000)
