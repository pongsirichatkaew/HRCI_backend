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
        WHERE employeeid=%s"
        cursor.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
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

        sql2 = "SELECT employee_MD.name_md,employee_MD.surname_md,employee_MD.position_id FROM employee_MD  INNER JOIN company ON employee_MD.companyid = company.companyid\
        WHERE employee_MD.companyid=%s"
        cursor.execute(sql2,result[0]['company_id'])
        columns2 = [column[0] for column in cursor.description]
        result2 = toJson(cursor.fetchall(),columns2)

        sql3 = "SELECT contract_id,Start_contract,End_contract,salary_thai,Authority_Distrinct_Id_Card FROM Contract WHERE ID_CardNo=%s"
        cursor.execute(sql3,result[0]['citizenid'])
        columns3 = [column[0] for column in cursor.description]
        result3 = toJson(cursor.fetchall(),columns3)
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
        resultlast={}
        resultlast["Name"] = result[0]['NameTh']
        resultlast["Now_year"] = date
        resultlast["HouseNo"] = result[0]['HouseNo']
        resultlast["Street"] = result[0]['Street']
        resultlast['Path_logo_company'] = encoded_Image
        resultlast["DISTRICT"] = result[0]['DISTRICT_ID']
        resultlast["AMPHUR"] = result[0]['AMPHUR_ID']
        resultlast["PROVINCE"] = result[0]['PROVINCE_ID']
        resultlast["Authority_Distrinct"] = result3[0]['Authority_Distrinct_Id_Card']
        resultlast["PostCode"] = result[0]['PostCode']
        resultlast["Surname"] = result[0]['SurnameTh']
        resultlast["citizenid"] = result[0]['ID_CardNo']
        resultlast["salary"] = result[0]['salary']
        resultlast["Shot_name_company"] = result[0]['company_short_name']
        resultlast["Name_company"] = result[0]['companyname']
        resultlast["Address_company"] = result[0]['address_company']
        resultlast["Employee_MD"] = result2
        resultlast["Contract_id"] = codesumlast
        resultlast["Contract"] = result3
        resultlast['ExpiryDate_idcard_Date'] = tranExpiryDate_idcard_Date
        resultlast['ExpiryDate_idcard_Year'] = tranExpiryDate_idcard_Year
        resultlast['ExpiryDate_idcard_Mounth'] = tranExpiryDate_idcard_Mounth
        return jsonify(resultlast)
    except Exception as e:
        logserver(e)
@app.route('/QryListContract', methods=['POST'])
@connect_sql()
def QryListContract(cursor):
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        sql = "SELECT * FROM employee INNER JOIN company ON employee.company_id = company.companyid\
                                      INNER JOIN section ON employee.section_id = section.sect_id\
                                      INNER JOIN position ON employee.position_id = position.position_id\
                                      INNER JOIN org_name ON employee.org_name_id = org_name.org_name_id\
                                      INNER JOIN cost_center_name ON employee.cost_center_name_id = cost_center_name.cost_center_name_id\
        "
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        connection.close()
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
