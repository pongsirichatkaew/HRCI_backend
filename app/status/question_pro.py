#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *
@app.route('/Insert_type_Question_pro', methods=['POST'])
@connect_sql()
def Insert_type_Question_pro(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sqlQry = "SELECT question_pro_id_type FROM question_pro_type ORDER BY question_pro_id_type DESC LIMIT 1"
        cursor.execute(sqlQry)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        question_pro_id_last_type=result[0]['question_pro_id_type']+1

        sql = "INSERT INTO question_pro_type (question_pro_id_type,question_pro_detail_type,createby) VALUES (%s,%s,%s)"
        cursor.execute(sql,(question_pro_id_last_type,data_new['question_pro_detail_type'],data_new['createby']))

        type_action = "ADD"

        sql_log = "INSERT INTO question_pro_log_type (question_pro_id_type,question_pro_detail_type,createby,type_action) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql_log,(question_pro_id_last_type,data_new['question_pro_detail_type'],data_new['createby'],type_action))

        add_PreQuestion_Probation(question_pro_id_last_type)
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Edit_type_Question_pro', methods=['POST'])
@connect_sql()
def Edit_type_Question_pro(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT * FROM question_pro_type WHERE question_pro_id_type=%s"
        cursor.execute(sql,(data_new['question_pro_id_type']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Edit"

        sql_log = "INSERT INTO question_pro_log_type (question_pro_id_type,question_pro_detail_type,createby,type_action) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql_log,(result[0]['question_pro_id_type'],result[0]['question_pro_detail_type'],data_new['createby'],type_action))

        sqlUp = "DELETE FROM question_pro_type WHERE question_pro_id_type=%s"
        cursor.execute(sqlUp,(data_new['question_pro_id_type']))

        sqlIn = "INSERT INTO question_pro_type (question_pro_id_type,question_pro_detail_type,createby) VALUES (%s,%s,%s)"
        cursor.execute(sqlIn,(result[0]['question_pro_id_type'],data_new['question_pro_detail_type'],data_new['createby']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Delete_type_Question_pro', methods=['POST'])
@connect_sql()
def Delete_type_Question_pro(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT * FROM question_pro_type WHERE question_pro_id_type=%s"
        cursor.execute(sql,(data_new['question_pro_id_type']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Delete"

        sql_log = "INSERT INTO question_pro_log_type (question_pro_id_type,question_pro_detail_type,createby,type_action) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql_log,(result[0]['question_pro_id_type'],result[0]['question_pro_detail_type'],data_new['createby'],type_action))

        sqlUp = "DELETE FROM question_pro_type WHERE question_pro_id_type=%s"
        cursor.execute(sqlUp,(data_new['question_pro_id_type']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qry_type_Question_pro', methods=['POST'])
@connect_sql()
def Qry_type_Question_pro(cursor):
    try:
        sql = "SELECT question_pro_id_type,question_pro_detail_type FROM question_pro_type"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Insert_form_Question_pro', methods=['POST'])
@connect_sql()
def Insert_form_Question_pro(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        i=0
        for i in xrange(len(data_new['question_pro'])):
            try:
                sqlQry = "SELECT question_pro_id FROM question_pro_form ORDER BY question_pro_id DESC LIMIT 1"
                cursor.execute(sqlQry)
                columns = [column[0] for column in cursor.description]
                result = toJson(cursor.fetchall(),columns)
                question_pro_id_last=result[0]['question_pro_id']+1
            except Exception as e:
                question_pro_id_last = 1
            sql = "INSERT INTO question_pro_form (question_pro_id,question_pro_id_type,question_pro_detail,type_check,group_q,createby) VALUES (%s,%s,%s,%s,%s,%s)"
            # cursor.execute(sql,(question_pro_id_last,data_new['question_pro_id_type'],data_new['question_pro'][i]['question_pro_detail'],data_new['question_pro'][i]['type'],data_new['question_pro'][i]['group'],data_new['createby']))
            cursor.execute(sql,(question_pro_id_last,data_new['question_pro_id_type'],data_new['question_pro'][i]['question_pro_detail'],data_new['question_pro'][i]['type'],data_new['group'],data_new['createby']))

            type_action = "ADD"

            sql_log = "INSERT INTO question_pro_log_form (question_pro_id,question_pro_id_type,question_pro_detail,type_check,group_q,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            # cursor.execute(sql_log,(question_pro_id_last,data_new['question_pro_id_type'],data_new['question_pro'][i]['question_pro_detail'],data_new['question_pro'][i]['type'],data_new['question_pro'][i]['group'],data_new['createby'],type_action))
            cursor.execute(sql_log,(question_pro_id_last,data_new['question_pro_id_type'],data_new['question_pro'][i]['question_pro_detail'],data_new['question_pro'][i]['type'],data_new['group'],data_new['createby'],type_action))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Edit_form_Question_pro', methods=['POST'])
@connect_sql()
def Edit_form_Question_pro(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT * FROM question_pro_form WHERE question_pro_id=%s AND question_pro_id_type=%s"
        cursor.execute(sql,(data_new['question_pro_id'],data_new['question_pro_id_type']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Edit"

        sql_log = "INSERT INTO question_pro_log_form (question_pro_id,question_pro_id_type,question_pro_detail,type_check,group_q,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(result[0]['question_pro_id'],result[0]['question_pro_id_type'],result[0]['question_pro_detail'],result[0]['type_check'],result[0]['group_q'],data_new['createby'],type_action))

        sqlUp = "UPDATE question_pro_form SET question_pro_id_type=%s,question_pro_detail=%s,type_check=%s,group_q=%s,createby=%s WHERE question_pro_id=%s AND question_pro_id_type=%s"
        cursor.execute(sqlUp,(data_new['New_question_pro_id_type'],data_new['New_question_pro_detail'],data_new['New_type_check'],data_new['group_q'],data_new['createby'],data_new['question_pro_id'],data_new['question_pro_id_type']))

        # sqlIn = "INSERT INTO question_pro_form (question_pro_id_type,question_pro_detail,type_check,createby) VALUES (%s,%s,%s,%s)"
        # cursor.execute(sqlIn,(data_new['New_question_pro_id_type'],data_new['New_question_pro_id'],data_new['New_type_check'],data_new['createby']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Delete_form_Question_pro', methods=['POST'])
@connect_sql()
def Delete_form_Question_pro(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT * FROM question_pro_form WHERE question_pro_id=%s AND question_pro_id_type=%s"
        cursor.execute(sql,(data_new['question_pro_id'],data_new['question_pro_id_type']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Delete"

        sql_log = "INSERT INTO question_pro_log_form (question_pro_id_type,question_pro_detail,type_check,group_q,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(result[0]['question_pro_id_type'],result[0]['question_pro_detail'],result[0]['type_check'],result[0]['group_q'],result[0]['createby'],type_action))

        sqlUp = "UPDATE question_pro_form SET validstatus=0 WHERE question_pro_id=%s AND question_pro_id_type=%s"
        cursor.execute(sqlUp,(data_new['question_pro_id'],data_new['question_pro_id_type']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qry_form_Question_pro', methods=['POST'])
@connect_sql()
def Qry_form_Question_pro(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT question_pro_detail_type FROM question_pro_type WHERE question_pro_id_type=%s"
        cursor.execute(sql,(data_new['question_pro_id_type']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        for i1 in result:
            question = []
            sql1 = """  SELECT question_pro_id,question_pro_detail,type_check,group_q FROM question_pro_form WHERE question_pro_id_type = %s AND validstatus=1 ORDER BY question_pro_id ASC"""
            cursor.execute(sql1,(data_new['question_pro_id_type']))
            columns = [column[0] for column in cursor.description]
            data2 = toJson(cursor.fetchall(),columns)
            for i2 in data2 :
                question.append(i2)
            i1['question'] = question
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"

@connect_sql()
def add_PreQuestion_Probation(cursor, question_pro_id_last_type):
    question_pro = [
        { 'question_pro_detail': '1.คุณภาพงาน ความละเอียดรอบคอบและความถูกต้องของงาน', 'type': '', 'group': 'SectQuestion', 'createby': 'SYSTEM' },
        { 'question_pro_detail': '2.ความรับผิดชอบและความเอาใจใส่ในหน้าที่การงาน', 'type': '', 'group': 'SectQuestion', 'createby': 'SYSTEM' },
        { 'question_pro_detail': '3.ความสามารถ และความเชี่ยวชาญในงานที่รับผิดชอบ', 'type': '', 'group': 'SectQuestion', 'createby': 'SYSTEM' },
        { 'question_pro_detail': '4.ความคืดริเริ่มสร้างสรรค์ นำแนวคิดมาพัฒนาการทำงาน', 'type': '', 'group': 'SectQuestion', 'createby': 'SYSTEM' },
        { 'question_pro_detail': '5.ความสามารถในการเรียนรู้งาน', 'type': '', 'group': 'SectQuestion', 'createby': 'SYSTEM' },
        { 'question_pro_detail': '6.ทัศนคตืและกาปฎิบัติงานร่วมกับผู้อื่น', 'type': '', 'group': 'SectQuestion', 'createby': 'SYSTEM' },
        { 'question_pro_detail': '7.การปฏิบัติตามคำสั่ง คำแนะนำ', 'type': '', 'group': 'SectQuestion', 'createby': 'SYSTEM' },
        { 'question_pro_detail': '8.ไหวพริบ การแก้ไขปัญหาเฉพาะหน้า', 'type': '', 'group': 'SectQuestion', 'createby': 'SYSTEM' },
        { 'question_pro_detail': '9.สภาพการมาปฏิบัติงาน', 'type': '', 'group': 'SectQuestion', 'createby': 'SYSTEM' },
        { 'question_pro_detail': '10.ความประพฤติ และการปฏิบัติตามกฎระเบียบของบริษัท', 'type': '', 'group': 'SectQuestion', 'createby': 'SYSTEM' },
        { 'question_pro_detail': 'หลักเกณฑ์ในการประเมินผลทดลองงาน (KPI)', 'type': '', 'group': 'SectionKPI', 'createby': 'SYSTEM' },
        # { 'question_pro_detail': 'ผลการปฎิบัติงานที่ได้ (เอกสารแนบ)', 'type': '', 'group': 'SectionKPI', 'createby': 'SYSTEM' },
        { 'question_pro_detail': 'เห็นควรบรรจุเป็นพนักงานประจำปรับตำแหน่ง', 'type': 'CheckboxWithTextfield', 'group': 'SectionSumPro', 'createby': 'SYSTEM' },
        { 'question_pro_detail': 'ขยายระยะเวลาทดลองงานเป็นเวลา(วัน)', 'type': 'CheckboxWithTextfield', 'group': 'SectionSumPro', 'createby': 'SYSTEM' },
        { 'question_pro_detail': 'แจ้งเลิกจ้าง', 'type': 'Checkbox', 'group': 'SectionSumPro', 'createby': 'SYSTEM' },
        { 'question_pro_detail': 'อื่นๆ โปรดระบุ', 'type': 'CheckboxWithTextfield', 'group': 'SectionSumPro', 'createby': 'SYSTEM' },
        { 'question_pro_detail': 'ปรับเงินเดือนเพิ่ม(บาท)ุ', 'type': 'CheckboxWithTextfield', 'group': 'SectionReqBenefits', 'createby': 'SYSTEM' },
        { 'question_pro_detail': 'ปรับเงินเพิ่มพิเศษ(บาท)', 'type': 'CheckboxWithTextfield', 'group': 'SectionReqBenefits', 'createby': 'SYSTEM' },
        { 'question_pro_detail': 'ค่าตำแหน่ง(บาท)', 'type': 'CheckboxWithTextfield', 'group': 'SectionReqBenefits', 'createby': 'SYSTEM' },
        { 'question_pro_detail': 'วงเงินค่าโทรศัพท์(บาท)', 'type': 'CheckboxWithTextfield', 'group': 'SectionReqBenefits', 'createby': 'SYSTEM' },
        { 'question_pro_detail': 'ค่าเดินทางหรือค่าน้ำมัน(บาท)ุ', 'type': 'CheckboxWithTextfield', 'group': 'SectionReqBenefits', 'createby': 'SYSTEM' },
        { 'question_pro_detail': 'อื่นๆ', 'type': 'CheckboxWithTextfield', 'group': 'SectionReqBenefits', 'createby': 'SYSTEM' }
    ]

    for item in question_pro:
        try:
            sqlQry = "SELECT question_pro_id FROM question_pro_form ORDER BY question_pro_id DESC LIMIT 1"
            cursor.execute(sqlQry)
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            question_pro_id_last=result[0]['question_pro_id']+1
        except Exception as e:
            question_pro_id_last = 1
        sql = "INSERT INTO question_pro_form (question_pro_id,question_pro_id_type,question_pro_detail,type_check,group_q,createby) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(question_pro_id_last, question_pro_id_last_type, item['question_pro_detail'], item['type'], item['group'], item['createby']))

        type_action = "ADD_BY_HeadQuestion"

        sql_log = "INSERT INTO question_pro_log_form (question_pro_id,question_pro_id_type,question_pro_detail,type_check,group_q,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(question_pro_id_last, question_pro_id_last_type, item['question_pro_detail'], item['type'], item['group'], item['createby'], type_action))
    return 'success'
