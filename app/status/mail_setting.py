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
        sqlQry = "SELECT mail_setting_id FROM mail_setting ORDER BY mail_setting_id DESC LIMIT 1"
        cursor.execute(sqlQry)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        mail_setting_id_last=result[0]['mail_setting_id']+1

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
@app.route('/uploads_pic_probation', methods=['POST'])
@connect_sql()
def uploads_pic_probation(cursor):
    try:
        path = 'uploads/'+'probation_mail'
        if not os.path.exists(path):
            os.makedirs(path)
        if request.method == 'POST':
            file = request.files['file']
        if file:
            file.save(os.path.join(path, 'probation_mail.png'))
        else:
            return 'file is not allowed'
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qry_uploads_pic_probation', methods=['POST'])
@connect_sql()
def Qry_uploads_pic_probation(cursor):
    try:
        img_base64 = []
        path_mail_pic = '../uploads/probation_mail/probation_mail.png'
        tranImage = path_mail_pic
        with open(tranImage, 'rb') as image_file:
            encoded_Image = base64.b64encode(image_file.read())
        img_base64 = encoded_Image
        img_base64 = []
        img_base64.append(encoded_Image)
        last_email = []
        last_email.append(path_mail_pic)
        keyEmail = ['path_email']
        # keyemail2 =['path_email_bass64']
        # result_mail = dict(zip(keyemail2,img_base64))
        result_mail2 = dict(zip(keyEmail,last_email))
        # sumall = dict(result_mail.items() + result_mail2.items())
        # all_result = []
        # all_result.append(sumall)
        return jsonify(result_mail2)
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
