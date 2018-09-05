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
    for (r, row) in enumerate(result):
        print row['homeAmphur']
        for c, col in enumerate(row):
            worksheet.write(r, c, col)
            worksheet.merge_range('A1:J1', 'รายชื่อผู้ตรวจสอบประวัติอาชญากรรม', merge_format)
            for i in range(1,10):
                worksheet.set_column(c+i, c+i, 20, data_format)
            worksheet.write('A2', 'ลำดับ', cell_format)
            worksheet.write('B2', 'ชื่อ-ชื่อสกุล', cell_format)
            worksheet.write('C2', 'เลขบัตรประจำตัวประชาชน', cell_format)
            worksheet.write('D2', 'วัน/เดือน/ปีเกิด', cell_format)
            worksheet.write('E2', 'ชื่อบิดา-มารดา', cell_format)
            worksheet.write('F2', 'ที่อยู่ปัจจุบันและภูมิลำเนา', cell_format)

        worksheet.write('A'+str(r+3), r+1)
        worksheet.write('B' + str(r + 3),row['NameTh'] + ' ' + row['SurnameTh'], data_format)
        worksheet.write('C' + str(r + 3),row['ID_CardNo'], data_format)
        worksheet.write('D' + str(r + 3),row['Birthdate'], data_format)
        worksheet.write('E' + str(r + 3),row['fatherName'] + ' ' + row['fatherSurname'] + '\n' + row['motherName'] + ' ' + row['motherSurname'], data_format)
        worksheet.write('F' + str(r + 3),'ที่อยู่ปัจจุบัน : บ้านเลขที่ ' + row['HouseNo'] + ' ถนน ' + row['Street'] + ' อำเภอ/เขต ' \
        + row['DISTRICT_ID'] + ' ตำบล/แขวง ' + row['AMPHUR_ID'] + ' จังหวัด ' + row['PROVINCE_ID'] + ' รหัสไปรษณีย์ ' +\
        row['PostCode'] + '\n' + 'ภูมิลำเนาเดิม : บ้านเลขที่ ' + row['homeHouseNo'] + ' ถนน ' + row['homeStreet'] + ' อำเภอ/เขต ' + \
        row['homeDistrict'] + ' ตำบล/แขวง ' + row['homeAmphur'] + ' จังหวัด ' + row['homeProvince'] + ' รหัสไปรษณีย์ ' + row['homePostCode'], data_format)
    workbook.close()
    conn.close()
    return "Success"
    directory = '/code/'
    filename = 'Criminal.xlsx'
    path = directory + filename
    return send_file(path,
                          mimetype='application/vnd.ms-excel',
                            as_attachment=True,
                            attachment_filename=filename)
