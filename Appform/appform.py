#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/QryAppform', methods=['POST'])
def QryAppform():
    try:
        connection = mysql3.connect()
        cursor = connection.cursor()
        sql = "SELECT EmploymentAppNo,AppliedPosition1,AppliedPosition2,StartExpectedSalary,EndExpectedSalary,NameTh,SurnameTh,Mobile,Email,date,status_id FROM Personal"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        connection.close()
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryDatbaseAppform', methods=['POST'])
def QryDatbaseAppform():
    try:
        connection = mysql3.connect()
        cursor = connection.cursor()
        dataInput = request.json
        sql = "SELECT * FROM Address WHERE EmploymentAppNo=%s"
        cursor.execute(sql,dataInput['EmploymentAppNo'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sql3 = "SELECT * FROM amphures"
        cursor.execute(sql3)
        columns3 = [column[0] for column in cursor.description]
        result3 = toJson(cursor.fetchall(),columns3)

        sql4 = "SELECT * FROM Attachment"
        cursor.execute(sql4)
        columns4 = [column[0] for column in cursor.description]
        result4 = toJson(cursor.fetchall(),columns4)

        sql6 = "SELECT * FROM ComputerSkill"
        cursor.execute(sql6)
        columns6 = [column[0] for column in cursor.description]
        result6 = toJson(cursor.fetchall(),columns6)

        sql7 = "SELECT * FROM districts"
        cursor.execute(sql7)
        columns7 = [column[0] for column in cursor.description]
        result7 = toJson(cursor.fetchall(),columns7)

        sql9 = "SELECT * FROM Education"
        cursor.execute(sql9)
        columns9 = [column[0] for column in cursor.description]
        result9 = toJson(cursor.fetchall(),columns9)

        sql10 = "SELECT * FROM Employment"
        cursor.execute(sql10)
        columns10 = [column[0] for column in cursor.description]
        result10 = toJson(cursor.fetchall(),columns10)

        sql11 = "SELECT * FROM Family"
        cursor.execute(sql11)
        columns11 = [column[0] for column in cursor.description]
        result11 = toJson(cursor.fetchall(),columns11)

        sql12 = "SELECT * FROM geography"
        cursor.execute(sql12)
        columns12 = [column[0] for column in cursor.description]
        result12 = toJson(cursor.fetchall(),columns12)

        sql13 = "SELECT * FROM LanguagesSkill"
        cursor.execute(sql13)
        columns13 = [column[0] for column in cursor.description]
        result13 = toJson(cursor.fetchall(),columns13)

        sql14 = "SELECT * FROM Personal"
        cursor.execute(sql14)
        columns14 = [column[0] for column in cursor.description]
        result14 = toJson(cursor.fetchall(),columns14)

        sql15 = "SELECT * FROM position"
        cursor.execute(sql15)
        columns15 = [column[0] for column in cursor.description]
        result15 = toJson(cursor.fetchall(),columns15)

        sql16 = "SELECT * FROM provinces"
        cursor.execute(sql16)
        columns16 = [column[0] for column in cursor.description]
        result16 = toJson(cursor.fetchall(),columns16)

        sql17 = "SELECT * FROM Reference"
        cursor.execute(sql17)
        columns17 = [column[0] for column in cursor.description]
        result17 = toJson(cursor.fetchall(),columns17)

        sql18 = "SELECT * FROM RefPerson"
        cursor.execute(sql18)
        columns18 = [column[0] for column in cursor.description]
        result18 = toJson(cursor.fetchall(),columns18)

        sql20 = "SELECT * FROM SpecialSkill"
        cursor.execute(sql20)
        columns20 = [column[0] for column in cursor.description]
        result20 = toJson(cursor.fetchall(),columns20)

        # sql21 = "SELECT * FROM status"
        # cursor.execute(sql21)
        # columns21 = [column[0] for column in cursor.description]
        # result21 = toJson(cursor.fetchall(),columns21)

        # sql22 = "SELECT * FROM temples"
        # cursor.execute(sql22)
        # columns22 = [column[0] for column in cursor.description]
        # result22 = toJson(cursor.fetchall(),columns22)

        sql23 = "SELECT * FROM TrainingCourse"
        cursor.execute(sql23)
        columns23 = [column[0] for column in cursor.description]
        result23 = toJson(cursor.fetchall(),columns23)

        sql25 = "SELECT * FROM zipcodes"
        cursor.execute(sql25)
        columns25 = [column[0] for column in cursor.description]
        result25 = toJson(cursor.fetchall(),columns25)
        connection.close()

        connection = mysql3.connect()
        cursor = connection.cursor()
        sqlIn = "INSERT INTO Address (EmploymentAppNo,AddressType,HouseNo,Street,DISTRICT_ID,AMPHUR_ID,PROVINCE_ID,PostCode,Tel,Fax) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn,(result[0]['EmploymentAppNo'],result[0]['AddressType'],result[0]['HouseNo'],result[0]['Street'],result[0]['DISTRICT_ID'],result[0]['AMPHUR_ID'],result[0]['PROVINCE_ID'],result[0]['PostCode'],result[0]['Tel'],result[0]['Fax']))

        sqlIn4 = "INSERT INTO Attachment (EmploymentAppNo,Type,PathFile) VALUES (%s,%s,%s)"
        cursor.execute(sqlIn4,(result4[0]['EmploymentAppNo'],result4[0]['Type'],result4[0]['PathFile']))

        sqlIn6 = "INSERT INTO ComputerSkill (EmploymentAppNo,ComSkill,Level) VALUES (%s,%s,%s)"
        cursor.execute(sqlIn6,(result6[0]['EmploymentAppNo'],result6[0]['ComSkill'],result6[0]['Level']))

        sqlIn9 = "INSERT INTO Education (EmploymentAppNo,EducationLevel,Institute,StartYear,EndYear,Qualification,Major,GradeAvg,ExtraCurricularActivities) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn9,(result9[0]['EmploymentAppNo'],result9[0]['EducationLevel'],result9[0]['Institute'],result9[0]['StartYear'],result9[0]['EndYear'],result9[0]['Qualification'],result9[0]['Major'],result9[0]['GradeAvg'],result9[0]['ExtraCurricularActivities']))

        sqlIn10 = "INSERT INTO Employment (EmploymentAppNo,CompanyName,CompanyAddress,PositionHeld,StartSalary,EndSalary,StartYear,EndYear,Responsibility,ReasonOfLeaving,Descriptionofwork) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn10,(result10[0]['EmploymentAppNo'],result10[0]['CompanyName'],result10[0]['CompanyAddress'],result10[0]['PositionHeld'],result10[0]['StartSalary'],result10[0]['EndSalary'],result10[0]['StartYear'],result10[0]['EndYear'], \
        result10[0]['Responsibility'],result10[0]['ReasonOfLeaving'],result10[0]['Descriptionofwork']))

        sqlIn11 = "INSERT INTO Family (EmploymentAppNo,MemberType,Name,Surname,Occupation,Address,Tel,Fax) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn11,(result11[0]['EmploymentAppNo'],result11[0]['MemberType'],result11[0]['Name'],result11[0]['Surname'],result11[0]['Occupation'],result11[0]['Address'],result11[0]['Tel'],result11[0]['Fax']))

        sqlIn13 = "INSERT INTO LanguagesSkill (EmploymentAppNo,Languages,Speaking,Reading,Writting) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn13,(result12[0]['EmploymentAppNo'],result12[0]['Languages'],result12[0]['Speaking'],result12[0]['Reading'],result12[0]['Writting']))

        sqlIn14 = """INSERT INTO Personal (EmploymentAppNo,AppliedPosition1,AppliedPosition2,StartExpectedSalary,EndExpectedSalary,NameTh,SurnameTh,NicknameTh,NameEn,SurnameEn,NicknameEn,Birthdate,BirthPlace,BirthProvince,BirthCountry,Age,Height,Weight,BloodGroup,Citizenship,Religion,ID_CardNo,IssueDate,ExpiryDate,MaritalStatus,NumberOfChildren,StudyChild,MilitaryService,Others,Worktel,Mobile,Email,EmergencyPerson,EmergencyRelation,EmergencyAddress,EmergencyTe,date,status_id) \
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sqlIn14,(result14[0]['EmploymentAppNo'],result14[0]['AppliedPosition1'],result14[0]['AppliedPosition2'],result14[0]['StartExpectedSalary'],result14[0]['EndExpectedSalary'],result14[0]['NameTh'],result14[0]['SurnameTh'],result14[0]['NicknameTh'],result14[0]['NameEn'],result14[0]['SurnameEn'],result14[0]['NicknameEn'],result14[0]['Birthdate'],result14[0]['BirthPlace'],result14[0]['BirthProvince'], \
        result14[0]['BirthCountry'],result14[0]['Age'],result14[0]['Height'],result14[0]['Weight'],result14[0]['BloodGroup'],result14[0]['Citizenship'],result14[0]['Religion'],result14[0]['ID_CardNo'], \
        result14[0]['IssueDate'],result14[0]['ExpiryDate'],result14[0]['MaritalStatus'],result14[0]['NumberOfChildren'],result14[0]['StudyChild'],result14[0]['MilitaryService'],result14[0]['Others'], \
        result14[0]['Worktel'],result14[0]['Mobile'],result14[0]['Email'],result14[0]['EmergencyPerson'],result14[0]['EmergencyRelation'],result14[0]['EmergencyAddress'],result14[0]['EmergencyTe'],result14[0]['date'],result14[0]['status_id']))

        sqlIn17 = "INSERT INTO Reference (EmploymentAppNo,RelativeName,RelativeSurname,RelativePosition,RelativeRelationship,PhysicalHandicap,PhysicalHandicapDetail,KnowFrom) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn17,(result17[0]['EmploymentAppNo'],result17[0]['RelativeName'],result17[0]['RelativeSurname'],result17[0]['RelativePosition'],result17[0]['RelativeRelationship'],result17[0]['PhysicalHandicap'],result17[0]['PhysicalHandicapDetail'],result17[0]['KnowFrom']))

        sqlIn18 = "INSERT INTO RefPerson (EmploymentAppNo,RefName,RefPosition,RefAddress,RefTel) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn18,(result18[0]['EmploymentAppNo'],result18[0]['RefName'],result18[0]['RefPosition'],result18[0]['RefAddress'],result18[0]['RefTel']))

        sqlIn20 = "INSERT INTO SpecialSkill (EmploymentAppNo,CarDrivingLicense,MotorBicycleDrivingLicense,OwnCar,OwnMotorBicycle,WorkUpCountry,StartWorkEarliest,PhysicalDisabilityOrDisease,DischargeFromEmployment,DischargeFromEmploymentReason,Arrested,ArrestedReason) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn20,(result20[0]['EmploymentAppNo'],result20[0]['CarDrivingLicense'],result20[0]['MotorBicycleDrivingLicense'],result20[0]['OwnCar'],result20[0]['OwnMotorBicycle'], \
        result20[0]['WorkUpCountry'],result20[0]['StartWorkEarliest'],result20[0]['PhysicalDisabilityOrDisease'],result20[0]['DischargeFromEmployment'],result20[0]['DischargeFromEmploymentReason'],result20[0]['Arrested'],result20[0]['ArrestedReason']))

        sqlIn23 = "INSERT INTO TrainingCourse (EmploymentAppNo,Subject,Place,StartDate,EndDate) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn23,(result23[0]['EmploymentAppNo'],result23[0]['Subject'],result23[0]['Place'],result23[0]['StartDate'],result23[0]['EndDate']))


        connection.commit()
        connection.close()

        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
