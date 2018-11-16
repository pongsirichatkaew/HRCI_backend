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
        WHERE Address.AddressType = 'Present' and Family.MemberType = 'Father' AND Personal.ID_CardNo = %s"""
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
        sql = "SELECT employee.name_th,employee.surname_th,employee.citizenid,employee.start_work,company.company_short_name,position.position_detail,section.sect_detail,org_name.org_name_detail,cost_center_name.cost_detail FROM employee INNER JOIN position ON position.position_id = employee.position_id\
                                      INNER JOIN company ON company.companyid = employee.company_id\
                                      INNER JOIN section ON section.sect_id = employee.section_id\
                                      INNER JOIN cost_center_name ON cost_center_name.cost_center_name_id = employee.cost_center_name_id\
                                      INNER JOIN org_name ON org_name.org_name_id = employee.org_name_id\
        "
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryEmployeeList_month_year', methods=['POST'])
@connect_sql()
def QryEmployeeList_month_year(cursor):
    dataInput = request.json
    source = dataInput['source']
    data_new = source
    year=str(data_new['year'])
    month=str(data_new['month'])
    try:
        sql = """SELECT employee.name_th,employee.surname_th,employee.citizenid,employee.start_work,company.company_short_name,position.position_detail,section.sect_detail,org_name.org_name_detail,cost_center_name.cost_detail FROM employee INNER JOIN position ON position.position_id = employee.position_id\
                                      INNER JOIN company ON company.companyid = employee.company_id\
                                      INNER JOIN section ON section.sect_id = employee.section_id\
                                      INNER JOIN cost_center_name ON cost_center_name.cost_center_name_id = employee.cost_center_name_id\
                                      INNER JOIN org_name ON org_name.org_name_id = employee.org_name_id\
        WHERE employee.start_work LIKE '%-{}-{}'""".format(month,year)
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryEmployeeList_month_year_company', methods=['POST'])
@connect_sql()
def QryEmployeeList_month_year_company(cursor):
    dataInput = request.json
    source = dataInput['source']
    data_new = source
    year=str(data_new['year'])
    month=str(data_new['month'])
    companyid=str(data_new['companyid'])
    try:
        sql = """SELECT employee.name_th,employee.surname_th,employee.citizenid,employee.start_work,company.company_short_name,position.position_detail,section.sect_detail,org_name.org_name_detail,cost_center_name.cost_detail FROM employee INNER JOIN position ON position.position_id = employee.position_id\
                                      INNER JOIN company ON company.companyid = employee.company_id\
                                      INNER JOIN section ON section.sect_id = employee.section_id\
                                      INNER JOIN cost_center_name ON cost_center_name.cost_center_name_id = employee.cost_center_name_id\
                                      INNER JOIN org_name ON org_name.org_name_id = employee.org_name_id\
        WHERE employee.company_id='{}' AND employee.start_work LIKE '%-{}-{}'""".format(month,year,companyid)
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
        sql4 ="""SELECT Personal.*,Address.AddressType, Address.HouseNo, Address.Street, Address.DISTRICT_ID, Address.AMPHUR_ID, Address.PROVINCE_ID, Address.PostCode, Address.Tel, Address.Fax,homeTable.AddressType as homeAddress, homeTable.HouseNo as homeHouseNo, homeTable.Street as homeStreet,employee.company_id as companyid,employee.start_work as start_work,position.position_detail as position_detail, \
        section.sect_detail as sect_detail,org_name.org_name_detail as org_name_detail,cost_center_name.cost_detail as cost_detail,company.company_short_name,
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
        WHERE Address.AddressType = 'Present' AND Family.MemberType = 'Father'"""
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

        sql4 ="""SELECT Personal.*,Address.AddressType, Address.HouseNo, Address.Street, Address.DISTRICT_ID, Address.AMPHUR_ID, Address.PROVINCE_ID, Address.PostCode, Address.Tel, Address.Fax,homeTable.AddressType as homeAddress, homeTable.HouseNo as homeHouseNo, homeTable.Street as homeStreet,employee.company_id as companyid,employee.start_work as start_work,position.position_detail as position_detail, \
        section.sect_detail as sect_detail,org_name.org_name_detail as org_name_detail,cost_center_name.cost_detail as cost_detail,company.company_short_name,
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
        WHERE Address.AddressType = 'Present' AND Family.MemberType = 'Father' AND employee.start_work LIKE '%-{}-{}' AND employee.company_id='{}'""".format(month,year,companyid)

        cursor.execute(sql4)
        columns = [column[0] for column in cursor.description]
        result4 = toJson(cursor.fetchall(),columns)
        return jsonify(result4)
    except Exception as e:
        logserver(e)
        return "fail"

@app.route('/export_criminal_by_month', methods=['POST'])
@connect_sql()
def export_criminal_by_month(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        year=str(data_new['year'])
        month=str(data_new['month'])
        companyid=str(data_new['companyid'])
        try:
            sql4 ="""SELECT Personal.*,Address.AddressType, Address.HouseNo, Address.Street, Address.DISTRICT_ID, Address.AMPHUR_ID, Address.PROVINCE_ID, Address.PostCode, Address.Tel, Address.Fax,homeTable.AddressType as homeAddress, homeTable.HouseNo as homeHouseNo, homeTable.Street as homeStreet,employee.company_id as companyid,employee.start_work as start_work,position.position_detail as position_detail,
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
            LEFT JOIN Family ON Family.ID_CardNo = Personal.ID_CardNo
            LEFT JOIN (SELECT * FROM Address WHERE AddressType = 'Home') AS homeTable ON homeTable.ID_CardNo = Personal.ID_CardNo
            LEFT JOIN (SELECT * FROM Family WHERE MemberType = 'Mother') AS motherTable ON motherTable.ID_CardNo = Personal.ID_CardNo
            WHERE Address.AddressType = 'Present' AND Family.MemberType = 'Father' AND employee.start_work LIKE '%-{}-{}' AND employee.company_id='{}'""".format(month,year,companyid)

            cursor.execute(sql4)
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            companyname_ = result[0]['companyname']
        except Exception as e:
            logserver(e)
            return "No_Data"

        isSuccess = True
        reasonCode = 200
        reasonText = ""
        now = datetime.now()
        datetimeStr = now.strftime('%Y%m%d_%H%M%S%f')
        filename_tmp = secure_filename('{}_{}'.format(datetimeStr, 'Template_Criminal_by.xlsx'))

        wb = load_workbook('../app/Template/Template_Criminal_by.xlsx')
        if len(result) > 0:

            sheet = wb['Sheet1']
            sheet['B'+str(4)] = year + '/' + month
            sheet['C'+str(4)] = companyname_
            offset = 6
            i = 0
            for i in xrange(len(result)):
                sheet['A'+str(offset + i)] = i+1
                sheet['B'+str(offset + i)] = result[i]['NameTh'] + ' ' + result[i]['SurnameTh']
                sheet['C'+str(offset + i)] = result[i]['ID_CardNo']
                sheet['D'+str(offset + i)] = result[i]['Birthdate_name']
                sheet['E'+str(offset + i)] = result[i]['fatherName'] + ' ' + result[i]['fatherSurname'] + '\n' + result[i]['motherName'] + ' ' + result[i]['motherSurname']
                sheet['F'+str(offset + i)] = 'ที่อยู่ปัจจุบัน : บ้านเลขที่ '.decode('utf-8') + result[i]['HouseNo'] + ' ถนน '.decode('utf-8') + result[i]['Street'] + ' อำเภอ/เขต '.decode('utf-8') \
                + result[i]['DISTRICT_ID'] + ' ตำบล/แขวง '.decode('utf-8') + result[i]['AMPHUR_ID'] + ' จังหวัด '.decode('utf-8') + result[i]['PROVINCE_ID'] + ' รหัสไปรษณีย์ '.decode('utf-8') +\
                result[i]['PostCode']
                i = i + 1
        wb.save(filename_tmp)
        with open(filename_tmp, "rb") as f:
            encoded_string = base64.b64encode(f.read())
        os.remove(filename_tmp)
        displayColumns = ['isSuccess','reasonCode','reasonText','excel_base64']
        displayData = [(isSuccess,reasonCode,reasonText,encoded_string)]
        return jsonify(toDict(displayData,displayColumns))
    except Exception as e:
        logserver(e)
        return "fail"
@app.route("/ExportToExcel", methods=['POST'])
@connect_sql()
def ExportToExcel(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        year=str(data_new['year'])
        month=str(data_new['month'])
        try:
            sql4 ="""SELECT Personal.* ,Address.AddressType, Address.HouseNo, Address.Street, Address.DISTRICT_ID, Address.AMPHUR_ID, Address.PROVINCE_ID, Address.PostCode, Address.Tel, Address.Fax,homeTable.AddressType as homeAddress, homeTable.HouseNo as homeHouseNo, homeTable.Street as homeStreet,employee.company_id as companyid,employee.start_work as start_work,position.position_detail as position_detail,
            section.sect_detail as sect_detail,org_name.org_name_detail as org_name_detail,cost_center_name.cost_detail as cost_detail,company.company_short_name,
            homeTable.DISTRICT_ID as homeDistrict, homeTable.AMPHUR_ID as homeAmphur, homeTable.PROVINCE_ID as homeProvince, homeTable.PostCode as homePostCode, homeTable.Tel as homeTel, homeTable.Fax as homeFax,employee.create_at as timedate,
            Family.Name as fatherName, Family.Surname as fatherSurname,motherTable.Name as motherName, motherTable.Surname as motherSurname
            FROM Personal
            LEFT JOIN employee ON employee.citizenid = Personal.ID_CardNo
            LEFT JOIN position ON position.position_id = employee.position_id
            LEFT JOIN section ON section.sect_id = employee.section_id
            LEFT JOIN org_name ON org_name.org_name_id = employee.org_name_id
            LEFT JOIN cost_center_name ON cost_center_name.cost_center_name_id = employee.cost_center_name_id
            LEFT JOIN company ON employee.company_id = company.companyid
            LEFT JOIN Address ON Address.ID_CardNo = Personal.ID_CardNo
            LEFT JOIN Family ON Family.ID_CardNo = Personal.ID_CardNo
            LEFT JOIN (SELECT * FROM Address WHERE AddressType = 'Home') AS homeTable ON homeTable.ID_CardNo = Personal.ID_CardNo
            LEFT JOIN (SELECT * FROM Family WHERE MemberType = 'Mother') AS motherTable ON motherTable.ID_CardNo = Personal.ID_CardNo
            WHERE Address.AddressType = 'Present' AND Family.MemberType = 'Father' AND employee.start_work LIKE '%-{}-{}'""".format(month,year)
            cursor.execute(sql4)
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            companyname_ = result[0]['company_short_name']
        except Exception as e:
            logserver(e)
            return "No_Data"

        isSuccess = True
        reasonCode = 200
        reasonText = ""
        now = datetime.now()
        datetimeStr = now.strftime('%Y%m%d_%H%M%S%f')
        filename_tmp = secure_filename('{}_{}'.format(datetimeStr, 'Template_Criminal.xlsx'))

        wb = load_workbook('../app/Template/Template_Criminal.xlsx')
        if len(result) > 0:

            sheet = wb['Sheet1']
            sheet['C'+str(3)] = year + '/' + month
            offset = 5
            i = 0
            for i in xrange(len(result)):
                sheet['A'+str(offset + i)] = i+1
                sheet['B'+str(offset + i)] = result[i]['company_short_name']
                sheet['C'+str(offset + i)] = result[i]['NameTh'] + ' ' + result[i]['SurnameTh']
                sheet['D'+str(offset + i)] = result[i]['ID_CardNo']
                sheet['E'+str(offset + i)] = result[i]['Birthdate_name']
                sheet['F'+str(offset + i)] = result[i]['fatherName'] + ' ' + result[i]['fatherSurname'] + '\n' + result[i]['motherName'] + ' ' + result[i]['motherSurname']
                sheet['G'+str(offset + i)] = 'ที่อยู่ปัจจุบัน : บ้านเลขที่ '.decode('utf-8') + result[i]['HouseNo'] + ' ถนน '.decode('utf-8') + result[i]['Street'] + ' อำเภอ/เขต '.decode('utf-8') \
                + result[i]['DISTRICT_ID'] + ' ตำบล/แขวง '.decode('utf-8') + result[i]['AMPHUR_ID'] + ' จังหวัด '.decode('utf-8') + result[i]['PROVINCE_ID'] + ' รหัสไปรษณีย์ '.decode('utf-8') +\
                result[i]['PostCode']
                i = i + 1
        wb.save(filename_tmp)
        with open(filename_tmp, "rb") as f:
            encoded_string = base64.b64encode(f.read())
        os.remove(filename_tmp)
        displayColumns = ['isSuccess','reasonCode','reasonText','excel_base64']
        displayData = [(isSuccess,reasonCode,reasonText,encoded_string)]
        return jsonify(toDict(displayData,displayColumns))
    except Exception as e:
        logserver(e)
        return e
