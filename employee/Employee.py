#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

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
def QryEmployee_one_person():
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        dataInput = request.json
        sql = "SELECT * FROM employee LEFT JOIN company ON company.companyid = employee.company_id\
                                      LEFT JOIN position ON position.position_id = employee.position_id\
                                      LEFT JOIN section ON section.sect_id = employee.section_id\
                                      LEFT JOIN org_name ON org_name.org_name_id = employee.org_name_id\
                                      LEFT JOIN cost_center_name ON cost_center_name.cost_center_name_id = employee.cost_center_name_id\
                WHERE employee.employeeid=%s"
        cursor.execute(sql,dataInput['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        connection.close()
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee', methods=['POST'])
@connect_sql()
def EditEmployee():
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sqlQryEM = "SELECT * FROM employee WHERE employeeid=%s"
        cursor.execute(sqlQryEM,(data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        resultsqlQryEM = toJson(cursor.fetchall(),columns)

        sqlEM = "INSERT INTO employee (employeeid,citizenid,name_th,name_eng,surname_th,surname_eng,nickname_employee,salary,email,phone_company,position_id,section_id,org_name_id,cost_center_name_id,company_id,start_work,EndWork_probation) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlEM,(resultsqlQryEM['employeeid'],resultsqlQryEM['ID_CardNo'],resultsqlQryEM['NameTh'],resultsqlQryEM['NameEn'],resultsqlQryEM['SurnameTh'],resultsqlQryEM['SurnameEn'],resultsqlQryEM['NicknameEn'],resultsqlQryEM['salary'],resultsqlQryEM['email'],resultsqlQryEM['phone_company'],resultsqlQryEM['position_id'],\
        resultsqlQryEM['section_id'],resultsqlQryEM['org_name_id'],resultsqlQryEM['cost_center_name_id'],resultsqlQryEM['company_id'],resultsqlQryEM['start_work'],resultsqlQryEM['EndWork_probation']))

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
            for i in xrange(len(result14)):
                sqlInContract = "INSERT INTO Contract (ID_CardNo,Start_contract,End_contract,salary_thai,Authority_Distrinct_Id_Card) VALUES (%s,%s,%s,%s,%s)"
                cursor.execute(sqlInContract,(request.form['ID_CardNo'],request.form['Start_contract'],request.form['End_contract'],request.form['salary_thai'],request.form['Authority_Distrinct_Id_Card']))
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

            sqlcompafirst = "SELECT acronym FROM company WHERE companyid=%s"
            cursor.execute(sqlcompafirst,request.form['company_id'])
            columnscompafirst = [column[0] for column in cursor.description]
            resultcompafirst = toJson(cursor.fetchall(),columnscompafirst)

            sqlEmployee = "SELECT employeeid FROM employee WHERE company_id=%s ORDER BY employeeid DESC LIMIT 1"
            cursor.execute(sqlEmployee,request.form['company_id'])
            columnsEmployee = [column[0] for column in cursor.description]
            resultEmployee = toJson(cursor.fetchall(),columnsEmployee)

            now = datetime.now()
            date = str(int(now.year)+543)
            form_employee = date[2:]
            type = resultEmployee[0]['employeeid']
            codelast = int(str(type[-3:]))+1
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

            sqlEM = "INSERT INTO employee (employeeid,citizenid,name_th,name_eng,surname_th,surname_eng,nickname_employee,salary,email,phone_company,position_id,section_id,org_name_id,cost_center_name_id,company_id,start_work,EndWork_probation,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlEM,(employeeid,request.form['ID_CardNo'],request.form['NameTh'],request.form['NameEn'],request.form['SurnameTh'],request.form['SurnameEn'],request.form['NicknameEn'],request.form['salary'],request.form['email'],\
            request.form['phone_company'],request.form['position_id'],\
            request.form['section_id'],request.form['org_name_id'],request.form['cost_center_name_id'],request.form['company_id'],request.form['Start_contract'],request.form['End_contract'],request.form['createby']))

            sqlEm_ga = "INSERT INTO employee_ga (employeeid,citizenid,phone_depreciate,notebook_depreciate,limit_phone,chair_table,pc,notebook,office_equipment,ms,car_ticket,band_car,color,regis_car_number,other,description,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlEm_ga,(employeeid,request.form['ID_CardNo'],request.form['phone_depreciate'],request.form['notebook_depreciate'],request.form['limit_phone'],request.form['chair_table'],request.form['pc'],request.form['notebook'],request.form['office_equipment'],\
            request.form['ms'],request.form['car_ticket'],request.form['band_car'],request.form['color'],\
            request.form['regis_car_number'],request.form['other'],request.form['description'],request.form['createby']))

            sqlEM_pro = "INSERT INTO Emp_probation (employeeid,citizenid,name_th,name_eng,surname_th,surname_eng,nickname_employee,salary,email,phone_company,position_id,section_id,org_name_id,cost_center_name_id,company_id,start_work,EndWork_probation,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlEM_pro,(employeeid,request.form['ID_CardNo'],request.form['NameTh'],request.form['NameEn'],request.form['SurnameTh'],request.form['SurnameEn'],request.form['NicknameEn'],request.form['salary'],\
            request.form['email'],request.form['phone_company'],request.form['position_id'],\
            request.form['section_id'],request.form['org_name_id'],request.form['cost_center_name_id'],request.form['company_id'],request.form['Start_contract'],request.form['End_contract'],request.form['createby']))
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
