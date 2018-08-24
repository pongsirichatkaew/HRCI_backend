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
                WHERE employee.validstatus='1'"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        connection.close()
        return jsonify(result)
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
                WHERE employee.employeeid=%s"
        cursor.execute(sqlEmployee,data_new['employeeid'])
        columnsEmployee = [column[0] for column in cursor.description]
        resultEmployee = toJson(cursor.fetchall(),columnsEmployee)

        sqlEm = "SELECT Address.AddressType,Address.HouseNo,Address.Street,Address.PostCode,Address.Tel,Address.Fax,amphures.AMPHUR_CODE,amphures.AMPHUR_NAME,provinces.PROVINCE_NAME,districts.DISTRICT_CODE,districts.DISTRICT_NAME FROM Address INNER JOIN provinces ON provinces.PROVINCE_ID=Address.PROVINCE_ID \
                                           INNER JOIN amphures ON amphures.AMPHUR_ID=Address.AMPHUR_ID \
                                           INNER JOIN districts ON districts.DISTRICT_CODE=Address.DISTRICT_ID \
                                           INNER JOIN Personal ON Personal.ID_CardNo=Address.ID_CardNo \
                     WHERE Personal.ID_CardNo=%s"
        cursor.execute(sqlEm,resultEmployee['citizenid'])
        columnsEm = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columnsEm)

        sql4 = "SELECT Attachment.Type,Attachment.PathFile FROM Attachment INNER JOIN Personal ON Personal.ID_CardNo=Attachment.ID_CardNo \
        WHERE Personal.ID_CardNo=%s"
        cursor.execute(sql4,resultEmployee['citizenid'])
        columns4 = [column[0] for column in cursor.description]
        result4 = toJson(cursor.fetchall(),columns4)

        sql6 = "SELECT ComputerSkill.ComSkill,ComputerSkill.Level FROM ComputerSkill INNER JOIN Personal ON Personal.ID_CardNo=ComputerSkill.ID_CardNo \
        WHERE Personal.ID_CardNo=%s"
        cursor.execute(sql6,resultEmployee['citizenid'])
        columns6 = [column[0] for column in cursor.description]
        result6 = toJson(cursor.fetchall(),columns6)

        sql9 = "SELECT Education.EducationLevel,Education.Institute,Education.StartYear,Education.EndYear,Education.Qualification,Education.Major,Education.GradeAvg,Education.ExtraCurricularActivities FROM Education INNER JOIN Personal ON Personal.ID_CardNo=Education.ID_CardNo \
        WHERE Personal.ID_CardNo=%s"
        cursor.execute(sql9,resultEmployee['citizenid'])
        columns9 = [column[0] for column in cursor.description]
        result9 = toJson(cursor.fetchall(),columns9)

        sql10 = "SELECT Employment.CompanyName,Employment.CompanyAddress,Employment.PositionHeld,Employment.StartSalary,Employment.EndSalary,Employment.StartYear,Employment.EndYear,Employment.Responsibility,Employment.ReasonOfLeaving,Employment.Descriptionofwork FROM Employment INNER JOIN Personal ON Personal.ID_CardNo=Employment.ID_CardNo \
        WHERE Personal.ID_CardNo=%s"
        cursor.execute(sql10,resultEmployee['citizenid'])
        columns10 = [column[0] for column in cursor.description]
        result10 = toJson(cursor.fetchall(),columns10)

        sqlfa = "SELECT Family.MemberType,Family.Name,Family.Surname,Family.Occupation,Family.Address,Family.Tel,Family.Fax FROM Family INNER JOIN Personal ON Personal.ID_CardNo=Family.ID_CardNo \
        WHERE (Family.MemberType = 'Father' OR Family.MemberType = 'Mother')AND Personal.ID_CardNo=%s"
        cursor.execute(sqlfa,resultEmployee['citizenid'])
        columnsfa = [column[0] for column in cursor.description]
        resultfa = toJson(cursor.fetchall(),columnsfa)

        sqlbro = "SELECT Family.MemberType,Family.Name,Family.Surname,Family.Occupation,Family.Address,Family.Tel,Family.Fax FROM Family INNER JOIN Personal ON Personal.ID_CardNo=Family.ID_CardNo \
        WHERE Family.MemberType = 'BrotherSister' AND Personal.ID_CardNo=%s"
        cursor.execute(sqlbro,resultEmployee['citizenid'])
        columnsbro = [column[0] for column in cursor.description]
        resultbro = toJson(cursor.fetchall(),columnsbro)

        sql13 = "SELECT LanguagesSkill.Languages,LanguagesSkill.Speaking,LanguagesSkill.Reading,LanguagesSkill.Writting FROM LanguagesSkill INNER JOIN Personal ON Personal.ID_CardNo=LanguagesSkill.ID_CardNo \
        WHERE Personal.ID_CardNo=%s"
        cursor.execute(sql13,resultEmployee['citizenid'])
        columns13 = [column[0] for column in cursor.description]
        result13 = toJson(cursor.fetchall(),columns13)

        sql14 = "SELECT * FROM Personal \
        WHERE Personal.ID_CardNo=%s"
        cursor.execute(sql14,resultEmployee['citizenid'])
        columns14 = [column[0] for column in cursor.description]
        result14 = toJson(cursor.fetchall(),columns14)

        # try:
        #     sqlPath = "SELECT PathFile FROM Attachment \
        #     WHERE ID_CardNo=%s AND Type='profile_image'"
        #     cursor.execute(sqlPath,resultEmployee['citizenid'])
        #     columnsPath = [column[0] for column in cursor.description]
        #     resulPath = toJson(cursor.fetchall(),columnsPath)
        #     test=str("http://career.inet.co.th/"+str(resulPath[0]['PathFile']))
        #     # with open(test, 'rb') as image_file:
        #     #     encoded_Image = base64.b64encode(image_file.read())
        #     encoded_Image = base64.b64encode(test)
        # except Exception as e:
        #     encoded_Image="No images"

        sql17 = "SELECT Reference.RelativeName,Reference.RelativeSurname,Reference.RelativePosition,Reference.RelativeRelationship,Reference.PhysicalHandicap,Reference.PhysicalHandicapDetail,Reference.KnowFrom FROM Reference INNER JOIN Personal ON Personal.ID_CardNo=Reference.ID_CardNo \
        WHERE Personal.ID_CardNo=%s"
        cursor.execute(sql17,resultEmployee['citizenid'])
        columns17 = [column[0] for column in cursor.description]
        result17 = toJson(cursor.fetchall(),columns17)

        sql18 = "SELECT RefPerson.RefName,RefPerson.RefPosition,RefPerson.RefAddress,RefPerson.RefTel FROM RefPerson INNER JOIN Personal ON Personal.ID_CardNo=RefPerson.ID_CardNo \
        WHERE Personal.ID_CardNo=%s"
        cursor.execute(sql18,resultEmployee['citizenid'])
        columns18 = [column[0] for column in cursor.description]
        result18 = toJson(cursor.fetchall(),columns18)

        sql20 = "SELECT SpecialSkill.CarDrivingLicense,SpecialSkill.MotorBicycleDrivingLicense,SpecialSkill.OwnCar,SpecialSkill.OwnMotorBicycle,SpecialSkill.WorkUpCountry,SpecialSkill.StartWorkEarliest,SpecialSkill.PhysicalDisabilityOrDisease,SpecialSkill.DischargeFromEmployment,SpecialSkill.DischargeFromEmploymentReason,SpecialSkill.Arrested,SpecialSkill.ArrestedReason FROM SpecialSkill INNER JOIN Personal ON Personal.ID_CardNo=SpecialSkill.ID_CardNo \
        WHERE Personal.ID_CardNo=%s"
        cursor.execute(sql20,resultEmployee['citizenid'])
        columns20 = [column[0] for column in cursor.description]
        result20 = toJson(cursor.fetchall(),columns20)

        sql23 = "SELECT TrainingCourse.Subject,TrainingCourse.Place,TrainingCourse.StartDate,TrainingCourse.EndDate FROM TrainingCourse INNER JOIN Personal ON Personal.ID_CardNo=TrainingCourse.ID_CardNo \
        WHERE Personal.ID_CardNo=%s"
        cursor.execute(sql23,resultEmployee['citizenid'])
        columns23 = [column[0] for column in cursor.description]
        result23 = toJson(cursor.fetchall(),columns23)
        arr={}
        arr["Address"] = result
        arr["employee"] = resultEmployee
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
@app.route('/EditEmployee', methods=['POST'])
@connect_sql()
def EditEmployee(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT citizenid FROM employee WHERE employeeid=%s"
        cursor.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sqlIn = "UPDATE Address SET(validstatus=0,ID_CardNo,AddressType,HouseNo,Street,DISTRICT_ID,AMPHUR_ID,PROVINCE_ID,PostCode,Tel,Fax) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) WHERE ID_CardNo=%s"
        cursor.execute(sqlIn,(data_new['ID_CardNo'],data_new['AddressType'],data_new['HouseNo'],
        data_new['Street'],data_new['DISTRICT_NAME'],data_new['AMPHUR_NAME'],data_new['PROVINCE_NAME'],data_new['PostCode'],data_new['Tel'],data_new['Fax'],result[0]['citizenid']))

        sqlI6de = "DELETE FROM ComputerSkill WHERE citizenid=%s"
        cursor.execute(sqlI6de,result[0]['citizenid'])
        i=0
        for i in xrange(len(data_new['ComSkill'])):
            sqlIn6 = "INSERT INTO ComputerSkill (ID_CardNo,ComSkill,Level) VALUES (%s,%s,%s)"
            cursor.execute(sqlIn6,(data_new[i]['ID_CardNo'],data_new[i]['ComSkill'],data_new[i]['Level']))

        sqlI9de = "DELETE FROM Education WHERE citizenid=%s"
        cursor.execute(sqlI9de,result[0]['citizenid'])
        i=0
        for i in xrange(len(data_new['EducationLevel'])):
            sqlIn9 = "INSERT INTO Education (ID_CardNo,EducationLevel,Institute,StartYear,EndYear,Qualification,Major,GradeAvg,ExtraCurricularActivities) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn9,(data_new[i]['ID_CardNo'],data_new[i]['EducationLevel'],data_new[i]['Institute'],data_new[i]['StartYear'],data_new[i]['EndYear'],data_new[i]['Qualification'],\
            data_new[i]['Major'],data_new[i]['GradeAvg'],data_new[i]['ExtraCurricularActivities']))

        sqlIn11 = "INSERT INTO Family (ID_CardNo,MemberType,Name,Surname,Occupation,Address,Tel,Fax) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn11,(data_new[i]['ID_CardNo'],data_new[i]['MemberType'],data_new[i]['Name'],data_new[i]['Surname'],data_new[i]['Occupation'],data_new[i]['Address'],data_new[i]['Tel'],data_new[i]['Fax']))
        i=0
        for i in xrange(len(data_new)):
            sqlIn13 = "INSERT INTO LanguagesSkill (ID_CardNo,Languages,Speaking,Reading,Writting) VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn13,(data_new[i]['ID_CardNo'],data_new[i]['Languages'],data_new[i]['Speaking'],data_new[i]['Reading'],data_new[i]['Writting']))

        sqlIn14 = """INSERT INTO Personal (NameTh,SurnameTh,NicknameTh,NameEn,SurnameEn,NicknameEn,Birthdate,BirthPlace,BirthProvince,BirthCountry,Age,Height,Weight,BloodGroup,Citizenship,Religion,ID_CardNo,IssueDate,ExpiryDate,MaritalStatus,NumberOfChildren,StudyChild,MilitaryService,Others,Worktel,Mobile,Email,EmergencyPerson,EmergencyRelation,EmergencyAddress,EmergencyTel,date) \
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sqlIn14,(data_new['NameTh'],data_new['SurnameTh'],data_new['NicknameTh'],data_new['NameEn'],\
        data_new['SurnameEn'],data_new['NicknameEn'],data_new['Birthdate'],data_new['BirthPlace'],data_new['BirthProvince'], \
        data_new['BirthCountry'],data_new['Age'],data_new['Height'],data_new['Weight'],data_new['BloodGroup'],data_new['Citizenship'],data_new['Religion'],data_new['ID_CardNo'], \
        data_new['IssueDate'],data_new['ExpiryDate'],data_new['MaritalStatus'],data_new['NumberOfChildren'],data_new['StudyChild'],data_new['MilitaryService'],data_new['Others'], \
        data_new['Worktel'],data_new['Mobile'],data_new['Email'],data_new['EmergencyPerson'],data_new['EmergencyRelation'],data_new['EmergencyAddress'],data_new['EmergencyTel'],data_new['date']))

        sqlI7de = "DELETE FROM Reference WHERE citizenid=%s"
        cursor.execute(sqlI7de,result[0]['citizenid'])
        i=0
        for i in xrange(len(data_new['RelativeName'])):
            sqlIn17 = "INSERT INTO Reference (ID_CardNo,RelativeName,RelativeSurname,RelativePosition,RelativeRelationship,PhysicalHandicap,PhysicalHandicapDetail,KnowFrom) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn17,(data_new[i]['ID_CardNo'],data_new[i]['RelativeName'],data_new[i]['RelativeSurname'],data_new[i]['RelativePosition'],data_new[i]['RelativeRelationship'],data_new[i]['PhysicalHandicap'],data_new[i]['PhysicalHandicapDetail'],data_new[i]['KnowFrom']))

        sqlI8de = "DELETE FROM RefPerson WHERE citizenid=%s"
        cursor.execute(sqlI8de,result[0]['citizenid'])
        i=0
        for i in xrange(len(data_new['RefName'])):
            sqlIn18 = "INSERT INTO RefPerson (ID_CardNo,RefName,RefPosition,RefAddress,RefTel) VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn18,(data_new[i]['ID_CardNo'],data_new[i]['RefName'],data_new[i]['RefPosition'],data_new[i]['RefAddress'],data_new[i]['RefTel']))

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
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/InsertEmployeeHRCI_Management', methods=['POST'])
@connect_sql()
def InsertEmployeeHRCI_Management(cursor):
    try:
        sqlblack = "SELECT ID_CardNo FROM blacklist WHERE validstatus=1"
        cursor.execute(sqlblack)
        columnsblack = [column[0] for column in cursor.description]
        resultblacklist = toJson(cursor.fetchall(),columnsblack)
        if request.form['ID_CardNo']==resultblacklist[0]['ID_CardNo']:
            print("Person is blacklist")
        else:
            i=0
            for i in xrange(len(request.form['AddressType'])):
                sqlIn = "INSERT INTO Address (ID_CardNo,AddressType,HouseNo,Street,DISTRICT_ID,AMPHUR_ID,PROVINCE_ID,PostCode,Tel,Fax) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn,(request.form[i]['ID_CardNo'],request.form[i]['AddressType'],request.form[i]['HouseNo'],
                request.form[i]['Street'],request.form[i]['DISTRICT_NAME'],request.form[i]['AMPHUR_NAME'],request.form[i]['PROVINCE_NAME'],request.form[i]['PostCode'],request.form[i]['Tel'],request.form[i]['Fax']))
            try:
                currentTime = datetime.today().strftime('%Y%m%d%H%M%S%f')
                path = 'uploads/' + request.form['ID_CardNo']
                path2 = request.form['ID_CardNo']
                if not os.path.exists(path):
                    os.makedirs(path)
                if request.method == 'POST':
                    file = request.files['file']
                if file:
                    file.save(os.path.join(path, currentTime + '_employee_img.png'))
                    path_file = path2+'/'+currentTime+'_employee_img.png'
                else:
                    return 'file is not allowed'
                sqlIn4 = "INSERT INTO Attachment (ID_CardNo,Type,PathFile) VALUES (%s,%s,%s)"
                cursor.execute(sqlIn4,(request.form['ID_CardNo'],request.form['Type'],path_file))
            except Exception as e:
                logserver(e)
            i=0
            for i in xrange(len(request.form['ComSkill'])):
                sqlIn6 = "INSERT INTO ComputerSkill (ID_CardNo,ComSkill,Level) VALUES (%s,%s,%s)"
                cursor.execute(sqlIn6,(request.form[i]['ID_CardNo'],request.form[i]['ComSkill'],request.form[i]['Level']))
            i=0
            for i in xrange(len(request.form['EducationLevel'])):
                sqlIn9 = "INSERT INTO Education (ID_CardNo,EducationLevel,Institute,StartYear,EndYear,Qualification,Major,GradeAvg,ExtraCurricularActivities) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn9,(request.form[i]['ID_CardNo'],request.form[i]['EducationLevel'],request.form[i]['Institute'],request.form[i]['StartYear'],request.form[i]['EndYear'],request.form[i]['Qualification'],request.form[i]['Major'],request.form[i]['GradeAvg'],\
                request.form[i]['ExtraCurricularActivities']))
            i=0
            for i in xrange(len(request.form['MemberType'])):
                sqlIn11 = "INSERT INTO Family (ID_CardNo,MemberType,Name,Surname,Occupation,Address,Tel,Fax) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn11,(request.form[i]['ID_CardNo'],request.form[i]['MemberType'],request.form[i]['Name'],request.form[i]['Surname'],request.form[i]['Occupation'],request.form[i]['Address'],request.form[i]['Tel'],request.form[i]['Fax']))
            i=0
            for i in xrange(len(request.form['Languages'])):
                sqlIn13 = "INSERT INTO LanguagesSkill (ID_CardNo,Languages,Speaking,Reading,Writting) VALUES (%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn13,(request.form[i]['ID_CardNo'],request.form[i]['Languages'],request.form[i]['Speaking'],request.form[i]['Reading'],request.form[i]['Writting']))

            sqlIn14 = """INSERT INTO Personal (NameTh,SurnameTh,NicknameTh,NameEn,SurnameEn,NicknameEn,Birthdate,BirthPlace,BirthProvince,BirthCountry,Age,Height,Weight,BloodGroup,Citizenship,Religion,ID_CardNo,IssueDate,ExpiryDate,MaritalStatus,NumberOfChildren,StudyChild,MilitaryService,Others,Worktel,Mobile,Email,EmergencyPerson,EmergencyRelation,EmergencyAddress,EmergencyTel,date) \
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(sqlIn14,(request.form['NameTh'],request.form['SurnameTh'],request.form['NicknameTh'],request.form['NameEn'],\
            request.form['SurnameEn'],request.form['NicknameEn'],request.form['Birthdate'],request.form['BirthPlace'],request.form['BirthProvince'], \
            request.form['BirthCountry'],request.form['Age'],request.form['Height'],request.form['Weight'],request.form['BloodGroup'],request.form['Citizenship'],request.form['Religion'],request.form['ID_CardNo'], \
            request.form['IssueDate'],request.form['ExpiryDate'],request.form['MaritalStatus'],request.form['NumberOfChildren'],request.form['StudyChild'],request.form['MilitaryService'],request.form['Others'], \
            request.form['Worktel'],request.form['Mobile'],request.form['Email'],request.form['EmergencyPerson'],request.form['EmergencyRelation'],request.form['EmergencyAddress'],request.form['EmergencyTel'],request.form['date']))
            i=0
            for i in xrange(len(request.form['RelativeName'])):
                sqlIn17 = "INSERT INTO Reference (ID_CardNo,RelativeName,RelativeSurname,RelativePosition,RelativeRelationship,PhysicalHandicap,PhysicalHandicapDetail,KnowFrom) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn17,(request.form[i]['ID_CardNo'],request.form[i]['RelativeName'],request.form[i]['RelativeSurname'],request.form[i]['RelativePosition'],request.form[i]['RelativeRelationship'],request.form[i]['PhysicalHandicap'],\
                request.form[i]['PhysicalHandicapDetail'],request.form[i]['KnowFrom']))
            i=0
            for i in xrange(len(request.form['RefName'])):
                sqlIn18 = "INSERT INTO RefPerson (ID_CardNo,RefName,RefPosition,RefAddress,RefTel) VALUES (%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn18,(request.form[i]['ID_CardNo'],request.form[i]['RefName'],request.form[i]['RefPosition'],request.form[i]['RefAddress'],request.form[i]['RefTel']))

            sqlIn20 = "INSERT INTO SpecialSkill (ID_CardNo,CarDrivingLicense,MotorBicycleDrivingLicense,OwnCar,OwnMotorBicycle,WorkUpCountry,StartWorkEarliest,PhysicalDisabilityOrDisease,DischargeFromEmployment,DischargeFromEmploymentReason,Arrested,ArrestedReason) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn20,(request.form[i]['ID_CardNo'],request.form[i]['CarDrivingLicense'],request.form[i]['MotorBicycleDrivingLicense'],request.form[i]['OwnCar'],request.form[i]['OwnMotorBicycle'], \
            request.form[i]['WorkUpCountry'],request.form[i]['StartWorkEarliest'],request.form[i]['PhysicalDisabilityOrDisease'],request.form[i]['DischargeFromEmployment'],request.form[i]['DischargeFromEmploymentReason'],request.form[i]['Arrested'],request.form[i]['ArrestedReason']))
            try:
                i=0
                for i in xrange(len(request.form['CompanyName'])):
                    sqlIn10 = "INSERT INTO Employment (ID_CardNo,CompanyName,CompanyAddress,PositionHeld,StartSalary,EndSalary,StartYear,EndYear,Responsibility,ReasonOfLeaving,Descriptionofwork) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sqlIn10,(request.form[i]['ID_CardNo'],request.form[i]['CompanyName'],request.form[i]['CompanyAddress'],request.form[i]['PositionHeld'],request.form[i]['StartSalary'],request.form[i]['EndSalary'],request.form[i]['StartYear'],request.form[i]['EndYear'], \
                    request.form[i]['Responsibility'],request.form[i]['ReasonOfLeaving'],request.form[i]['Descriptionofwork']))
            except Exception as e:
                logserver(e)
            try:
                i=0
                for i in xrange(len(request.form['Subject'])):
                    sqlIn23 = "INSERT INTO TrainingCourse(ID_CardNo,Subject,Place,StartDate,EndDate) VALUES (%s,%s,%s,%s,%s)"
                    cursor.execute(sqlIn23,(request.form[i]['ID_CardNo'],request.form[i]['Subject'],request.form[i]['Place'],request.form[i]['StartDate'],request.form[i]['EndDate']))
            except Exception as e:
                logserver(e)

            sqlEM = "INSERT INTO employee (employeeid,citizenid,name_th,name_eng,surname_th,surname_eng,nickname_employee,salary,email,phone_company,position_id,section_id,org_name_id,cost_center_name_id,company_id,start_work,EndWork_probation,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlEM,(request.form['employeeid'],request.form['ID_CardNo'],request.form['NameTh'],request.form['NameEn'],request.form['SurnameTh'],request.form['SurnameEn'],request.form['NicknameEn'],request.form['salary'],request.form['email'],\
            request.form['phone_company'],request.form['position_id'],\
            request.form['section_id'],request.form['org_name_id'],request.form['cost_center_name_id'],request.form['company_id'],request.form['Start_contract'],request.form['End_contract'],request.form['createby']))

            sqlEm_ga = "INSERT INTO employee_ga (employeeid,citizenid,phone_depreciate,notebook_depreciate,limit_phone,chair_table,pc,notebook,office_equipment,ms,car_ticket,band_car,color,regis_car_number,other,description,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlEm_ga,(request.form['employeeid'],request.form['ID_CardNo'],request.form['phone_depreciate'],request.form['notebook_depreciate'],request.form['limit_phone'],request.form['chair_table'],request.form['pc'],request.form['notebook'],request.form['office_equipment'],\
            request.form['ms'],request.form['car_ticket'],request.form['band_car'],request.form['color'],\
            request.form['regis_car_number'],request.form['other'],request.form['description'],request.form['createby']))

            sqlEM_pro = "INSERT INTO Emp_probation (employeeid,citizenid,name_th,name_eng,surname_th,surname_eng,nickname_employee,salary,email,phone_company,position_id,section_id,org_name_id,cost_center_name_id,company_id,start_work,EndWork_probation,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlEM_pro,(request.form['employeeid'],request.form['ID_CardNo'],request.form['NameTh'],request.form['NameEn'],request.form['SurnameTh'],request.form['SurnameEn'],request.form['NicknameEn'],request.form['salary'],\
            request.form['email'],request.form['phone_company'],request.form['position_id'],\
            request.form['section_id'],request.form['org_name_id'],request.form['cost_center_name_id'],request.form['company_id'],request.form['Start_contract'],request.form['End_contract'],request.form['createby']))
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
