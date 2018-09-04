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
# @app.route('/export', methods=['POST'])
# # from flask import send_file
# # import xlsxwriter
# def export():
#     params = request.get_json()
#     print params['startdate']
#     startdate = datetime.strptime(params['startdate'], "%Y-%m-%d")
#     enddate = datetime.strptime(params['enddate'], "%Y-%m-%d")
#     days = []
#     for dt in daterange(startdate, enddate):
#         days.append(dt.strftime("%Y-%m-%d"))
#     datedata = []
#     try:
#         conn = mysql.connect()
#         cursor = conn.cursor()
#         print "connect DB"
#     except Exception as e:
#         print "can't connect database", e
#
#     for i in days:
#         querydate = '%s %%' % i
#         # print querydate
#         try:
#             query_string = "SELECT * FROM bill INNER JOIN bill_status ON bill.b_id = bill_status.b_id WHERE bill_status.create_at LIKE '%s' AND bill_status.status = 'Approved';" % querydate
#             cursor.execute(query_string)
#         except Exception as e:
#             print "Error:", e
#         data = cursor.fetchall()
#         # print data
#         columns = [column[0] for column in cursor.description]
#         result = toJson(data, columns)
#         # print len(result)
#         if result != []:
#             datedata.append(result)
#
#     workbook = xlsxwriter.Workbook('Bill_list.xlsx')
#     # Create a format to use in the merged range.
#
#     merge_format = workbook.add_format({
#         'bold': 1.5,
#         'align': 'center',
#         'valign': 'vcenter',
#         'font_size': '14'
#     })
#     cell_format = workbook.add_format({'bold': True,'align': 'center',
#         'valign': 'vcenter'})
#     data_format = workbook.add_format({'text_wrap': True})
#     # data_format.set_text_wrap()
#     worksheet = workbook.add_worksheet()
#
#
#     for (r, row) in enumerate(datedata):
#         # print datedata[r]['b_vendorname']
#         for c, col in enumerate(row):
#             # worksheet.write(r, c, col)
#             worksheet.merge_range('A1:J1', 'รายชื่อผู้วางบิล', merge_format)
#             for i in range(1,10):
#                 worksheet.set_column(c+i, c+i, 20, data_format)
#             worksheet.write('A2', 'ลำดับ', cell_format)
#             worksheet.write('B2', 'บริษัท', cell_format)
#             worksheet.write('C2', 'เลข invoice', cell_format)
#             worksheet.write('D2', 'ที่อยู่', cell_format)
#             worksheet.write('E2', 'อีเมล', cell_format)
#             worksheet.write('F2', 'รายละเอียด', cell_format)
#             worksheet.write('G2', 'ธนาคาร', cell_format)
#             worksheet.write('H2', 'ราคา', cell_format)
#             worksheet.write('I2', 'ภาษีหัก ณ ที่จ่าย', cell_format)
#             worksheet.write('J2', 'ราคาสุทธิ', cell_format)
#
#             worksheet.write('A'+str(r+3), r+1)
#             worksheet.write('B' + str(r + 3), row[0]['b_vendorname'], data_format)
#             worksheet.write('C' + str(r + 3), row[0]['b_invoice'], data_format)
#             worksheet.write('D' + str(r + 3), row[0]['b_vendoraddress'], data_format)
#             worksheet.write('E' + str(r + 3), row[0]['b_vendoremail'], data_format)
#             worksheet.write('F' + str(r + 3), row[0]['b_detail'], data_format)
#             worksheet.write('G' + str(r + 3), row[0]['bank_name'], data_format)
#             worksheet.write('H' + str(r + 3), row[0]['b_price'], data_format)
#             worksheet.write('I' + str(r + 3), row[0]['b_tax'], data_format)
#             worksheet.write('J' + str(r + 3), row[0]['b_totalprice'], data_format)
#
#     workbook.close()
#     conn.close()
#     # return "Success"
#     directory = '/code/'
#     filename = 'Bill_list.xlsx'
#     path = directory + filename
#     return send_file(path,
#                           mimetype='application/vnd.ms-excel',
#                             as_attachment=True,
#                             attachment_filename=filename)
