#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, current_app, abort, send_from_directory
from flask_cors import CORS, cross_origin
from functools import wraps
from flaskext.mysql import MySQL


app = Flask(__name__)
CORS(app)

app.config['MYSQL_DATABASE_USER'] = "root"
app.config['MYSQL_DATABASE_PASSWORD'] = "devops@Pass01"
app.config['MYSQL_DATABASE_DB'] = 'HRCI'
app.config['MYSQL_DATABASE_HOST'] = '203.154.58.87'
mysql = MySQL()
mysql.init_app(app)


def connect_sql():
    def wrap(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                # Setup connection
                connection = mysql.connect()
                cursor = connection.cursor()
                return_val = fn(cursor, *args, **kwargs)
            finally:
                # Close connection
                connection.commit()
                connection.close()
            return return_val
        return wrapper
    return wrap

def toJson(data,columns):
    results = []
    for row in data:
        results.append(dict(zip(columns, row)))
    return results
