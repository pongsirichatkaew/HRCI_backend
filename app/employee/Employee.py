#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/InsertEmployee_resign', methods=['POST'])
@connect_sql()
def InsertEmployee_resign(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT name_th,surname_th,citizenid,start_work FROM employee WHERE employeeid=%s"
        cursor.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sqlemployee = "UPDATE employee SET validstatus=0 WHERE employeeid=%s"
        cursor.execute(sqlemployee,data_new['employeeid'])

        sqlemployee_ga = "UPDATE employee_ga SET validstatus=0 WHERE employeeid=%s"
        cursor.execute(sqlemployee_ga,data_new['employeeid'])

        sqlEmp_pro = "UPDATE Emp_probation SET validstatus=0 WHERE employeeid=%s"
        cursor.execute(sqlEmp_pro,data_new['employeeid'])

        sqlIn4 = "INSERT INTO employee_resign (employeeid,name_th,surname_th,ID_CardNo,star_work,issue_date,createby,Description) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn4,(data_new['employeeid'],result[0]['name_th'],result[0]['surname_th'],result[0]['citizenid'],result[0]['start_work'],data_new['issue_date'],data_new['createby'],data_new['Descriptions']))
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryEmployee_resign', methods=['POST'])
@connect_sql()
def QryEmployee_resign(cursor):
    try:
        sql = "SELECT * FROM employee_resign"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/UpdateStatus_Employee', methods=['POST'])
@connect_sql()
def UpdateStatus_Employee(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sqlUp = "UPDATE employee SET validstatus=%s WHERE employeeid=%s"
        cursor.execute(sqlUp,(data_new['validstatus'],data_new['employeeid']))
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryEmployee', methods=['POST'])
def QryEmployee():
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        sql = "SELECT * FROM employee LEFT JOIN company ON company.companyid = employee.company_id\
                                      LEFT JOIN position ON position.position_id = employee.position_id\
                                      LEFT JOIN section ON section.sect_id = employee.section_id\
                                      LEFT JOIN org_name ON org_name.org_name_id = employee.org_name_id\
                                      LEFT JOIN cost_center_name ON cost_center_name.cost_center_name_id = employee.cost_center_name_id\
                                      LEFT JOIN status ON status.status_id = employee.validstatus\
        WHERE employee.validstatus=1 AND company.validstatus=1 AND position.validstatus=1 AND section.validstatus=1 AND org_name.validstatus=1 AND cost_center_name.validstatus=1 AND status.validstatus=1"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        connection.close()
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee_ga', methods=['POST'])
@connect_sql()
def EditEmployee_ga(cursor):
    try:
        data = request.json
        source = data['source']
        data_new = source

        sqlUp = "UPDATE employee_ga SET validstatus=0,createby=%s WHERE employeeid=%s"
        cursor.execute(sqlUp,(data_new['createby'],data_new['employeeid']))

        sqlEm_ga = "INSERT INTO employee_ga (employeeid,citizenid,phone_depreciate,notebook_depreciate,limit_phone,chair_table,pc,notebook,office_equipment,ms,car_ticket,band_car,color,regis_car_number,other,description,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlEm_ga,(employeeid,result14[0]['ID_CardNo'],data_new['phone_depreciate'],data_new['notebook_depreciate'],data_new['limit_phone'],data_new['chair_table'],data_new['pc'],data_new['notebook'],data_new['office_equipment'],data_new['ms'],data_new['car_ticket'],data_new['band_car'],data_new['color'],\
        data_new['regis_car_number'],data_new['other'],data_new['description'],data_new['createby']))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryEmployee_one_person', methods=['POST'])
@connect_sql()
def QryEmployee_one_person(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sqlEmployee = "SELECT * FROM employee LEFT JOIN company ON company.companyid = employee.company_id\
                                      LEFT JOIN position ON position.position_id = employee.position_id\
                                      LEFT JOIN section ON section.sect_id = employee.section_id\
                                      LEFT JOIN org_name ON org_name.org_name_id = employee.org_name_id\
                                      LEFT JOIN cost_center_name ON cost_center_name.cost_center_name_id = employee.cost_center_name_id\
        WHERE employee.employeeid=%s AND employee.validstatus=1 AND company.validstatus=1 AND position.validstatus=1 AND section.validstatus=1 AND org_name.validstatus=1 AND cost_center_name.validstatus=1"
        cursor.execute(sqlEmployee,data_new['employeeid'])
        columnsEmployee = [column[0] for column in cursor.description]
        resultEmployee = toJson(cursor.fetchall(),columnsEmployee)
        decodesalary = base64.b64decode(resultEmployee[0]['salary'])

        sqlEmployee_email = "SELECT email FROM employee WHERE employee.employeeid=%s AND employee.validstatus=1"
        cursor.execute(sqlEmployee_email,data_new['employeeid'])
        columnsEmployeeEmail = [column[0] for column in cursor.description]
        resultEmployee_Email = toJson(cursor.fetchall(),columnsEmployeeEmail)

        sqlEm = "SELECT Address.AddressType,Address.HouseNo,Address.Street,Address.DISTRICT_ID,Address.AMPHUR_ID,Address.PROVINCE_ID,Address.PostCode,Address.Tel,Address.Fax FROM Address INNER JOIN Personal ON Personal.ID_CardNo=Address.ID_CardNo \
        WHERE Personal.ID_CardNo=%s AND Personal.validstatus=1 AND Address.validstatus=1"
        cursor.execute(sqlEm,resultEmployee[0]['citizenid'])
        columnsEm = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columnsEm)

        sql4 = "SELECT Attachment.Type,Attachment.PathFile FROM Attachment INNER JOIN Personal ON Personal.ID_CardNo=Attachment.ID_CardNo \
        WHERE Personal.ID_CardNo=%s AND Personal.validstatus=1"
        cursor.execute(sql4,resultEmployee[0]['citizenid'])
        columns4 = [column[0] for column in cursor.description]
        result4 = toJson(cursor.fetchall(),columns4)

        sql6 = "SELECT ComputerSkill.ComSkill,ComputerSkill.Level FROM ComputerSkill INNER JOIN Personal ON Personal.ID_CardNo=ComputerSkill.ID_CardNo \
        WHERE Personal.ID_CardNo=%s AND Personal.validstatus=1"
        cursor.execute(sql6,resultEmployee[0]['citizenid'])
        columns6 = [column[0] for column in cursor.description]
        result6 = toJson(cursor.fetchall(),columns6)

        sql9 = "SELECT Education.EducationLevel,Education.Institute,Education.StartYear,Education.EndYear,Education.Qualification,Education.Major,Education.GradeAvg,Education.ExtraCurricularActivities FROM Education INNER JOIN Personal ON Personal.ID_CardNo=Education.ID_CardNo \
        WHERE Personal.ID_CardNo=%s AND Personal.validstatus=1"
        cursor.execute(sql9,resultEmployee[0]['citizenid'])
        columns9 = [column[0] for column in cursor.description]
        result9 = toJson(cursor.fetchall(),columns9)

        sql10 = "SELECT Employment.CompanyName,Employment.CompanyAddress,Employment.PositionHeld,Employment.StartSalary,Employment.EndSalary,Employment.StartYear,Employment.EndYear,Employment.Responsibility,Employment.ReasonOfLeaving,Employment.Descriptionofwork FROM Employment INNER JOIN Personal ON Personal.ID_CardNo=Employment.ID_CardNo \
        WHERE Personal.ID_CardNo=%s AND Personal.validstatus=1"
        cursor.execute(sql10,resultEmployee[0]['citizenid'])
        columns10 = [column[0] for column in cursor.description]
        result10 = toJson(cursor.fetchall(),columns10)

        sqlfa = "SELECT Family.MemberType,Family.Name,Family.Surname,Family.Occupation,Family.Address,Family.Tel,Family.Fax FROM Family INNER JOIN Personal ON Personal.ID_CardNo=Family.ID_CardNo \
        WHERE (Family.MemberType = 'Father' OR Family.MemberType = 'Mother')AND Personal.ID_CardNo=%s AND Personal.validstatus=1 AND Family.validstatus=1"
        cursor.execute(sqlfa,resultEmployee[0]['citizenid'])
        columnsfa = [column[0] for column in cursor.description]
        resultfa = toJson(cursor.fetchall(),columnsfa)

        sqlbro = "SELECT Family.MemberType,Family.Name,Family.Surname,Family.Occupation,Family.Address,Family.Tel,Family.Fax FROM Family INNER JOIN Personal ON Personal.ID_CardNo=Family.ID_CardNo \
        WHERE Family.MemberType = 'BrotherSister' AND Personal.ID_CardNo=%s AND Personal.validstatus=1 AND Family.validstatus=1"
        cursor.execute(sqlbro,resultEmployee[0]['citizenid'])
        columnsbro = [column[0] for column in cursor.description]
        resultbro = toJson(cursor.fetchall(),columnsbro)

        sql13 = "SELECT LanguagesSkill.Languages,LanguagesSkill.Speaking,LanguagesSkill.Reading,LanguagesSkill.Writting FROM LanguagesSkill INNER JOIN Personal ON Personal.ID_CardNo=LanguagesSkill.ID_CardNo \
        WHERE Personal.ID_CardNo=%s AND Personal.validstatus=1"
        cursor.execute(sql13,resultEmployee[0]['citizenid'])
        columns13 = [column[0] for column in cursor.description]
        result13 = toJson(cursor.fetchall(),columns13)

        sql14 = "SELECT * FROM Personal \
        WHERE ID_CardNo=%s AND validstatus=1"
        cursor.execute(sql14,resultEmployee[0]['citizenid'])
        columns14 = [column[0] for column in cursor.description]
        result14 = toJson(cursor.fetchall(),columns14)

        try:
            encoded_Image=str("http://intranet.inet.co.th/assets/upload/staff/"+str(data_new['employeeid'])+".jpg")
            open_path_ = urllib.urlopen(encoded_Image)
            htmlSource = open_path_.read()
            open_path_.close()
            test= htmlSource.decode('utf-8')
            encoded_Image=str("http://intranet.inet.co.th/assets/upload/staff/"+str(data_new['employeeid'])+"s.jpg")
        except Exception as e:
            encoded_Image=str("http://intranet.inet.co.th/assets/upload/staff/"+str(data_new['employeeid'])+".jpg")

        sql17 = "SELECT Reference.RelativeName,Reference.RelativeSurname,Reference.RelativePosition,Reference.RelativeRelationship,Reference.PhysicalHandicap,Reference.PhysicalHandicapDetail,Reference.KnowFrom FROM Reference INNER JOIN Personal ON Personal.ID_CardNo=Reference.ID_CardNo \
        WHERE Personal.ID_CardNo=%s AND Personal.validstatus=1"
        cursor.execute(sql17,resultEmployee[0]['citizenid'])
        columns17 = [column[0] for column in cursor.description]
        result17 = toJson(cursor.fetchall(),columns17)

        sql18 = "SELECT RefPerson.RefName,RefPerson.RefPosition,RefPerson.RefAddress,RefPerson.RefTel FROM RefPerson INNER JOIN Personal ON Personal.ID_CardNo=RefPerson.ID_CardNo \
        WHERE Personal.ID_CardNo=%s AND Personal.validstatus=1"
        cursor.execute(sql18,resultEmployee[0]['citizenid'])
        columns18 = [column[0] for column in cursor.description]
        result18 = toJson(cursor.fetchall(),columns18)

        sql20 = "SELECT SpecialSkill.CarDrivingLicense,SpecialSkill.MotorBicycleDrivingLicense,SpecialSkill.OwnCar,SpecialSkill.OwnMotorBicycle,SpecialSkill.WorkUpCountry,SpecialSkill.StartWorkEarliest,SpecialSkill.PhysicalDisabilityOrDisease,SpecialSkill.DischargeFromEmployment,SpecialSkill.DischargeFromEmploymentReason,SpecialSkill.Arrested,SpecialSkill.ArrestedReason FROM SpecialSkill INNER JOIN Personal ON Personal.ID_CardNo=SpecialSkill.ID_CardNo \
        WHERE Personal.ID_CardNo=%s AND Personal.validstatus=1 AND SpecialSkill.validstatus=1"
        cursor.execute(sql20,resultEmployee[0]['citizenid'])
        columns20 = [column[0] for column in cursor.description]
        result20 = toJson(cursor.fetchall(),columns20)

        sql23 = "SELECT TrainingCourse.Subject,TrainingCourse.Place,TrainingCourse.StartDate,TrainingCourse.EndDate FROM TrainingCourse INNER JOIN Personal ON Personal.ID_CardNo=TrainingCourse.ID_CardNo \
        WHERE Personal.ID_CardNo=%s AND Personal.validstatus=1"
        cursor.execute(sql23,resultEmployee[0]['citizenid'])
        columns23 = [column[0] for column in cursor.description]
        result23 = toJson(cursor.fetchall(),columns23)
        arr={}
        arr["Address"] = result
        arr["employee"] = resultEmployee
        arr["Attachment"] = result4
        arr["Image_profile"] = encoded_Image
        arr["EmailEmp"] = resultEmployee_Email
        arr["Decodesalary"] = decodesalary
        arr["ComputerSkill"] = result6
        arr["Education"] = result9
        arr["Employment"] = result10
        arr['fatherAndmother'] = resultfa
        arr['BrotherSister'] = resultbro
        arr["LanguagesSkill"] = result13
        arr["Personal"] = result14
        arr["Reference"] = result17
        arr["RefPerson"] = result18
        arr["SpecialSkill"] = result20
        arr["TrainingCourse"] = result23
        return jsonify(arr)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee', methods=['POST'])
@connect_sql()
def EditEmployee(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT citizenid FROM employee WHERE employeeid=%s AND validstatus=1"
        cursor.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sql_Select_Personal = "SELECT * FROM Personal WHERE ID_CardNo=%s AND validstatus=1"
        cursor.execute(sql_Select_Personal,data_new['ID_CardNo'])
        columns = [column[0] for column in cursor.description]
        result_Personal = toJson(cursor.fetchall(),columns)

        sql_Up_Personal = "UPDATE Personal SET validstatus=0 WHERE ID_CardNo=%s"
        cursor.execute(sql_Up_Personal,(result[0]['citizenid']))

        sqlIn14 = """INSERT INTO Personal (NameTh,SurnameTh,NicknameTh,NameEn,SurnameEn,NicknameEn,Birthdate,BirthPlace,BirthProvince,BirthCountry,Age,Height,Weight,BloodGroup,Citizenship,Religion,ID_CardNo,IssueDate,ExpiryDate,MaritalStatus,NumberOfChildren,StudyChild,MilitaryService,Others,Worktel,Mobile,Email,EmergencyPerson,EmergencyRelation,EmergencyAddress,EmergencyTel,date) \
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sqlIn14,(data_new['NameTh'],data_new['SurnameTh'],data_new['NicknameTh'],data_new['NameEn'],\
        data_new['SurnameEn'],data_new['NicknameEn'],result_Personal[0]['Birthdate'],result_Personal[0]['BirthPlace'],result_Personal[0]['BirthProvince'], \
        result_Personal[0]['BirthCountry'],result_Personal[0]['Age'],result_Personal[0]['Height'],result_Personal[0]['Weight'],result_Personal[0]['BloodGroup'],result_Personal[0]['Citizenship'],result_Personal[0]['Religion'],result_Personal[0]['ID_CardNo'], \
        result_Personal[0]['IssueDate'],result_Personal[0]['ExpiryDate'],result_Personal[0]['MaritalStatus'],result_Personal[0]['NumberOfChildren'],result_Personal[0]['StudyChild'],result_Personal[0]['MilitaryService'],result_Personal[0]['Others'], \
        result_Personal[0]['Worktel'],data_new['Mobile'],result_Personal[0]['Email'],result_Personal[0]['EmergencyPerson'],result_Personal[0]['EmergencyRelation'],result_Personal[0]['EmergencyAddress'],result_Personal[0]['EmergencyTel'],result_Personal[0]['date']))

        # sql_Up_Personal = "UPDATE Personal SET validstatus=0 WHERE ID_CardNo=%s"
        # cursor.execute(sql_Up_Personal,(result[0]['citizenid']))
        # sqlIn14 = """INSERT INTO Personal (NameTh,SurnameTh,NicknameTh,NameEn,SurnameEn,NicknameEn,ID_CardNo,Mobile) \
        # VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
        # cursor.execute(sqlIn14,(data_new['NameTh'],data_new['SurnameTh'],data_new['NicknameTh'],data_new['NameEn'],\
        # data_new['SurnameEn'],data_new['NicknameEn'],data_new['ID_CardNo'],data_new['Mobile']))

        date1 = data_new['Start_contract']
        star_date = date1.split("-")
        Day_s = int(star_date[0])
        Mon_s =int(star_date[1])
        year_s = int(star_date[2])
        next_3_m = date(year_s,Mon_s,Day_s) + relativedelta(days=89)
        next_3_m2 = str(next_3_m)
        end_date = next_3_m2.split("-")
        Day_e = end_date[2]
        Mon_e =end_date[1]
        year_e = end_date[0]
        End_probation_date = Day_e+"-"+Mon_e+"-"+year_e
        encodedsalary = base64.b64encode(data_new['salary'])

        # sql_qry_Em = "SELECT salary,position_id,section_id,org_name_id,cost_center_name_id,company_id FROM employee WHERE employeeid=%s AND validstatus=1"
        # cursor.execute(sql_qry_Em,data_new['employeeid'])
        # columns = [column[0] for column in cursor.description]
        # result_qry_EM = toJson(cursor.fetchall(),columns)

        sql_Up_EM = "UPDATE employee SET validstatus=0 WHERE citizenid=%s"
        cursor.execute(sql_Up_EM,(result[0]['citizenid']))

        # try:
        #     sql = "SELECT employeeid FROM employee WHERE employeeid=%s AND company_id=%s"
        #     cursor.execute(sql,(data_new['employeeid'],data_new['company_id']))
        #     columns = [column[0] for column in cursor.description]
        #     result = toJson(cursor.fetchall(),columns)
        #     return "Duplicate_employeeid"
        # except Exception as e:
        #     pass

        sqlEM = "INSERT INTO employee (employeeid,citizenid,name_th,name_eng,surname_th,surname_eng,nickname_employee,salary,email,phone_company,position_id,section_id,org_name_id,cost_center_name_id,company_id,start_work,EndWork_probation,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlEM,(data_new['employeeid'],data_new['ID_CardNo'],data_new['NameTh'],data_new['NameEn'],data_new['SurnameTh'],data_new['SurnameEn'],data_new['NicknameEn'],encodedsalary,data_new['Email'],\
        data_new['phone_company'],data_new['position_id'],\
        data_new['section_id'],data_new['org_name_id'],data_new['cost_center_name_id'],data_new['company_id'],data_new['Start_contract'],End_probation_date,data_new['createby']))

        sql_Up_EM_pro = "UPDATE Emp_probation SET validstatus=0 WHERE citizenid=%s"
        cursor.execute(sql_Up_EM_pro,(result[0]['citizenid']))

        sqlEM_pro = "INSERT INTO Emp_probation (employeeid,citizenid,name_th,name_eng,surname_th,surname_eng,nickname_employee,salary,email,phone_company,position_id,section_id,org_name_id,cost_center_name_id,company_id,start_work,EndWork_probation,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlEM_pro,(data_new['employeeid'],data_new['ID_CardNo'],data_new['NameTh'],data_new['NameEn'],data_new['SurnameTh'],data_new['SurnameEn'],data_new['NicknameEn'],encodedsalary,data_new['Email'],\
        data_new['phone_company'],data_new['position_id'],\
        data_new['section_id'],data_new['org_name_id'],data_new['cost_center_name_id'],data_new['company_id'],data_new['Start_contract'],End_probation_date,data_new['createby']))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee_Personal', methods=['POST'])
@connect_sql()
def EditEmployee_Personal(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT citizenid FROM employee WHERE employeeid=%s AND validstatus=1"
        cursor.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sql_Select_Personal = "SELECT * FROM Personal WHERE ID_CardNo=%s AND validstatus=1"
        cursor.execute(sql_Select_Personal,(result[0]['citizenid']))
        columns = [column[0] for column in cursor.description]
        result_Personal = toJson(cursor.fetchall(),columns)

        sql_Up_Personal = "UPDATE Personal SET validstatus=0 WHERE ID_CardNo=%s"
        cursor.execute(sql_Up_Personal,(result[0]['citizenid']))

        date_name = str(data_new['Birthdate'])
        date_name__ = date_name.split("-")
        date_year = str(int(date_name__[2])+543)
        date_mounth = int(date_name__[1])
        if   date_mounth==1:
             Mounth_name ="มกราคม"
        elif date_mounth==2:
             Mounth_name="กุมภาพันธ์"
        elif date_mounth==3:
             Mounth_name="มีนาคม"
        elif date_mounth==4:
             Mounth_name="เมษายน"
        elif date_mounth==5:
             Mounth_name="พฤษภาคม"
        elif date_mounth==6:
             Mounth_name="มิถุนายน"
        elif date_mounth==7:
             Mounth_name="กรกฎาคม"
        elif date_mounth==8:
             Mounth_name="สิงหาคม"
        elif date_mounth==9:
             Mounth_name="กันยายน"
        elif date_mounth==10:
             Mounth_name="ตุลาคม"
        elif date_mounth==11:
             Mounth_name="พฤศจิกายน"
        else:
             Mounth_name="ธันวาคม"
        Birthdate_name = str(int(date_name__[0]))+" "+Mounth_name.decode('utf-8')+" "+date_year

        sqlIn14 = """INSERT INTO Personal (NameTh,SurnameTh,NicknameTh,NameEn,SurnameEn,NicknameEn,Birthdate,Birthdate_name,BirthPlace,BirthProvince,BirthCountry,Age,Height,Weight,BloodGroup,Citizenship,Religion,ID_CardNo,IssueDate,ExpiryDate,MaritalStatus,NumberOfChildren,StudyChild,MilitaryService,Others,Worktel,Mobile,Email,EmergencyPerson,EmergencyRelation,EmergencyAddress, \
        EmergencyTel,date)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sqlIn14,(result_Personal[0]['NameTh'],result_Personal[0]['SurnameTh'],result_Personal[0]['NicknameTh'],result_Personal[0]['NameEn'],result_Personal[0]['SurnameEn'],result_Personal[0]['NicknameEn'],data_new['Birthdate'],Birthdate_name,data_new['BirthPlace'],data_new['BirthProvince'],data_new['BirthCountry'],\
         data_new['Age'],data_new['Height'],data_new['Weight'],data_new['BloodGroup'],data_new['Citizenship'],data_new['Religion'],data_new['ID_CardNo'],data_new['IssueDate'],data_new['ExpiryDate'],data_new['MaritalStatus'],data_new['NumberOfChildren'],data_new['StudyChild'],data_new['MilitaryService'],\
         data_new['Others'],result_Personal[0]['Worktel'],result_Personal[0]['Mobile'],result_Personal[0]['Email'],result_Personal[0]['EmergencyPerson'],result_Personal[0]['EmergencyRelation'],result_Personal[0]['EmergencyAddress'],result_Personal[0]['EmergencyTel'],result_Personal[0]['date']))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee_AddressType', methods=['POST'])
@connect_sql()
def EditEmployee_AddressType(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT citizenid FROM employee WHERE employeeid=%s AND validstatus=1"
        cursor.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sql_Up_Address = "UPDATE Address SET validstatus=0 WHERE ID_CardNo=%s"
        cursor.execute(sql_Up_Address,(result[0]['citizenid']))
        if data_new['AddressTypeHome']=='Home':
            sqlIn = "INSERT INTO Address (ID_CardNo,AddressType,HouseNo,Street,DISTRICT_ID,AMPHUR_ID,PROVINCE_ID,PostCode,Tel,Fax) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn,(data_new['ID_CardNo'],data_new['AddressTypeHome'],data_new['HomeNo'],
            data_new['HomeStreet'],data_new['HomeDistrict'],data_new['HomeAmphur'],data_new['HomeProvince'],data_new['HomePostCode'],data_new['HomeTel'],data_new['HomeFax']))
        if data_new['AddressTypePresent']=='Present':
            sqlIn = "INSERT INTO Address (ID_CardNo,AddressType,HouseNo,Street,DISTRICT_ID,AMPHUR_ID,PROVINCE_ID,PostCode,Tel,Fax) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn,(data_new['ID_CardNo'],data_new['AddressTypePresent'],data_new['PresentNo'],
            data_new['PresentStreet'],data_new['PresentDistrict'],data_new['PresentAmphur'],data_new['PresentProvince'],data_new['PresentPostCode'],data_new['PresentTel'],data_new['PresentFax']))
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee_EmergencyContact', methods=['POST'])
@connect_sql()
def EditEmployee_EmergencyContact(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT citizenid FROM employee WHERE employeeid=%s AND validstatus=1"
        cursor.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sql_Select_Personal = "SELECT * FROM Personal WHERE ID_CardNo=%s AND validstatus=1"
        cursor.execute(sql_Select_Personal,(result[0]['citizenid']))
        columns = [column[0] for column in cursor.description]
        result_Personal = toJson(cursor.fetchall(),columns)

        sqlUp_EmerContact = "UPDATE Personal SET EmergencyPerson=%s,EmergencyRelation=%s,EmergencyAddress=%s,EmergencyTel=%s WHERE ID_CardNo=%s AND validstatus=1"
        cursor.execute(sqlUp_EmerContact,(data_new['EmergencyPerson'],data_new['EmergencyRelation'],data_new['EmergencyAddress'],data_new['EmergencyTel'],result[0]['citizenid']))
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee_ComputerSkill', methods=['POST'])
@connect_sql()
def EditEmployee_ComputerSkill(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT citizenid FROM employee WHERE employeeid=%s AND validstatus=1"
        cursor.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sqlI6de = "DELETE FROM ComputerSkill WHERE ID_CardNo=%s"
        cursor.execute(sqlI6de,result[0]['citizenid'])
        i=0
        for i in xrange(len(data_new['ComSkill'])):
            sqlIn6 = "INSERT INTO ComputerSkill (ID_CardNo,ComSkill,Level) VALUES (%s,%s,%s)"
            cursor.execute(sqlIn6,(data_new['ComSkill'][i]['ID_CardNo'],data_new['ComSkill'][i]['ComSkill'],data_new['ComSkill'][i]['Level']))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee_Education', methods=['POST'])
@connect_sql()
def EditEmployee_Education(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT citizenid FROM employee WHERE employeeid=%s AND validstatus=1"
        cursor.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sqlI9de = "DELETE FROM Education WHERE ID_CardNo=%s"
        cursor.execute(sqlI9de,result[0]['citizenid'])
        i=0
        for i in xrange(len(data_new['EducationLevel'])):
            sqlIn9 = "INSERT INTO Education (ID_CardNo,EducationLevel,Institute,StartYear,EndYear,Qualification,Major,GradeAvg,ExtraCurricularActivities) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn9,(data_new['EducationLevel'][i]['ID_CardNo'],data_new['EducationLevel'][i]['EducationLevel'],data_new['EducationLevel'][i]['Institute'],data_new['EducationLevel'][i]['StartYear'],data_new['EducationLevel'][i]['EndYear'],data_new['EducationLevel'][i]['Qualification'],\
            data_new['EducationLevel'][i]['Major'],data_new['EducationLevel'][i]['GradeAvg'],data_new['EducationLevel'][i]['ExtraCurricularActivities']))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee_Family', methods=['POST'])
@connect_sql()
def EditEmployee_Family(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT citizenid FROM employee WHERE employeeid=%s AND validstatus=1"
        cursor.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sql_Up_Family = "UPDATE Family SET validstatus=0 WHERE ID_CardNo=%s"
        cursor.execute(sql_Up_Family,(result[0]['citizenid']))

        if data_new['MemberTypeDad']=='Father':
            sqlIn = "INSERT INTO Family (ID_CardNo,MemberType,Name,Surname,Occupation,Address,Tel,Fax) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn,(data_new['ID_CardNoDad'],data_new['MemberTypeDad'],data_new['FatherName'],
            data_new['FatherSurName'],data_new['FatherJob'],data_new['FatherTel'],data_new['FatherFax'],data_new['FatherAddress']))
        if data_new['MemberTypeMom']=='Mother':
            sqlIn = "INSERT INTO Family (ID_CardNo,MemberType,Name,Surname,Occupation,Address,Tel,Fax) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn,(data_new['ID_CardNoMom'],data_new['MemberTypeMom'],data_new['MotherName'],
            data_new['MotherSurname'],data_new['MotherJob'],data_new['Mothertel'],data_new['MotherFax'],data_new['MotherAddress']))

        i=0
        for i in xrange(len(data_new['BrotherAndSister'])):
            sqlIn11 = "INSERT INTO Family (ID_CardNo,MemberType,Name,Surname,Occupation,Address,Tel,Fax) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn11,(data_new['BrotherAndSister'][i]['ID_CardNo'],data_new['BrotherAndSister'][i]['MemberType'],data_new['BrotherAndSister'][i]['BroAndSisName'],data_new['BrotherAndSister'][i]['BroAndSisSurName'],data_new['BrotherAndSister'][i]['BroAndSisJob'],\
            data_new['BrotherAndSister'][i]['BroAndSisTel'],data_new['BrotherAndSister'][i]['BroAndSisFax'],data_new['BrotherAndSister'][i]['BroAndSisAddress']))
        # i=0
        # for i in xrange(len(data_new['MemberType'])):
        #     sqlIn11 = "INSERT INTO Family (ID_CardNo,MemberType,Name,Surname,Occupation,Address,Tel,Fax) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        #     cursor.execute(sqlIn11,(data_new['MemberType'][i]['ID_CardNo'],data_new['MemberType'][i]['MemberType'],data_new['MemberType'][i]['Name'],data_new['MemberType'][i]['Surname'],data_new['MemberType'][i]['Occupation'],\
        #     data_new['MemberType'][i]['Address'],data_new['MemberType'][i]['Tel'],data_new['MemberType'][i]['Fax']))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee_LanguagesSkill', methods=['POST'])
@connect_sql()
def EditEmployee_LanguagesSkill(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT citizenid FROM employee WHERE employeeid=%s AND validstatus=1"
        cursor.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sqlI13de = "DELETE FROM LanguagesSkill WHERE ID_CardNo=%s"
        cursor.execute(sqlI13de,result[0]['citizenid'])
        i=0
        for i in xrange(len(data_new['Languages'])):
            sqlIn13 = "INSERT INTO LanguagesSkill (ID_CardNo,Languages,Speaking,Reading,Writting) VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn13,(data_new['Languages'][i]['ID_CardNo'],data_new['Languages'][i]['languageskill'],data_new['Languages'][i]['languagespeak'],data_new['Languages'][i]['languageread'],data_new['Languages'][i]['languagewrite']))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee_SpecialSkill', methods=['POST'])
@connect_sql()
def EditEmployee_SpecialSkill(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT citizenid FROM employee WHERE employeeid=%s AND validstatus=1"
        cursor.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sql_Up_SpecialSkill = "UPDATE SpecialSkill SET validstatus=0 WHERE ID_CardNo=%s"
        cursor.execute(sql_Up_SpecialSkill,(result[0]['citizenid']))

        # sqlIn20 = "INSERT INTO SpecialSkill (ID_CardNo,CarDrivingLicense,MotorBicycleDrivingLicense,OwnCar,OwnMotorBicycle,WorkUpCountry,StartWorkEarliest,PhysicalDisabilityOrDisease,DischargeFromEmployment,DischargeFromEmploymentReason,Arrested,ArrestedReason) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # cursor.execute(sqlIn20,(data_new[i]['ID_CardNo'],data_new[i]['CarDrivingLicense'],data_new[i]['MotorBicycleDrivingLicense'],data_new[i]['OwnCar'],data_new[i]['OwnMotorBicycle'], \
        # data[i]['WorkUpCountry'],data_new[i]['StartWorkEarliest'],data_new[i]['PhysicalDisabilityOrDisease'],data[i]['DischargeFromEmployment'],data_new[i]['DischargeFromEmploymentReason'],data_new[i]['Arrested'],data_new[i]['ArrestedReason']))

        sqlIn20 = "INSERT INTO SpecialSkill (ID_CardNo,CarDrivingLicense,MotorBicycleDrivingLicense,OwnCar,OwnMotorBicycle,WorkUpCountry,PhysicalDisabilityOrDisease,DischargeFromEmployment,DischargeFromEmploymentReason,Arrested,ArrestedReason) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn20,(data_new['ID_CardNo'],data_new['CarDrivingLicense'],data_new['MotorBicycleDrivingLicense'],data_new['OwnCar'],data_new['OwnMotorBicycle'], \
        data_new['WorkUpCountry'],data_new['PhysicalDisabilityOrDisease'],data_new['DischargeFromEmployment'],data_new['DischargeFromEmploymentReason'],data_new['Arrested'],data_new['ArrestedReason']))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee_Employment', methods=['POST'])
@connect_sql()
def EditEmployee_Employment(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT citizenid FROM employee WHERE employeeid=%s AND validstatus=1"
        cursor.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        try:
            sqlI10de = "DELETE FROM Employment WHERE ID_CardNo=%s"
            cursor.execute(sqlI10de,result[0]['citizenid'])
            i=0
            for i in xrange(len(data_new['CompanyName'])):
                sqlIn10 = "INSERT INTO Employment (ID_CardNo,CompanyName,CompanyAddress,PositionHeld,StartSalary,EndSalary,StartYear,EndYear,Responsibility,ReasonOfLeaving,Descriptionofwork) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn10,(data_new['CompanyName'][i]['ID_CardNo'],data_new['CompanyName'][i]['CompanyName'],data_new['CompanyName'][i]['CompanyAddress'],data_new['CompanyName'][i]['PositionHeld'],data_new['CompanyName'][i]['StartSalary'],\
                data_new['CompanyName'][i]['EndSalary'],data_new['CompanyName'][i]['StartYear'],data_new['CompanyName'][i]['EndYear'], \
                data_new['CompanyName'][i]['Responsibility'],data_new['CompanyName'][i]['ReasonOfLeaving'],data_new['CompanyName'][i]['Descriptionofwork']))
        except Exception as e:
            pass
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee_TrainingCourse', methods=['POST'])
@connect_sql()
def EditEmployee_TrainingCourse(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT citizenid FROM employee WHERE employeeid=%s AND validstatus=1"
        cursor.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        try:
            sqlI23de = "DELETE FROM TrainingCourse WHERE ID_CardNo=%s"
            cursor.execute(sqlI23de,result[0]['citizenid'])
            i=0
            for i in xrange(len(data_new['Subject'])):
                sqlIn23 = "INSERT INTO TrainingCourse(ID_CardNo,Subject,Place,StartDate,EndDate) VALUES (%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn23,(data_new['Subject'][i]['ID_CardNo'],data_new['Subject'][i]['Subject'],data_new['Subject'][i]['Place'],data_new['Subject'][i]['StartDate'],data_new['Subject'][i]['EndDate']))
        except Exception as e:
            pass
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee_Employeeid', methods=['POST'])
@connect_sql()
def EditEmployee_Employeeid(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT citizenid FROM employee WHERE employeeid=%s AND validstatus=1"
        cursor.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        try:
            sql2 = "SELECT employeeid FROM employee WHERE employeeid=%s AND company_id=%s"
            cursor.execute(sql2,(data_new['employeeid'],data_new['company_id']))
            columns = [column[0] for column in cursor.description]
            result2 = toJson(cursor.fetchall(),columns)
            employeeid__ = result2[0]['employeeid']
            return "Duplicate_employeeid"
        except Exception as e:

            insert_emp_log = "INSERT INTO employee_id_log (old_employeeid,new_employeeid,create_by) VALUES (%s,%s,%s)"
            cursor.execute(insert_emp_log,(data_new['Old_EmpId'],data_new['employeeid'],data_new['createby']))

            sqlUp = "UPDATE employee SET employeeid=%s WHERE employeeid=%s AND validstatus=1"
            cursor.execute(sqlUp,(data_new['employeeid'],data_new['Old_EmpId']))

            sqlUp_gA = "UPDATE employee_ga SET employeeid=%s WHERE employeeid=%s AND validstatus=1"
            cursor.execute(sqlUp_gA,(data_new['employeeid'],data_new['Old_EmpId']))

            sqlUp_pro = "UPDATE Emp_probation SET employeeid=%s WHERE employeeid=%s AND validstatus=1"
            cursor.execute(sqlUp_pro,(data_new['employeeid'],data_new['Old_EmpId']))
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/InsertEmployeeHRCI_Management', methods=['POST'])
@connect_sql()
def InsertEmployeeHRCI_Management(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sqlblack = "SELECT ID_CardNo FROM blacklist WHERE validstatus=1"
        cursor.execute(sqlblack)
        columnsblack = [column[0] for column in cursor.description]
        resultblacklist = toJson(cursor.fetchall(),columnsblack)
        if data_new['ID_CardNo']==resultblacklist[0]['ID_CardNo']:
            print("Person is blacklist")
        else:
            # i=0
            # for i in xrange(len(data_new['AddressType'])):
            #     sqlIn = "INSERT INTO Address (ID_CardNo,AddressType,HouseNo,Street,DISTRICT_ID,AMPHUR_ID,PROVINCE_ID,PostCode,Tel,Fax) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            #     cursor.execute(sqlIn,(data_new[i]['ID_CardNo'],data_new[i]['AddressType'],data_new[i]['HouseNo'],
            #     data_new[i]['Street'],data_new[i]['DISTRICT_NAME'],data_new[i]['AMPHUR_NAME'],data_new[i]['PROVINCE_NAME'],data_new[i]['PostCode'],data_new[i]['Tel'],data_new[i]['Fax']))
            if data_new['AddressTypeHome']=='Home':
                sqlIn = "INSERT INTO Address (ID_CardNo,AddressType,HouseNo,Street,DISTRICT_ID,AMPHUR_ID,PROVINCE_ID,PostCode,Tel,Fax) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn,(data_new['ID_CardNo'],data_new['AddressTypeHome'],data_new['AddressHome'],
                data_new['StreetHome'],data_new['SubdistrictHome'],data_new['DistrictHome'],data_new['ProvinceHome'],data_new['PostalcodeHome'],data_new['PhoneHome'],data_new['FaxHome']))
            if data_new['AddressTypePresent']=='Present':
                sqlIn = "INSERT INTO Address (ID_CardNo,AddressType,HouseNo,Street,DISTRICT_ID,AMPHUR_ID,PROVINCE_ID,PostCode,Tel,Fax) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn,(data_new['ID_CardNo'],data_new['AddressTypePresent'],data_new['AddressPresent'],
                data_new['StreetPresent'],data_new['SubDistrictPresent'],data_new['DistrictPresent'],data_new['ProvincePresent'],data_new['PostalCodePresent'],data_new['PhonePresent'],data_new['FaxPresent']))

            i=0
            for i in xrange(len(data_new['ComSkill'])):
                sqlIn6 = "INSERT INTO ComputerSkill (ID_CardNo,ComSkill,Level) VALUES (%s,%s,%s)"
                cursor.execute(sqlIn6,(data_new['ComSkill'][i]['ID_CardNo'],data_new['ComSkill'][i]['SkillCom'],data_new['ComSkill'][i]['LevelCom']))

            # for dataSkillcomputer in data_new['ComSkill']:
            #     sqlIn6 = "INSERT INTO ComputerSkill (ID_CardNo,ComSkill,Level) VALUES (%s,%s,%s)"
            #     cursor.execute(sqlIn6,(dataSkillcomputer['ID_CardNo'],dataSkillcomputer['SkillCom'],dataSkillcomputer['LevelCom']))
            i=0
            for i in xrange(len(data_new['EducationLevel'])):
                sqlIn9 = "INSERT INTO Education (ID_CardNo,EducationLevel,Institute,StartYear,EndYear,Qualification,Major,GradeAvg,ExtraCurricularActivities) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn9,(data_new['EducationLevel'][i]['ID_CardNo'],data_new['EducationLevel'][i]['edulevel'],data_new['EducationLevel'][i]['eduName'],data_new['EducationLevel'][i]['eduStartyear'],data_new['EducationLevel'][i]['eduEndyear'], \
                data_new['EducationLevel'][i]['eduQua'],data_new['EducationLevel'][i]['edumajor'],data_new['EducationLevel'][i]['edugpa'],\
                data_new['EducationLevel'][i]['eduActivities']))

            if data_new['MemberTypeDad']=='Father':
                sqlIn = "INSERT INTO Family (ID_CardNo,MemberType,Name,Surname,Occupation,Address,Tel,Fax) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn,(data_new['ID_CardNoDad'],data_new['MemberTypeDad'],data_new['FatherName'],
                data_new['FatherSurName'],data_new['FatherJob'],data_new['FatherTel'],data_new['FatherFax'],data_new['FatherAddress']))
            if data_new['MemberTypeMom']=='Mother':
                sqlIn = "INSERT INTO Family (ID_CardNo,MemberType,Name,Surname,Occupation,Address,Tel,Fax) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn,(data_new['ID_CardNoMom'],data_new['MemberTypeMom'],data_new['MotherName'],
                data_new['MotherSurname'],data_new['MotherJob'],data_new['Mothertel'],data_new['MotherFax'],data_new['MotherAddress']))

            i=0
            for i in xrange(len(data_new['BrotherAndSister'])):
                sqlIn11 = "INSERT INTO Family (ID_CardNo,MemberType,Name,Surname,Occupation,Address,Tel,Fax) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn11,(data_new['BrotherAndSister'][i]['ID_CardNo'],data_new['BrotherAndSister'][i]['MemberType'],data_new['BrotherAndSister'][i]['BroAndSisName'],data_new['BrotherAndSister'][i]['BroAndSisSurName'],data_new['BrotherAndSister'][i]['BroAndSisJob'],\
                data_new['BrotherAndSister'][i]['BroAndSisTel'],data_new['BrotherAndSister'][i]['BroAndSisFax'],data_new['BrotherAndSister'][i]['BroAndSisAddress']))
            # i=0
            # for i in xrange(len(data_new['MemberType'])):
            #     sqlIn11 = "INSERT INTO Family (ID_CardNo,MemberType,Name,Surname,Occupation,Address,Tel,Fax) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            #     cursor.execute(sqlIn11,(data_new['MemberType'][i]['ID_CardNo'],data_ne['MemberType'][i]['MemberType'],data_new['MemberType'][i]['Name'],data_new['MemberType'][i]['Surname'],data_new['MemberType'][i]['Occupation'], \
            #     data_new['MemberType'][i]['Address'],data_new['MemberType'][i]['Tel'],data_new['MemberType'][i]['Fax']))

            i=0
            for i in xrange(len(data_new['Languages'])):
                sqlIn13 = "INSERT INTO LanguagesSkill (ID_CardNo,Languages,Speaking,Reading,Writting) VALUES (%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn13,(data_new['Languages'][i]['ID_CardNo'],data_new['Languages'][i]['languageskill'],data_new['Languages'][i]['languagespeak'],data_new['Languages'][i]['languageread'],data_new['Languages'][i]['languagewrite']))

            date_name = str(data_new['Birthdate'])
            date_name__ = date_name.split("-")
            date_year = str(int(date_name__[2])+543)
            date_mounth = int(date_name__[1])
            if   date_mounth==1:
                 Mounth_name ="มกราคม"
            elif date_mounth==2:
                 Mounth_name="กุมภาพันธ์"
            elif date_mounth==3:
                 Mounth_name="มีนาคม"
            elif date_mounth==4:
                 Mounth_name="เมษายน"
            elif date_mounth==5:
                 Mounth_name="พฤษภาคม"
            elif date_mounth==6:
                 Mounth_name="มิถุนายน"
            elif date_mounth==7:
                 Mounth_name="กรกฎาคม"
            elif date_mounth==8:
                 Mounth_name="สิงหาคม"
            elif date_mounth==9:
                 Mounth_name="กันยายน"
            elif date_mounth==10:
                 Mounth_name="ตุลาคม"
            elif date_mounth==11:
                 Mounth_name="พฤศจิกายน"
            else:
                 Mounth_name="ธันวาคม"
            Birthdate_name = str(int(date_name__[0]))+" "+Mounth_name.decode('utf-8')+" "+date_year

            sqlIn14 = """INSERT INTO Personal (NameTh,SurnameTh,NicknameTh,NameEn,SurnameEn,NicknameEn,Birthdate,Birthdate_name,BirthPlace,BirthProvince,BirthCountry,Age,Height,Weight,BloodGroup,Citizenship,Religion,ID_CardNo,IssueDate,ExpiryDate,MaritalStatus,NumberOfChildren,StudyChild,MilitaryService,Others,Worktel,Mobile,Email,EmergencyPerson,EmergencyRelation,EmergencyAddress,EmergencyTel) \
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(sqlIn14,(data_new['NameTh'],data_new['SurnameTh'],data_new['NicknameTh'],data_new['NameEn'],\
            data_new['SurnameEn'],data_new['NicknameEn'],data_new['Birthdate'],Birthdate_name,data_new['BirthPlace'],data_new['BirthProvince'], \
            data_new['BirthCountry'],data_new['Age'],data_new['Height'],data_new['Weight'],data_new['BloodGroup'],data_new['Citizenship'],data_new['Religion'],data_new['ID_CardNo'], \
            data_new['IssueDate'],data_new['ExpiryDate'],data_new['MaritalStatus'],data_new['NumberOfChildren'],data_new['StudyChild'],data_new['MilitaryService'],data_new['other'], \
            data_new['phone_company'],data_new['Mobile'],data_new['email'],data_new['EmergencyPerson'],data_new['EmergencyRelation'],data_new['EmergencyAddress'],data_new['EmergencyTel']))
            # i=0
            # for i in xrange(len(data_new['RelativeName'])):
            #     sqlIn17 = "INSERT INTO Reference (ID_CardNo,RelativeName,RelativeSurname,RelativePosition,RelativeRelationship,PhysicalHandicap,PhysicalHandicapDetail,KnowFrom) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            #     cursor.execute(sqlIn17,(data_new['RelativeName'][i]['ID_CardNo'],data_new['RelativeName'][i]['RelativeName'],data_new['RelativeName'][i]['RelativeSurname'],data_new['RelativeName'][i]['RelativePosition'],data_new['RelativeName'][i]['RelativeRelationship'],data_new['RelativeName'][i]['PhysicalHandicap'],\
            #     data_new['RelativeName'][i]['PhysicalHandicapDetail'],data_new['RelativeName'][i]['KnowFrom']))
            # i=0
            # for i in xrange(len(data_new['RefName'])):
            #     sqlIn18 = "INSERT INTO RefPerson (ID_CardNo,RefName,RefPosition,RefAddress,RefTel) VALUES (%s,%s,%s,%s,%s)"
            #     cursor.execute(sqlIn18,(data_new['RefName'][i]['ID_CardNo'],data_new['RefName'][i]['RefName'],data_new['RefName'][i]['RefPosition'],data_new['RefName'][i]['RefAddress'],data_new['RefName'][i]['RefTel']))
            # WorkUpCountry ='ไม่ขัดข้อง'
            # StartWorkEarliest = 'test'
            sqlIn20 = "INSERT INTO SpecialSkill (ID_CardNo,CarDrivingLicense,MotorBicycleDrivingLicense,OwnCar,OwnMotorBicycle,WorkUpCountry,StartWorkEarliest,PhysicalDisabilityOrDisease,DischargeFromEmployment,DischargeFromEmploymentReason,Arrested,ArrestedReason) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn20,(data_new['ID_CardNo'],data_new['CarDrivingLicense'],data_new['MotorBicycleDrivingLicense'],data_new['OwnCar'],data_new['OwnMotorBicycle'], \
            data_new['WorkUpCountry'],data_new['StartWorkEarliest'],data_new['PhysicalDisabilityOrDisease'],data_new['DischargeFromEmployment'],data_new['DischargeFromEmploymentReason'],data_new['Arrested'],data_new['ArrestedReason']))
            try:
                i=0
                for i in xrange(len(data_new['CompanyName'])):
                    sqlIn10 = "INSERT INTO Employment (ID_CardNo,CompanyName,CompanyAddress,PositionHeld,StartSalary,EndSalary,StartYear,EndYear,Responsibility,ReasonOfLeaving,Descriptionofwork) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sqlIn10,(data_new['CompanyName'][i]['ID_CardNo'],data_new['CompanyName'][i]['CompanyName'],data_new['CompanyName'][i]['CompanyAddress'],data_new['CompanyName'][i]['PositionHeld'],data_new['CompanyName'][i]['StartSalary'],data_new['CompanyName'][i]['EndSalary'], \
                    data_new['CompanyName'][i]['StartYear'],data_new['CompanyName'][i]['EndYear'], \
                    data_new['CompanyName'][i]['Responsibility'],data_new['CompanyName'][i]['ReasonOfLeaving'],data_new['CompanyName'][i]['Descriptionofwork']))
            except Exception as e:
                logserver(e)
            try:
                i=0
                for i in xrange(len(data_new['Subject'])):
                    sqlIn23 = "INSERT INTO TrainingCourse(ID_CardNo,Subject,Place,StartDate,EndDate) VALUES (%s,%s,%s,%s,%s)"
                    cursor.execute(sqlIn23,(data_new['Subject'][i]['ID_CardNo'],data_new['Subject'][i]['Subject'],data_new['Subject'][i]['Place'],data_new['Subject'][i]['StartDate'],data_new['Subject'][i]['EndDate']))
            except Exception as e:
                logserver(e)

            date1 = data_new['Start_contract']
            star_date = date1.split("-")
            Day_s = int(star_date[0])
            Mon_s =int(star_date[1])
            year_s = int(star_date[2])
            next_3_m = date(year_s,Mon_s,Day_s) + relativedelta(days=89)
            next_3_m2 = str(next_3_m)
            end_date = next_3_m2.split("-")
            Day_e = end_date[2]
            Mon_e =end_date[1]
            year_e = end_date[0]
            End_probation_date = Day_e+"-"+Mon_e+"-"+year_e

            # salary ='15000'
            encodedsalary = base64.b64encode(data_new['Salary'])
            sqlEM = "INSERT INTO employee (employeeid,citizenid,name_th,name_eng,surname_th,surname_eng,nickname_employee,salary,email,phone_company,position_id,section_id,org_name_id,cost_center_name_id,company_id,start_work,EndWork_probation,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlEM,(data_new['employeeid'],data_new['ID_CardNo'],data_new['NameTh'],data_new['NameEn'],data_new['SurnameTh'],data_new['SurnameEn'],data_new['NicknameEn'],encodedsalary,data_new['email'],\
            data_new['phone_company'],data_new['position_id'],\
            data_new['sect_id'],data_new['org_name_id'],data_new['cost_center_name_id'],data_new['companyid'],data_new['Start_contract'],End_probation_date,data_new['createby']))

            sqlEm_ga = "INSERT INTO employee_ga (employeeid,citizenid,phone_depreciate,notebook_depreciate,limit_phone,chair_table,pc,notebook,office_equipment,ms,car_ticket,band_car,color,regis_car_number,other,description,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlEm_ga,(data_new['employeeid'],data_new['ID_CardNo'],data_new['phone_depreciate'],data_new['notebook_depreciate'],data_new['limit_phone'],data_new['chair_table'],data_new['pc'],data_new['notebook'],data_new['office_equipment'],\
            data_new['ms'],data_new['car_ticket'],data_new['band_car'],data_new['color'],\
            data_new['regis_car_number'],data_new['other'],data_new['description'],data_new['createby']))

            sqlEM_pro = "INSERT INTO Emp_probation (employeeid,citizenid,name_th,name_eng,surname_th,surname_eng,nickname_employee,salary,email,phone_company,position_id,section_id,org_name_id,cost_center_name_id,company_id,start_work,EndWork_probation,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlEM_pro,(data_new['employeeid'],data_new['ID_CardNo'],data_new['NameTh'],data_new['NameEn'],data_new['SurnameTh'],data_new['SurnameEn'],data_new['NicknameEn'],encodedsalary,\
            data_new['email'],data_new['phone_company'],data_new['position_id'],\
            data_new['sect_id'],data_new['org_name_id'],data_new['cost_center_name_id'],data_new['companyid'],data_new['Start_contract'],End_probation_date,data_new['createby']))
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Insert_img_employee', methods=['POST'])
@connect_sql()
def Insert_img_employee(cursor):
    try:
        sqlQry = "SELECT citizenid FROM employee WHERE employeeid=%s AND validstatus=1"
        cursor.execute(sqlQry,request.form['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        currentTime = datetime.today().strftime('%Y%m%d%H%M%S%f')
        path = 'uploads/employee/' + request.form['employeeid']
        path2 = request.form['employeeid']
        if not os.path.exists(path):
            os.makedirs(path)
        if request.method == 'POST':
            file = request.files['file']
        if file:
            file.save(os.path.join(path, currentTime + '_employee_img.png'))
            path_image = path2+'/'+currentTime+'_employee_img.png'
        else:
            return 'file is not allowed'
        sql = "INSERT INTO Attachment(ID_CardNo,Type,PathFile) VALUES (%s,%s,%s)"
        cursor.execute(sql,(result['citizenid'],request.form['Type'],path_image))
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qry_type_image', methods=['POST'])
@connect_sql()
def Qry_type_image(cursor):
    try:
        sql = "SELECT * FROM Type_upload_image"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Export_Employee_by_month', methods=['POST'])
@connect_sql()
def Export_Employee_by_month(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        year=str(data_new['year'])
        month=str(data_new['month'])
        companyid=str(data_new['companyid'])
        try:
            sql = """SELECT employee.employeeid,employee.name_th,employee.surname_th,employee.name_eng,employee.surname_eng,employee.nickname_employee,employee.email,employee.start_work,Personal.Mobile,position.position_detail,section.sect_detail,org_name.org_name_detail,cost_center_name.cost_detail,company.companyname FROM employee LEFT JOIN company ON company.companyid = employee.company_id\
                                          LEFT JOIN position ON position.position_id = employee.position_id\
                                          LEFT JOIN section ON section.sect_id = employee.section_id\
                                          LEFT JOIN org_name ON org_name.org_name_id = employee.org_name_id\
                                          LEFT JOIN cost_center_name ON cost_center_name.cost_center_name_id = employee.cost_center_name_id\
                                          LEFT JOIN Personal ON Personal.ID_CardNo = employee.citizenid\
                                          LEFT JOIN status ON status.status_id = employee.validstatus\
            WHERE employee.validstatus=1 AND company.validstatus=1 AND position.validstatus=1 AND section.validstatus=1 AND org_name.validstatus=1 AND cost_center_name.validstatus=1 AND status.validstatus=1 AND Personal.validstatus=1 AND \
            employee.start_work LIKE '%""" + month + """-""" + year + """' AND employee.company_id='"""+companyid +"""'"""
            cursor.execute(sql)
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
        filename_tmp = secure_filename('{}_{}'.format(datetimeStr, 'Template_Employee_by.xlsx'))

        wb = load_workbook('../app/Template/Template_Employee_by.xlsx')
        if len(result) > 0:

            sheet = wb['Sheet1']
            sheet['B'+str(3)] = year + '/' + month
            sheet['C'+str(3)] = companyname_
            offset = 6
            i = 0
            for i in xrange(len(result)):
                sheet['A'+str(offset + i)] = result[i]['employeeid']
                sheet['B'+str(offset + i)] = result[i]['name_th'] + ' ' + result[i]['surname_th']
                sheet['C'+str(offset + i)] =  result[i]['name_eng'] + ' ' + result[i]['surname_eng']
                sheet['D'+str(offset + i)] = result[i]['nickname_employee']
                sheet['E'+str(offset + i)] = result[i]['email']
                sheet['F'+str(offset + i)] = result[i]['position_detail']
                sheet['G'+str(offset + i)] = result[i]['sect_detail']
                sheet['H'+str(offset + i)] = result[i]['org_name_detail']
                sheet['I'+str(offset + i)] = result[i]['cost_detail']
                sheet['J'+str(offset + i)] = result[i]['Mobile']
                sheet['K'+str(offset + i)] = result[i]['start_work']
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
@app.route('/Qry_Employee_by_month', methods=['POST'])
@connect_sql()
def Qry_Employee_by_month(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        year=str(data_new['year'])
        month=str(data_new['month'])
        companyid=str(data_new['companyid'])
        sql = """SELECT employee.employeeid,employee.name_th,employee.surname_th,employee.name_eng,employee.surname_eng,employee.nickname_employee,employee.email,\
        employee.start_work,employee.validstatus,Personal.Mobile,position.position_detail,section.sect_detail,org_name.org_name_detail,cost_center_name.cost_detail,company.company_short_name,status.path_color,status.font_color,status.status_detail FROM employee LEFT JOIN company ON company.companyid = employee.company_id\
                                      LEFT JOIN position ON position.position_id = employee.position_id\
                                      LEFT JOIN section ON section.sect_id = employee.section_id\
                                      LEFT JOIN org_name ON org_name.org_name_id = employee.org_name_id\
                                      LEFT JOIN cost_center_name ON cost_center_name.cost_center_name_id = employee.cost_center_name_id\
                                      LEFT JOIN Personal ON Personal.ID_CardNo = employee.citizenid\
                                      LEFT JOIN status ON status.status_id = employee.validstatus\
        WHERE employee.validstatus=1 AND company.validstatus=1 AND position.validstatus=1 AND section.validstatus=1 AND org_name.validstatus=1 AND cost_center_name.validstatus=1 AND status.validstatus=1 AND Personal.validstatus=1 AND \
        employee.start_work LIKE '%""" + month + """-""" + year + """' AND employee.company_id='"""+companyid +"""'"""
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Export_Employee_All_company', methods=['POST'])
@connect_sql()
def Export_Employee_All_company(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        year=str(data_new['year'])
        month=str(data_new['month'])
        try:
            sql = """SELECT employee.employeeid,employee.name_th,employee.surname_th,employee.name_eng,employee.surname_eng,employee.nickname_employee,employee.email,employee.start_work,Personal.Mobile,position.position_detail,section.sect_detail,org_name.org_name_detail,cost_center_name.cost_detail,company.company_short_name FROM employee LEFT JOIN company ON company.companyid = employee.company_id\
                                          LEFT JOIN position ON position.position_id = employee.position_id\
                                          LEFT JOIN section ON section.sect_id = employee.section_id\
                                          LEFT JOIN org_name ON org_name.org_name_id = employee.org_name_id\
                                          LEFT JOIN cost_center_name ON cost_center_name.cost_center_name_id = employee.cost_center_name_id\
                                          LEFT JOIN Personal ON Personal.ID_CardNo = employee.citizenid\
                                          LEFT JOIN status ON status.status_id = employee.validstatus\
            WHERE employee.validstatus=1 AND company.validstatus=1 AND position.validstatus=1 AND section.validstatus=1 AND org_name.validstatus=1 AND cost_center_name.validstatus=1 AND status.validstatus=1 AND Personal.validstatus=1 AND \
            employee.start_work LIKE '%""" + month + """-""" + year + """'"""
            cursor.execute(sql)
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
        filename_tmp = secure_filename('{}_{}'.format(datetimeStr, 'Template_Employee_All.xlsx'))

        wb = load_workbook('../app/Template/Template_Employee_All.xlsx')
        if len(result) > 0:

            sheet = wb['Sheet1']
            sheet['C'+str(3)] = year + '/' + month
            offset = 6
            i = 0
            for i in xrange(len(result)):
                sheet['A'+str(offset + i)] = result[i]['company_short_name']
                sheet['B'+str(offset + i)] = result[i]['employeeid']
                sheet['C'+str(offset + i)] = result[i]['name_th'] + ' ' + result[i]['surname_th']
                sheet['D'+str(offset + i)] =  result[i]['name_eng'] + ' ' + result[i]['surname_eng']
                sheet['E'+str(offset + i)] = result[i]['nickname_employee']
                sheet['F'+str(offset + i)] = result[i]['email']
                sheet['G'+str(offset + i)] = result[i]['position_detail']
                sheet['H'+str(offset + i)] = result[i]['sect_detail']
                sheet['I'+str(offset + i)] = result[i]['org_name_detail']
                sheet['J'+str(offset + i)] = result[i]['cost_detail']
                sheet['K'+str(offset + i)] = result[i]['Mobile']
                sheet['L'+str(offset + i)] = result[i]['start_work']
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
@app.route('/Qry_Province', methods=['POST'])
@connect_sql3()
def Qry_Province(cursor3):
    try:
        sql = "SELECT PROVINCE_ID, PROVINCE_NAME FROM provinces ORDER BY PROVINCE_NAME ASC"
        cursor3.execute(sql)
        columns = [column[0] for column in cursor3.description]
        result = toJson(cursor3.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qry_Al_Amphurs', methods=['POST'])
@connect_sql3()
def Qry_Al_Amphurs(cursor3):
    try:
        sql = "SELECT AMPHUR_ID, AMPHUR_NAME FROM amphures ORDER BY AMPHUR_NAME ASC"
        cursor3.execute(sql)
        columns = [column[0] for column in cursor3.description]
        result = toJson(cursor3.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qry_Al_Districts', methods=['POST'])
@connect_sql3()
def Qry_Al_Districts(cursor3):
    try:
        sql = "SELECT DISTRICT_NAME FROM districts ORDER BY DISTRICT_NAME ASC"
        cursor3.execute(sql)
        columns = [column[0] for column in cursor3.description]
        result = toJson(cursor3.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qry_Amphurs', methods=['POST'])
@connect_sql3()
def Qry_Amphurs(cursor3):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT AMPHUR_ID, AMPHUR_NAME FROM amphures WHERE PROVINCE_ID=%s ORDER BY AMPHUR_NAME ASC"
        cursor3.execute(sql,data_new['PROVINCE_ID'])
        columns = [column[0] for column in cursor3.description]
        result = toJson(cursor3.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qry_Districts', methods=['POST'])
@connect_sql3()
def Qry_Districts(cursor3):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT DISTRICT_NAME FROM districts WHERE AMPHUR_ID=%s ORDER BY DISTRICT_NAME ASC"
        cursor3.execute(sql,data_new['AMPHUR_ID'])
        columns = [column[0] for column in cursor3.description]
        result = toJson(cursor3.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Edit_Employee_GA', methods=['POST'])
@connect_sql()
def Edit_Employee_GA(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT citizenid,benefits_id,benefits_values FROM employee_benefits WHERE employee_benefits=%s"
        cursor.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        i=0
        for i in xrange(len(result)):
            sqlIn = "INSERT INTO employee_benefits_log (employeeid,citizenid,benefits_id,benefits_values,createby) VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn,(data_new['employeeid'],result[i]['citizenid'],result[i]['benefits_id'],result[i]['benefits_values'],data_new['createby']))

        sqlde = "DELETE FROM employee_benefits WHERE employeeid=%s"
        cursor.execute(sqlde,(data_new['employeeid']))

        i=0
        for i in xrange(len(result)):
            sqlIn = "INSERT INTO employee_benefits(employeeid,citizenid,benefits_id,benefits_values,createby) VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn,(data_new['employeeid'],data_new[i]['citizenid'],data_new[i]['benefits_id'],data_new[i]['benefits_values'],data_new['createby']))
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qry_Employee_GA', methods=['POST'])
@connect_sql()
def Qry_Employee_GA(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT benefits.benefits_detail,employee_benefits.benefits_values FROM employee_benefits LEFT JOIN benefits ON employee_benefits.benefits_id = benefits.benefits_id \
         WHERE employee_benefits.employeeid=%s AND benefits.validstatus = 1"
        cursor.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
