#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/QryEmployee', methods=['POST'])
def QryEmployee():
    try:
        connection = mysql3.connect()
        cursor = connection.cursor()
        data = request.json
        citizenid = data['citizenid']
        EmploymentAppNo = data['EmploymentAppNo']
        sql = "SELECT EmploymentAppNo,AppliedPosition1,AppliedPosition2,StartExpectedSalary,EndExpectedSalary,NameTh,SurnameTh,Mobile,Email,date FROM Personal WHERE ID_CardNo=%s AND EmploymentAppNo=%s"
        cursor.execute(sql,(citizenid,EmploymentAppNo))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        connection.close()

        # connection = mysql.connect()
        # cursor = connection.cursor()
        # sqlIn = "INSERT INTO employee (employeeid,citizenid,name_th,name_eng,surname_th,surname_eng,nickname_employee,address_employee,salary,email,,phone_company,position_id,section_id,org_name_id,cost_center_name_id,company_id,start_work) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # cursor.execute(sqlIn,(status_detail,path_color))
        # connection.commit()
        # connection.close()
        # return "success"

        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee', methods=['POST'])
def EditEmployee():
    try:
        connection = mysql3.connect()
        cursor = connection.cursor()
        dataInput = request.json
        citizenid = data['citizenid']
        EmploymentAppNo = data['EmploymentAppNo']
        sql = "SELECT EmploymentAppNo,AppliedPosition1,AppliedPosition2,StartExpectedSalary,EndExpectedSalary,NameTh,SurnameTh,Mobile,Email,date FROM Personal WHERE ID_CardNo=%s AND EmploymentAppNo=%s"
        cursor.execute(sql,(citizenid,EmploymentAppNo))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        connection.close()

        # connection = mysql.connect()
        # cursor = connection.cursor()
        # i=0
        # for i in xrange(len(result)):
        #     sqlIn = "INSERT INTO Address (EmploymentAppNo,ID_CardNo,AddressType,HouseNo,Street,DISTRICT_ID,AMPHUR_ID,PROVINCE_ID,PostCode,Tel,Fax) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        #     cursor.execute(sqlIn,(result[i]['EmploymentAppNo'],result[i]['ID_CardNo'],result[i]['AddressType'],result[i]['HouseNo'],
        #     result[i]['Street'],result[i]['DISTRICT_NAME'],result[i]['AMPHUR_NAME'],result[i]['PROVINCE_NAME'],result[i]['PostCode'],result[i]['Tel'],result[i]['Fax']))
        # i=0
        # for i in xrange(len(result4)):
        #     sqlIn4 = "INSERT INTO Attachment (EmploymentAppNo,ID_CardNo,Type,PathFile) VALUES (%s,%s,%s,%s)"
        #     cursor.execute(sqlIn4,(result4[i]['EmploymentAppNo'],result4[i]['ID_CardNo'],result4[i]['Type'],result4[i]['PathFile']))
        # i=0
        # for i in xrange(len(result6)):
        #     sqlIn6 = "INSERT INTO ComputerSkill (EmploymentAppNo,ID_CardNo,ComSkill,Level) VALUES (%s,%s,%s,%s)"
        #     cursor.execute(sqlIn6,(result6[i]['EmploymentAppNo'],result6[i]['ID_CardNo'],result6[i]['ComSkill'],result6[i]['Level']))
        # i=0
        # for i in xrange(len(result9)):
        #     sqlIn9 = "INSERT INTO Education (EmploymentAppNo,ID_CardNo,EducationLevel,Institute,StartYear,EndYear,Qualification,Major,GradeAvg,ExtraCurricularActivities) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        #     cursor.execute(sqlIn9,(result9[i]['EmploymentAppNo'],result9[i]['ID_CardNo'],result9[i]['EducationLevel'],result9[i]['Institute'],result9[i]['StartYear'],result9[i]['EndYear'],result9[i]['Qualification'],result9[i]['Major'],result9[i]['GradeAvg'],result9[i]['ExtraCurricularActivities']))
        # i=0
        # for i in xrange(len(result11)):
        #     sqlIn11 = "INSERT INTO Family (EmploymentAppNo,ID_CardNo,MemberType,Name,Surname,Occupation,Address,Tel,Fax) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        #     cursor.execute(sqlIn11,(result11[i]['EmploymentAppNo'],result11[i]['ID_CardNo'],result11[i]['MemberType'],result11[i]['Name'],result11[i]['Surname'],result11[i]['Occupation'],result11[i]['Address'],result11[i]['Tel'],result11[i]['Fax']))
        # i=0
        # for i in xrange(len(result13)):
        #     sqlIn13 = "INSERT INTO LanguagesSkill (EmploymentAppNo,ID_CardNo,Languages,Speaking,Reading,Writting) VALUES (%s,%s,%s,%s,%s,%s)"
        #     cursor.execute(sqlIn13,(result13[i]['EmploymentAppNo'],result13[i]['ID_CardNo'],result13[i]['Languages'],result13[i]['Speaking'],result13[i]['Reading'],result13[i]['Writting']))
        #
        # sqlIn14 = """INSERT INTO Personal (EmploymentAppNo,AppliedPosition1,AppliedPosition2,StartExpectedSalary,EndExpectedSalary,NameTh,SurnameTh,NicknameTh,NameEn,SurnameEn,NicknameEn,Birthdate,BirthPlace,BirthProvince,BirthCountry,Age,Height,Weight,BloodGroup,Citizenship,Religion,ID_CardNo,IssueDate,ExpiryDate,MaritalStatus,NumberOfChildren,StudyChild,MilitaryService,Others,Worktel,Mobile,Email,EmergencyPerson,EmergencyRelation,EmergencyAddress,EmergencyTel,date) \
        # VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        # cursor.execute(sqlIn14,(result14[0]['EmploymentAppNo'],result14[0]['AppliedPosition1'],result14[0]['AppliedPosition2'],result14[0]['StartExpectedSalary'],result14[0]['EndExpectedSalary'],result14[0]['NameTh'],result14[0]['SurnameTh'],result14[0]['NicknameTh'],result14[0]['NameEn'],result14[0]['SurnameEn'],result14[0]['NicknameEn'],result14[0]['Birthdate'],result14[0]['BirthPlace'],result14[0]['BirthProvince'], \
        # result14[0]['BirthCountry'],result14[0]['Age'],result14[0]['Height'],result14[0]['Weight'],result14[0]['BloodGroup'],result14[0]['Citizenship'],result14[0]['Religion'],result14[0]['ID_CardNo'], \
        # result14[0]['IssueDate'],result14[0]['ExpiryDate'],result14[0]['MaritalStatus'],result14[0]['NumberOfChildren'],result14[0]['StudyChild'],result14[0]['MilitaryService'],result14[0]['Others'], \
        # result14[0]['Worktel'],result14[0]['Mobile'],result14[0]['Email'],result14[0]['EmergencyPerson'],result14[0]['EmergencyRelation'],result14[0]['EmergencyAddress'],result14[0]['EmergencyTel'],result14[0]['date']))
        # i=0
        # for i in xrange(len(result17)):
        #     sqlIn17 = "INSERT INTO Reference (EmploymentAppNo,ID_CardNo,RelativeName,RelativeSurname,RelativePosition,RelativeRelationship,PhysicalHandicap,PhysicalHandicapDetail,KnowFrom) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        #     cursor.execute(sqlIn17,(result17[i]['EmploymentAppNo'],result17[i]['ID_CardNo'],result17[i]['RelativeName'],result17[i]['RelativeSurname'],result17[i]['RelativePosition'],result17[i]['RelativeRelationship'],result17[i]['PhysicalHandicap'],result17[i]['PhysicalHandicapDetail'],result17[i]['KnowFrom']))
        # i=0
        # for i in xrange(len(result18)):
        #     sqlIn18 = "INSERT INTO RefPerson (EmploymentAppNo,ID_CardNo,RefName,RefPosition,RefAddress,RefTel) VALUES (%s,%s,%s,%s,%s,%s)"
        #     cursor.execute(sqlIn18,(result18[i]['EmploymentAppNo'],result18[i]['ID_CardNo'],result18[i]['RefName'],result18[i]['RefPosition'],result18[i]['RefAddress'],result18[i]['RefTel']))
        # i=0
        # for i in xrange(len(result20)):
        #     sqlIn20 = "INSERT INTO SpecialSkill (EmploymentAppNo,ID_CardNo,CarDrivingLicense,MotorBicycleDrivingLicense,OwnCar,OwnMotorBicycle,WorkUpCountry,StartWorkEarliest,PhysicalDisabilityOrDisease,DischargeFromEmployment,DischargeFromEmploymentReason,Arrested,ArrestedReason) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        #     cursor.execute(sqlIn20,(result20[i]['EmploymentAppNo'],result20[i]['ID_CardNo'],result20[i]['CarDrivingLicense'],result20[i]['MotorBicycleDrivingLicense'],result20[i]['OwnCar'],result20[i]['OwnMotorBicycle'], \
        #     result20[i]['WorkUpCountry'],result20[i]['StartWorkEarliest'],result20[i]['PhysicalDisabilityOrDisease'],result20[i]['DischargeFromEmployment'],result20[i]['DischargeFromEmploymentReason'],result20[i]['Arrested'],result20[i]['ArrestedReason']))
        # try:
        #     i=0
        #     for i in xrange(len(result10)):
        #         sqlIn10 = "INSERT INTO Employment (EmploymentAppNo,ID_CardNo,CompanyName,CompanyAddress,PositionHeld,StartSalary,EndSalary,StartYear,EndYear,Responsibility,ReasonOfLeaving,Descriptionofwork) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        #         cursor.execute(sqlIn10,(result10[i]['EmploymentAppNo'],result10[i]['ID_CardNo'],result10[i]['CompanyName'],result10[i]['CompanyAddress'],result10[i]['PositionHeld'],result10[i]['StartSalary'],result10[i]['EndSalary'],result10[i]['StartYear'],result10[i]['EndYear'], \
        #         result10[i]['Responsibility'],result10[i]['ReasonOfLeaving'],result10[i]['Descriptionofwork']))
        # except Exception as e:
        #     logserver(e)
        # try:
        #     i=0
        #     for i in xrange(len(result23)):
        #         sqlIn23 = "INSERT INTO TrainingCourse(EmploymentAppNo,ID_CardNo,Subject,Place,StartDate,EndDate) VALUES (%s,%s,%s,%s,%s,%s)"
        #         cursor.execute(sqlIn23,(result23[i]['EmploymentAppNo'],result23[i]['ID_CardNo'],result23[i]['Subject'],result23[i]['Place'],result23[i]['StartDate'],result23[i]['EndDate']))
        # except Exception as e:
        #     logserver(e)
        # connection.commit()
        # connection.close()
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/InsertEmployeeHRCI_Management', methods=['POST'])
@connect_sql()
def InsertEmployeeHRCI_Management():
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        # now = datetime.now()
        # date = str(int(now.year)+543)
        # form_employee = date[2:]
        sqlEM = "INSERT INTO employee (employeeid,citizenid,name_th,name_eng,surname_th,surname_eng,nickname_employee,salary,email,phone_company,position_id,section_id,org_name_id,cost_center_name_id,company_id,start_work,EndWork_probation) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlEM,(data_new['employeeid'],data_new['ID_CardNo'],data_new['NameTh'],data_new['NameEn'],data_new['SurnameTh'],data_new['SurnameEn'],data_new['NicknameEn'],data_new['salary'],data_new['email'],data_new['phone_company'],data_new['position_id'],\
        data_new['section_id'],data_new['org_name_id'],data_new['cost_center_name_id'],data_new['company_id'],data_new['start_work'],data_new['EndWork_probation']))

        sqlEm_ga = """INSERT INTO employee_ga (employeeid,phone_depreciate,notebook_depreciate,limit_phone,chair_table,pc,notebook,office_equipment,ms,car_ticket,band_car,color,regis_car_number,other,description) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sqlEm_ga,(data_new['employeeid'],data_new['phone_depreciate'],data_new['notebook_depreciate'],data_new['limit_phone'],data_new['chair_table'],data_new['pc'],data_new['notebook'],data_new['office_equipment'],data_new['ms'],data_new['car_ticket'],data_new['band_car'],data_new['color'],data_new['regis_car_number'],\
        data_new['other'],data_new['description']))
        i=0
        for i in xrange(len(data_new)):
            sqlIn = "INSERT INTO Address (ID_CardNo,AddressType,HouseNo,Street,DISTRICT_ID,AMPHUR_ID,PROVINCE_ID,PostCode,Tel,Fax) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn,(data_new[i]['ID_CardNo'],data_new[i]['AddressType'],data_new[i]['HouseNo'],
            data_new[i]['Street'],data_new[i]['DISTRICT_NAME'],data_new[i]['AMPHUR_NAME'],data_new[i]['PROVINCE_NAME'],data_new[i]['PostCode'],data_new[i]['Tel'],data_new[i]['Fax']))
        # i=0
        # for i in xrange(len(data_new)):
        #     type = data_new[i]['PathFile']
        #     typefile = type[-4:]
        #     typename = type[46:-4]
        #     url = 'http://career.inet.co.th/'+data_new[i]['PathFile']
        #     image_name = data_new[i]['EmploymentAppNo']+typename+typefile
        #     Path = "pig/" + image_name
        #     wget.download(url,Path)
        #     sqlIn4 = "INSERT INTO Attachment (EmploymentAppNo,ID_CardNo,Type,PathFile) VALUES (%s,%s,%s,%s)"
        #     cursor.execute(sqlIn4,(data_new[i]['EmploymentAppNo'],data_new[i]['ID_CardNo'],data_new[i]['Type'],data_new[i]['PathFile']))
        i=0
        for i in xrange(len(data_new)):
            sqlIn6 = "INSERT INTO ComputerSkill (ID_CardNo,ComSkill,Level) VALUES (%s,%s,%s)"
            cursor.execute(sqlIn6,(data_new[i]['ID_CardNo'],data_new[i]['ComSkill'],data_new[i]['Level']))
        i=0
        for i in xrange(len(data_new)):
            sqlInContract = "INSERT INTO Contract (ID_CardNo,Start_contract,End_contract,salary_thai) VALUES (%s,%s,%s,%s)"
            cursor.execute(sqlInContract,data_new[0]['ID_CardNo'],data_new['Start_contract'],data_new['End_contract'],data_new['salary_thai'])
        i=0
        for i in xrange(len(data_new)):
            sqlIn9 = "INSERT INTO Education (ID_CardNo,EducationLevel,Institute,StartYear,EndYear,Qualification,Major,GradeAvg,ExtraCurricularActivities) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn9,(data_new[i]['ID_CardNo'],data_new[i]['EducationLevel'],data_new[i]['Institute'],data_new[i]['StartYear'],data_new[i]['EndYear'],data_new[i]['Qualification'],\
            data_new[i]['Major'],data_new[i]['GradeAvg'],data_new[i]['ExtraCurricularActivities']))
        i=0
        for i in xrange(len(data_new)):
            sqlIn11 = "INSERT INTO Family (ID_CardNo,MemberType,Name,Surname,Occupation,Address,Tel,Fax) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn11,(data_new[i]['ID_CardNo'],data_new[i]['MemberType'],data_new[i]['Name'],data_new[i]['Surname'],data_new[i]['Occupation'],data_new[i]['Address'],data_new[i]['Tel'],data_new[i]['Fax']))
        i=0
        for i in xrange(len(data_new)):
            sqlIn13 = "INSERT INTO LanguagesSkill (ID_CardNo,Languages,Speaking,Reading,Writting) VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn13,(data_new[i]['ID_CardNo'],data_new[i]['Languages'],data_new[i]['Speaking'],data_new[i]['Reading'],data_new[i]['Writting']))

        # sqlIn14 = """INSERT INTO Personal (EmploymentAppNo,AppliedPosition1,AppliedPosition2,StartExpectedSalary,EndExpectedSalary,NameTh,SurnameTh,NicknameTh,NameEn,SurnameEn,NicknameEn,Birthdate,BirthPlace,BirthProvince,BirthCountry,Age,Height,Weight,BloodGroup,Citizenship,Religion,ID_CardNo,IssueDate,ExpiryDate,MaritalStatus,NumberOfChildren,StudyChild,MilitaryService,Others,Worktel,Mobile,Email,EmergencyPerson,EmergencyRelation,EmergencyAddress,EmergencyTel,date) \
        # VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        # cursor.execute(sqlIn14,(data_new['EmploymentAppNo'],data_new['AppliedPosition1'],data_new['AppliedPosition2'],data_new['StartExpectedSalary'],data_new['EndExpectedSalary'],data_new['NameTh'],data_new['SurnameTh'],data_new['NicknameTh'],data_new['NameEn'],\
        # data_new['SurnameEn'],data_new['NicknameEn'],data_new['Birthdate'],data_new['BirthPlace'],data_new['BirthProvince'], \
        # data_new['BirthCountry'],data_new['Age'],data_new['Height'],data_new['Weight'],data_new['BloodGroup'],data_new['Citizenship'],data_new['Religion'],data_new['ID_CardNo'], \
        # data_new['IssueDate'],data_new['ExpiryDate'],data_new['MaritalStatus'],data_new['NumberOfChildren'],data_new['StudyChild'],data_new['MilitaryService'],data_new['Others'], \
        # data_new['Worktel'],data_new['Mobile'],data_new['Email'],data_new['EmergencyPerson'],data_new['EmergencyRelation'],data['EmergencyAddress'],data_new['EmergencyTel'],data_new['date']))
        i=0
        for i in xrange(len(data)):
            sqlIn17 = "INSERT INTO Reference (ID_CardNo,RelativeName,RelativeSurname,RelativePosition,RelativeRelationship,PhysicalHandicap,PhysicalHandicapDetail,KnowFrom) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn17,(data_new[i]['ID_CardNo'],data_new[i]['RelativeName'],data_new[i]['RelativeSurname'],data_new[i]['RelativePosition'],data_new[i]['RelativeRelationship'],data_new[i]['PhysicalHandicap'],data_new[i]['PhysicalHandicapDetail'],data_new[i]['KnowFrom']))
        i=0
        for i in xrange(len(data)):
            sqlIn18 = "INSERT INTO RefPerson (ID_CardNo,RefName,RefPosition,RefAddress,RefTel) VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn18,(data_new[i]['ID_CardNo'],data_new[i]['RefName'],data_new[i]['RefPosition'],data_new[i]['RefAddress'],data_new[i]['RefTel']))
        i=0
        for i in xrange(len(data)):
            sqlIn20 = "INSERT INTO SpecialSkill (ID_CardNo,CarDrivingLicense,MotorBicycleDrivingLicense,OwnCar,OwnMotorBicycle,WorkUpCountry,StartWorkEarliest,PhysicalDisabilityOrDisease,DischargeFromEmployment,DischargeFromEmploymentReason,Arrested,ArrestedReason) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn20,(data_new[i]['ID_CardNo'],data_new[i]['CarDrivingLicense'],data_new[i]['MotorBicycleDrivingLicense'],data_new[i]['OwnCar'],data_new[i]['OwnMotorBicycle'], \
            data[i]['WorkUpCountry'],data_new[i]['StartWorkEarliest'],data_new[i]['PhysicalDisabilityOrDisease'],data[i]['DischargeFromEmployment'],data_new[i]['DischargeFromEmploymentReason'],data_new[i]['Arrested'],data_new[i]['ArrestedReason']))
        try:
            i=0
            for i in xrange(len(data)):
                sqlIn10 = "INSERT INTO Employment (ID_CardNo,CompanyName,CompanyAddress,PositionHeld,StartSalary,EndSalary,StartYear,EndYear,Responsibility,ReasonOfLeaving,Descriptionofwork) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn10,(data_new[i]['ID_CardNo'],data_new[i]['CompanyName'],data_new[i]['CompanyAddress'],data_new[i]['PositionHeld'],data_new[i]['StartSalary'],data_new[i]['EndSalary'],data_new[i]['StartYear'],data_new[i]['EndYear'], \
                data[i]['Responsibility'],data_new[i]['ReasonOfLeaving'],data_new[i]['Descriptionofwork']))
        except Exception as e:
            logserver(e)
        try:
            i=0
            for i in xrange(len(data)):
                sqlIn23 = "INSERT INTO TrainingCourse(ID_CardNo,Subject,Place,StartDate,EndDate) VALUES (%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn23,(data_new[i]['ID_CardNo'],data_new[i]['Subject'],data_new[i]['Place'],data_new[i]['StartDate'],data_new[i]['EndDate']))
        except Exception as e:
            logserver(e)
    except Exception as e:
        logserver(e)
        return "fail"
