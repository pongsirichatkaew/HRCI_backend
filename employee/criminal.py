#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/QryCriminal', methods=['POST'])
@connect_sql()
def QryCriminal(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql ="""SELECT Personal.*,Address.AddressType, Address.HouseNo, Address.Street, Address.DISTRICT_ID, Address.AMPHUR_ID, Address.PROVINCE_ID, Address.PostCode, Address.Tel, Address.Fax,homeTable.AddressType as homeAddress, homeTable.HouseNo as homeHouseNo, homeTable.Street as homeStreet,
        homeTable.DISTRICT_ID as homeDistrict, homeTable.AMPHUR_ID as homeAmphur, homeTable.PROVINCE_ID as homeProvince, homeTable.PostCode as homePostCode, homeTable.Tel as homeTel, homeTable.Fax as homeFax,
        Family.Name as fatherName, Family.Surname as fatherSurname,motherTable.Name as motherName, motherTable.Surname as motherSurname
        FROM Personal
        LEFT JOIN Address ON Address.ID_CardNo = Personal.ID_CardNo
        LEFT JOIN Family ON Family.ID_CardNo = Personal.ID_CardNo
        LEFT JOIN (SELECT * FROM Address WHERE AddressType = 'Home') AS homeTable ON homeTable.ID_CardNo = Personal.ID_CardNo
        LEFT JOIN (SELECT * FROM Family WHERE MemberType = 'Mother') AS motherTable ON motherTable.ID_CardNo = Personal.ID_CardNo
        WHERE Address.AddressType = 'Present' and Family.MemberType = 'Father' AND Personal.ID_CardNo = %s AND Personal.validstatus=1 AND Address.validstatus=1 AND Family.validstatus=1 """
        cursor.execute(sql,data_new['ID_CardNo'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryEmployeeList', methods=['POST'])
@connect_sql()
def QryEmployeeList(cursor):
    try:
        sql = "SELECT * FROM employee WHERE validstatus=1"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryAllEmployeeCrimeList', methods=['POST'])
@connect_sql()
def QryAllEmployeeCrimeList(cursor):
    try:
        sql4 ="""SELECT Personal.*,Address.AddressType, Address.HouseNo, Address.Street, Address.DISTRICT_ID, Address.AMPHUR_ID, Address.PROVINCE_ID, Address.PostCode, Address.Tel, Address.Fax,homeTable.AddressType as homeAddress, homeTable.HouseNo as homeHouseNo, homeTable.Street as homeStreet,
        homeTable.DISTRICT_ID as homeDistrict, homeTable.AMPHUR_ID as homeAmphur, homeTable.PROVINCE_ID as homeProvince, homeTable.PostCode as homePostCode, homeTable.Tel as homeTel, homeTable.Fax as homeFax,
        Family.Name as fatherName, Family.Surname as fatherSurname,motherTable.Name as motherName, motherTable.Surname as motherSurname
        FROM Personal
        LEFT JOIN Address ON Address.ID_CardNo = Personal.ID_CardNo
        LEFT JOIN Family ON Family.ID_CardNo = Personal.ID_CardNo
        LEFT JOIN (SELECT * FROM Address WHERE AddressType = 'Home') AS homeTable ON homeTable.ID_CardNo = Personal.ID_CardNo
        LEFT JOIN (SELECT * FROM Family WHERE MemberType = 'Mother') AS motherTable ON motherTable.ID_CardNo = Personal.ID_CardNo
        WHERE Address.AddressType = 'Present' and Family.MemberType = 'Father' AND Personal.validstatus=1 AND Address.validstatus=1 AND Family.validstatus=1  """
        cursor.execute(sql4)
        columns = [column[0] for column in cursor.description]
        result4 = toJson(cursor.fetchall(),columns)
        return jsonify(result4)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryAllEmployee_by_month', methods=['POST'])
@connect_sql()
def QryAllEmployee_by_month(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        year=str(data_new['year'])
        month=str(data_new['month'])
        companyid=str(data_new['companyid'])
        print companyid
        # sql4 ="""SELECT Personal.*,Address.AddressType, Address.HouseNo, Address.Street, Address.DISTRICT_ID, Address.AMPHUR_ID, Address.PROVINCE_ID, Address.PostCode, Address.Tel, Address.Fax,homeTable.AddressType as homeAddress, homeTable.HouseNo as homeHouseNo, homeTable.Street as homeStreet,employee.company_id as companyid,
        # homeTable.DISTRICT_ID as homeDistrict, homeTable.AMPHUR_ID as homeAmphur, homeTable.PROVINCE_ID as homeProvince, homeTable.PostCode as homePostCode, homeTable.Tel as homeTel, homeTable.Fax as homeFax,employee.create_at as timedate,
        # Family.Name as fatherName, Family.Surname as fatherSurname,motherTable.Name as motherName, motherTable.Surname as motherSurname
        # FROM Personal
        # LEFT JOIN employee ON employee.citizenid = Personal.ID_CardNo
        # LEFT JOIN Address ON Address.ID_CardNo = Personal.ID_CardNo
        # LEFT JOIN Family ON Family.ID_CardNo = Personal.ID_CardNo
        # LEFT JOIN (SELECT * FROM Address WHERE AddressType = 'Home') AS homeTable ON homeTable.ID_CardNo = Personal.ID_CardNo
        # LEFT JOIN (SELECT * FROM Family WHERE MemberType = 'Mother') AS motherTable ON motherTable.ID_CardNo = Personal.ID_CardNo
        # WHERE Address.AddressType = 'Present' AND Family.MemberType = 'Father' AND Personal.validstatus=1 AND Address.validstatus=1 AND Family.validstatus=1 AND employee.create_at LIKE '""" + year + """-""" + month + """%' AND employee.company_id='"""+companyid +"""'"""
        sql4 ="""SELECT Personal.*,Address.AddressType, Address.HouseNo, Address.Street, Address.DISTRICT_ID, Address.AMPHUR_ID, Address.PROVINCE_ID, Address.PostCode, Address.Tel, Address.Fax,homeTable.AddressType as homeAddress, homeTable.HouseNo as homeHouseNo, homeTable.Street as homeStreet,employee.company_id as companyid,employee.start_work as start_work,position.position_detail as position_detail, \
        section.sect_detail as sect_detail,org_name.org_name_detail as org_name_detail,cost_center_name.cost_detail as cost_detail,company.companyname,
        homeTable.DISTRICT_ID as homeDistrict, homeTable.AMPHUR_ID as homeAmphur, homeTable.PROVINCE_ID as homeProvince, homeTable.PostCode as homePostCode, homeTable.Tel as homeTel, homeTable.Fax as homeFax,employee.create_at as timedate,
        Family.Name as fatherName, Family.Surname as fatherSurname,motherTable.Name as motherName, motherTable.Surname as motherSurname
        FROM Personal
        LEFT JOIN employee ON employee.citizenid = Personal.ID_CardNo
        LEFT JOIN position ON position.position_id = employee.position_id
		LEFT JOIN section ON section.sect_id = employee.section_id
        LEFT JOIN org_name ON org_name.org_name_id = employee.org_name_id
        LEFT JOIN cost_center_name ON cost_center_name.cost_center_name_id = employee.cost_center_name_id
        LEFT JOIN company ON company.companyid = employee.company_id
        LEFT JOIN Address ON Address.ID_CardNo = Personal.ID_CardNo
        LEFT JOIN Family ON Family.ID_CardNo = Personal.ID_CardNo \
        LEFT JOIN (SELECT * FROM Address WHERE AddressType = 'Home') AS homeTable ON homeTable.ID_CardNo = Personal.ID_CardNo
        LEFT JOIN (SELECT * FROM Family WHERE MemberType = 'Mother') AS motherTable ON motherTable.ID_CardNo = Personal.ID_CardNo
        WHERE Address.AddressType = 'Present' AND Family.MemberType = 'Father' AND Personal.validstatus=1 AND Address.validstatus=1 AND Family.validstatus=1 AND position.validstatus=1 AND \
        section.validstatus=1 AND org_name.validstatus=1 AND cost_center_name.validstatus=1 AND company.validstatus=1 AND \
        employee.create_at LIKE '""" + year + """-""" + month + """%' AND employee.company_id='"""+companyid +"""'"""

        cursor.execute(sql4)
        columns = [column[0] for column in cursor.description]
        result4 = toJson(cursor.fetchall(),columns)
        return jsonify(result4)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/export', methods=['POST'])
# # from flask import send_file
# # import xlsxwriter
def export():
    connection = mysql.connect()
    cursor = connection.cursor()
    sql4 ="""SELECT Personal.*,Address.AddressType, Address.HouseNo, Address.Street, Address.DISTRICT_ID, Address.AMPHUR_ID, Address.PROVINCE_ID, Address.PostCode, Address.Tel, Address.Fax,homeTable.AddressType as homeAddress, homeTable.HouseNo as homeHouseNo, homeTable.Street as homeStreet,
    homeTable.DISTRICT_ID as homeDistrict, homeTable.AMPHUR_ID as homeAmphur, homeTable.PROVINCE_ID as homeProvince, homeTable.PostCode as homePostCode, homeTable.Tel as homeTel, homeTable.Fax as homeFax,
    Family.Name as fatherName, Family.Surname as fatherSurname,motherTable.Name as motherName, motherTable.Surname as motherSurname
    FROM Personal
    LEFT JOIN Address ON Address.ID_CardNo = Personal.ID_CardNo
    LEFT JOIN Family ON Family.ID_CardNo = Personal.ID_CardNo
    LEFT JOIN (SELECT * FROM Address WHERE AddressType = 'Home') AS homeTable ON homeTable.ID_CardNo = Personal.ID_CardNo
    LEFT JOIN (SELECT * FROM Family WHERE MemberType = 'Mother') AS motherTable ON motherTable.ID_CardNo = Personal.ID_CardNo
    WHERE Address.AddressType = 'Present' and Family.MemberType = 'Father' AND Personal.validstatus=1 AND Address.validstatus=1 AND Family.validstatus=1  """
    cursor.execute(sql4)
    columns = [column[0] for column in cursor.description]
    result = toJson(cursor.fetchall(),columns)
    # datedata = []
    # if result != []:
    #     datedata.append(result)
    # return jsonify(result)
    workbook = xlsxwriter.Workbook('Criminal.xlsx')
    # Create a format to use in the merged range.
    merge_format = workbook.add_format({
        'bold': 1.5,
        'align': 'center',
        'valign': 'vcenter',
        'font_size': '14'
    })
    cell_format = workbook.add_format({'bold': True,'align': 'center',
        'valign': 'vcenter'})
    data_format = workbook.add_format({'text_wrap': True})
    data_format.set_text_wrap()
    worksheet = workbook.add_worksheet()
    worksheet.merge_range('A1:J1', 'รายชื่อผู้ตรวจสอบประวัติอาชญากรรม'.decode('utf-8'), merge_format)
    worksheet.write('A2', 'ลำดับ'.decode('utf-8'), cell_format)
    worksheet.write('B2', 'ชื่อ-ชื่อสกุล'.decode('utf-8'), cell_format)
    worksheet.write('C2', 'เลขบัตรประจำตัวประชาชน'.decode('utf-8'), cell_format)
    worksheet.write('D2', 'วัน/เดือน/ปีเกิด'.decode('utf-8'), cell_format)
    worksheet.write('E2', 'ชื่อบิดา-มารดา'.decode('utf-8'), cell_format)
    worksheet.write('F2', 'ที่อยู่ปัจจุบันและภูมิลำเนา'.decode('utf-8'), cell_format)
    i=0
    for i in xrange(len(result)):
        worksheet.write('A'+str(i+3), i+1)
        worksheet.write('B' + str(i + 3),result[i]['NameTh'] + ' ' + result[i]['SurnameTh'], data_format)
        worksheet.write('C' + str(i + 3),result[i]['ID_CardNo'], data_format)
        worksheet.write('D' + str(i + 3),result[i]['Birthdate'], data_format)
        worksheet.write('E' + str(i + 3),result[i]['fatherName'] + ' ' + result[i]['fatherSurname'] + '\n' + result[i]['motherName'] + ' ' + result[i]['motherSurname'], data_format)
        worksheet.write('F' + str(i + 3),'ที่อยู่ปัจจุบัน : บ้านเลขที่ '.decode('utf-8') + result[i]['HouseNo'] + ' ถนน '.decode('utf-8') + result[i]['Street'] + ' อำเภอ/เขต '.decode('utf-8') \
        + result[i]['DISTRICT_ID'] + ' ตำบล/แขวง '.decode('utf-8') + result[i]['AMPHUR_ID'] + ' จังหวัด '.decode('utf-8') + result[i]['PROVINCE_ID'] + ' รหัสไปรษณีย์ '.decode('utf-8') +\
        result[i]['PostCode'] + '\n' + 'ภูมิลำเนาเดิม : บ้านเลขที่ '.decode('utf-8') + result[i]['homeHouseNo'] + ' ถนน '.decode('utf-8') + result[i]['homeStreet'] + ' อำเภอ/เขต '.decode('utf-8') + \
        result[i]['homeDistrict'] + ' ตำบล/แขวง '.decode('utf-8') + result[i]['homeAmphur'] + ' จังหวัด '.decode('utf-8') + result[i]['homeProvince'] + ' รหัสไปรษณีย์ '.decode('utf-8') + result[i]['homePostCode'], data_format)
    workbook.close()
    connection.commit()
    connection.close()
    # return "Success"
    directory = '/code/'
    filename = 'Criminal.xlsx'
    path = directory + filename
    return send_file(path,
                          mimetype='application/vnd.ms-excel',
                            as_attachment=True,
                            attachment_filename=filename)
