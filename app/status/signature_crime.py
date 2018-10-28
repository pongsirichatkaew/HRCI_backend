#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/InsertSignature_crime', methods=['POST'])
@connect_sql()
def InsertSignature_crime(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sqlQry = "SELECT name_signature_crime_id FROM signature_crime ORDER BY name_signature_crime_id DESC LIMIT 1"
        cursor3.execute(sqlQry)
        columns = [column[0] for column in cursor3.description]
        result = toJson(cursor3.fetchall(),columns)
        name_signature_crime_id_last=result[0]['name_signature_crime_id']+1

        sql = "INSERT INTO signature_crime (name_signature_crime_id,name_signature_crime,surname_signature_crime,position_signature_crime,createby) VALUES (%s,%s,%s,%s,%s)"
        cursor3.execute(sql,(name_signature_crime_id_last,data_new['name_signature_crime'],data_new['surname_signature_crime'],data_new['position_signature_crime'],data_new['createby']))

        type_action = "ADD"

        sql_log = "INSERT INTO signature_crime_log (name_signature_crime_id,name_signature_crime,surname_signature_crime,position_signature_crime,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor3.execute(sql_log,(name_signature_crime_id_last,data_new['name_signature_crime'],data_new['surname_signature_crime'],data_new['position_signature_crime'],data_new['createby'],type_action))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditSignature_crime', methods=['POST'])
@connect_sql()
def EditSignature_crime(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sqlQry = "SELECT * FROM signature_crime WHERE name_signature_crime_id=%s"
        cursor3.execute(sqlQry,data_new['name_signature_crime_id'])
        columns = [column[0] for column in cursor3.description]
        result = toJson(cursor3.fetchall(),columns)

        type_action = "Edit"

        sql_log = "INSERT INTO signature_crime_log (name_signature_crime_id,name_signature_crime,surname_signature_crime,position_signature_crime,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor3.execute(sql_log,(result[0]['name_signature_crime_id'],result[0]['name_signature_crime'],result[0]['surname_signature_crime'],result[0]['position_signature_crime'],data_new['createby'],type_action))

        sqlUp = "DELETE FROM signature_crime WHERE name_signature_crime_id=%s"
        cursor3.execute(sqlUp,(data_new['name_signature_crime_id']))

        sql = "INSERT INTO signature_crime (name_signature_crime_id,name_signature_crime,surname_signature_crime,position_signature_crime	,createby) VALUES (%s,%s,%s,%s,%s)"
        cursor3.execute(sql,(result[0]['name_signature_crime_id'],data_new['name_signature_crime'],data_new['surname_signature_crime'],data_new['position_signature_crime'],data_new['createby']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QrySignature_crime', methods=['POST'])
@connect_sql()
def QrySignature_crime(cursor):
    try:
        sql = "SELECT name_signature_crime,surname_signature_crime,name_signature_crime_id,position_signature_crime FROM signature_crime"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/DeleteSignature_crime', methods=['POST'])
def DeleteSignature_crime():
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sqlQry = "SELECT * FROM signature_crime WHERE name_signature_crime_id=%s"
        cursor3.execute(sqlQry,data_new['name_signature_crime_id'])
        columns = [column[0] for column in cursor3.description]
        result = toJson(cursor3.fetchall(),columns)

        type_action = "Delete"

        sql_log = "INSERT INTO signature_crime_log (name_signature_crime_id,name_signature_crime,surname_signature_crime,position_signature_crime,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor3.execute(sql_log,(result[0]['name_signature_crime_id'],result[0]['name_signature_crime'],result[0]['surname_signature_crime'],result[0]['position_signature_crime'],data_new['createby'],type_action))

        sqlUp = "DELETE FROM signature_crime WHERE name_signature_crime_id=%s"
        cursor3.execute(sqlUp,(data_new['name_signature_crime_id']))
        connection.commit()
        connection.close()
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
