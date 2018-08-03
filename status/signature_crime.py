#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/InsertSignature_crime', methods=['POST'])
@connect_sql()
def InsertSignature_crime(cursor):
    try:
        data = request.json
        name_signature_crime = data['name_signature_crime']
        surname_signature_crime = data['surname_signature_crime']
        position_signature_crime = data['position_signature_crime']
        sql = "INSERT INTO signature_crime (name_signature_crime,surname_signature_crime,position_signature_crime) VALUES (%s,%s,%s)"
        cursor.execute(sql,(name_signature_crime,surname_signature_crime,position_signature_crime))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditSignature_crime', methods=['POST'])
@connect_sql()
def EditSignature_crime(cursor):
    try:
        data = request.json
        id = data['id']
        name_signature_crime = data['name_signature_crime']
        surname_signature_crime = data['surname_signature_crime']
        position_signature_crime = data['position_signature_crime']
        sqlUp = "UPDATE signature_crime SET validstatus = '0' WHERE id=%s"
        cursor.execute(sqlUp,(data['id']))
        sqlIn = "INSERT INTO signature_crime (name_signature_crime,surname_signature_crime,position_signature_crime) VALUES (%s,%s,%s)"
        cursor.execute(sqlIn,(name_signature_crime,surname_signature_crime,position_signature_crime))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QrySignature_crime', methods=['POST'])
@connect_sql()
def QrySignature_crime(cursor):
    try:
        sql = "SELECT name_signature_crime,surname_signature_crime,id,position_signature_crime FROM signature_crime WHERE validstatus=1"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
