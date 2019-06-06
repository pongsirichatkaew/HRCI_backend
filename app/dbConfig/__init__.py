#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, current_app, abort, send_from_directory
from flask_cors import CORS, cross_origin
from functools import wraps
from flask import send_file
from flaskext.mysql import MySQL
import hashlib
import base64
import datetime
from datetime import datetime, date
import string
import random
import os
import wget
import base64
import xlsxwriter
import urllib
import time
import uuid
import sys
import requests
from werkzeug import secure_filename
from openpyxl import load_workbook
from dateutil.relativedelta import relativedelta
# lib email
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
CORS(app)
app.config['ALLOWED_EXTENSIONS'] = set(['xls', 'xlsm', 'xlsx', 'csv', 'txt', 'xml','docx','jpg','pdf'])

app.config['MYSQL_DATABASE_USER'] = "root"
app.config['MYSQL_DATABASE_PASSWORD'] = "^dglnvg8hkw,j0y[,nv-"
app.config['MYSQL_DATABASE_DB'] = 'HRCI_Management_stateging'
app.config['MYSQL_DATABASE_HOST'] = '203.151.50.137'
# app.config['MYSQL_DATABASE_USER'] = "root"
# app.config['MYSQL_DATABASE_PASSWORD'] = "^dglnvg8hkw,j0y[,nv-"
# app.config['MYSQL_DATABASE_DB'] = 'HRCI_Management_backup_test2'
# app.config['MYSQL_DATABASE_HOST'] = '203.151.50.137'
mysql = MySQL()
mysql.init_app(app)

app2 = Flask(__name__)
app2.config['MYSQL_DATABASE_USER'] = "root"
app2.config['MYSQL_DATABASE_PASSWORD'] = "l^9i@xib,kIlkily,ryoTN"
app2.config['MYSQL_DATABASE_DB'] = 'intranetdb'
app2.config['MYSQL_DATABASE_HOST'] = '203.150.57.159'
mysql2 = MySQL()
mysql2.init_app(app2)

app3 = Flask(__name__)
# app3.config['MYSQL_DATABASE_USER'] = "root"
# app3.config['MYSQL_DATABASE_PASSWORD'] = "vpjk.shCyo8bf"
# app3.config['MYSQL_DATABASE_DB'] = 'applicationform'
# app3.config['MYSQL_DATABASE_HOST'] = '203.154.71.156'
app3.config['MYSQL_DATABASE_USER'] = "root"
app3.config['MYSQL_DATABASE_PASSWORD'] = "vpjk.shCyo8bf"
app3.config['MYSQL_DATABASE_DB'] = 'applicationform_dev'
app3.config['MYSQL_DATABASE_HOST'] = '203.154.71.156'
mysql3 = MySQL()
mysql3.init_app(app3)

app4 = Flask(__name__)
app4.config['MYSQL_DATABASE_USER'] = "root"
app4.config['MYSQL_DATABASE_PASSWORD'] = "devops@Pass01"
app4.config['MYSQL_DATABASE_DB'] = 'HRCI_Appform'
app4.config['MYSQL_DATABASE_HOST'] = '203.154.58.87'
mysql4 = MySQL()
mysql4.init_app(app4)

CORS(app2)
CORS(app3)
CORS(app4)


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
                    cursor2 = connection.cursor()
                    return_val = fn(cursor2, *args, **kwargs)
                finally:
                    # Close connection
                    connection.commit()
                    connection.close()
                return return_val
            return wrapper
        return wrap
def connect_sql3():
        def wrap(fn):
            @wraps(fn)
            def wrapper(*args, **kwargs):
                try:
                    # Setup connection
                    connection = mysql3.connect()
                    cursor3 = connection.cursor()
                    return_val = fn(cursor3, *args, **kwargs)
                finally:
                    # Close connection
                    connection.commit()
                    connection.close()
                return return_val
            return wrapper
        return wrap
def connect_sql4():
        def wrap(fn):
            @wraps(fn)
            def wrapper(*args, **kwargs):
                try:
                    # Setup connection
                    connection4 = mysql4.connect()
                    cursor4 = connection4.cursor()
                    return_val = fn(cursor4, *args, **kwargs)
                finally:
                    # Close connection
                    connection4.commit()
                    connection4.close()
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
def CheckTokenAssessor(employeeid,token):
    now = str(datetime.now())
    now = now.split("-")
    token_mounth = now[1]
    new_day = now[2].split(" ")
    token_day = new_day[0]
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        sql3 = "SELECT employeeid FROM assessor_pro WHERE employeeid='{}' AND token='{}' AND time_token LIKE '%{}-{}%'".format(employeeid,token,token_mounth,token_day)
        cursor.execute(sql3)
        data3 = cursor.fetchall()
        columns3 = [column[0] for column in cursor.description]
        _output3 = toJson(data3, columns3)
        connection.commit()
        connection.close()
        token_check = _output3[0]['employeeid']
        chek_tk = 'pass'
    except Exception as e:
        chek_tk = 'Not pass'
    return chek_tk
def CheckTokenAssessor_kpi(employeeid,token):
    now = str(datetime.now())
    now = now.split("-")
    token_mounth = now[1]
    new_day = now[2].split(" ")
    token_day = new_day[0]
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        sql3 = "SELECT employeeid FROM assessor_kpi WHERE employeeid='{}' AND status='active' AND token='{}' AND time_token LIKE '%{}-{}%'".format(employeeid,token,token_mounth,token_day)
        cursor.execute(sql3)
        data3 = cursor.fetchall()
        columns3 = [column[0] for column in cursor.description]
        _output3 = toJson(data3, columns3)
        connection.commit()
        connection.close()
        token_check = _output3[0]['employeeid']
        chek_tk = 'pass'
    except Exception as e:
        chek_tk = 'Not pass'
    return chek_tk
def CheckTokenAdmin(employeeid,token):
    now = str(datetime.now())
    now = now.split("-")
    token_mounth = now[1]
    new_day = now[2].split(" ")
    token_day = new_day[0]
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        sql3 = "SELECT employeeid FROM Admin WHERE employeeid='{}' AND token='{}' AND time_token LIKE '%{}-{}%'".format(employeeid,token,token_mounth,token_day)
        cursor.execute(sql3)
        data3 = cursor.fetchall()
        columns3 = [column[0] for column in cursor.description]
        _output3 = toJson(data3, columns3)
        connection.commit()
        connection.close()
        token_check = _output3[0]['employeeid']
        chek_tk = 'pass'
    except Exception as e:
        chek_tk = 'Not pass'
    return chek_tk
def CheckTokenGM(employeeid,token):
    now = str(datetime.now())
    now = now.split("-")
    token_mounth = now[1]
    new_day = now[2].split(" ")
    token_day = new_day[0]
    GM = 'GM'
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        sql3 = "SELECT employeeid FROM Admin WHERE employeeid='{}' AND permission='{}' AND token='{}' AND time_token LIKE '%{}-{}%'".format(employeeid,GM,token,token_mounth,token_day)
        cursor.execute(sql3)
        data3 = cursor.fetchall()
        columns3 = [column[0] for column in cursor.description]
        _output3 = toJson(data3, columns3)
        connection.commit()
        connection.close()
        token_check = _output3[0]['employeeid']
        chek_tk = 'pass'
    except Exception as e:
        chek_tk = 'Not pass'
    return chek_tk
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
def toDict(data,columns):
    results = {}
    for row in data:
        results = dict(zip(columns, row))
    return results
def allowed_file(filename):
    return '.' in filename and \
    filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
