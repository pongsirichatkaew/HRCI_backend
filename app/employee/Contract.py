#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/QryContract', methods=['POST'])
@connect_sql()
def QryContract(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT * FROM employee INNER JOIN company ON employee.company_id = company.companyid\
                                      INNER JOIN Address ON employee.citizenid = Address.ID_CardNo\
                                      INNER JOIN Personal ON employee.citizenid = Personal.ID_CardNo\
                                      INNER JOIN position ON employee.position_id = position.position_id\
        WHERE employee.employeeid=%s"
        cursor.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sql2 = "SELECT * FROM employee INNER JOIN company ON employee.company_id = company.companyid\
                                      INNER JOIN Address ON employee.citizenid = Address.ID_CardNo\
                                      INNER JOIN Personal ON employee.citizenid = Personal.ID_CardNo\
                                      INNER JOIN position ON employee.position_id = position.position_id\
        WHERE employee.employeeid=%s AND Address.AddressType='Home'"
        cursor.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result__2 = toJson(cursor.fetchall(),columns)

        decodesalary = base64.b64decode(result[0]['salary'])
        tranImage = 'uploads/'+result[0]['imageName']
        with open(tranImage, 'rb') as image_file:
            encoded_Image = base64.b64encode(image_file.read())
        tranExpiryDate_idcard = result[0]['ExpiryDate']
        idcard_expi = tranExpiryDate_idcard.split("-")
        tranExpiryDate_idcard_Date = str(int(idcard_expi[0]))
        tranExpiryDate_idcard_Year = str(int(idcard_expi[2])+543)
        tranExpiryDate_idcard_Mounth = int(idcard_expi[1])
        if   tranExpiryDate_idcard_Mounth==1:
             tranExpiryDate_idcard_Mounth="มกราคม"
        elif tranExpiryDate_idcard_Mounth==2:
             tranExpiryDate_idcard_Mounth="กุมภาพันธ์"
        elif tranExpiryDate_idcard_Mounth==3:
             tranExpiryDate_idcard_Mounth="มีนาคม"
        elif tranExpiryDate_idcard_Mounth==4:
             tranExpiryDate_idcard_Mounth="เมษายน"
        elif tranExpiryDate_idcard_Mounth==5:
             tranExpiryDate_idcard_Mounth="พฤษภาคม"
        elif tranExpiryDate_idcard_Mounth==6:
             tranExpiryDate_idcard_Mounth="มิถุนายน"
        elif tranExpiryDate_idcard_Mounth==7:
             tranExpiryDate_idcard_Mounth="กรกฏาคม"
        elif tranExpiryDate_idcard_Mounth==8:
             tranExpiryDate_idcard_Mounth="สิงหาคม"
        elif tranExpiryDate_idcard_Mounth==9:
             tranExpiryDate_idcard_Mounth="กันยายน"
        elif tranExpiryDate_idcard_Mounth==10:
             tranExpiryDate_idcard_Mounth="ตุลาคม"
        elif tranExpiryDate_idcard_Mounth==11:
             tranExpiryDate_idcard_Mounth="พฤศจิกายน"
        else:
             tranExpiryDate_idcard_Mounth="ธันวาคม"

        tranExpiryDate_start_work = result[0]['start_work']
        start_work_expi = tranExpiryDate_start_work.split("-")
        tranExpiryDate_start_work_Date = str(int(start_work_expi[0]))
        tranExpiryDate_start_work_Year = str(int(start_work_expi[2])+543)
        tranExpiryDate_start_work_Mounth = int(start_work_expi[1])
        if   tranExpiryDate_start_work_Mounth==1:
             tranExpiryDate_start_work_Mounth="มกราคม"
        elif tranExpiryDate_start_work_Mounth==2:
             tranExpiryDate_start_work_Mounth="กุมภาพันธ์"
        elif tranExpiryDate_start_work_Mounth==3:
             tranExpiryDate_start_work_Mounth="มีนาคม"
        elif tranExpiryDate_start_work_Mounth==4:
             tranExpiryDate_start_work_Mounth="เมษายน"
        elif tranExpiryDate_start_work_Mounth==5:
             tranExpiryDate_start_work_Mounth="พฤษภาคม"
        elif tranExpiryDate_start_work_Mounth==6:
             tranExpiryDate_start_work_Mounth="มิถุนายน"
        elif tranExpiryDate_start_work_Mounth==7:
             tranExpiryDate_start_work_Mounth="กรกฏาคม"
        elif tranExpiryDate_start_work_Mounth==8:
             tranExpiryDate_start_work_Mounth="สิงหาคม"
        elif tranExpiryDate_start_work_Mounth==9:
             tranExpiryDate_start_work_Mounth="กันยายน"
        elif tranExpiryDate_start_work_Mounth==10:
             tranExpiryDate_start_work_Mounth="ตุลาคม"
        elif tranExpiryDate_start_work_Mounth==11:
             tranExpiryDate_start_work_Mounth="พฤศจิกายน"
        else:
             tranExpiryDate_start_work_Mounth="ธันวาคม"

        tranExpiryDate_EndWork_probation = result[0]['EndWork_probation']
        EndWork_probation_expi = tranExpiryDate_EndWork_probation.split("-")
        tranExpiryDate_EndWork_probation_Date = str(int(EndWork_probation_expi[0]))
        tranExpiryDate_EndWork_probation_Year = str(int(EndWork_probation_expi[2])+543)
        tranExpiryDate_EndWork_probation_Mounth = int(EndWork_probation_expi[1])
        if   tranExpiryDate_EndWork_probation_Mounth==1:
             tranExpiryDate_EndWork_probation_Mounth="มกราคม"
        elif tranExpiryDate_EndWork_probation_Mounth==2:
             tranExpiryDate_EndWork_probation_Mounth="กุมภาพันธ์"
        elif tranExpiryDate_EndWork_probation_Mounth==3:
             tranExpiryDate_EndWork_probation_Mounth="มีนาคม"
        elif tranExpiryDate_EndWork_probation_Mounth==4:
             tranExpiryDate_EndWork_probation_Mounth="เมษายน"
        elif tranExpiryDate_EndWork_probation_Mounth==5:
             tranExpiryDate_EndWork_probation_Mounth="พฤษภาคม"
        elif tranExpiryDate_EndWork_probation_Mounth==6:
             tranExpiryDate_EndWork_probation_Mounth="มิถุนายน"
        elif tranExpiryDate_EndWork_probation_Mounth==7:
             tranExpiryDate_EndWork_probation_Mounth="กรกฏาคม"
        elif tranExpiryDate_EndWork_probation_Mounth==8:
             tranExpiryDate_EndWork_probation_Mounth="สิงหาคม"
        elif tranExpiryDate_EndWork_probation_Mounth==9:
             tranExpiryDate_EndWork_probation_Mounth="กันยายน"
        elif tranExpiryDate_EndWork_probation_Mounth==10:
             tranExpiryDate_EndWork_probation_Mounth="ตุลาคม"
        elif tranExpiryDate_EndWork_probation_Mounth==11:
             tranExpiryDate_EndWork_probation_Mounth="พฤศจิกายน"
        else:
             tranExpiryDate_EndWork_probation_Mounth="ธันวาคม"

        sql2 = "SELECT employee_MD.name_md,employee_MD.surname_md,employee_MD.position_id,position.position_detail FROM employee_MD INNER JOIN company ON employee_MD.companyid = company.companyid INNER JOIN position ON employee_MD.position_id = position.position_id WHERE employee_MD.companyid=%s"
        cursor.execute(sql2,result[0]['company_id'])
        columns2 = [column[0] for column in cursor.description]
        result2 = toJson(cursor.fetchall(),columns2)

        sql3 = "SELECT contract_id,contract_date,Authority_Distrinct_Id_Card FROM Contract WHERE ID_CardNo=%s"
        cursor.execute(sql3,result[0]['citizenid'])
        columns3 = [column[0] for column in cursor.description]
        result3 = toJson(cursor.fetchall(),columns3)

        tranExpiryDate_contract_date = result3[0]['contract_date']
        EndWork_contract_date_expi = tranExpiryDate_contract_date.split("-")
        tranExpiryDate_contract_date_Date = str(int(EndWork_contract_date_expi[0]))
        tranExpiryDate_contract_date_Year = str(int(EndWork_contract_date_expi[2])+543)
        tranExpiryDate_contract_date_Mounth = int(EndWork_contract_date_expi[1])
        if   tranExpiryDate_contract_date_Mounth==1:
             tranExpiryDate_contract_date_Mounth="มกราคม"
        elif tranExpiryDate_contract_date_Mounth==2:
             tranExpiryDate_contract_date_Mounth="กุมภาพันธ์"
        elif tranExpiryDate_contract_date_Mounth==3:
             tranExpiryDate_contract_date_Mounth="มีนาคม"
        elif tranExpiryDate_contract_date_Mounth==4:
             tranExpiryDate_contract_date_Mounth="เมษายน"
        elif tranExpiryDate_contract_date_Mounth==5:
             tranExpiryDate_contract_date_Mounth="พฤษภาคม"
        elif tranExpiryDate_contract_date_Mounth==6:
             tranExpiryDate_contract_date_Mounth="มิถุนายน"
        elif tranExpiryDate_contract_date_Mounth==7:
             tranExpiryDate_contract_date_Mounth="กรกฏาคม"
        elif tranExpiryDate_contract_date_Mounth==8:
             tranExpiryDate_contract_date_Mounth="สิงหาคม"
        elif tranExpiryDate_contract_date_Mounth==9:
             tranExpiryDate_contract_date_Mounth="กันยายน"
        elif tranExpiryDate_contract_date_Mounth==10:
             tranExpiryDate_contract_date_Mounth="ตุลาคม"
        elif tranExpiryDate_contract_date_Mounth==11:
             tranExpiryDate_contract_date_Mounth="พฤศจิกายน"
        else:
             tranExpiryDate_contract_date_Mounth="ธันวาคม"

        tranCon_id = result3[0]['contract_id']
        if   tranCon_id<=9:
             tranCon=str(tranCon_id)
             codesumlast="000"+tranCon
        elif tranCon_id<=99:
             tranCon=str(tranCon_id)
             codesumlast="00"+tranCon
        elif tranCon_id<=999:
             tranCon=str(tranCon_id)
             codesumlast="0"+tranCon
        else:
             codesumlast=str(tranCon_id)
        now = datetime.now()
        date = str(int(now.year)+543)

        salary = decodesalary
        salary= (str(salary)[::-1])
        thai_number = ("ศูนย์","หนึ่ง","สอง","สาม","สี่","ห้า","หก","เจ็ด","แปด","เก้า")
        unit = ("","สิบ","ร้อย","พัน","หมื่น","แสน","ล้าน")
        length = len(salary) > 1
        resultSalary = ""
        for index, current in enumerate(map(int, salary)):
            if current:
                if index:
                   resultSalary = unit[index] + resultSalary
                if length and current == 1 and index == 0:
                    resultSalary += 'เอ็ด'
                elif index == 1 and current == 2:
                    resultSalary = 'ยี่' + resultSalary
                elif index != 1 or current != 1:
                    resultSalary = thai_number[current] + resultSalary

        decodesalary = "{:,}".format(int(decodesalary))
        resultlast={}
        resultlast["Name"] = result[0]['NameTh']
        resultlast["Now_year"] = date
        resultlast["HouseNo"] = result__2[0]['HouseNo']
        resultlast["Street"] = result__2[0]['Street']
        resultlast['Path_logo_company'] = encoded_Image
        resultlast["DISTRICT"] = result__2[0]['DISTRICT_ID']
        resultlast["AMPHUR"] = result__2[0]['AMPHUR_ID']
        resultlast["PROVINCE"] = result__2[0]['PROVINCE_ID']
        resultlast["Authority_Distrinct"] = result3[0]['Authority_Distrinct_Id_Card']
        resultlast["PostCode"] = result__2[0]['PostCode']
        resultlast["Surname"] = result[0]['SurnameTh']
        resultlast["citizenid"] = result[0]['ID_CardNo']
        resultlast["position_detail"] = result[0]['position_detail']
        resultlast["salary"] = result[0]['salary']
        resultlast["Shot_name_company"] = result[0]['company_short_name']
        resultlast["Name_company"] = result[0]['companyname']
        resultlast["Address_company"] = result[0]['address_company']
        resultlast["Employee_MD"] = result2
        resultlast["Contract_id"] = codesumlast
        resultlast["Contract"] = result3
        resultlast["salary_thai"] = resultSalary
        resultlast["Decodesalary"] = decodesalary
        resultlast['ExpiryDate_idcard_Date'] = tranExpiryDate_idcard_Date
        resultlast['ExpiryDate_idcard_Year'] = tranExpiryDate_idcard_Year
        resultlast['ExpiryDate_idcard_Mounth'] = tranExpiryDate_idcard_Mounth
        resultlast['start_work_Date'] = tranExpiryDate_start_work_Date
        resultlast['start_work_Year'] = tranExpiryDate_start_work_Year
        resultlast['start_work_Mounth'] = tranExpiryDate_start_work_Mounth
        resultlast['EndWork_probation_Date'] = tranExpiryDate_EndWork_probation_Date
        resultlast['EndWork_probation_Year'] = tranExpiryDate_EndWork_probation_Year
        resultlast['EndWork_probation_Mounth'] = tranExpiryDate_EndWork_probation_Mounth
        resultlast['Start_contract_date_Date'] = tranExpiryDate_contract_date_Date
        resultlast['Start_contract_date_Year'] = tranExpiryDate_contract_date_Year
        resultlast['Start_contract_date_Mounth'] = tranExpiryDate_contract_date_Mounth
        return jsonify(resultlast)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryListContract', methods=['POST'])
@connect_sql()
def QryListContract(cursor):
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        sql = "SELECT employee.name_th,employee.employeeid,employee.surname_th,employee.citizenid,company.company_short_name,position.position_detail,section.sect_detail,org_name.org_name_detail,cost_center_name.cost_detail FROM employee LEFT JOIN company ON employee.company_id = company.companyid\
                                      LEFT JOIN position ON employee.position_id = position.position_id\
                                      LEFT JOIN section ON employee.section_id = section.sect_id\
                                      LEFT JOIN org_name ON employee.org_name_id = org_name.org_name_id\
                                      LEFT JOIN cost_center_name ON employee.cost_center_name_id = cost_center_name.cost_center_name_id"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        connection.close()
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Update_Contract_date', methods=['POST'])
@connect_sql()
def Update_Contract_date(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT citizenid FROM employee WHERE employeeid=%s"
        cursor.execute(sql,(data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sqlUp = "UPDATE Contract SET contract_date=%s WHERE ID_CardNo=%s"
        cursor.execute(sqlUp,(data_new['contract_date'],result[0]['citizenid']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryListContract_by_mounth', methods=['POST'])
@connect_sql()
def QryListContract_by_mounth(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        year=str(data_new['year'])
        month=str(data_new['month'])
        companyid=str(data_new['companyid'])
        sql = """SELECT employee.name_th,employee.employeeid,employee.surname_th,employee.citizenid,company.company_short_name,position.position_detail,section.sect_detail,org_name.org_name_detail,cost_center_name.cost_detail FROM employee LEFT JOIN company ON employee.company_id = company.companyid\
                                      LEFT JOIN section ON employee.section_id = section.sect_id\
                                      LEFT JOIN position ON employee.position_id = position.position_id\
                                      LEFT JOIN org_name ON employee.org_name_id = org_name.org_name_id\
                                      LEFT JOIN cost_center_name ON employee.cost_center_name_id = cost_center_name.cost_center_name_id\
        WHERE employee.start_work LIKE '%""" + month + """-""" + year + """' AND employee.company_id='"""+companyid +"""'"""
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryListContract_by_mounth_new', methods=['POST'])
@connect_sql()
def QryListContract_by_mounth_new(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        year=str(data_new['year'])
        month=str(data_new['month'])
        sql = """SELECT employee.name_th,employee.employeeid,employee.surname_th,employee.citizenid,company.company_short_name,position.position_detail,section.sect_detail,org_name.org_name_detail,cost_center_name.cost_detail FROM employee LEFT JOIN company ON employee.company_id = company.companyid\
                                      LEFT JOIN section ON employee.section_id = section.sect_id\
                                      LEFT JOIN position ON employee.position_id = position.position_id\
                                      LEFT JOIN org_name ON employee.org_name_id = org_name.org_name_id\
                                      LEFT JOIN cost_center_name ON employee.cost_center_name_id = cost_center_name.cost_center_name_id\
        WHERE employee.start_work LIKE '%""" + month + """-""" + year + """'"""
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee_Contract', methods=['POST'])
@connect_sql()
def EditEmployee_Contract(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT employee.citizenid,employee.company_id,employee.start_work,Contract.contract_id FROM employee INNER JOIN Contract ON employee.citizenid = Contract.ID_CardNo WHERE employeeid=%s"
        cursor.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sql_log = "INSERT INTO Contract_log (employeeid_old,ID_CardNo,contract_id,company_id,createby) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sql_log,(data_new['employeeid'],result[0]['citizenid'],result[0]['contract_id'],result[0]['company_id'],data_new['createby']))

        start_date_ = result[0]['start_work']
        split_str_date = start_date_.split("-")
        str_date_year = split_str_date[2]

        now_contract = str_date_year
        date_contract = str(int(now_contract)+543)
        date_sub_contract = date_contract[2:]
        try:
            sql_contract_id = "SELECT contract_id,year FROM Contract WHERE companyid=%s AND year=%s ORDER BY contract_id DESC LIMIT 1"
            cursor.execute(sql_contract_id,(data_new['company_id'],date_contract))
            columns = [column[0] for column in cursor.description]
            resultsql_contract_id = toJson(cursor.fetchall(),columns)
            year_contract = resultsql_contract_id[0]['year']
            contract_id_ = resultsql_contract_id[0]['contract_id']
            year_sub_con = year_contract[2:]
            if year_sub_con==date_sub_contract:
                contract_id_ = resultsql_contract_id[0]['contract_id']
            else:
                contract_id_ = 0
        except Exception as e:
            contract_id_ = 0
        contract_id_last = int(contract_id_)+1

        sqlUp_EmerContact = "UPDATE Contract SET contract_id=%s,companyid=%s WHERE ID_CardNo=%s"
        cursor.execute(sqlUp_EmerContact,(contract_id_last,data_new['company_id'],result[0]['citizenid']))

        companyid__ = int(data_new['company_id'])
        if companyid__==1:
            now = str_date_year
            date_n = str(int(now))
            form_employee = date_n
        elif companyid__==21:
            now = str_date_year
            date_n = str(int(now))
            form_employee = date_n[2:]
        else:
            now = str_date_year
            date_n = str(int(now)+543)
            form_employee = date_n[2:]
        sqlcompafirst = "SELECT acronym FROM company WHERE companyid=%s"
        cursor.execute(sqlcompafirst,data_new['company_id'])
        columnscompafirst = [column[0] for column in cursor.description]
        resultcompafirst = toJson(cursor.fetchall(),columnscompafirst)
        coun_length =len(resultcompafirst[0]['acronym'])
        coun_company = str(resultcompafirst[0]['acronym'])
        try:
            sqlEmployee = "SELECT employeeid FROM employee WHERE company_id=%s ORDER BY employeeid DESC LIMIT 1"
            cursor.execute(sqlEmployee,data_new['company_id'])
            columnsEmployee = [column[0] for column in cursor.description]
            resultEmployee = toJson(cursor.fetchall(),columnsEmployee)
            Emp_last = resultEmployee[0]['employeeid']
            if companyid__!=1:
                form_employee2 = Emp_last[coun_length:]
                form_employee3 = form_employee2[:-3]
                if form_employee3==form_employee:
                    Emp_last = resultEmployee[0]['employeeid']
                else:
                    Emp_last = coun_company+"000"
            else:
                form_employee2 = Emp_last[coun_length:]
                form_employee3 = form_employee2[:-4]
                if form_employee3==form_employee:
                    Emp_last = resultEmployee[0]['employeeid']
                else:
                    Emp_last = coun_company+"000"
        except Exception as e:
            if companyid__!=1:
                Emp_last = coun_company+"000"
            else:
               Emp_last = coun_company+"000"
        type = Emp_last
        if  coun_length==0:
            coun_length=2
        elif coun_length==1:
            coun_length=3
        else:
            coun_length=coun_length+2
        if companyid__!=1:
            codelast = int(str(type[coun_length:]))+1
        else:
            codelast = str(int(str(type[coun_length:]))+1)
            codelast = codelast[2:]
            if codelast=="":
               codelast=1
            else:
                codelast=codelast
        if companyid__!=1:
            if  codelast<=9:
                codelast=str(codelast)
                codesumlast="00"+codelast
            elif codelast<=99:
                codelast=str(codelast)
                codesumlast="0"+codelast
            else:
                codesumlast=str(codelast)
        else:
            if  codelast<=9:
                codelast=str(codelast)
                codesumlast="000"+codelast
            elif codelast<=99:
                codelast=str(codelast)
                codesumlast="00"+codelast
            elif codelast<=999:
                codelast=str(codelast)
                codesumlast="0"+codelast
            else:
                codesumlast=str(codelast)
        first_character = resultcompafirst[0]['acronym']
        if companyid__==1:
            employeeid = first_character+form_employee+codesumlast
        elif companyid__==21:
            employeeid = first_character+form_employee+codesumlast
        else:
            employeeid = first_character+form_employee+codesumlast

        sqlUp_Emp_ = "UPDATE employee SET employeeid=%s,company_id=%s WHERE citizenid=%s"
        cursor.execute(sqlUp_Emp_,(employeeid,data_new['company_id'],result[0]['citizenid']))
        resultlast={}
        resultlast["employeeid"] = employeeid
        resultlast["message"] = "Success"
        return jsonify(resultlast)
    except Exception as e:
        resultlast={}
        resultlast["message"] = "fail"
        logserver(e)
        return jsonify(resultlast)
