#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, current_app, abort, send_from_directory
from flask_cors import CORS, cross_origin
from functools import wraps
from flaskext.mysql import MySQL

import hashlib
import base64
import datetime
from datetime import datetime
import string
import random


app = Flask(__name__)
CORS(app)

app.config['MYSQL_DATABASE_USER'] = "root"
app.config['MYSQL_DATABASE_PASSWORD'] = "devops@Pass01"
app.config['MYSQL_DATABASE_DB'] = 'HRCI'
app.config['MYSQL_DATABASE_HOST'] = '203.154.58.87'
mysql = MySQL()
mysql.init_app(app)

app2 = Flask(__name__)
app2.config['MYSQL_DATABASE_USER'] = "root"
app2.config['MYSQL_DATABASE_PASSWORD'] = "l^9i@xib,kIlkily,ryoTN"
app2.config['MYSQL_DATABASE_DB'] = 'intranetdb'
app2.config['MYSQL_DATABASE_HOST'] = '203.150.57.159'
mysql2 = MySQL()
mysql2.init_app(app2)


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
def connect_sql2():
        def wrap(fn):
            @wraps(fn)
            def wrapper(*args, **kwargs):
                try:
                    # Setup connection
                    connection = mysql2.connect()
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
def logserver(msg):
    current_app.logger.info(msg)
def decode(data):
    return base64.b64decode(data[:-5][::-1])

def encode(data):
    return (base64.b64encode(str(data)))[::-1] + id_generator()

def logserver(message):
    current_app.logger.info(message)

def id_generator():
    size = 5
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))
def converterDate (output):
    if isinstance(output, datetime.date):
        return output.__str__()
