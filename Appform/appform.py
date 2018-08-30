#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/QryAppform', methods=['POST'])
def QryAppform():
    try:
        connection = mysql3.connect()
        cursor = connection.cursor()
        sql = """SELECT Personal.EmploymentAppNo, Personal.ID_CardNo, Personal.AppliedPosition1, Personal.AppliedPosition2, Personal.StartExpectedSalary, Personal.EndExpectedSalary, Personal.NameTh, Personal.SurnameTh, Personal.Mobile, Personal.Email, Personal.date, status_hrci.status_detail, status_hrci.status_id, status_hrci.path_color, status_hrci.font_color
        FROM Personal INNER JOIN status_hrci ON Personal.status_id_hrci = status_hrci.status_id WHERE status_hrci.validstatus = 1 ORDER BY Personal.EmploymentAppNo DESC"""
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        connection.close()
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryBlacklist', methods=['POST'])
@connect_sql()
def QryBlacklist(cursor):
    try:
        sql = "SELECT * FROM blacklist WHERE validstatus=1"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/InsertBlacklist', methods=['POST'])
def InsertBlacklist():
    try:
        connection = mysql3.connect()
        cursor = connection.cursor()
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT NameTh,SurnameTh,ID_CardNo,Mobile FROM Personal WHERE EmploymentAppNo=%s"
        cursor.execute(sql,data_new['EmploymentAppNo'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        connection.commit()
        connection.close()

        connection = mysql.connect()
        cursor = connection.cursor()
        sqlIn4 = "INSERT INTO blacklist (ID_CardNo,NameTh,SurnameTh,Mobile,createby,Description) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn4,(result[0]['ID_CardNo'],result[0]['NameTh'],result[0]['SurnameTh'],result[0]['Mobile'],data_new['createby'],data_new['Descriptions']))

        sqlemployee = "DELETE FROM employee WHERE citizenid=%s"
        cursor.execute(sqlemployee,result[0]['ID_CardNo'])

        sqlemployee_ga = "DELETE FROM employee_ga WHERE citizenid=%s"
        cursor.execute(sqlemployee_ga,result[0]['ID_CardNo'])

        sqlEmp_pro = "DELETE FROM Emp_probation WHERE citizenid=%s"
        cursor.execute(sqlEmp_pro,result[0]['ID_CardNo'])
        connection.commit()
        connection.close()
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/InsertBlacklist_Appform', methods=['POST'])
def InsertBlacklist_Appform():
    try:
        connection = mysql3.connect()
        cursor = connection.cursor()
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT NameTh,SurnameTh,ID_CardNo,Mobile FROM Personal WHERE EmploymentAppNo=%s"
        cursor.execute(sql,data_new['EmploymentAppNo'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sqlUp = "UPDATE Personal SET status_id_hrci=5 WHERE EmploymentAppNo=%s"
        cursor.execute(sqlUp,data_new['EmploymentAppNo'])
        connection.commit()
        connection.close()

        connection = mysql.connect()
        cursor = connection.cursor()
        sqlIn4 = "INSERT INTO blacklist (ID_CardNo,NameTh,SurnameTh,Mobile,createby,Description) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn4,(result[0]['ID_CardNo'],result[0]['NameTh'],result[0]['SurnameTh'],result[0]['Mobile'],data_new['createby'],data_new['Descriptions']))

        sqlIn4 = "INSERT INTO Update_statusAppform_log (EmploymentAppNo,status_id,create_by) VALUES (%s,%s,%s)"
        cursor.execute(sqlIn4,(data['EmploymentAppNo'],data['status_id'],data['create_by']))

        connection.commit()
        connection.close()
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/DeleteBlacklist', methods=['POST'])
def DeleteBlacklist():
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sqlUp = "UPDATE blacklist SET validstatus=0,createby=%s WHERE ID_CardNo=%s"
        cursor3.execute(sqlUp,(data_new['createby'],data_new['ID_CardNo']))
        connection.commit()
        connection.close()
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryAppform_by_status', methods=['POST'])
def QryAppform_by_status():
    try:
        connection = mysql3.connect()
        cursor = connection.cursor()
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = """SELECT Personal.EmploymentAppNo, Personal.AppliedPosition1, Personal.AppliedPosition2, Personal.StartExpectedSalary, Personal.EndExpectedSalary, Personal.NameTh, Personal.SurnameTh, Personal.Mobile, Personal.Email, Personal.date, status_hrci.status_detail, status_hrci.font_color, status_hrci.path_color
        FROM Personal INNER JOIN status_hrci ON Personal.status_id_hrci = status_hrci.status_id WHERE status_hrci.status_id=%s AND status_hrci.validstatus = 1 ORDER BY Personal.EmploymentAppNo DESC"""
        cursor.execute(sql,data_new['status_id'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        connection.close()
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"

@app.route('/UpdateEmpStatus', methods=['POST'])
def UpdateEmpStatus():
    try:
        data = request.json
        # source = data['source']
        # data_new = source
        status_id = data['status_id']
        EmploymentAppNo = data['EmploymentAppNo']

        connection = mysql3.connect()
        cursor = connection.cursor()
        sqlqryIDcard = "SELECT ID_CardNo FROM Personal WHERE EmploymentAppNo=%s"
        cursor.execute(sqlqryIDcard,EmploymentAppNo)
        columnsIDcard = [column[0] for column in cursor.description]
        resultIDcard = toJson(cursor.fetchall(),columnsIDcard)
        connection.commit()
        connection.close()
        try:
            connection = mysql.connect()
            cursor = connection.cursor()
            sqlblack = "SELECT ID_CardNo FROM blacklist WHERE ID_CardNo=%s AND validstatus=1"
            cursor.execute(sqlblack,resultIDcard[0]['ID_CardNo'])
            columnsblack = [column[0] for column in cursor.description]
            resultblacklist = toJson(cursor.fetchall(),columnsblack)
            connection.commit()
            connection.close()

            if len(resultblacklist) != 0:
               connection = mysql3.connect()
               cursor = connection.cursor()
               sqlUp = "UPDATE Personal SET status_id_hrci=5 WHERE EmploymentAppNo=%s"
               cursor.execute(sqlUp,EmploymentAppNo)
               connection.commit()
               connection.close()
               return "Blacklist"
            else:
               connection = mysql3.connect()
               cursor = connection.cursor()
               sqlUp = "UPDATE Personal SET status_id_hrci = %s WHERE EmploymentAppNo = %s"
               cursor.execute(sqlUp,(status_id, EmploymentAppNo))
               connection.commit()
               connection.close()

               connection = mysql.connect()
               cursor = connection.cursor()
               sqlIn4 = "INSERT INTO Update_statusAppform_log (EmploymentAppNo,status_id,create_by) VALUES (%s,%s,%s)"
               cursor.execute(sqlIn4,(data['EmploymentAppNo'],data['status_id'],data['create_by']))
               connection.commit()
               connection.close()
               return "Success"
        except Exception as e:
            logserver(e)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryDatbaseAppform', methods=['POST'])
def QryDatbaseAppform():
    try:
        connection = mysql3.connect()
        cursor = connection.cursor()
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sqlEm = "SELECT * FROM Address INNER JOIN provinces ON provinces.PROVINCE_ID=Address.PROVINCE_ID \
                                       INNER JOIN amphures ON amphures.AMPHUR_ID=Address.AMPHUR_ID \
                                       INNER JOIN districts ON districts.DISTRICT_CODE=Address.DISTRICT_ID \
                                       INNER JOIN Personal ON Personal.EmploymentAppNo=Address.EmploymentAppNo \
                 WHERE Personal.EmploymentAppNo=%s"
        cursor.execute(sqlEm,data_new['EmploymentAppNo'])
        columnsEm = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columnsEm)

        sql4 = "SELECT * FROM Attachment INNER JOIN Personal ON Personal.EmploymentAppNo=Attachment.EmploymentAppNo \
         WHERE Personal.EmploymentAppNo=%s"
        cursor.execute(sql4,data_new['EmploymentAppNo'])
        columns4 = [column[0] for column in cursor.description]
        result4 = toJson(cursor.fetchall(),columns4)

        sql6 = "SELECT * FROM ComputerSkill INNER JOIN Personal ON Personal.EmploymentAppNo=ComputerSkill.EmploymentAppNo \
        WHERE Personal.EmploymentAppNo=%s"
        cursor.execute(sql6,data_new['EmploymentAppNo'])
        columns6 = [column[0] for column in cursor.description]
        result6 = toJson(cursor.fetchall(),columns6)

        sql9 = "SELECT * FROM Education INNER JOIN Personal ON Personal.EmploymentAppNo=Education.EmploymentAppNo \
        WHERE Personal.EmploymentAppNo=%s"
        cursor.execute(sql9,data_new['EmploymentAppNo'])
        columns9 = [column[0] for column in cursor.description]
        result9 = toJson(cursor.fetchall(),columns9)

        sql10 = "SELECT * FROM Employment INNER JOIN Personal ON Personal.EmploymentAppNo=Employment.EmploymentAppNo \
        WHERE Personal.EmploymentAppNo=%s"
        cursor.execute(sql10,data_new['EmploymentAppNo'])
        columns10 = [column[0] for column in cursor.description]
        result10 = toJson(cursor.fetchall(),columns10)

        sql11 = "SELECT * FROM Family INNER JOIN Personal ON Personal.EmploymentAppNo=Family.EmploymentAppNo \
        WHERE Personal.EmploymentAppNo=%s"
        cursor.execute(sql11,data_new['EmploymentAppNo'])
        columns11 = [column[0] for column in cursor.description]
        result11 = toJson(cursor.fetchall(),columns11)

        sql13 = "SELECT * FROM LanguagesSkill INNER JOIN Personal ON Personal.EmploymentAppNo=LanguagesSkill.EmploymentAppNo \
        WHERE Personal.EmploymentAppNo=%s"
        cursor.execute(sql13,data_new['EmploymentAppNo'])
        columns13 = [column[0] for column in cursor.description]
        result13 = toJson(cursor.fetchall(),columns13)

        sql14 = "SELECT * FROM Personal \
        WHERE Personal.EmploymentAppNo=%s"
        cursor.execute(sql14,data_new['EmploymentAppNo'])
        columns14 = [column[0] for column in cursor.description]
        result14 = toJson(cursor.fetchall(),columns14)

        sql17 = "SELECT * FROM Reference INNER JOIN Personal ON Personal.EmploymentAppNo=Reference.EmploymentAppNo \
        WHERE Personal.EmploymentAppNo=%s"
        cursor.execute(sql17,data_new['EmploymentAppNo'])
        columns17 = [column[0] for column in cursor.description]
        result17 = toJson(cursor.fetchall(),columns17)

        sql18 = "SELECT * FROM RefPerson INNER JOIN Personal ON Personal.EmploymentAppNo=RefPerson.EmploymentAppNo \
        WHERE Personal.EmploymentAppNo=%s"
        cursor.execute(sql18,data_new['EmploymentAppNo'])
        columns18 = [column[0] for column in cursor.description]
        result18 = toJson(cursor.fetchall(),columns18)

        sql20 = "SELECT * FROM SpecialSkill INNER JOIN Personal ON Personal.EmploymentAppNo=SpecialSkill.EmploymentAppNo \
        WHERE Personal.EmploymentAppNo=%s"
        cursor.execute(sql20,data_new['EmploymentAppNo'])
        columns20 = [column[0] for column in cursor.description]
        result20 = toJson(cursor.fetchall(),columns20)

        sql23 = "SELECT * FROM TrainingCourse INNER JOIN Personal ON Personal.EmploymentAppNo=TrainingCourse.EmploymentAppNo \
        WHERE Personal.EmploymentAppNo=%s"
        cursor.execute(sql23,data_new['EmploymentAppNo'])
        columns23 = [column[0] for column in cursor.description]
        result23 = toJson(cursor.fetchall(),columns23)
        connection.commit()
        connection.close()

        connection = mysql.connect()
        cursor = connection.cursor()
        sqlblack = "SELECT ID_CardNo FROM blacklist WHERE validstatus=1"
        cursor.execute(sqlblack)
        columnsblack = [column[0] for column in cursor.description]
        resultblacklist = toJson(cursor.fetchall(),columnsblack)
        if result14[0]['ID_CardNo']==resultblacklist[0]['ID_CardNo']:
            print("Person is blacklist")
        else:
            i=0
            for i in xrange(len(result)):
                sqlIn = "INSERT INTO Address (ID_CardNo,AddressType,HouseNo,Street,DISTRICT_ID,AMPHUR_ID,PROVINCE_ID,PostCode,Tel,Fax) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn,(result[i]['ID_CardNo'],result[i]['AddressType'],result[i]['HouseNo'],
                result[i]['Street'],result[i]['DISTRICT_NAME'],result[i]['AMPHUR_NAME'],result[i]['PROVINCE_NAME'],result[i]['PostCode'],result[i]['Tel'],result[i]['Fax']))
            try:
                i=0
                for i in xrange(len(result4)):
                    type = result4[i]['PathFile']
                    typefile = type[-4:]
                    typename = type[46:-4]
                    url = 'http://career.inet.co.th/'+result4[i]['PathFile']
                    image_name = result4[i]['EmploymentAppNo']+typename+typefile
                    Path = "pig/" + image_name
                    wget.download(url,Path)
                    sqlIn4 = "INSERT INTO Attachment (ID_CardNo,Type,PathFile) VALUES (%s,%s,%s)"
                    cursor.execute(sqlIn4,(result4[i]['ID_CardNo'],result4[i]['Type'],result4[i]['PathFile']))
            except Exception as e:
                logserver(e)
            i=0
            for i in xrange(len(result6)):
                sqlIn6 = "INSERT INTO ComputerSkill (ID_CardNo,ComSkill,Level) VALUES (%s,%s,%s)"
                cursor.execute(sqlIn6,(result6[i]['ID_CardNo'],result6[i]['ComSkill'],result6[i]['Level']))
            i=0
            for i in xrange(len(result14)):
                sqlInContract = "INSERT INTO Contract (ID_CardNo,salary_thai,Authority_Distrinct_Id_Card) VALUES (%s,%s,%s)"
                cursor.execute(sqlInContract,(result14[0]['ID_CardNo'],data_new['salary_thai'],data_new['Authority_Distrinct_Id_Card']))
            i=0
            for i in xrange(len(result9)):
                sqlIn9 = "INSERT INTO Education (ID_CardNo,EducationLevel,Institute,StartYear,EndYear,Qualification,Major,GradeAvg,ExtraCurricularActivities) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn9,(result9[i]['ID_CardNo'],result9[i]['EducationLevel'],result9[i]['Institute'],result9[i]['StartYear'],result9[i]['EndYear'],result9[i]['Qualification'],result9[i]['Major'],result9[i]['GradeAvg'],result9[i]['ExtraCurricularActivities']))
            i=0
            for i in xrange(len(result11)):
                sqlIn11 = "INSERT INTO Family (ID_CardNo,MemberType,Name,Surname,Occupation,Address,Tel,Fax) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn11,(result11[i]['ID_CardNo'],result11[i]['MemberType'],result11[i]['Name'],result11[i]['Surname'],result11[i]['Occupation'],result11[i]['Address'],result11[i]['Tel'],result11[i]['Fax']))
            i=0
            for i in xrange(len(result13)):
                sqlIn13 = "INSERT INTO LanguagesSkill (ID_CardNo,Languages,Speaking,Reading,Writting) VALUES (%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn13,(result13[i]['ID_CardNo'],result13[i]['Languages'],result13[i]['Speaking'],result13[i]['Reading'],result13[i]['Writting']))

            sqlIn14 = """INSERT INTO Personal (NameTh,SurnameTh,NicknameTh,NameEn,SurnameEn,NicknameEn,Birthdate,BirthPlace,BirthProvince,BirthCountry,Age,Height,Weight,BloodGroup,Citizenship,Religion,ID_CardNo,IssueDate,ExpiryDate,MaritalStatus,NumberOfChildren,StudyChild,MilitaryService,Others,Worktel,Mobile,Email,EmergencyPerson,EmergencyRelation,EmergencyAddress,EmergencyTel,date) \
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(sqlIn14,(result14[0]['NameTh'],result14[0]['SurnameTh'],result14[0]['NicknameTh'],result14[0]['NameEn'],\
            result14[0]['SurnameEn'],result14[0]['NicknameEn'],result14[0]['Birthdate'],result14[0]['BirthPlace'],result14[0]['BirthProvince'], \
            result14[0]['BirthCountry'],result14[0]['Age'],result14[0]['Height'],result14[0]['Weight'],result14[0]['BloodGroup'],result14[0]['Citizenship'],result14[0]['Religion'],result14[0]['ID_CardNo'], \
            result14[0]['IssueDate'],result14[0]['ExpiryDate'],result14[0]['MaritalStatus'],result14[0]['NumberOfChildren'],result14[0]['StudyChild'],result14[0]['MilitaryService'],result14[0]['Others'], \
            result14[0]['Worktel'],result14[0]['Mobile'],result14[0]['Email'],result14[0]['EmergencyPerson'],result14[0]['EmergencyRelation'],result14[0]['EmergencyAddress'],result14[0]['EmergencyTel'],result14[0]['date']))
            i=0
            for i in xrange(len(result17)):
                sqlIn17 = "INSERT INTO Reference (ID_CardNo,RelativeName,RelativeSurname,RelativePosition,RelativeRelationship,PhysicalHandicap,PhysicalHandicapDetail,KnowFrom) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn17,(result17[i]['ID_CardNo'],result17[i]['RelativeName'],result17[i]['RelativeSurname'],result17[i]['RelativePosition'],result17[i]['RelativeRelationship'],result17[i]['PhysicalHandicap'],result17[i]['PhysicalHandicapDetail'],result17[i]['KnowFrom']))
            i=0
            for i in xrange(len(result18)):
                sqlIn18 = "INSERT INTO RefPerson (ID_CardNo,RefName,RefPosition,RefAddress,RefTel) VALUES (%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn18,(result18[i]['ID_CardNo'],result18[i]['RefName'],result18[i]['RefPosition'],result18[i]['RefAddress'],result18[i]['RefTel']))
            i=0
            for i in xrange(len(result20)):
                sqlIn20 = "INSERT INTO SpecialSkill (ID_CardNo,CarDrivingLicense,MotorBicycleDrivingLicense,OwnCar,OwnMotorBicycle,WorkUpCountry,StartWorkEarliest,PhysicalDisabilityOrDisease,DischargeFromEmployment,DischargeFromEmploymentReason,Arrested,ArrestedReason) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn20,(result20[i]['ID_CardNo'],result20[i]['CarDrivingLicense'],result20[i]['MotorBicycleDrivingLicense'],result20[i]['OwnCar'],result20[i]['OwnMotorBicycle'], \
                result20[i]['WorkUpCountry'],result20[i]['StartWorkEarliest'],result20[i]['PhysicalDisabilityOrDisease'],result20[i]['DischargeFromEmployment'],result20[i]['DischargeFromEmploymentReason'],result20[i]['Arrested'],result20[i]['ArrestedReason']))
            try:
                i=0
                for i in xrange(len(result10)):
                    sqlIn10 = "INSERT INTO Employment (ID_CardNo,CompanyName,CompanyAddress,PositionHeld,StartSalary,EndSalary,StartYear,EndYear,Responsibility,ReasonOfLeaving,Descriptionofwork) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sqlIn10,(result10[i]['ID_CardNo'],result10[i]['CompanyName'],result10[i]['CompanyAddress'],result10[i]['PositionHeld'],result10[i]['StartSalary'],result10[i]['EndSalary'],result10[i]['StartYear'],result10[i]['EndYear'], \
                    result10[i]['Responsibility'],result10[i]['ReasonOfLeaving'],result10[i]['Descriptionofwork']))
            except Exception as e:
                logserver(e)
            try:
                i=0
                for i in xrange(len(result23)):
                    sqlIn23 = "INSERT INTO TrainingCourse(ID_CardNo,Subject,Place,StartDate,EndDate) VALUES (%s,%s,%s,%s,%s)"
                    cursor.execute(sqlIn23,(result23[i]['ID_CardNo'],result23[i]['Subject'],result23[i]['Place'],result23[i]['StartDate'],result23[i]['EndDate']))
            except Exception as e:
                logserver(e)

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
            except Exception as e:
                Emp_last = coun_company+"000"

            now = datetime.now()
            date = str(int(now.year)+543)
            form_employee = date[2:]
            type = Emp_last
            codelast = int(str(type[-coun_length:]))+1
            if   codelast<=9:
                 codelast=str(codelast)
                 codesumlast="00"+codelast
            elif codelast<=99:
                 codelast=str(codelast)
                 codesumlast="0"+codelast
            else:
                 codesumlast=str(codelast)
            first_character = resultcompafirst[0]['acronym']
            employeeid = first_character+form_employee+codesumlast
            encodedsalary = base64.b64encode(data_new['salary'])

            sqlEM = "INSERT INTO employee (employeeid,citizenid,name_th,name_eng,surname_th,surname_eng,nickname_employee,salary,email,phone_company,position_id,section_id,org_name_id,cost_center_name_id,company_id,start_work,EndWork_probation,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlEM,(employeeid,result14[0]['ID_CardNo'],result14[0]['NameTh'],result14[0]['NameEn'],result14[0]['SurnameTh'],result14[0]['SurnameEn'],result14[0]['NicknameEn'],encodedsalary,data_new['email'],data_new['phone_company'],data_new['position_id'],\
            data_new['section_id'],data_new['org_name_id'],data_new['cost_center_name_id'],data_new['company_id'],data_new['Start_contract'],data_new['End_contract'],data_new['createby']))

            sqlEm_ga = "INSERT INTO employee_ga (employeeid,citizenid,phone_depreciate,notebook_depreciate,limit_phone,chair_table,pc,notebook,office_equipment,ms,car_ticket,band_car,color,regis_car_number,other,description,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlEm_ga,(employeeid,result14[0]['ID_CardNo'],data_new['phone_depreciate'],data_new['notebook_depreciate'],data_new['limit_phone'],data_new['chair_table'],data_new['pc'],data_new['notebook'],data_new['office_equipment'],data_new['ms'],data_new['car_ticket'],data_new['band_car'],data_new['color'],\
            data_new['regis_car_number'],data_new['other'],data_new['description'],data_new['createby']))

            sqlEM_pro = "INSERT INTO Emp_probation (employeeid,citizenid,name_th,name_eng,surname_th,surname_eng,nickname_employee,salary,email,phone_company,position_id,section_id,org_name_id,cost_center_name_id,company_id,start_work,EndWork_probation,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlEM_pro,(employeeid,result14[0]['ID_CardNo'],result14[0]['NameTh'],result14[0]['NameEn'],result14[0]['SurnameTh'],result14[0]['SurnameEn'],result14[0]['NicknameEn'],encodedsalary,data_new['email'],data_new['phone_company'],data_new['position_id'],\
            data_new['section_id'],data_new['org_name_id'],data_new['cost_center_name_id'],data_new['company_id'],data_new['Start_contract'],data_new['End_contract'],data_new['createby']))
        connection.commit()
        connection.close()
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryAppform_One_person', methods=['POST'])
def QryAppform_One_person():
    try:
        connection = mysql3.connect()
        cursor = connection.cursor()
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sqlEm = "SELECT Address.AddressType,Address.HouseNo,Address.Street,Address.PostCode,Address.Tel,Address.Fax,amphures.AMPHUR_CODE,amphures.AMPHUR_NAME,provinces.PROVINCE_NAME,districts.DISTRICT_CODE,districts.DISTRICT_NAME FROM Address INNER JOIN provinces ON provinces.PROVINCE_ID=Address.PROVINCE_ID \
                                           INNER JOIN amphures ON amphures.AMPHUR_ID=Address.AMPHUR_ID \
                                           INNER JOIN districts ON districts.DISTRICT_CODE=Address.DISTRICT_ID \
                                           INNER JOIN Personal ON Personal.EmploymentAppNo=Address.EmploymentAppNo \
                     WHERE Personal.EmploymentAppNo=%s"
        cursor.execute(sqlEm,data_new['EmploymentAppNo'])
        columnsEm = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columnsEm)

        sql4 = "SELECT Attachment.Type,Attachment.PathFile FROM Attachment INNER JOIN Personal ON Personal.EmploymentAppNo=Attachment.EmploymentAppNo \
        WHERE Personal.EmploymentAppNo=%s"
        cursor.execute(sql4,data_new['EmploymentAppNo'])
        columns4 = [column[0] for column in cursor.description]
        result4 = toJson(cursor.fetchall(),columns4)

        sql6 = "SELECT ComputerSkill.ComSkill,ComputerSkill.Level FROM ComputerSkill INNER JOIN Personal ON Personal.EmploymentAppNo=ComputerSkill.EmploymentAppNo \
        WHERE Personal.EmploymentAppNo=%s"
        cursor.execute(sql6,data_new['EmploymentAppNo'])
        columns6 = [column[0] for column in cursor.description]
        result6 = toJson(cursor.fetchall(),columns6)

        sql9 = "SELECT Education.EducationLevel,Education.Institute,Education.StartYear,Education.EndYear,Education.Qualification,Education.Major,Education.GradeAvg,Education.ExtraCurricularActivities FROM Education INNER JOIN Personal ON Personal.EmploymentAppNo=Education.EmploymentAppNo \
        WHERE Personal.EmploymentAppNo=%s"
        cursor.execute(sql9,data_new['EmploymentAppNo'])
        columns9 = [column[0] for column in cursor.description]
        result9 = toJson(cursor.fetchall(),columns9)

        sql10 = "SELECT Employment.CompanyName,Employment.CompanyAddress,Employment.PositionHeld,Employment.StartSalary,Employment.EndSalary,Employment.StartYear,Employment.EndYear,Employment.Responsibility,Employment.ReasonOfLeaving,Employment.Descriptionofwork FROM Employment INNER JOIN Personal ON Personal.EmploymentAppNo=Employment.EmploymentAppNo \
        WHERE Personal.EmploymentAppNo=%s"
        cursor.execute(sql10,data_new['EmploymentAppNo'])
        columns10 = [column[0] for column in cursor.description]
        result10 = toJson(cursor.fetchall(),columns10)

        sqlfa = "SELECT Family.MemberType,Family.Name,Family.Surname,Family.Occupation,Family.Address,Family.Tel,Family.Fax FROM Family INNER JOIN Personal ON Personal.EmploymentAppNo=Family.EmploymentAppNo \
        WHERE (Family.MemberType = 'Father' OR Family.MemberType = 'Mother')AND Personal.EmploymentAppNo=%s"
        cursor.execute(sqlfa,data_new['EmploymentAppNo'])
        columnsfa = [column[0] for column in cursor.description]
        resultfa = toJson(cursor.fetchall(),columnsfa)

        sqlbro = "SELECT Family.MemberType,Family.Name,Family.Surname,Family.Occupation,Family.Address,Family.Tel,Family.Fax FROM Family INNER JOIN Personal ON Personal.EmploymentAppNo=Family.EmploymentAppNo \
        WHERE Family.MemberType = 'BrotherSister' AND Personal.EmploymentAppNo=%s"
        cursor.execute(sqlbro,data_new['EmploymentAppNo'])
        columnsbro = [column[0] for column in cursor.description]
        resultbro = toJson(cursor.fetchall(),columnsbro)

        sql13 = "SELECT LanguagesSkill.Languages,LanguagesSkill.Speaking,LanguagesSkill.Reading,LanguagesSkill.Writting FROM LanguagesSkill INNER JOIN Personal ON Personal.EmploymentAppNo=LanguagesSkill.EmploymentAppNo \
        WHERE Personal.EmploymentAppNo=%s"
        cursor.execute(sql13,data_new['EmploymentAppNo'])
        columns13 = [column[0] for column in cursor.description]
        result13 = toJson(cursor.fetchall(),columns13)

        sql14 = "SELECT * FROM Personal \
        WHERE Personal.EmploymentAppNo=%s"
        cursor.execute(sql14,data_new['EmploymentAppNo'])
        columns14 = [column[0] for column in cursor.description]
        result14 = toJson(cursor.fetchall(),columns14)

        try:
            sqlPath = "SELECT PathFile FROM Attachment \
            WHERE EmploymentAppNo=%s AND Type='profile_image'"
            cursor.execute(sqlPath,data_new['EmploymentAppNo'])
            columnsPath = [column[0] for column in cursor.description]
            resulPath = toJson(cursor.fetchall(),columnsPath)
            test=str("http://career.inet.co.th/"+str(resulPath[0]['PathFile']))
            # with open(test, 'rb') as image_file:
            #     encoded_Image = base64.b64encode(image_file.read())
            encoded_Image = base64.b64encode(test)
        except Exception as e:
            encoded_Image="No images"

        sql17 = "SELECT Reference.RelativeName,Reference.RelativeSurname,Reference.RelativePosition,Reference.RelativeRelationship,Reference.PhysicalHandicap,Reference.PhysicalHandicapDetail,Reference.KnowFrom FROM Reference INNER JOIN Personal ON Personal.EmploymentAppNo=Reference.EmploymentAppNo \
        WHERE Personal.EmploymentAppNo=%s"
        cursor.execute(sql17,data_new['EmploymentAppNo'])
        columns17 = [column[0] for column in cursor.description]
        result17 = toJson(cursor.fetchall(),columns17)

        sql18 = "SELECT RefPerson.RefName,RefPerson.RefPosition,RefPerson.RefAddress,RefPerson.RefTel FROM RefPerson INNER JOIN Personal ON Personal.EmploymentAppNo=RefPerson.EmploymentAppNo \
        WHERE Personal.EmploymentAppNo=%s"
        cursor.execute(sql18,data_new['EmploymentAppNo'])
        columns18 = [column[0] for column in cursor.description]
        result18 = toJson(cursor.fetchall(),columns18)

        sql20 = "SELECT SpecialSkill.CarDrivingLicense,SpecialSkill.MotorBicycleDrivingLicense,SpecialSkill.OwnCar,SpecialSkill.OwnMotorBicycle,SpecialSkill.WorkUpCountry,SpecialSkill.StartWorkEarliest,SpecialSkill.PhysicalDisabilityOrDisease,SpecialSkill.DischargeFromEmployment,SpecialSkill.DischargeFromEmploymentReason,SpecialSkill.Arrested,SpecialSkill.ArrestedReason FROM SpecialSkill INNER JOIN Personal ON Personal.EmploymentAppNo=SpecialSkill.EmploymentAppNo \
        WHERE Personal.EmploymentAppNo=%s"
        cursor.execute(sql20,data_new['EmploymentAppNo'])
        columns20 = [column[0] for column in cursor.description]
        result20 = toJson(cursor.fetchall(),columns20)

        sql23 = "SELECT TrainingCourse.Subject,TrainingCourse.Place,TrainingCourse.StartDate,TrainingCourse.EndDate FROM TrainingCourse INNER JOIN Personal ON Personal.EmploymentAppNo=TrainingCourse.EmploymentAppNo \
        WHERE Personal.EmploymentAppNo=%s"
        cursor.execute(sql23,data_new['EmploymentAppNo'])
        columns23 = [column[0] for column in cursor.description]
        result23 = toJson(cursor.fetchall(),columns23)
        connection.commit()
        connection.close()
        arr={}
        arr["Address"] = result
        arr["Attachment"] = result4
        arr["Image_profile"] = encoded_Image
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
