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
        cursor.execute(sqlQry)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        name_signature_crime_id_last=result[0]['name_signature_crime_id']+1

        sql = "INSERT INTO signature_crime (employeeid,name_signature_crime_id,name_signature_crime,surname_signature_crime,position_id,createby) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(data_new['employeeid'],name_signature_crime_id_last,data_new['name_signature_crime'],data_new['surname_signature_crime'],data_new['position_id'],data_new['createby']))

        type_action = "ADD"

        sql_log = "INSERT INTO signature_crime_log (employeeid,name_signature_crime_id,name_signature_crime,surname_signature_crime,position_id,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(data_new['employeeid'],name_signature_crime_id_last,data_new['name_signature_crime'],data_new['surname_signature_crime'],data_new['position_id'],data_new['createby'],type_action))
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
        cursor.execute(sqlQry,data_new['name_signature_crime_id'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Edit"

        sql_log = "INSERT INTO signature_crime_log (employeeid,name_signature_crime_id,name_signature_crime,surname_signature_crime,position_id,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(result[0]['employeeid'],result[0]['name_signature_crime_id'],result[0]['name_signature_crime'],result[0]['surname_signature_crime'],result[0]['position_id'],data_new['createby'],type_action))

        sqlUp = "DELETE FROM signature_crime WHERE name_signature_crime_id=%s"
        cursor.execute(sqlUp,(data_new['name_signature_crime_id']))

        sql = "INSERT INTO signature_crime (employeeid,name_signature_crime_id,name_signature_crime,surname_signature_crime,position_id,createby) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(result[0]['employeeid'],result[0]['name_signature_crime_id'],data_new['name_signature_crime'],data_new['surname_signature_crime'],data_new['position_id'],data_new['createby']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QrySignature_crime', methods=['POST'])
@connect_sql()
def QrySignature_crime(cursor):
    try:
        sql = "SELECT signature_crime.employeeid,signature_crime.name_signature_crime_id,signature_crime.name_signature_crime,signature_crime.surname_signature_crime,signature_crime.position_id,position.position_detail FROM signature_crime INNER JOIN position ON signature_crime.position_id = position.position_id"
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
        cursor.execute(sqlQry,data_new['name_signature_crime_id'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Delete"

        sql_log = "INSERT INTO signature_crime_log (employeeid,name_signature_crime_id,name_signature_crime,surname_signature_crime,position_id,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(result[0]['employeeid'],result[0]['name_signature_crime_id'],result[0]['name_signature_crime'],result[0]['surname_signature_crime'],result[0]['position_id'],data_new['createby'],type_action))

        sqlUp = "DELETE FROM signature_crime WHERE name_signature_crime_id=%s"
        cursor.execute(sqlUp,(data_new['name_signature_crime_id']))
        connection.commit()
        connection.close()
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
