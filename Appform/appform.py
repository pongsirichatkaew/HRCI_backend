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
        sqlEm = "SELECT * FROM Address INNER JOIN provinces ON provinces.PROVINCE_ID=Address.PROVINCE_ID \
                                       INNER JOIN amphures ON amphures.AMPHUR_ID=Address.AMPHUR_ID \
                                       INNER JOIN districts ON districts.DISTRICT_CODE=Address.DISTRICT_ID \
                 WHERE EmploymentAppNo=%s"
        cursor.execute(sqlEm,dataInput['EmploymentAppNo'])
        columnsEm = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columnsEm)

        sql4 = "SELECT * FROM Attachment INNER JOIN Personal ON Personal.EmploymentAppNo=Attachment.EmploymentAppNo \
         WHERE EmploymentAppNo=%s"
        cursor.execute(sql4,dataInput['EmploymentAppNo'])
        columns4 = [column[0] for column in cursor.description]
        result4 = toJson(cursor.fetchall(),columns4)

        sql6 = "SELECT * FROM ComputerSkill INNER JOIN Personal ON Personal.EmploymentAppNo=ComputerSkill.EmploymentAppNo \
        WHERE EmploymentAppNo=%s"
        cursor.execute(sql6,dataInput['EmploymentAppNo'])
        columns6 = [column[0] for column in cursor.description]
        result6 = toJson(cursor.fetchall(),columns6)

        sql9 = "SELECT * FROM Education INNER JOIN Personal ON Personal.EmploymentAppNo=Education.EmploymentAppNo \
        WHERE EmploymentAppNo=%s"
        cursor.execute(sql9,dataInput['EmploymentAppNo'])
        columns9 = [column[0] for column in cursor.description]
        result9 = toJson(cursor.fetchall(),columns9)

        sql10 = "SELECT * FROM Employment INNER JOIN Personal ON Personal.EmploymentAppNo=Employment.EmploymentAppNo \
        WHERE EmploymentAppNo=%s"
        cursor.execute(sql10,dataInput['EmploymentAppNo'])
        columns10 = [column[0] for column in cursor.description]
        result10 = toJson(cursor.fetchall(),columns10)

        sql11 = "SELECT * FROM Family INNER JOIN Personal ON Personal.EmploymentAppNo=Family.EmploymentAppNo \
        WHERE EmploymentAppNo=%s"
        cursor.execute(sql11,dataInput['EmploymentAppNo'])
        columns11 = [column[0] for column in cursor.description]
        result11 = toJson(cursor.fetchall(),columns11)

        sql13 = "SELECT * FROM LanguagesSkill INNER JOIN Personal ON Personal.EmploymentAppNo=LanguagesSkill.EmploymentAppNo \
        WHERE EmploymentAppNo=%s"
        cursor.execute(sql13,dataInput['EmploymentAppNo'])
        columns13 = [column[0] for column in cursor.description]
        result13 = toJson(cursor.fetchall(),columns13)

        sql14 = "SELECT * FROM Personal \
        WHERE EmploymentAppNo=%s"
        cursor.execute(sql14,dataInput['EmploymentAppNo'])
        columns14 = [column[0] for column in cursor.description]
        result14 = toJson(cursor.fetchall(),columns14)

        sql17 = "SELECT * FROM Reference INNER JOIN Personal ON Personal.EmploymentAppNo=Reference.EmploymentAppNo \
        WHERE EmploymentAppNo=%s"
        cursor.execute(sql17,dataInput['EmploymentAppNo'])
        columns17 = [column[0] for column in cursor.description]
        result17 = toJson(cursor.fetchall(),columns17)

        sql18 = "SELECT * FROM RefPerson INNER JOIN Personal ON Personal.EmploymentAppNo=RefPerson.EmploymentAppNo \
        WHERE EmploymentAppNo=%s"
        cursor.execute(sql18,dataInput['EmploymentAppNo'])
        columns18 = [column[0] for column in cursor.description]
        result18 = toJson(cursor.fetchall(),columns18)

        sql20 = "SELECT * FROM SpecialSkill INNER JOIN Personal ON Personal.EmploymentAppNo=SpecialSkill.EmploymentAppNo \
        WHERE EmploymentAppNo=%s"
        cursor.execute(sql20,dataInput['EmploymentAppNo'])
        columns20 = [column[0] for column in cursor.description]
        result20 = toJson(cursor.fetchall(),columns20)

        sql23 = "SELECT * FROM TrainingCourse INNER JOIN Personal ON Personal.EmploymentAppNo=TrainingCourse.EmploymentAppNo \
        WHERE EmploymentAppNo=%s"
        cursor.execute(sql23,dataInput['EmploymentAppNo'])
        columns23 = [column[0] for column in cursor.description]
        result23 = toJson(cursor.fetchall(),columns23)
        connection.commit()
        connection.close()

        connection = mysql4.connect()
        cursor = connection.cursor()
        sqlIn = "INSERT INTO Address (EmploymentAppNo,ID_CardNo,AddressType,HouseNo,Street,DISTRICT_ID,AMPHUR_ID,PROVINCE_ID,PostCode,Tel,Fax) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn,(result[0]['EmploymentAppNo'],result[0]['ID_CardNo'],result[0]['AddressType'],result[0]['HouseNo'], \
         result[0]['Street'],result[0]['DISTRICT_NAME'],result[0]['AMPHUR_NAME'],result[0]['PROVINCE_NAME'],result[0]['PostCode'],result[0]['Tel'],result[0]['Fax']))

        sqlIn4 = "INSERT INTO Attachment (EmploymentAppNo,ID_CardNo,Type,PathFile) VALUES (%s,%s,%s)"
        cursor.execute(sqlIn4,(result4[0]['EmploymentAppNo'],result4[0]['ID_CardNo'],result4[0]['Type'],result4[0]['PathFile']))

        sqlIn6 = "INSERT INTO ComputerSkill (EmploymentAppNo,ID_CardNo,ComSkill,Level) VALUES (%s,%s,%s)"
        cursor.execute(sqlIn6,(result6[0]['EmploymentAppNo'],result6[0]['ID_CardNo'],result6[0]['ComSkill'],result6[0]['Level']))

        sqlIn9 = "INSERT INTO Education (EmploymentAppNo,ID_CardNo,EducationLevel,Institute,StartYear,EndYear,Qualification,Major,GradeAvg,ExtraCurricularActivities) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn9,(result9[0]['EmploymentAppNo'],result9[0]['ID_CardNo'],result9[0]['EducationLevel'],result9[0]['Institute'],result9[0]['StartYear'],result9[0]['EndYear'],result9[0]['Qualification'],result9[0]['Major'],result9[0]['GradeAvg'],result9[0]['ExtraCurricularActivities']))

        sqlIn11 = "INSERT INTO Family (EmploymentAppNo,ID_CardNo,MemberType,Name,Surname,Occupation,Address,Tel,Fax) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn11,(result11[0]['EmploymentAppNo'],result11[0]['ID_CardNo'],result11[0]['MemberType'],result11[0]['Name'],result11[0]['Surname'],result11[0]['Occupation'],result11[0]['Address'],result11[0]['Tel'],result11[0]['Fax']))

        sqlIn13 = "INSERT INTO LanguagesSkill (EmploymentAppNo,ID_CardNo,Languages,Speaking,Reading,Writting) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn13,(result13[0]['EmploymentAppNo'],result13[0]['ID_CardNo'],result13[0]['Languages'],result13[0]['Speaking'],result13[0]['Reading'],result13[0]['Writting']))

        sqlIn14 = """INSERT INTO Personal (EmploymentAppNo,AppliedPosition1,AppliedPosition2,StartExpectedSalary,EndExpectedSalary,NameTh,SurnameTh,NicknameTh,NameEn,SurnameEn,NicknameEn,Birthdate,BirthPlace,BirthProvince,BirthCountry,Age,Height,Weight,BloodGroup,Citizenship,Religion,ID_CardNo,IssueDate,ExpiryDate,MaritalStatus,NumberOfChildren,StudyChild,MilitaryService,Others,Worktel,Mobile,Email,EmergencyPerson,EmergencyRelation,EmergencyAddress,EmergencyTel,date) \
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sqlIn14,(result14[0]['EmploymentAppNo'],result14[0]['AppliedPosition1'],result14[0]['AppliedPosition2'],result14[0]['StartExpectedSalary'],result14[0]['EndExpectedSalary'],result14[0]['NameTh'],result14[0]['SurnameTh'],result14[0]['NicknameTh'],result14[0]['NameEn'],result14[0]['SurnameEn'],result14[0]['NicknameEn'],result14[0]['Birthdate'],result14[0]['BirthPlace'],result14[0]['BirthProvince'], \
        result14[0]['BirthCountry'],result14[0]['Age'],result14[0]['Height'],result14[0]['Weight'],result14[0]['BloodGroup'],result14[0]['Citizenship'],result14[0]['Religion'],result14[0]['ID_CardNo'], \
        result14[0]['IssueDate'],result14[0]['ExpiryDate'],result14[0]['MaritalStatus'],result14[0]['NumberOfChildren'],result14[0]['StudyChild'],result14[0]['MilitaryService'],result14[0]['Others'], \
        result14[0]['Worktel'],result14[0]['Mobile'],result14[0]['Email'],result14[0]['EmergencyPerson'],result14[0]['EmergencyRelation'],result14[0]['EmergencyAddress'],result14[0]['EmergencyTel'],result14[0]['date']))

        sqlIn17 = "INSERT INTO Reference (EmploymentAppNo,ID_CardNo,RelativeName,RelativeSurname,RelativePosition,RelativeRelationship,PhysicalHandicap,PhysicalHandicapDetail,KnowFrom) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn17,(result17[0]['EmploymentAppNo'],result17[0]['ID_CardNo'],result17[0]['RelativeName'],result17[0]['RelativeSurname'],result17[0]['RelativePosition'],result17[0]['RelativeRelationship'],result17[0]['PhysicalHandicap'],result17[0]['PhysicalHandicapDetail'],result17[0]['KnowFrom']))

        sqlIn18 = "INSERT INTO RefPerson (EmploymentAppNo,ID_CardNo,RefName,RefPosition,RefAddress,RefTel) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn18,(result18[0]['EmploymentAppNo'],result18[0]['ID_CardNo'],result18[0]['RefName'],result18[0]['RefPosition'],result18[0]['RefAddress'],result18[0]['RefTel']))

        sqlIn20 = "INSERT INTO SpecialSkill (EmploymentAppNo,ID_CardNo,CarDrivingLicense,MotorBicycleDrivingLicense,OwnCar,OwnMotorBicycle,WorkUpCountry,StartWorkEarliest,PhysicalDisabilityOrDisease,DischargeFromEmployment,DischargeFromEmploymentReason,Arrested,ArrestedReason) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn20,(result20[0]['EmploymentAppNo'],result20[0]['ID_CardNo'],result20[0]['CarDrivingLicense'],result20[0]['MotorBicycleDrivingLicense'],result20[0]['OwnCar'],result20[0]['OwnMotorBicycle'], \
        result20[0]['WorkUpCountry'],result20[0]['StartWorkEarliest'],result20[0]['PhysicalDisabilityOrDisease'],result20[0]['DischargeFromEmployment'],result20[0]['DischargeFromEmploymentReason'],result20[0]['Arrested'],result20[0]['ArrestedReason']))
        try:
            sqlIn10 = "INSERT INTO Employment (EmploymentAppNo,ID_CardNo,CompanyName,CompanyAddress,PositionHeld,StartSalary,EndSalary,StartYear,EndYear,Responsibility,ReasonOfLeaving,Descriptionofwork) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn10,(result10[0]['EmploymentAppNo'],result10[0]['ID_CardNo'],result10[0]['CompanyName'],result10[0]['CompanyAddress'],result10[0]['PositionHeld'],result10[0]['StartSalary'],result10[0]['EndSalary'],result10[0]['StartYear'],result10[0]['EndYear'], \
            result10[0]['Responsibility'],result10[0]['ReasonOfLeaving'],result10[0]['Descriptionofwork']))
        except Exception as e:
            logserver(e)
        try:
            sqlIn23 = "INSERT INTO TrainingCourse(EmploymentAppNo,ID_CardNo,Subject,Place,StartDate,EndDate) VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn23,(result23[0]['EmploymentAppNo'],result23[0]['ID_CardNo'],result23[0]['Subject'],result23[0]['Place'],result23[0]['StartDate'],result23[0]['EndDate']))
        except Exception as e:
            logserver(e)
        connection.commit()
        connection.close()
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
