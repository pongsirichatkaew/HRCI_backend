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
def InsertEmployeeHRCI_Management():
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sqlcompafirst = "SELECT acronym FROM company WHERE companyid=%s"
        cursor.execute(sqlcompafirst,data_new['company_id'])
        columnscompafirst = [column[0] for column in cursor.description]
        resultcompafirst = toJson(cursor.fetchall(),columnscompafirst)

        sqlEmployee = "SELECT employeeid FROM employee WHERE company_id=%s ORDER BY employeeid DESC LIMIT 1"
        cursor.execute(sqlEmployee,data_new['company_id'])
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
        cursor.execute(sqlEM,(employeeid,result14[0]['ID_CardNo'],result14[0]['NameTh'],result14[0]['NameEn'],result14[0]['SurnameTh'],result14[0]['SurnameEn'],result14[0]['NicknameEn'],data_new['salary'],data_new['email'],data_new['phone_company'],data_new['position_id'],\
        data_new['section_id'],data_new['org_name_id'],data_new['cost_center_name_id'],data_new['company_id'],data_new['Start_contract'],data_new['End_contract'],data_new['createby']))

        sqlEm_ga = "INSERT INTO employee_ga (employeeid,citizenid,phone_depreciate,notebook_depreciate,limit_phone,chair_table,pc,notebook,office_equipment,ms,car_ticket,band_car,color,regis_car_number,other,description,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlEm_ga,(employeeid,result14[0]['ID_CardNo'],data_new['phone_depreciate'],data_new['notebook_depreciate'],data_new['limit_phone'],data_new['chair_table'],data_new['pc'],data_new['notebook'],data_new['office_equipment'],data_new['ms'],data_new['car_ticket'],data_new['band_car'],data_new['color'],\
        data_new['regis_car_number'],data_new['other'],data_new['description'],data_new['createby']))

        sqlEM_pro = "INSERT INTO Emp_probation (employeeid,citizenid,name_th,name_eng,surname_th,surname_eng,nickname_employee,salary,email,phone_company,position_id,section_id,org_name_id,cost_center_name_id,company_id,start_work,EndWork_probation,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlEM_pro,(employeeid,result14[0]['ID_CardNo'],result14[0]['NameTh'],result14[0]['NameEn'],result14[0]['SurnameTh'],result14[0]['SurnameEn'],result14[0]['NicknameEn'],data_new['salary'],data_new['email'],data_new['phone_company'],data_new['position_id'],\
        data_new['section_id'],data_new['org_name_id'],data_new['cost_center_name_id'],data_new['company_id'],data_new['Start_contract'],data_new['End_contract'],data_new['createby']))

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
@app.route('/test_update', methods=['POST'])
@connect_sql()
def test_update(cursor):
    # try:
        dataInput = request.json
        # sqlUp = "UPDATE org_name SET validstatus=0 WHERE org_name_id=%s"
        # cursor.execute(sqlUp,(data_new['org_name_id']))
        # i=0
        # for i in xrange(len(dataInput)):
        sqlIn6 = "UPDATE ComputerSkill SET ComSkill=%s,Level=%s WHERE ID_CardNo=%s"
        cursor.execute(sqlIn6,(dataInput['ComSkill'],dataInput['Level'],dataInput['ID_CardNo']))
        return "success"
    # except Exception as e:
    #     logserver(e)
    #     return "fail"
