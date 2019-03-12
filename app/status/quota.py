#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/Insertquota', methods=['POST'])
@connect_sql()
def Insertquota(cursor):
    try:
        sqlQry = "SELECT quota_id FROM quota ORDER BY quota_id DESC LIMIT 1"
        cursor.execute(sqlQry)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        quota_id_last=str(result[0]['quota_id']+1)

        sql = "INSERT INTO quota (quota_id,year,companyid,position_id,member,createby) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(quota_id_last,request.form['year'],request.form['companyid'],request.form['position_id'],request.form['member'],request.form['createby']))

        type_action = "ADD"

        sql_log = "INSERT INTO quota_log (quota_id,year,companyid,position_id,member,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(quota_id_last,request.form['year'],request.form['companyid'],request.form['position_id'],request.form['member'],request.form['createby'],type_action))

        currentTime = datetime.today().strftime('%Y%m%d%H%M%S%f')
        path = 'uploads/quota/' + quota_id_last
        path2 = quota_id_last
        if not os.path.exists(path):
            os.makedirs(path)
        if request.method == 'POST':
            file = request.files['file']
        if file:
            file.save(os.path.join(path, currentTime + 'quota_id.png'))
            path_image = path2+'/'+currentTime+'quota_id.png'
        else:
            return 'file is not allowed'

        sql_insert = "INSERT INTO picture_jd(quota_id,imageName,createby) VALUES (%s,%s,%s)"
        cursor.execute(sql_insert,(quota_id_last,path_image,request.form['createby']))

        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Editquota', methods=['POST'])
@connect_sql()
def Editquota(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT quota_id,year,position_id,companyid,member FROM quota WHERE quota_id=%s"
        cursor.execute(sql,(data_new['quota_id']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Edit"

        sql_log = "INSERT INTO quota_log (quota_id,year,companyid,position_id,member,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(result[0]['quota_id'],result[0]['year'],result[0]['companyid'],result[0]['position_id'],result[0]['member'],data_new['createby'],type_action))

        sqlUp = "DELETE FROM quota WHERE quota_id=%s"
        cursor.execute(sqlUp,(data_new['quota_id']))

        sqlIn = "INSERT INTO quota (quota_id,year,companyid,position_id,member,createby) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn,(result[0]['quota_id'],data_new['year'],data_new['companyid'],data_new['position_id'],data_new['member'],data_new['createby']))

        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qryquota', methods=['POST'])
@connect_sql()
def Qryquota(cursor):
    try:
        quota_id = ""
        try:
            dataInput = request.json
            source = dataInput['source']
            data_new = source
            quota_id = 'WHERE quota_id='+'"'+str(data_new['quota_id'])+'"'
        except Exception as e:
            pass
        sql = "SELECT quota.quota_id,quota.year,company.companyid,company.company_short_name,position.position_detail,quota.position_id,quota.member FROM quota LEFT JOIN company ON company.companyid = quota.companyid\
                                                                                                                                   LEFT JOIN position ON position.position_id = quota.position_id "+quota_id+" "
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        for i1 in result:
            quota_detail = []
            sql1 = "SELECT COUNT(employee.employeeid) AS now_member,  CONVERT(quota.member,SIGNED)-CONVERT(COUNT(employee.employeeid),SIGNED) AS remain_member\
                        FROM employee LEFT JOIN quota ON employee.quota_id = quota.quota_id WHERE employee.quota_id = %s "
            cursor.execute(sql1,(i1['quota_id']))
            columns = [column[0] for column in cursor.description]
            data2 = toJson(cursor.fetchall(),columns)
            for i2 in data2 :
                quota_detail.append(i2)
                i2['remain_member'] = int(i1['member'])-int(i2['now_member'])
            i1['quota_detail'] = quota_detail
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Deletequota', methods=['POST'])
@connect_sql()
def Deletequota(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT quota_id,year,position_id,companyid,member FROM quota WHERE quota_id=%s"
        cursor.execute(sql,(data_new['quota_id']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Delete"

        sql_log = "INSERT INTO quota_log (quota_id,year,companyid,position_id,member,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(result[0]['quota_id'],result[0]['year'],result[0]['companyid'],result[0]['position_id'],result[0]['member'],data_new['createby'],type_action))

        sqlUp = "DELETE FROM quota WHERE quota_id=%s"
        cursor.execute(sqlUp,(data_new['quota_id']))

        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/uploads_pic_jd', methods=['POST'])
@connect_sql()
def uploads_pic_jd(cursor):
    try:
        try:
            sqlDe = "DELETE FROM picture_jd WHERE quota_id=%s"
            cursor.execute(sqlDe,(request.form['quota_id']))
        except Exception as e:
            pass

        currentTime = datetime.today().strftime('%Y%m%d%H%M%S%f')
        path = 'uploads/quota/' + request.form['quota_id']
        path2 = request.form['quota_id']
        if not os.path.exists(path):
            os.makedirs(path)
        if request.method == 'POST':
            file = request.files['file']
        if file:
            file.save(os.path.join(path, currentTime + 'quota_id.png'))
            path_image = path2+'/'+currentTime+'quota_id.png'
        else:
            return 'file is not allowed'

        sql = "INSERT INTO picture_jd(quota_id,imageName,createby) VALUES (%s,%s,%s)"
        cursor.execute(sql,(request.form['quota_id'],path_image,request.form['createby']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qry_uploads_pic_jd', methods=['POST'])
@connect_sql()
def Qry_uploads_pic_jd(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT quota_id,imageName FROM picture_jd WHERE quota_id=%s"
        cursor.execute(sql,(data_new['quota_id']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/userGetFileImageQuota/<path>/<fileName>', methods=['GET'])
def userGetFileImageQuota(path, fileName):
    # current_app.logger.info('userGetFile')
    # current_app.logger.info(path)
    # current_app.logger.info(fileName)
    return send_from_directory('../uploads/quota/' + path, fileName)
    # return "ssss"
