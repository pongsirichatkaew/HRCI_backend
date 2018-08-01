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

        # connection = mysql4.connect()
        # cursor = connection.cursor()
        # sqlIn = "INSERT INTO Address (EmploymentAppNo,AddressType,HouseNo,Street,DISTRICT_ID,AMPHUR_ID,PROVINCE_ID,PostCode,Tel,Fax) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # cursor.execute(sqlIn,(dataInput[0]['EmploymentAppNo'],dataInput[0]['AddressType'],dataInput[0]['HouseNo'], \
        #  dataInput[0]['Street'],dataInput[0]['DISTRICT_NAME'],dataInput[0]['AMPHUR_NAME'],dataInput[0]['PROVINCE_NAME'],dataInput[0]['PostCode'],dataInput[0]['Tel'],dataInput[0]['Fax']))
        #
        # sqlIn4 = "INSERT INTO Attachment (EmploymentAppNo,Type,PathFile) VALUES (%s,%s,%s)"
        # cursor.execute(sqlIn4,(dataInput[0]['EmploymentAppNo'],dataInput[0]['Type'],dataInput[0]['PathFile']))
        #
        # sqlIn6 = "INSERT INTO ComputerSkill (EmploymentAppNo,ComSkill,Level) VALUES (%s,%s,%s)"
        # cursor.execute(sqlIn6,(dataInput[0]['EmploymentAppNo'],dataInput[0]['ComSkill'],dataInput[0]['Level']))
        #
        # sqlIn9 = "INSERT INTO Education (EmploymentAppNo,EducationLevel,Institute,StartYear,EndYear,Qualification,Major,GradeAvg,ExtraCurricularActivities) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # cursor.execute(sqlIn9,(dataInput[0]['EmploymentAppNo'],dataInput[0]['EducationLevel'],dataInput[0]['Institute'],dataInput[0]['StartYear'],dataInput[0]['EndYear'],dataInput[0]['Qualification'],dataInput[0]['Major'],dataInput[0]['GradeAvg'],dataInput[0]['ExtraCurricularActivities']))
        #
        # sqlIn11 = "INSERT INTO Family (EmploymentAppNo,MemberType,Name,Surname,Occupation,Address,Tel,Fax) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        # cursor.execute(sqlIn11,(dataInput[0]['EmploymentAppNo'],dataInput[0]['MemberType'],dataInput[0]['Name'],dataInput[0]['Surname'],dataInput[0]['Occupation'],dataInput[0]['Address'],dataInput[0]['Tel'],dataInput[0]['Fax']))
        #
        # sqlIn13 = "INSERT INTO LanguagesSkill (EmploymentAppNo,Languages,Speaking,Reading,Writting) VALUES (%s,%s,%s,%s,%s)"
        # cursor.execute(sqlIn13,(dataInput[0]['EmploymentAppNo'],dataInput[0]['Languages'],dataInput[0]['Speaking'],dataInput[0]['Reading'],dataInput[0]['Writting']))
        #
        # sqlIn14 = """INSERT INTO Personal (EmploymentAppNo,AppliedPosition1,AppliedPosition2,StartExpectedSalary,EndExpectedSalary,NameTh,SurnameTh,NicknameTh,NameEn,SurnameEn,NicknameEn,Birthdate,BirthPlace,BirthProvince,BirthCountry,Age,Height,Weight,BloodGroup,Citizenship,Religion,ID_CardNo,IssueDate,ExpiryDate,MaritalStatus,NumberOfChildren,StudyChild,MilitaryService,Others,Worktel,Mobile,Email,EmergencyPerson,EmergencyRelation,EmergencyAddress,EmergencyTel,date) \
        # VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        # cursor.execute(sqlIn14,(dataInput[0]['EmploymentAppNo'],dataInput[0]['AppliedPosition1'],dataInput[0]['AppliedPosition2'],dataInput[0]['StartExpectedSalary'],dataInput[0]['EndExpectedSalary'],dataInput[0]['NameTh'],dataInput[0]['SurnameTh'],dataInput[0]['NicknameTh'],dataInput[0]['NameEn'],dataInput[0]['SurnameEn'],dataInput[0]['NicknameEn'],dataInput[0]['Birthdate'],dataInput[0]['BirthPlace'],dataInput[0]['BirthProvince'], \
        # dataInput[0]['BirthCountry'],dataInput[0]['Age'],dataInput[0]['Height'],dataInput[0]['Weight'],dataInput[0]['BloodGroup'],dataInput[0]['Citizenship'],dataInput[0]['Religion'],dataInput[0]['ID_CardNo'], \
        # dataInput[0]['IssueDate'],dataInput[0]['ExpiryDate'],dataInput[0]['MaritalStatus'],dataInput[0]['NumberOfChildren'],dataInput[0]['StudyChild'],dataInput[0]['MilitaryService'],dataInput[0]['Others'], \
        # dataInput[0]['Worktel'],dataInput[0]['Mobile'],dataInput[0]['Email'],dataInput[0]['EmergencyPerson'],dataInput[0]['EmergencyRelation'],dataInput[0]['EmergencyAddress'],dataInput[0]['EmergencyTel'],dataInput[0]['date']))
        #
        # sqlIn17 = "INSERT INTO Reference (EmploymentAppNo,RelativeName,RelativeSurname,RelativePosition,RelativeRelationship,PhysicalHandicap,PhysicalHandicapDetail,KnowFrom) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        # cursor.execute(sqlIn17,(dataInput[0]['EmploymentAppNo'],dataInput[0]['RelativeName'],dataInput[0]['RelativeSurname'],dataInput[0]['RelativePosition'],dataInput[0]['RelativeRelationship'],dataInput[0]['PhysicalHandicap'],dataInput[0]['PhysicalHandicapDetail'],dataInput[0]['KnowFrom']))
        #
        # sqlIn18 = "INSERT INTO RefPerson (EmploymentAppNo,RefName,RefPosition,RefAddress,RefTel) VALUES (%s,%s,%s,%s,%s)"
        # cursor.execute(sqlIn18,(dataInput[0]['EmploymentAppNo'],dataInput[0]['RefName'],dataInput[0]['RefPosition'],dataInput[0]['RefAddress'],dataInput[0]['RefTel']))
        #
        # sqlIn20 = "INSERT INTO SpecialSkill (EmploymentAppNo,CarDrivingLicense,MotorBicycleDrivingLicense,OwnCar,OwnMotorBicycle,WorkUpCountry,StartWorkEarliest,PhysicalDisabilityOrDisease,DischargeFromEmployment,DischargeFromEmploymentReason,Arrested,ArrestedReason) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # cursor.execute(sqlIn20,(dataInput[0]['EmploymentAppNo'],dataInput[0]['CarDrivingLicense'],dataInput[0]['MotorBicycleDrivingLicense'],dataInput[0]['OwnCar'],dataInput[0]['OwnMotorBicycle'], \
        # dataInput[0]['WorkUpCountry'],dataInput[0]['StartWorkEarliest'],dataInput[0]['PhysicalDisabilityOrDisease'],dataInput[0]['DischargeFromEmployment'],dataInput[0]['DischargeFromEmploymentReason'],dataInput[0]['Arrested'],dataInput[0]['ArrestedReason']))
        # try:
        #     sqlIn10 = "INSERT INTO Employment (EmploymentAppNo,CompanyName,CompanyAddress,PositionHeld,StartSalary,EndSalary,StartYear,EndYear,Responsibility,ReasonOfLeaving,Descriptionofwork) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        #     cursor.execute(sqlIn10,(dataInput[0]['EmploymentAppNo'],dataInput[0]['CompanyName'],dataInput[0]['CompanyAddress'],dataInput[0]['PositionHeld'],dataInput[0]['StartSalary'],dataInput[0]['EndSalary'],dataInput[0]['StartYear'],dataInput[0]['EndYear'], \
        #     dataInput[0]['Responsibility'],dataInput[0]['ReasonOfLeaving'],dataInput[0]['Descriptionofwork']))
        # except Exception as e:
        #     logserver(e)
        # try:
        #     sqlIn23 = "INSERT INTO TrainingCourse(EmploymentAppNo,Subject,Place,StartDate,EndDate) VALUES (%s,%s,%s,%s,%s)"
        #     cursor.execute(sqlIn23,(dataInput[0]['EmploymentAppNo'],dataInput[0]['Subject'],dataInput[0]['Place'],dataInput[0]['StartDate'],dataInput[0]['EndDate']))
        # except Exception as e:
        #     logserver(e)
        # connection.commit()
        # connection.close()
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryBlacklist', methods=['POST'])
@connect_sql()
def QryBlacklist(cursor):
    try:
        sql = "SELECT * FROM blacklist"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
