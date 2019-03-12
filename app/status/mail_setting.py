#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/Insertmail_setting', methods=['POST'])
@connect_sql()
def Insertmail_setting(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        
        try:
            sqlQry = "SELECT mail_setting_id FROM mail_setting ORDER BY mail_setting_id DESC LIMIT 1"
            cursor.execute(sqlQry)
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            mail_setting_id_last=result[0]['mail_setting_id']+1
        except Exception as e:
            mail_setting_id_last=1

        sql = "INSERT INTO mail_setting (mail_setting_id,mail_setting_detail,createby) VALUES (%s,%s,%s)"
        cursor.execute(sql,(mail_setting_id_last,data_new['mail_setting_detail'],data_new['createby']))

        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Editmail_setting', methods=['POST'])
@connect_sql()
def Editmail_setting(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sqlUp = "DELETE FROM mail_setting WHERE mail_setting_id=%s"
        cursor.execute(sqlUp,(data_new['mail_setting_id']))

        sqlIn = "INSERT INTO mail_setting (mail_setting_id,mail_setting_detail,createby) VALUES (%s,%s,%s)"
        cursor.execute(sqlIn,(data_new['mail_setting_id'],data_new['mail_setting_detail'],data_new['createby']))

        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qrymail_setting', methods=['POST'])
@connect_sql()
def Qrymail_setting(cursor):
    try:
        sql = "SELECT mail_setting_id,mail_setting_detail FROM mail_setting"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Deletemail_setting', methods=['POST'])
@connect_sql()
def Deletemail_setting(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT mail_setting_id,mail_setting_detail FROM mail_setting WHERE mail_setting_id=%s"
        cursor.execute(sql,(data_new['mail_setting_id']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sqlUp = "DELETE FROM mail_setting WHERE mail_setting_id=%s"
        cursor.execute(sqlUp,(data_new['mail_setting_id']))

        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/uploads_pic_mail', methods=['POST'])
@connect_sql()
def uploads_pic_mail(cursor):
    try:
        sqlDe = "DELETE FROM mail_pic WHERE mail_type=%s"
        cursor.execute(sqlDe,(request.form['mail_type']))

        currentTime = datetime.today().strftime('%Y%m%d%H%M%S%f')
        path = 'uploads/' + request.form['mail_type']
        path2 = request.form['mail_type']
        if not os.path.exists(path):
            os.makedirs(path)
        if request.method == 'POST':
            file = request.files['file']
        if file:
            file.save(os.path.join(path, currentTime + 'mail_type.png'))
            path_image = path2+'/'+currentTime+'mail_type.png'
        else:
            return 'file is not allowed'

        sql = "INSERT INTO mail_pic(mail_type,imageName,createby) VALUES (%s,%s,%s)"
        cursor.execute(sql,(request.form['mail_type'],path_image,request.form['createby']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qry_uploads_pic_mail', methods=['POST'])
@connect_sql()
def Qry_uploads_pic_mail(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT mail_type,imageName FROM mail_pic WHERE mail_type=%s"
        cursor.execute(sql,(data_new['mail_type']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/userGetFileImageMail/<path>/<fileName>', methods=['GET'])
def userGetFileImageMail(path, fileName):
    # current_app.logger.info('userGetFile')
    # current_app.logger.info(path)
    # current_app.logger.info(fileName)
    return send_from_directory('../uploads/' + path, fileName)
    # return "ssss"
