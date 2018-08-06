#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/QryAppform', methods=['POST'])
def QryAppform():
    try:
        connection = mysql3.connect()
        cursor = connection.cursor()
        sql = """SELECT Personal.EmploymentAppNo, Personal.AppliedPosition1, Personal.AppliedPosition2, Personal.StartExpectedSalary, Personal.EndExpectedSalary, Personal.NameTh, Personal.SurnameTh, Personal.Mobile, Personal.Email, Personal.date, status.status_name
        FROM Personal INNER JOIN status ON Personal.status_id = status.status_id ORDER BY Personal.EmploymentAppNo DESC"""
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        connection.close()
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryAppform_Wait_interview', methods=['POST'])
def QryAppform_Wait_interview():
    try:
        connection = mysql3.connect()
        cursor = connection.cursor()
        sql = """SELECT Personal.EmploymentAppNo, Personal.AppliedPosition1, Personal.AppliedPosition2, Personal.StartExpectedSalary, Personal.EndExpectedSalary, Personal.NameTh, Personal.SurnameTh, Personal.Mobile, Personal.Email, Personal.date, status.status_name
        FROM Personal INNER JOIN status ON Personal.status_id = status.status_id WHERE status.status_id='1' ORDER BY Personal.EmploymentAppNo DESC"""
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        connection.close()
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryAppform_Come_interview', methods=['POST'])
def QryAppform_Come_interview():
    try:
        connection = mysql3.connect()
        cursor = connection.cursor()
        sql = """SELECT Personal.EmploymentAppNo, Personal.AppliedPosition1, Personal.AppliedPosition2, Personal.StartExpectedSalary, Personal.EndExpectedSalary, Personal.NameTh, Personal.SurnameTh, Personal.Mobile, Personal.Email, Personal.date, status.status_name
        FROM Personal INNER JOIN status ON Personal.status_id = status.status_id WHERE status.status_id='2' ORDER BY Personal.EmploymentAppNo DESC"""
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        connection.close()
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryAppform_Pass_interview', methods=['POST'])
def QryAppform_Pass_interview():
    try:
        connection = mysql3.connect()
        cursor = connection.cursor()
        sql = """SELECT Personal.EmploymentAppNo, Personal.AppliedPosition1, Personal.AppliedPosition2, Personal.StartExpectedSalary, Personal.EndExpectedSalary, Personal.NameTh, Personal.SurnameTh, Personal.Mobile, Personal.Email, Personal.date, status.status_name
        FROM Personal INNER JOIN status ON Personal.status_id = status.status_id WHERE status.status_id='3' ORDER BY Personal.EmploymentAppNo DESC"""
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        connection.close()
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryAppform_Notpass_interview', methods=['POST'])
def QryAppform_Notpass_interview():
    try:
        connection = mysql3.connect()
        cursor = connection.cursor()
        sql = """SELECT Personal.EmploymentAppNo, Personal.AppliedPosition1, Personal.AppliedPosition2, Personal.StartExpectedSalary, Personal.EndExpectedSalary, Personal.NameTh, Personal.SurnameTh, Personal.Mobile, Personal.Email, Personal.date, status.status_name
        FROM Personal INNER JOIN status ON Personal.status_id = status.status_id WHERE status.status_id='4' ORDER BY Personal.EmploymentAppNo DESC"""
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        connection.close()
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/UpdateEmpStatus', methods=['POST'])
@connect_sql3()
def UpdateEmpStatus(cursor):
    try:
        data = request.json
        source = data['source']
        data_new = source
        status_id = data_new['status_id']
        EmploymentAppNo = data_new['EmploymentAppNo']
        sqlUp = "UPDATE Personal SET status_id = %s WHERE EmploymentAppNo = %s"
        cursor.execute(sqlUp,(status_id, EmploymentAppNo))
        return "success"
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
        sqlblack = "SELECT citizenid FROM blacklist"
        cursor.execute(sqlblack)
        columnsblack = [column[0] for column in cursor.description]
        resultblacklist = toJson(cursor.fetchall(),columnsblack)
        connection.commit()
        connection.close()
        if result14[0]['ID_CardNo']==resultblacklist[0]['citizenid']:
            print("Person is blacklist")
        else:
            connection = mysql4.connect()
            cursor = connection.cursor()
            i=0
            for i in xrange(len(result)):
                sqlIn = "INSERT INTO Address (EmploymentAppNo,ID_CardNo,AddressType,HouseNo,Street,DISTRICT_ID,AMPHUR_ID,PROVINCE_ID,PostCode,Tel,Fax) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn,(result[i]['EmploymentAppNo'],result[i]['ID_CardNo'],result[i]['AddressType'],result[i]['HouseNo'],
                result[i]['Street'],result[i]['DISTRICT_NAME'],result[i]['AMPHUR_NAME'],result[i]['PROVINCE_NAME'],result[i]['PostCode'],result[i]['Tel'],result[i]['Fax']))
            i=0
            for i in xrange(len(result4)):
                sqlIn4 = "INSERT INTO Attachment (EmploymentAppNo,ID_CardNo,Type,PathFile) VALUES (%s,%s,%s,%s)"
                cursor.execute(sqlIn4,(result4[i]['EmploymentAppNo'],result4[i]['ID_CardNo'],result4[i]['Type'],result4[i]['PathFile']))
            i=0
            for i in xrange(len(result6)):
                sqlIn6 = "INSERT INTO ComputerSkill (EmploymentAppNo,ID_CardNo,ComSkill,Level) VALUES (%s,%s,%s,%s)"
                cursor.execute(sqlIn6,(result6[i]['EmploymentAppNo'],result6[i]['ID_CardNo'],result6[i]['ComSkill'],result6[i]['Level']))
            i=0
            for i in xrange(len(result9)):
                sqlIn9 = "INSERT INTO Education (EmploymentAppNo,ID_CardNo,EducationLevel,Institute,StartYear,EndYear,Qualification,Major,GradeAvg,ExtraCurricularActivities) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn9,(result9[i]['EmploymentAppNo'],result9[i]['ID_CardNo'],result9[i]['EducationLevel'],result9[i]['Institute'],result9[i]['StartYear'],result9[i]['EndYear'],result9[i]['Qualification'],result9[i]['Major'],result9[i]['GradeAvg'],result9[i]['ExtraCurricularActivities']))
            i=0
            for i in xrange(len(result11)):
                sqlIn11 = "INSERT INTO Family (EmploymentAppNo,ID_CardNo,MemberType,Name,Surname,Occupation,Address,Tel,Fax) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn11,(result11[i]['EmploymentAppNo'],result11[i]['ID_CardNo'],result11[i]['MemberType'],result11[i]['Name'],result11[i]['Surname'],result11[i]['Occupation'],result11[i]['Address'],result11[i]['Tel'],result11[i]['Fax']))
            i=0
            for i in xrange(len(result13)):
                sqlIn13 = "INSERT INTO LanguagesSkill (EmploymentAppNo,ID_CardNo,Languages,Speaking,Reading,Writting) VALUES (%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn13,(result13[i]['EmploymentAppNo'],result13[i]['ID_CardNo'],result13[i]['Languages'],result13[i]['Speaking'],result13[i]['Reading'],result13[i]['Writting']))

            sqlIn14 = """INSERT INTO Personal (EmploymentAppNo,AppliedPosition1,AppliedPosition2,StartExpectedSalary,EndExpectedSalary,NameTh,SurnameTh,NicknameTh,NameEn,SurnameEn,NicknameEn,Birthdate,BirthPlace,BirthProvince,BirthCountry,Age,Height,Weight,BloodGroup,Citizenship,Religion,ID_CardNo,IssueDate,ExpiryDate,MaritalStatus,NumberOfChildren,StudyChild,MilitaryService,Others,Worktel,Mobile,Email,EmergencyPerson,EmergencyRelation,EmergencyAddress,EmergencyTel,date) \
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(sqlIn14,(result14[0]['EmploymentAppNo'],result14[0]['AppliedPosition1'],result14[0]['AppliedPosition2'],result14[0]['StartExpectedSalary'],result14[0]['EndExpectedSalary'],result14[0]['NameTh'],result14[0]['SurnameTh'],result14[0]['NicknameTh'],result14[0]['NameEn'],result14[0]['SurnameEn'],result14[0]['NicknameEn'],result14[0]['Birthdate'],result14[0]['BirthPlace'],result14[0]['BirthProvince'], \
            result14[0]['BirthCountry'],result14[0]['Age'],result14[0]['Height'],result14[0]['Weight'],result14[0]['BloodGroup'],result14[0]['Citizenship'],result14[0]['Religion'],result14[0]['ID_CardNo'], \
            result14[0]['IssueDate'],result14[0]['ExpiryDate'],result14[0]['MaritalStatus'],result14[0]['NumberOfChildren'],result14[0]['StudyChild'],result14[0]['MilitaryService'],result14[0]['Others'], \
            result14[0]['Worktel'],result14[0]['Mobile'],result14[0]['Email'],result14[0]['EmergencyPerson'],result14[0]['EmergencyRelation'],result14[0]['EmergencyAddress'],result14[0]['EmergencyTel'],result14[0]['date']))
            i=0
            for i in xrange(len(result17)):
                sqlIn17 = "INSERT INTO Reference (EmploymentAppNo,ID_CardNo,RelativeName,RelativeSurname,RelativePosition,RelativeRelationship,PhysicalHandicap,PhysicalHandicapDetail,KnowFrom) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn17,(result17[i]['EmploymentAppNo'],result17[i]['ID_CardNo'],result17[i]['RelativeName'],result17[i]['RelativeSurname'],result17[i]['RelativePosition'],result17[i]['RelativeRelationship'],result17[i]['PhysicalHandicap'],result17[i]['PhysicalHandicapDetail'],result17[i]['KnowFrom']))
            i=0
            for i in xrange(len(result18)):
                sqlIn18 = "INSERT INTO RefPerson (EmploymentAppNo,ID_CardNo,RefName,RefPosition,RefAddress,RefTel) VALUES (%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn18,(result18[i]['EmploymentAppNo'],result18[i]['ID_CardNo'],result18[i]['RefName'],result18[i]['RefPosition'],result18[i]['RefAddress'],result18[i]['RefTel']))
            i=0
            for i in xrange(len(result20)):
                sqlIn20 = "INSERT INTO SpecialSkill (EmploymentAppNo,ID_CardNo,CarDrivingLicense,MotorBicycleDrivingLicense,OwnCar,OwnMotorBicycle,WorkUpCountry,StartWorkEarliest,PhysicalDisabilityOrDisease,DischargeFromEmployment,DischargeFromEmploymentReason,Arrested,ArrestedReason) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn20,(result20[i]['EmploymentAppNo'],result20[i]['ID_CardNo'],result20[i]['CarDrivingLicense'],result20[i]['MotorBicycleDrivingLicense'],result20[i]['OwnCar'],result20[i]['OwnMotorBicycle'], \
                result20[i]['WorkUpCountry'],result20[i]['StartWorkEarliest'],result20[i]['PhysicalDisabilityOrDisease'],result20[i]['DischargeFromEmployment'],result20[i]['DischargeFromEmploymentReason'],result20[i]['Arrested'],result20[i]['ArrestedReason']))
            try:
                i=0
                for i in xrange(len(result10)):
                    sqlIn10 = "INSERT INTO Employment (EmploymentAppNo,ID_CardNo,CompanyName,CompanyAddress,PositionHeld,StartSalary,EndSalary,StartYear,EndYear,Responsibility,ReasonOfLeaving,Descriptionofwork) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sqlIn10,(result10[i]['EmploymentAppNo'],result10[i]['ID_CardNo'],result10[i]['CompanyName'],result10[i]['CompanyAddress'],result10[i]['PositionHeld'],result10[i]['StartSalary'],result10[i]['EndSalary'],result10[i]['StartYear'],result10[i]['EndYear'], \
                    result10[i]['Responsibility'],result10[i]['ReasonOfLeaving'],result10[i]['Descriptionofwork']))
            except Exception as e:
                logserver(e)
            try:
                i=0
                for i in xrange(len(result23)):
                    sqlIn23 = "INSERT INTO TrainingCourse(EmploymentAppNo,ID_CardNo,Subject,Place,StartDate,EndDate) VALUES (%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sqlIn23,(result23[i]['EmploymentAppNo'],result23[i]['ID_CardNo'],result23[i]['Subject'],result23[i]['Place'],result23[i]['StartDate'],result23[i]['EndDate']))
            except Exception as e:
                logserver(e)
        connection.commit()
        connection.close()
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
