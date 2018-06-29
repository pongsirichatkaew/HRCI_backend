from dbConfig import *
from test import *

@app.route('/hello/<firstname>/<lastname>', methods=['GET'])
@connect_sql()
def hello(cursor, firstname, lastname):
    sql = "SELECT * FROM test WHERE firstname=%s AND lastname=%s"
    cursor.execute(sql,(firstname, lastname))
    columns = [column[0] for column in cursor.description]
    result = toJson(cursor.fetchall(),columns)
    return jsonify(result)


@app.route('/getName', methods=['POST'])
@connect_sql()
def getName(cursor):
    data = request.json
    sql = "SELECT * FROM test WHERE firstname=%s AND lastname=%s"
    cursor.execute(sql,(data['firstname'], data['lastname']))
    columns = [column[0] for column in cursor.description]
    result = toJson(cursor.fetchall(),columns)
    return jsonify(result)

@app.route('/hello2', methods=['GET'])
def hello2():
    return jsonify(getData('hello'))

@connect_sql()
def getData(c, data):
    print data
    c.execute("SELECT * FROM test")
    columns = [column[0] for column in c.description]
    result = toJson(c.fetchall(),columns)
    return result

@app.route('/insertdata/<firstname>/<lastname>', methods=['GET'])
@connect_sql()
def InsertData(cursor,firstname, lastname):
    sql = """
    INSERT INTO test(firstname, lastname)
    VALUES (%s,%s)
    """
    cursor.execute(sql, (firstname, lastname))
    return 'success'
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',threaded=True,port=5000)
