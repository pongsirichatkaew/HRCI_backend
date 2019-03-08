#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/QryAppform', methods=['POST'])
def QryAppform():
    try:
        connection = mysql3.connect()
        cursor = connection.cursor()
        sql = """SELECT Personal.EmploymentAppNo, Personal.ID_CardNo, Personal.AppliedPosition1, Personal.AppliedPosition2, Personal.StartExpectedSalary, Personal.EndExpectedSalary, Personal.NameTh, Personal.SurnameTh, Personal.Mobile, Personal.Email, Personal.date, Personal.check_mail, status_hrci.status_detail, status_hrci.status_id, status_hrci.path_color, status_hrci.font_color
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
        sql = "SELECT * FROM blacklist"
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
        connection = mysql.connect()
        cursor = connection.cursor()
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sqlqry = "SELECT citizenid FROM employee WHERE employeeid=%s"
        cursor.execute(sqlqry,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        resultsqlqry = toJson(cursor.fetchall(),columns)

        sql = "SELECT NameTh,SurnameTh,ID_CardNo,Mobile FROM Personal WHERE ID_CardNo=%s"
        cursor.execute(sql,resultsqlqry[0]['citizenid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sqlIn4 = "INSERT INTO blacklist (ID_CardNo,NameTh,SurnameTh,Mobile,createby,Description) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn4,(result[0]['ID_CardNo'],result[0]['NameTh'],result[0]['SurnameTh'],result[0]['Mobile'],data_new['createby'],data_new['Descriptions']))

        type_action = "ADD"

        sqlIn5 = "INSERT INTO blacklist_log (ID_CardNo,NameTh,SurnameTh,Mobile,createby,Description,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn5,(result[0]['ID_CardNo'],result[0]['NameTh'],result[0]['SurnameTh'],result[0]['Mobile'],data_new['createby'],data_new['Descriptions'],type_action))

        sqlemployee = "DELETE FROM employee WHERE citizenid=%s"
        cursor.execute(sqlemployee,result[0]['ID_CardNo'])

        sqlemployee_log = "DELETE FROM employee_log WHERE citizenid=%s"
        cursor.execute(sqlemployee_log,result[0]['ID_CardNo'])

        sqlemployee_benefits = "DELETE FROM employee_benefits WHERE citizenid=%s"
        cursor.execute(sqlemployee_benefits,result[0]['ID_CardNo'])

        sqlemployee_benefits_log = "DELETE FROM employee_benefits_log WHERE citizenid=%s"
        cursor.execute(sqlemployee_benefits_log,result[0]['ID_CardNo'])

        sqlEmp_pro = "DELETE FROM Emp_probation WHERE citizenid=%s"
        cursor.execute(sqlEmp_pro,result[0]['ID_CardNo'])

        sqlEmp_pro_log = "DELETE FROM Emp_probation_log WHERE citizenid=%s"
        cursor.execute(sqlEmp_pro_log,result[0]['ID_CardNo'])

        sqlpersonal = "DELETE FROM Personal WHERE ID_CardNo=%s"
        cursor.execute(sqlpersonal,result[0]['ID_CardNo'])

        sqlpersonal_log = "DELETE FROM Personal_log WHERE ID_CardNo=%s"
        cursor.execute(sqlpersonal_log,result[0]['ID_CardNo'])

        sqlAddress = "DELETE FROM Address WHERE ID_CardNo=%s"
        cursor.execute(sqlAddress,result[0]['ID_CardNo'])

        sqlAddress_log = "DELETE FROM Address_log WHERE ID_CardNo=%s"
        cursor.execute(sqlAddress_log,result[0]['ID_CardNo'])

        try:
            sqlAttachment = "DELETE FROM Attachment WHERE ID_CardNo=%s"
            cursor.execute(sqlAttachment,result[0]['ID_CardNo'])
        except Exception as e:
            pass

        try:
            sqlComputerSkill = "DELETE FROM ComputerSkill WHERE ID_CardNo=%s"
            cursor.execute(sqlComputerSkill,result[0]['ID_CardNo'])

            sqlComputerSkill_log = "DELETE FROM ComputerSkill_log WHERE ID_CardNo=%s"
            cursor.execute(sqlComputerSkill_log,result[0]['ID_CardNo'])
        except Exception as e:
            pass

        try:
            sqlEducation = "DELETE FROM Education WHERE ID_CardNo=%s"
            cursor.execute(sqlEducation,result[0]['ID_CardNo'])

            sqlEducation_log = "DELETE FROM Education_log WHERE ID_CardNo=%s"
            cursor.execute(sqlEducation_log,result[0]['ID_CardNo'])
        except Exception as e:
            pass

        try:
            sqlEmployment = "DELETE FROM Employment WHERE ID_CardNo=%s"
            cursor.execute(sqlEmployment,result[0]['ID_CardNo'])

            sqlEmployment_log = "DELETE FROM Employment_log WHERE ID_CardNo=%s"
            cursor.execute(sqlEmployment_log,result[0]['ID_CardNo'])
        except Exception as e:
            pass

        try:
            sqlFamily = "DELETE FROM Family WHERE ID_CardNo=%s"
            cursor.execute(sqlFamily,result[0]['ID_CardNo'])

            sqlFamily_log = "DELETE FROM Family_log WHERE ID_CardNo=%s"
            cursor.execute(sqlFamily_log,result[0]['ID_CardNo'])
        except Exception as e:
            pass

        try:
            sqlLanguagesSkill = "DELETE FROM LanguagesSkill WHERE ID_CardNo=%s"
            cursor.execute(sqlLanguagesSkill,result[0]['ID_CardNo'])

            sqlLanguagesSkill_log = "DELETE FROM LanguagesSkill_log WHERE ID_CardNo=%s"
            cursor.execute(sqlLanguagesSkill_log,result[0]['ID_CardNo'])
        except Exception as e:
            pass

        try:
            sqlReference = "DELETE FROM Reference WHERE ID_CardNo=%s"
            cursor.execute(sqlReference,result[0]['ID_CardNo'])

            sqlReference_log = "DELETE FROM Reference_log WHERE ID_CardNo=%s"
            cursor.execute(sqlReference_log,result[0]['ID_CardNo'])
        except Exception as e:
            pass

        try:
            sqlRefPerson = "DELETE FROM RefPerson WHERE ID_CardNo=%s"
            cursor.execute(sqlRefPerson,result[0]['ID_CardNo'])

            sqlRefPerson_log = "DELETE FROM RefPerson_log WHERE ID_CardNo=%s"
            cursor.execute(sqlRefPerson_log,result[0]['ID_CardNo'])
        except Exception as e:
            pass

        try:
            sqlSpecialSkill = "DELETE FROM SpecialSkill WHERE ID_CardNo=%s"
            cursor.execute(sqlSpecialSkill,result[0]['ID_CardNo'])

            sqlSpecialSkill_log = "DELETE FROM SpecialSkill_log WHERE ID_CardNo=%s"
            cursor.execute(sqlSpecialSkill_log,result[0]['ID_CardNo'])
        except Exception as e:
            pass

        try:
            sqlTrainingCourse = "DELETE FROM TrainingCourse WHERE ID_CardNo=%s"
            cursor.execute(sqlTrainingCourse,result[0]['ID_CardNo'])

            sqlTrainingCourse_log = "DELETE FROM TrainingCourse_log WHERE ID_CardNo=%s"
            cursor.execute(sqlTrainingCourse_log,result[0]['ID_CardNo'])
        except Exception as e:
            pass

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

        connection.commit()
        connection.close()

        try:
            ID_CardNo=result[0]['ID_CardNo']
            ID_CardNo_split = ID_CardNo.split("-")
            ID_CardNo = ID_CardNo_split[0]+ID_CardNo_split[1]+ID_CardNo_split[2]+ID_CardNo_split[3]+ID_CardNo_split[4]
        except Exception as e:
            ID_CardNo=result[0]['ID_CardNo']

        connection = mysql.connect()
        cursor = connection.cursor()
        sqlIn4 = "INSERT INTO blacklist (ID_CardNo,NameTh,SurnameTh,Mobile,createby,Description) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn4,(ID_CardNo,result[0]['NameTh'],result[0]['SurnameTh'],result[0]['Mobile'],data_new['createby'],data_new['Descriptions']))

        type_action = "ADD"

        sqlIn5 = "INSERT INTO blacklist_log (ID_CardNo,NameTh,SurnameTh,Mobile,createby,Description,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn5,(result[0]['ID_CardNo'],result[0]['NameTh'],result[0]['SurnameTh'],result[0]['Mobile'],data_new['createby'],data_new['Descriptions'],type_action))

        sqlIn4 = "INSERT INTO Update_statusAppform_log (EmploymentAppNo,status_id,create_by) VALUES (%s,%s,%s)"
        cursor.execute(sqlIn4,(data_new['EmploymentAppNo'],data_new['status_id'],data_new['createby']))

        connection.commit()
        connection.close()
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/UpdateStatusBlacklist_appform', methods=['POST'])
def UpdateStatusBlacklist_appform():
    try:
        connection = mysql3.connect()
        cursor = connection.cursor()
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sqlUp = "UPDATE Personal SET status_id_hrci=5 WHERE EmploymentAppNo=%s"
        cursor.execute(sqlUp,data_new['EmploymentAppNo'])
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

        sql_bl = "SELECT * FROM blacklist WHERE ID_CardNo=%s"
        cursor.execute(sql_bl,(data_new['cardNo']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Delete"
        sqlIn5 = "INSERT INTO blacklist_log (ID_CardNo,NameTh,SurnameTh,Mobile,createby,Description) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn5,(result[0]['ID_CardNo'],result[0]['NameTh'],result[0]['SurnameTh'],result[0]['Mobile'],data_new['createby'],data_new['Descriptions'],type_action))


        sqlUp = "DELETE FROM blacklist WHERE ID_CardNo=%s"
        cursor.execute(sqlUp,(data_new['cardNo']))
        connection.commit()
        connection.close()
        try:
             connection = mysql3.connect()
             cursor = connection.cursor()
             sqlUpAppform = "UPDATE Personal SET status_id_hrci=1 WHERE ID_CardNo=%s"
             cursor.execute(sqlUpAppform,data_new['cardNo'])
             connection.commit()
             connection.close()
        except Exception as e:
            logserver(e)
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
        sql = """SELECT Personal.EmploymentAppNo, Personal.AppliedPosition1, Personal.AppliedPosition2, Personal.StartExpectedSalary, Personal.EndExpectedSalary, Personal.NameTh, Personal.SurnameTh, Personal.Mobile, Personal.Email, Personal.date, status_hrci.status_detail, status_hrci.status_id, status_hrci.font_color, status_hrci.path_color
        FROM Personal INNER JOIN status_hrci ON Personal.status_id_hrci = status_hrci.status_id WHERE status_hrci.status_id=%s AND status_hrci.validstatus = 1 ORDER BY Personal.EmploymentAppNo DESC"""
        cursor.execute(sql,data_new['status_id'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        connection.close()
        return jsonify(result)
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
        try:
            sqlEm = "SELECT Address.EmploymentAppNo,Address.AddressType,Address.HouseNo,Address.Street,Address.PostCode,Address.Tel,Address.Fax,amphures.AMPHUR_CODE,amphures.AMPHUR_NAME,provinces.PROVINCE_NAME,districts.DISTRICT_CODE,districts.DISTRICT_NAME FROM Address INNER JOIN provinces ON provinces.PROVINCE_ID=Address.PROVINCE_ID \
                                               INNER JOIN amphures ON amphures.AMPHUR_ID=Address.AMPHUR_ID \
                                               INNER JOIN districts ON districts.DISTRICT_CODE=Address.DISTRICT_ID \
                                               INNER JOIN Personal ON Personal.EmploymentAppNo=Address.EmploymentAppNo \
                         WHERE Personal.EmploymentAppNo=%s AND Address.AddressType='Present'"
            cursor.execute(sqlEm,data_new['EmploymentAppNo'])
            columnsEm = [column[0] for column in cursor.description]
            result_home = toJson(cursor.fetchall(),columnsEm)
            test = result_home[0]['AddressType']

            sqlEm = "SELECT Address.AddressType,Address.HouseNo,Address.Street,Address.PostCode,Address.Tel,Address.Fax,amphures.AMPHUR_CODE,amphures.AMPHUR_NAME,provinces.PROVINCE_NAME,districts.DISTRICT_CODE,districts.DISTRICT_NAME FROM Address INNER JOIN provinces ON provinces.PROVINCE_ID=Address.PROVINCE_ID \
                                               INNER JOIN amphures ON amphures.AMPHUR_ID=Address.AMPHUR_ID \
                                               INNER JOIN districts ON districts.DISTRICT_CODE=Address.DISTRICT_ID \
                                               INNER JOIN Personal ON Personal.EmploymentAppNo=Address.EmploymentAppNo \
                         WHERE Personal.EmploymentAppNo=%s"
            cursor.execute(sqlEm,data_new['EmploymentAppNo'])
            columnsEm = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columnsEm)
        except Exception as e:
            sqlEm = "SELECT EmploymentAppNo,AddressType,HouseNo,Street,DISTRICT_ID,AMPHUR_ID,PROVINCE_ID,PostCode,Tel,Fax FROM Address WHERE EmploymentAppNo=%s AND AddressType='Home'"
            cursor.execute(sqlEm,data_new['EmploymentAppNo'])
            columnsEm = [column[0] for column in cursor.description]
            result_home = toJson(cursor.fetchall(),columnsEm)

            Address_Type_Present = "Present"


            sqlIn = "INSERT INTO Address (EmploymentAppNo,AddressType,HouseNo,Street,DISTRICT_ID,AMPHUR_ID,PROVINCE_ID,PostCode,Tel,Fax) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn,(result_home[0]['EmploymentAppNo'],Address_Type_Present,result_home[0]['HouseNo'],
            result_home[0]['Street'],result_home[0]['DISTRICT_ID'],result_home[0]['AMPHUR_ID'],result_home[0]['PROVINCE_ID'],result_home[0]['PostCode'],result_home[0]['Tel'],result_home[0]['Fax']))

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
            # encoded_Image = base64.b64encode(test)
            encoded_Image = test
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
@app.route('/UpdateEmpStatus', methods=['POST'])
def UpdateEmpStatus():
    try:
        data = request.json
        source = data['source']
        data_new = source
        EmploymentAppNo = data_new['EmploymentAppNo']

        connection = mysql3.connect()
        cursor = connection.cursor()
        sqlqryIDcard = "SELECT ID_CardNo FROM Personal WHERE EmploymentAppNo=%s"
        cursor.execute(sqlqryIDcard,EmploymentAppNo)
        columnsIDcard = [column[0] for column in cursor.description]
        resultIDcard = toJson(cursor.fetchall(),columnsIDcard)
        connection.commit()
        connection.close()

        try:
            ID_CardNo=resultIDcard[0]['ID_CardNo']
            ID_CardNo_split = ID_CardNo.split("-")
            ID_CardNo = ID_CardNo_split[0]+ID_CardNo_split[1]+ID_CardNo_split[2]+ID_CardNo_split[3]+ID_CardNo_split[4]
        except Exception as e:
            ID_CardNo=resultIDcard[0]['ID_CardNo']

        try:
            connection = mysql.connect()
            cursor = connection.cursor()
            sqlblack = "SELECT ID_CardNo FROM blacklist WHERE ID_CardNo=%s"
            cursor.execute(sqlblack,ID_CardNo)
            columnsblack = [column[0] for column in cursor.description]
            resultblacklist = toJson(cursor.fetchall(),columnsblack)

            sqlemployee = "SELECT citizenid FROM employee WHERE citizenid=%s"
            cursor.execute(sqlemployee,ID_CardNo)
            columnsemployee = [column[0] for column in cursor.description]
            resultemployee = toJson(cursor.fetchall(),columnsemployee)
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
            elif len(resultemployee) != 0:
               connection = mysql3.connect()
               cursor = connection.cursor()
               sqlUp = "UPDATE Personal SET status_id_hrci=0 WHERE EmploymentAppNo=%s"
               cursor.execute(sqlUp,EmploymentAppNo)
               connection.commit()
               connection.close()
               return "Employee"
            else:
               connection = mysql3.connect()
               cursor = connection.cursor()
               sqlUp = "UPDATE Personal SET status_id_hrci = %s WHERE EmploymentAppNo = %s"
               cursor.execute(sqlUp,(data_new['status_id'], EmploymentAppNo))
               connection.commit()
               connection.close()

               connection = mysql.connect()
               cursor = connection.cursor()
               sqlIn4 = "INSERT INTO Update_statusAppform_log (EmploymentAppNo,status_id,create_by) VALUES (%s,%s,%s)"
               cursor.execute(sqlIn4,(data_new['EmploymentAppNo'],data_new['status_id'],data_new['create_by']))
               connection.commit()
               connection.close()
               return "success"
        except Exception as e:
            logserver(e)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/QryDatbaseAppform', methods=['POST'])
def QryDatbaseAppform():

    data = request.json
    source = data['source']
    data_new = source
    EmploymentAppNo = data_new['EmploymentAppNo']

    if int(data_new['long_date'])>180:
        return "too long day"

    connection = mysql.connect()
    cursor = connection.cursor()
    try:
        sql2 = "SELECT employeeid FROM employee WHERE employeeid=%s AND company_id=%s"
        cursor.execute(sql2,(data_new['employeeid'],data_new['company_id']))
        columns = [column[0] for column in cursor.description]
        result2 = toJson(cursor.fetchall(),columns)
        employeeid__ = result2[0]['employeeid']
        return "Duplicate_employeeid"
    except Exception as e:
        pass
    connection.commit()
    connection.close()

    connection = mysql3.connect()
    cursor = connection.cursor()
    sqlqryIDcard = "SELECT ID_CardNo FROM Personal WHERE EmploymentAppNo=%s"
    cursor.execute(sqlqryIDcard,EmploymentAppNo)
    columnsIDcard = [column[0] for column in cursor.description]
    resultIDcard = toJson(cursor.fetchall(),columnsIDcard)
    connection.commit()
    connection.close()

    try:
        ID_CardNo=resultIDcard[0]['ID_CardNo']
        ID_CardNo_split = ID_CardNo.split("-")
        ID_CardNo = ID_CardNo_split[0]+ID_CardNo_split[1]+ID_CardNo_split[2]+ID_CardNo_split[3]+ID_CardNo_split[4]
    except Exception as e:
        ID_CardNo=resultIDcard[0]['ID_CardNo']

    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        sqlblack = "SELECT ID_CardNo FROM blacklist WHERE ID_CardNo=%s"
        cursor.execute(sqlblack,ID_CardNo)
        columnsblack = [column[0] for column in cursor.description]
        resultblacklist = toJson(cursor.fetchall(),columnsblack)

        sqlemployee = "SELECT citizenid FROM employee WHERE citizenid=%s"
        cursor.execute(sqlemployee,ID_CardNo)
        columnsemployee = [column[0] for column in cursor.description]
        resultemployee = toJson(cursor.fetchall(),columnsemployee)
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
        elif len(resultemployee) != 0:
           return "Employee"
        else:
            if data_new['status_id']!=3:
               connection = mysql3.connect()
               cursor = connection.cursor()
               sqlUp = "UPDATE Personal SET status_id_hrci = %s WHERE EmploymentAppNo = %s"
               cursor.execute(sqlUp,(data_new['status_id'], EmploymentAppNo))
               connection.commit()
               connection.close()

               connection = mysql.connect()
               cursor = connection.cursor()
               sqlIn4 = "INSERT INTO Update_statusAppform_log (EmploymentAppNo,status_id,create_by) VALUES (%s,%s,%s)"
               cursor.execute(sqlIn4,(data_new['EmploymentAppNo'],data_new['status_id'],data_new['create_by']))
               connection.commit()
               connection.close()
               return "success_update_status"
            else:
    # except Exception as e:
    #     pass
                try:
                    connection = mysql3.connect()
                    cursor = connection.cursor()
                    # dataInput = request.json
                    # source = dataInput['source']
                    # data_new = source
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

                    type_action = "ADD_appform"

                    try:
                        ID_CardNo = result[0]['ID_CardNo']
                        ID_CardNo_split = ID_CardNo.split("-")
                        ID_CardNo = ID_CardNo_split[0]+ID_CardNo_split[1]+ID_CardNo_split[2]+ID_CardNo_split[3]+ID_CardNo_split[4]
                    except Exception as e:
                        ID_CardNo = result[0]['ID_CardNo']

                    connection = mysql.connect()
                    cursor = connection.cursor()
                    i=0
                    for i in xrange(len(result)):
                        sqlIn = "INSERT INTO Address (ID_CardNo,AddressType,HouseNo,Street,DISTRICT_ID,AMPHUR_ID,PROVINCE_ID,PostCode,Tel,Fax,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        cursor.execute(sqlIn,(ID_CardNo,result[i]['AddressType'],result[i]['HouseNo'],
                        result[i]['Street'],result[i]['DISTRICT_NAME'],result[i]['AMPHUR_NAME'],result[i]['PROVINCE_NAME'],result[i]['PostCode'],result[i]['Tel'],result[i]['Fax'],data_new['createby']))

                    i=0
                    for i in xrange(len(result)):
                        sqlIn_log = "INSERT INTO Address_log (ID_CardNo,AddressType,HouseNo,Street,DISTRICT_ID,AMPHUR_ID,PROVINCE_ID,PostCode,Tel,Fax,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        cursor.execute(sqlIn_log,(ID_CardNo,result[i]['AddressType'],result[i]['HouseNo'],
                        result[i]['Street'],result[i]['DISTRICT_NAME'],result[i]['AMPHUR_NAME'],result[i]['PROVINCE_NAME'],result[i]['PostCode'],result[i]['Tel'],result[i]['Fax'],data_new['createby'],type_action))
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
                            cursor.execute(sqlIn4,(ID_CardNo,result4[i]['Type'],result4[i]['PathFile']))
                    except Exception as e:
                        logserver(e)
                    i=0
                    for i in xrange(len(result6)):
                        sqlIn6 = "INSERT INTO ComputerSkill (ID_CardNo,ComSkill,Level,createby) VALUES (%s,%s,%s,%s)"
                        cursor.execute(sqlIn6,(ID_CardNo,result6[i]['ComSkill'],result6[i]['Level'],data_new['createby']))

                    i=0
                    for i in xrange(len(result6)):
                        sqlIn6_log = "INSERT INTO ComputerSkill_log (ID_CardNo,ComSkill,Level,createby,type_action) VALUES (%s,%s,%s,%s,%s)"
                        cursor.execute(sqlIn6_log,(ID_CardNo,result6[i]['ComSkill'],result6[i]['Level'],data_new['createby'],type_action))

                    start_date_ = data_new['Start_contract']
                    split_str_date = start_date_.split("-")
                    str_date_year = split_str_date[2]

                    now_contract = str_date_year
                    date_contract = str(int(now_contract)+543)
                    date_sub_contract = date_contract[2:]
                    try:
                        sql_contract_id = "SELECT contract_id,year FROM Contract WHERE companyid=%s AND year=%s ORDER BY contract_id DESC LIMIT 1"
                        cursor.execute(sql_contract_id,(data_new['company_id'],date_contract))
                        columns = [column[0] for column in cursor.description]
                        resultsql_contract_id = toJson(cursor.fetchall(),columns)
                        year_contract = resultsql_contract_id[0]['year']
                        contract_id_ = resultsql_contract_id[0]['contract_id']
                        year_sub_con = year_contract[2:]
                        if year_sub_con==date_sub_contract:
                            contract_id_ = resultsql_contract_id[0]['contract_id']
                        else:
                            contract_id_ = 0
                    except Exception as e:
                        contract_id_ = 0
                    contract_id_last = int(contract_id_)+1

                    sqlInContract = "INSERT INTO Contract (contract_id,companyid,year,ID_CardNo,Authority_Distrinct_Id_Card) VALUES (%s,%s,%s,%s,%s)"
                    cursor.execute(sqlInContract,(contract_id_last,data_new['company_id'],date_contract,ID_CardNo,data_new['Authority_Distrinct_Id_Card']))

                    i=0
                    for i in xrange(len(result9)):
                        sqlIn9 = "INSERT INTO Education (ID_CardNo,EducationLevel,Institute,StartYear,EndYear,Qualification,Major,GradeAvg,ExtraCurricularActivities,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        cursor.execute(sqlIn9,(ID_CardNo,result9[i]['EducationLevel'],result9[i]['Institute'],result9[i]['StartYear'],result9[i]['EndYear'],result9[i]['Qualification'],result9[i]['Major'],result9[i]['GradeAvg'],result9[i]['ExtraCurricularActivities'],data_new['createby']))

                    i=0
                    for i in xrange(len(result9)):
                        sqlIn9_log = "INSERT INTO Education_log (ID_CardNo,EducationLevel,Institute,StartYear,EndYear,Qualification,Major,GradeAvg,ExtraCurricularActivities,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        cursor.execute(sqlIn9_log,(ID_CardNo,result9[i]['EducationLevel'],result9[i]['Institute'],result9[i]['StartYear'],result9[i]['EndYear'],result9[i]['Qualification'],result9[i]['Major'],result9[i]['GradeAvg'],result9[i]['ExtraCurricularActivities'],data_new['createby'],type_action))

                    i=0
                    for i in xrange(len(result11)):
                        sqlIn11 = "INSERT INTO Family (ID_CardNo,MemberType,Name,Surname,Occupation,Address,Tel,Fax,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        cursor.execute(sqlIn11,(ID_CardNo,result11[i]['MemberType'],result11[i]['Name'],result11[i]['Surname'],result11[i]['Occupation'],result11[i]['Address'],result11[i]['Tel'],result11[i]['Fax'],data_new['createby']))

                    i=0
                    for i in xrange(len(result11)):
                        sqlIn11_log = "INSERT INTO Family_log (ID_CardNo,MemberType,Name,Surname,Occupation,Address,Tel,Fax,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        cursor.execute(sqlIn11_log,(ID_CardNo,result11[i]['MemberType'],result11[i]['Name'],result11[i]['Surname'],result11[i]['Occupation'],result11[i]['Address'],result11[i]['Tel'],result11[i]['Fax'],data_new['createby'],type_action))

                    i=0
                    for i in xrange(len(result13)):
                        sqlIn13 = "INSERT INTO LanguagesSkill (ID_CardNo,Languages,Speaking,Reading,Writting,createby) VALUES (%s,%s,%s,%s,%s,%s)"
                        cursor.execute(sqlIn13,(ID_CardNo,result13[i]['Languages'],result13[i]['Speaking'],result13[i]['Reading'],result13[i]['Writting'],data_new['createby']))

                    i=0
                    for i in xrange(len(result13)):
                        sqlIn13_log = "INSERT INTO LanguagesSkill_log (ID_CardNo,Languages,Speaking,Reading,Writting,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                        cursor.execute(sqlIn13_log,(ID_CardNo,result13[i]['Languages'],result13[i]['Speaking'],result13[i]['Reading'],result13[i]['Writting'],data_new['createby'],type_action))

                    date_name = str(result14[0]['Birthdate'])
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

                    sqlIn14 = """INSERT INTO Personal (NameTh,SurnameTh,NicknameTh,NameEn,SurnameEn,NicknameEn,Birthdate,Birthdate_name,BirthPlace,BirthProvince,BirthCountry,Age,Height,Weight,BloodGroup,Citizenship,Religion,ID_CardNo,IssueDate,ExpiryDate,MaritalStatus,NumberOfChildren,StudyChild,MilitaryService,Others,Worktel,Mobile,Email,EmergencyPerson,EmergencyRelation,EmergencyAddress,EmergencyTel,date,createby) \
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                    cursor.execute(sqlIn14,(result14[0]['NameTh'],result14[0]['SurnameTh'],result14[0]['NicknameTh'],result14[0]['NameEn'],\
                    result14[0]['SurnameEn'],result14[0]['NicknameEn'],result14[0]['Birthdate'],Birthdate_name,result14[0]['BirthPlace'],result14[0]['BirthProvince'], \
                    result14[0]['BirthCountry'],result14[0]['Age'],result14[0]['Height'],result14[0]['Weight'],result14[0]['BloodGroup'],result14[0]['Citizenship'],result14[0]['Religion'],ID_CardNo, \
                    result14[0]['IssueDate'],result14[0]['ExpiryDate'],result14[0]['MaritalStatus'],result14[0]['NumberOfChildren'],result14[0]['StudyChild'],result14[0]['MilitaryService'],result14[0]['Others'], \
                    result14[0]['Worktel'],result14[0]['Mobile'],result14[0]['Email'],result14[0]['EmergencyPerson'],result14[0]['EmergencyRelation'],result14[0]['EmergencyAddress'],result14[0]['EmergencyTel'],result14[0]['date'],data_new['createby']))

                    sqlIn14_log = """INSERT INTO Personal_log (NameTh,SurnameTh,NicknameTh,NameEn,SurnameEn,NicknameEn,Birthdate,Birthdate_name,BirthPlace,BirthProvince,BirthCountry,Age,Height,Weight,BloodGroup,Citizenship,Religion,ID_CardNo,IssueDate,ExpiryDate,MaritalStatus,NumberOfChildren,StudyChild,MilitaryService,Others,Worktel,Mobile,Email,EmergencyPerson,EmergencyRelation,EmergencyAddress,EmergencyTel,date,createby,type_action) \
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                    cursor.execute(sqlIn14_log,(result14[0]['NameTh'],result14[0]['SurnameTh'],result14[0]['NicknameTh'],result14[0]['NameEn'],\
                    result14[0]['SurnameEn'],result14[0]['NicknameEn'],result14[0]['Birthdate'],Birthdate_name,result14[0]['BirthPlace'],result14[0]['BirthProvince'], \
                    result14[0]['BirthCountry'],result14[0]['Age'],result14[0]['Height'],result14[0]['Weight'],result14[0]['BloodGroup'],result14[0]['Citizenship'],result14[0]['Religion'],ID_CardNo, \
                    result14[0]['IssueDate'],result14[0]['ExpiryDate'],result14[0]['MaritalStatus'],result14[0]['NumberOfChildren'],result14[0]['StudyChild'],result14[0]['MilitaryService'],result14[0]['Others'], \
                    result14[0]['Worktel'],result14[0]['Mobile'],result14[0]['Email'],result14[0]['EmergencyPerson'],result14[0]['EmergencyRelation'],result14[0]['EmergencyAddress'],result14[0]['EmergencyTel'],result14[0]['date'],data_new['createby'],type_action))

                    i=0
                    for i in xrange(len(result17)):
                        sqlIn17 = "INSERT INTO Reference (ID_CardNo,RelativeName,RelativeSurname,RelativePosition,RelativeRelationship,PhysicalHandicap,PhysicalHandicapDetail,KnowFrom,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        cursor.execute(sqlIn17,(ID_CardNo,result17[i]['RelativeName'],result17[i]['RelativeSurname'],result17[i]['RelativePosition'],result17[i]['RelativeRelationship'],result17[i]['PhysicalHandicap'],result17[i]['PhysicalHandicapDetail'],result17[i]['KnowFrom'],data_new['createby']))

                    i=0
                    for i in xrange(len(result17)):
                        sqlIn17_log = "INSERT INTO Reference_log (ID_CardNo,RelativeName,RelativeSurname,RelativePosition,RelativeRelationship,PhysicalHandicap,PhysicalHandicapDetail,KnowFrom,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        cursor.execute(sqlIn17_log,(ID_CardNo,result17[i]['RelativeName'],result17[i]['RelativeSurname'],result17[i]['RelativePosition'],result17[i]['RelativeRelationship'],result17[i]['PhysicalHandicap'],result17[i]['PhysicalHandicapDetail'],result17[i]['KnowFrom'],data_new['createby'],type_action))

                    i=0
                    for i in xrange(len(result18)):
                        sqlIn18 = "INSERT INTO RefPerson (ID_CardNo,RefName,RefPosition,RefAddress,RefTel,createby) VALUES (%s,%s,%s,%s,%s,%s)"
                        cursor.execute(sqlIn18,(ID_CardNo,result18[i]['RefName'],result18[i]['RefPosition'],result18[i]['RefAddress'],result18[i]['RefTel'],data_new['createby']))

                    i=0
                    for i in xrange(len(result18)):
                        sqlIn18_log = "INSERT INTO RefPerson_log (ID_CardNo,RefName,RefPosition,RefAddress,RefTel,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                        cursor.execute(sqlIn18_log,(ID_CardNo,result18[i]['RefName'],result18[i]['RefPosition'],result18[i]['RefAddress'],result18[i]['RefTel'],data_new['createby'],type_action))

                    i=0
                    for i in xrange(len(result20)):
                        sqlIn20 = "INSERT INTO SpecialSkill (ID_CardNo,CarDrivingLicense,MotorBicycleDrivingLicense,OwnCar,OwnMotorBicycle,WorkUpCountry,StartWorkEarliest,PhysicalDisabilityOrDisease,DischargeFromEmployment,DischargeFromEmploymentReason,Arrested,ArrestedReason,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        cursor.execute(sqlIn20,(ID_CardNo,result20[i]['CarDrivingLicense'],result20[i]['MotorBicycleDrivingLicense'],result20[i]['OwnCar'],result20[i]['OwnMotorBicycle'], \
                        result20[i]['WorkUpCountry'],result20[i]['StartWorkEarliest'],result20[i]['PhysicalDisabilityOrDisease'],result20[i]['DischargeFromEmployment'],result20[i]['DischargeFromEmploymentReason'],result20[i]['Arrested'],result20[i]['ArrestedReason'],data_new['createby']))

                    i=0
                    for i in xrange(len(result20)):
                        sqlIn20_log = "INSERT INTO SpecialSkill_log (ID_CardNo,CarDrivingLicense,MotorBicycleDrivingLicense,OwnCar,OwnMotorBicycle,WorkUpCountry,StartWorkEarliest,PhysicalDisabilityOrDisease,DischargeFromEmployment,DischargeFromEmploymentReason,Arrested,ArrestedReason,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        cursor.execute(sqlIn20_log,(ID_CardNo,result20[i]['CarDrivingLicense'],result20[i]['MotorBicycleDrivingLicense'],result20[i]['OwnCar'],result20[i]['OwnMotorBicycle'], \
                        result20[i]['WorkUpCountry'],result20[i]['StartWorkEarliest'],result20[i]['PhysicalDisabilityOrDisease'],result20[i]['DischargeFromEmployment'],result20[i]['DischargeFromEmploymentReason'],result20[i]['Arrested'],result20[i]['ArrestedReason'],data_new['createby'],type_action))
                    try:
                        i=0
                        for i in xrange(len(result10)):
                            sqlIn10 = "INSERT INTO Employment (ID_CardNo,CompanyName,CompanyAddress,PositionHeld,StartSalary,EndSalary,StartYear,EndYear,Responsibility,ReasonOfLeaving,Descriptionofwork,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                            cursor.execute(sqlIn10,(ID_CardNo,result10[i]['CompanyName'],result10[i]['CompanyAddress'],result10[i]['PositionHeld'],result10[i]['StartSalary'],result10[i]['EndSalary'],result10[i]['StartYear'],result10[i]['EndYear'], \
                            result10[i]['Responsibility'],result10[i]['ReasonOfLeaving'],result10[i]['Descriptionofwork'],data_new['createby']))

                        i=0
                        for i in xrange(len(result10)):
                            sqlIn10_log = "INSERT INTO Employment_log (ID_CardNo,CompanyName,CompanyAddress,PositionHeld,StartSalary,EndSalary,StartYear,EndYear,Responsibility,ReasonOfLeaving,Descriptionofwork,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                            cursor.execute(sqlIn10_log,(ID_CardNo,result10[i]['CompanyName'],result10[i]['CompanyAddress'],result10[i]['PositionHeld'],result10[i]['StartSalary'],result10[i]['EndSalary'],result10[i]['StartYear'],result10[i]['EndYear'], \
                            result10[i]['Responsibility'],result10[i]['ReasonOfLeaving'],result10[i]['Descriptionofwork'],data_new['createby'],type_action))
                    except Exception as e:
                            pass
                    try:
                        i=0
                        for i in xrange(len(result23)):
                            sqlIn23 = "INSERT INTO TrainingCourse(ID_CardNo,Subject,Place,StartDate,EndDate,createby) VALUES (%s,%s,%s,%s,%s,%s)"
                            cursor.execute(sqlIn23,(ID_CardNo,result23[i]['Subject'],result23[i]['Place'],result23[i]['StartDate'],result23[i]['EndDate'],data_new['createby']))

                        i=0
                        for i in xrange(len(result23)):
                            sqlIn23_log = "INSERT INTO_log TrainingCourse(ID_CardNo,Subject,Place,StartDate,EndDate,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                            cursor.execute(sqlIn23_log,(ID_CardNo,result23[i]['Subject'],result23[i]['Place'],result23[i]['StartDate'],result23[i]['EndDate'],data_new['createby'],type_action))
                    except Exception as e:
                            pass

                    companyid__ = int(data_new['company_id'])
                    if companyid__==1:
                        now = str_date_year
                        date_n = str(int(now))
                        form_employee = date_n
                    elif companyid__==21:
                        now = str_date_year
                        date_n = str(int(now))
                        form_employee = date_n[2:]
                    else:
                        now = str_date_year
                        date_n = str(int(now)+543)
                        form_employee = date_n[2:]
                    sqlcompafirst = "SELECT acronym FROM company WHERE companyid=%s"
                    cursor.execute(sqlcompafirst,data_new['company_id'])
                    columnscompafirst = [column[0] for column in cursor.description]
                    resultcompafirst = toJson(cursor.fetchall(),columnscompafirst)
                    coun_length =len(resultcompafirst[0]['acronym'])
                    coun_company = str(resultcompafirst[0]['acronym'])
                    try:
                        sqlEmployee = "SELECT employeeid FROM employee WHERE company_id=%s AND type_em='employee' AND start_work LIKE '%-%-{}' ORDER BY employeeid DESC LIMIT 1".format(str_date_year)
                        cursor.execute(sqlEmployee,data_new['company_id'])
                        columnsEmployee = [column[0] for column in cursor.description]
                        resultEmployee = toJson(cursor.fetchall(),columnsEmployee)
                        Emp_last = resultEmployee[0]['employeeid']
                        if companyid__!=1:
                            form_employee2 = Emp_last[coun_length:]
                            form_employee3 = form_employee2[:-3]
                            if form_employee3==form_employee:
                                Emp_last = resultEmployee[0]['employeeid']
                            else:
                                Emp_last = coun_company+"000"
                        else:
                            form_employee2 = Emp_last[coun_length:]
                            form_employee3 = form_employee2[:-4]
                            if form_employee3==form_employee:
                                Emp_last = resultEmployee[0]['employeeid']
                            else:
                                Emp_last = coun_company+"000"
                    except Exception as e:
                        if companyid__!=1:
                            Emp_last = coun_company+"000"
                        else:
                           Emp_last = coun_company+"000"
                    type = Emp_last
                    if  coun_length==0:
                        coun_length=2
                    elif coun_length==1:
                        coun_length=3
                    else:
                        coun_length=coun_length+2
                    if companyid__!=1:
                        codelast = int(str(type[coun_length:]))+1
                    else:
                        codelast = str(int(str(type[coun_length:]))+1)
                        codelast = codelast[2:]
                        if codelast=="":
                           codelast=1
                        else:
                            codelast=codelast
                    if companyid__!=1:
                        if  codelast<=9:
                            codelast=str(codelast)
                            codesumlast="00"+codelast
                        elif codelast<=99:
                            codelast=str(codelast)
                            codesumlast="0"+codelast
                        else:
                            codesumlast=str(codelast)
                    else:
                        if  codelast<=9:
                            codelast=str(codelast)
                            codesumlast="000"+codelast
                        elif codelast<=99:
                            codelast=str(codelast)
                            codesumlast="00"+codelast
                        elif codelast<=999:
                            codelast=str(codelast)
                            codesumlast="0"+codelast
                        else:
                            codesumlast=str(codelast)
                    first_character = resultcompafirst[0]['acronym']
                    if companyid__==1:
                        employeeid = first_character+form_employee+codesumlast
                    elif companyid__==21:
                        employeeid = first_character+form_employee+codesumlast
                    else:
                        employeeid = first_character+form_employee+codesumlast
                    encodedsalary = base64.b64encode(data_new['salary'])

                    date1 = data_new['Start_contract']
                    long_date = int(data_new['long_date'])-1
                    star_date = date1.split("-")
                    Day_s = int(star_date[0])
                    Mon_s = int(star_date[1])
                    year_s = int(star_date[2])
                    next_3_mm = date(year_s,Mon_s,Day_s) + relativedelta(days=long_date)
                    next_3_m2 = str(next_3_mm)
                    end_date = next_3_m2.split("-")
                    Day_e = end_date[2]
                    Mon_e =end_date[1]
                    year_e = end_date[0]
                    End_probation_date = Day_e+"-"+Mon_e+"-"+year_e
                    check_type_em = str(data_new['position_id'])
                    if check_type_em=='158':
                        type_em_ = 'trainee'
                    else:
                        type_em_ = 'employee'

                    sqlEM = "INSERT INTO employee (employeeid,citizenid,name_th,name_eng,surname_th,surname_eng,nickname_employee,salary,email,phone_company,position_id,section_id,org_name_id,cost_center_name_id,company_id,type_em,start_work,EndWork_probation,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sqlEM,(data_new['employeeid'],ID_CardNo,result14[0]['NameTh'],result14[0]['NameEn'],result14[0]['SurnameTh'],result14[0]['SurnameEn'],result14[0]['NicknameEn'],encodedsalary,data_new['email'],data_new['phone_company'],data_new['position_id'],\
                    data_new['section_id'],data_new['org_name_id'],data_new['cost_center_name_id'],data_new['company_id'],data_new['type_em_'],data_new['Start_contract'],End_probation_date,data_new['createby']))

                    sqlEM_log = "INSERT INTO employee_log (employeeid,citizenid,name_th,name_eng,surname_th,surname_eng,nickname_employee,salary,email,phone_company,position_id,section_id,org_name_id,cost_center_name_id,company_id,start_work,EndWork_probation,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sqlEM_log,(data_new['employeeid'],ID_CardNo,result14[0]['NameTh'],result14[0]['NameEn'],result14[0]['SurnameTh'],result14[0]['SurnameEn'],result14[0]['NicknameEn'],encodedsalary,data_new['email'],data_new['phone_company'],data_new['position_id'],\
                    data_new['section_id'],data_new['org_name_id'],data_new['cost_center_name_id'],data_new['company_id'],data_new['Start_contract'],End_probation_date,data_new['createby'],type_action))

                    i=0
                    for i in xrange(len(data_new['benefits'])):
                        sqlIn_be = "INSERT INTO employee_benefits(employeeid,citizenid,benefits_id,benefits_values,type_check,createby) VALUES (%s,%s,%s,%s,%s,%s)"
                        cursor.execute(sqlIn_be,(data_new['employeeid'],ID_CardNo,data_new['benefits'][i]['benefits_id'],data_new['benefits'][i]['benefits_values'],data_new['benefits'][i]['type_check'],data_new['createby']))

                    i=0
                    for i in xrange(len(data_new['benefits'])):
                        sqlIn_be_log = "INSERT INTO employee_benefits_log(employeeid,citizenid,benefits_id,benefits_values,type_check,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                        cursor.execute(sqlIn_be_log,(data_new['employeeid'],ID_CardNo,data_new['benefits'][i]['benefits_id'],data_new['benefits'][i]['benefits_values'],data_new['benefits'][i]['type_check'],data_new['createby'],type_action))

                    sqlEM_pro = "INSERT INTO Emp_probation (employeeid,citizenid,name_th,name_eng,surname_th,surname_eng,nickname_employee,salary,email,phone_company,position_id,section_id,org_name_id,cost_center_name_id,company_id,start_work,EndWork_probation,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sqlEM_pro,(data_new['employeeid'],ID_CardNo,result14[0]['NameTh'],result14[0]['NameEn'],result14[0]['SurnameTh'],result14[0]['SurnameEn'],result14[0]['NicknameEn'],encodedsalary,data_new['email'],data_new['phone_company'],data_new['position_id'],\
                    data_new['section_id'],data_new['org_name_id'],data_new['cost_center_name_id'],data_new['company_id'],data_new['Start_contract'],End_probation_date,data_new['createby']))

                    sqlEM_pro_log = "INSERT INTO Emp_probation_log (employeeid,citizenid,name_th,name_eng,surname_th,surname_eng,nickname_employee,salary,email,phone_company,position_id,section_id,org_name_id,cost_center_name_id,company_id,start_work,EndWork_probation,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sqlEM_pro_log,(data_new['employeeid'],ID_CardNo,result14[0]['NameTh'],result14[0]['NameEn'],result14[0]['SurnameTh'],result14[0]['SurnameEn'],result14[0]['NicknameEn'],encodedsalary,data_new['email'],data_new['phone_company'],data_new['position_id'],\
                    data_new['section_id'],data_new['org_name_id'],data_new['cost_center_name_id'],data_new['company_id'],data_new['Start_contract'],End_probation_date,data_new['createby'],type_action))
                    connection.commit()
                    connection.close()

                    connection = mysql3.connect()
                    cursor = connection.cursor()
                    sqlUp = "UPDATE Personal SET status_id_hrci = %s WHERE EmploymentAppNo = %s"
                    cursor.execute(sqlUp,(data_new['status_id'], EmploymentAppNo))
                    connection.commit()
                    connection.close()

                    connection = mysql.connect()
                    cursor = connection.cursor()
                    sqlIn4 = "INSERT INTO Update_statusAppform_log (EmploymentAppNo,status_id,create_by) VALUES (%s,%s,%s)"
                    cursor.execute(sqlIn4,(data_new['EmploymentAppNo'],data_new['status_id'],data_new['create_by']))
                    connection.commit()
                    connection.close()
                    return "success_insert_employee"
                except Exception as e:
                    logserver(e)
                    return "fail_insert_employee"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/send_Mail_appointment', methods=['POST'])
def send_Mail_appointment():
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        connection = mysql3.connect()
        cursor = connection.cursor()

        sqlUp = "UPDATE Personal SET check_mail = 2 WHERE EmploymentAppNo = %s"
        cursor.execute(sqlUp,(data_new['EmploymentAppNo']))

        sqlcheck = "SELECT NameTh,SurnameTh,Email FROM Personal WHERE EmploymentAppNo = %s"
        cursor.execute(sqlcheck,(data_new['EmploymentAppNo']))
        columns = [column[0] for column in cursor.description]
        result_per = toJson(cursor.fetchall(),columns)
        # for item in result_per:
        prefix = ['นาย', 'นาง', 'นางสาว']
        for i in xrange(len(prefix)):
    	    Name_e = result_per[0]['NameTh'].split(prefix[i])
            if len(Name_e)==2:
                Name_ea = Name_e[1]
        connection.commit()
        connection.close()

        connection = mysql.connect()
        cursor = connection.cursor()
        sqlIn4 = "INSERT INTO appoint_mail_log (EmploymentAppNo,appoint_day,appoint_time,appoint_place,position,create_by) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn4,(data_new['EmploymentAppNo'],data_new['appoint_day'],data_new['appoint_time'],data_new['appoint_place'],data_new['position'],data_new['create_by']))

        sqlhr = "SELECT name_hr,surname_hr,phone,nickname,email_hr FROM mail_hr WHERE employeeid = %s"
        cursor.execute(sqlhr,(data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        result_hr = toJson(cursor.fetchall(),columns)

        connection.commit()
        connection.close()
        sendMail_appointment(result_per[0]['Email'],data_new['appoint_day'],data_new['appoint_time'],data_new['appoint_place'],data_new['position'],Name_ea,result_per[0]['SurnameTh'],result_hr[0]['name_hr'],result_hr[0]['surname_hr'],result_hr[0]['email_hr'],result_hr[0]['phone'],result_hr[0]['nickname'])
        return "success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/get_Mail_appointment', methods=['POST'])
def get_Mail_appointment():
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        connection = mysql3.connect()
        cursor = connection.cursor()

        sqlcheck = "SELECT NameTh,SurnameTh,Email FROM Personal WHERE EmploymentAppNo = %s"
        cursor.execute(sqlcheck,(data_new['EmploymentAppNo']))
        columns = [column[0] for column in cursor.description]
        result_per = toJson(cursor.fetchall(),columns)

        prefix = ['นาย', 'นาง', 'นางสาว']
        for i in xrange(len(prefix)):
    	    Name_e = result_per[0]['NameTh'].split(prefix[i])
            if len(Name_e)==2:
                Name_ea = Name_e[1]
        connection.commit()
        connection.close()

        connection = mysql.connect()
        cursor = connection.cursor()

        sqlhr = "SELECT name_hr,surname_hr,phone,nickname,email_hr FROM mail_hr WHERE employeeid = %s"
        cursor.execute(sqlhr,(data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        result_hr = toJson(cursor.fetchall(),columns)

        connection.commit()
        connection.close()
        resultlast={}
        resultlast['personal_detail'] = result_per
        resultlast['hr_detail'] = result_hr
        return jsonify(resultlast)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/send_Mail_starwork', methods=['POST'])
@connect_sql()
def send_Mail_starwork(cursor):
    dataInput = request.json
    source = dataInput['source']
    data_new = source
    for item in data_new:
        print(item)
    newkey = len(list(data_new.keys()))
    for max in range(newkey):
        newvalues = str("%s,"*(max+1))
        newvalues = newvalues[:-1]
    print(newvalues)
    return 'hello'
def sendMail_appointment(email,appoint_day,appoint_time,appoint_place,position,name,surname,name_hr,surname_hr,email_hr,phone,nickname):
    send_from = " "+name_hr+" "+surname_hr+" <"+email_hr+">"
    send_to = email
    send_cc = email_hr
    send_bcc = email_hr
    subject = "ขอเรียนเชิญสัมภาษณ์งาน ตำแหน่ง "+position+" บริษัท อินเทอร์เน็ตประเทศไทย จำกัด (มหาชน)"
    text = """\
                <html>
                  <body>
                    <p style="font-size: 16px;margin-bottom: 40px;"><span style="font-weight: bold;">เรียน</span>  คุณ"""+name+""" """+surname+"""</p>

                      <p style="text-indent: 20px;">บริษัท อินเทอร์เน็ตประเทศไทย จำกัด (มหาชน)  ขอเรียนเชิญสัมภาษณ์งาน <span style="font-weight:bold; background-color: rgb(255, 204, 153);">ตำแหน่ง """+position+"""</span><br>
                       ใน<span style="font-weight:bold; background-color: rgb(255, 204, 153);">วันที่ """+appoint_day+""" เวลา """+appoint_time+""" น.</span> ณ อาคารไทยซัมมิททาวเวอร์  ชั้น IT ห้องประชุม INET """+appoint_place+"""</p>
                      <p><span style="font-weight:bold;">สามารถดูรายละเอียดลักษณะงานได้ที่ :</span> <a href="http://www.inet.co.th/careers/">http://www.inet.co.th/careers/</a></p>

                      <p style="font-weight:bold; line-height: 30px;"><span style="background-color: yellow;">ทั้งนี้รบกวนตอบกลับเข้ารับการสัมภาษณ์ทาง Email ด้วยนะครับ</span></p>

                      <p style="font-weight:bold; line-height: 30px;">กรอกใบสมัครออนไลน์ <a href="http://career.inet.co.th/">http://career.inet.co.th/</a><span style="font-weight:bold; background-color: rgb(255, 204, 153);">(กรุณากรอกก่อนเข้ามาสัมภาษณ์)</span></p>
                      <p style="font-weight:bold;">โดยเตรียมเอกสารเอกสารประกอบการสมัครงาน ดังนี้</p>
                      <p>- สำเนาบัตรประชาชน                                              จำนวน    2  ฉบับ (สำเนาถูกต้องด้วยหมึกปากกาสีน้ำเงินเท่านั้น)</p>
                      <p>- สำเนาทะเบียนบ้าน                                               จำนวน    1  ฉบับ (สำเนาถูกต้องด้วยหมึกปากกาสีน้ำเงินเท่านั้น)</p>
                      <p>- สำเนาหลักฐานการศึกษา                                           จำนวน    1  ฉบับ (สำเนาถูกต้องด้วยหมึกปากกาสีน้ำเงินเท่านั้น)</p>
                      <p>- รูปถ่าย 1นิ้ว ไม่เกิน 6 เดือน                                        จำนวน    1   ใบ</p>
                      <p>- หลักฐานการผ่านหรือได้รับการยกเว้นการเกณฑ์ทหาร (ถ้ามี)</p>
                      <p>- ผู้สมัครสามารถนำ Resume  / CV หรือแฟ้มแสดงผลงาน (Port Folio)  มาแสดงเพื่อประกอบการสัมภาษณ์ได้</p></br>

                      <p style="font-weight: bold;">เส้นทางการเดินทาง</p>
                      <p>- รถไฟฟ้าใต้ดิน ลงสถานีเพชรบุรี ออกทางออกที่ 1 ขึ้นบนผิวถนนมองทางซ้ายมือจะเห็นอาคารไทยซัมมิท</p>
                      <p>เดินมาทางซ้ายมือ ข้ามสะพานลอยเข้าอาคาร</p>
                      <p>- ทางเรือคลองแสนแสบ ลงท่าประสานมิตร ขึ้นท่าเรือจะเห็นสะพานข้ามคลอง เดินข้ามสะพานและเดินออกมาที่ถนนใหญ่</p>
                      <p>ถึงถนนเพชรบุรีเลี้ยวขวา เดินเข้าตึกอาคารไทยซัมมิท</p>
                      <p>- รถประจำทาง สาย 11, 23, 206, 113, 99, 72,58,93,60, 512,ปอ.พ.23,ปอ.พ.10,ปอ.185,ปอ.136 เป็นต้น</p>
                      <p>เข้ามาในอาคารขึ้นบันไดเลื่อน ลิฟท์อยู่ทางซ้ายมือ  ( ลิฟท์ Medium Zone)  กดชั้น IT</p>
                      <p>- แผนที่บริษัท <a href="http://www.inet.co.th/contact/"> http://www.inet.co.th/contact/</a></p></br>

                      <p>--</p>
                      <p style="font-size: 18px;">Best regards,</p></br>

                      <p style="font-weight: bold; margin: 0px;font-size: 18px;">"""+name_hr+""" """+surname_hr+""" | """+nickname+"""</p>
                      <p style="margin: 0px;font-size: 18px;">Human Resource Officer</p>
                      <p style="margin: 0px;font-size: 18px; font-style: italic;">Internet Thailand Public Co., Ltd.</p>
                      <p style="margin: 0px;font-size: 18px;">Tel : """+phone+"""</p>
                      <p style="margin: 0px;font-size: 18px;">E-mail : """+email_hr+"""</p>
                      <p style="margin: 0px;font-size: 18px;">Website : <a href="https://inet.co.th/"> https://inet.co.th/</a></p></br>
                       <img src="https://inet.co.th/images/inetlogo.png"></br>
                  </body>
                </html>
        """
    server="mailtx.inet.co.th"

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Cc'] = send_cc
    msg['Bcc'] = send_bcc
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(text, "html","utf-8"))

    try:
        smtp = smtplib.SMTP(server)
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.close()
        result = {'status' : 'done', 'statusDetail' : 'Send email has done'}
        return jsonify(result)
    except:
        result = {'status' : 'error', 'statusDetail' : 'Send email has error : This system cannot send email'}
        return jsonify(result)
def sendMail_starwork(email,name,surname,star_work,position,name_hr,surname_hr,email_hr,phone,nickname):
    send_from = " "+name_hr+" "+surname_hr+" <"+email_hr+">"
    send_to = email
    subject = "ขอยืนยันผลสัมภาษณ์งานตำแหน่ง "+position+" บริษัท อินเทอร์เน็ตประเทศไทย จำกัด (มหาชน)"
    text = """\
                <html>
                  <body>
                 <b>เรียน  """+name+""" """+surname+"""</b></br>
                   <p>บริษัท อินเทอร์เน็ตประเทศไทย จำกัด (มหาชน) <br>
                    ขอยืนยันวันเริ่มงาน ในวันที่ """+star_work+"""  ตำแหน่ง """+position+""" รบกวนเตรียมเอกสารดังนี้ </p>
                   <p>เอกสารที่ต้องสแกนส่งทางอีเมลหากไม่ได้นำมาในวันเริ่มงาน ดังนี้</p></br>
                   <p>- สำเนาบัตรประชาชน                                              จำนวน    2  ฉบับ (สำเนาถูกต้องด้วยหมึกปากกาสีน้ำเงินเท่านั้น)</p></br>
                   <p>- สำเนาทะเบียนบ้าน                                               จำนวน    1  ฉบับ (สำเนาถูกต้องด้วยหมึกปากกาสีน้ำเงินเท่านั้น)</p></br>
                   <p>- สำเนาหลักฐานการศึกษา                                           จำนวน    1  ฉบับ (สำเนาถูกต้องด้วยหมึกปากกาสีน้ำเงินเท่านั้น)</p></br>
                   <p>- รูปถ่าย 1นิ้ว ไม่เกิน 6 เดือน                                        จำนวน    1   ใบ</p></br>
                   <p>เอกสารที่ต้องเตรียมในวันเริ่มงาน ดังนี้</p></br>
                   <p>- สำเนาบัญชี ธนาคารกรุงไทย   พร้อมเซ็นสำเนาถูกต้อง</p></br>
                   <p>- ใบรับรองแพทย์ตรวจสุขภาพทั่วไป 5 โรค  และตรวจเชื้อไวรัสตับอักเสบบี</p></br>
                   <p>ตรวจสุขภาพทั่วไป 5 โรค</p></br>
                   <p>1.วัณโรคในระยะแพร่กระจายเชื้อ</p></br>
                   <p>2.โรคเท้าช้างในระยะที่ปรากฎอาการเป็นที่รังเกียจแก่สังคม</p></br>
                   <p>3.โรคติดยาเสพติดให้โทษ</p></br>
                   <p>4.โรคพิษสุราเรื้อรัง</p></br>
                   <p>5.โรคติดต่อร้ายแรงหรือโรคเรื้อรังที่ปรากฏอาการเด่นชัดหรือรุนแรงและเป็นอุปสรรคต่อการปฏิบัติหน้าที่</p></br></br>
                   <p>กรอกใบสมัครออนไลน์ <a href="http://career.inet.co.th/">http://career.inet.co.th/</a></p></br></br>
                   <p>ทั้งนี้หากได้รับ Email หรือ มีการเปลี่ยนแปลงวันเริ่มงาน กรุณาตอบรับกลับทาง Email ครับ</p></br></br>
                   <p>เส้นทางการเดินทาง</p></br>
                   <p>- รถไฟฟ้าใต้ดิน ลงสถานีเพชรบุรี ออกทางออกที่ 1 ขึ้นบนผิวถนนมองทางซ้ายมือจะเห็นอาคารไทยซัมมิท</p></br>
                   <p>เดินมาทางซ้ายมือ ข้ามสะพานลอยเข้าอาคาร</p></br>
                   <p>- ทางเรือคลองแสนแสบ ลงท่าประสานมิตร ขึ้นท่าเรือจะเห็นสะพานข้ามคลอง เดินข้ามสะพานและเดินออกมาที่ถนนใหญ่</p></br>
                   <p>ถึงถนนเพชรบุรีเลี้ยวขวา เดินเข้าตึกอาคารไทยซัมมิท</p></br>
                   <p>- รถประจำทาง สาย 11, 23, 206, 113, 99, 72,58,93,60, 512,ปอ.พ.23,ปอ.พ.10,ปอ.185,ปอ.136 เป็นต้น</p></br>
                   <p>เข้ามาในอาคารขึ้นบันไดเลื่อน ลิฟท์อยู่ทางซ้ายมือ  ( ลิฟท์ Medium Zone)  กดชั้น IT</p></br>
                   <p>- แผนที่บริษัท <a href="http://www.inet.co.th/contact/"> http://www.inet.co.th/contact/</a></p></br></br>
                   <p>--</p>
                   <p>Best regards,</p>
                   <p>"""+name_hr+""" """+surname_hr+""" | """+nickname+"""</p>
                   <p>Human Resource Officer</p>
                   <p>Internet Thailand Public Co., Ltd.</p>
                   <p>Tel : """+phone+"""</p>
                   <p>E-mail : """+email_hr+"""</p>
                   <p>Website : <a href="https://inet.co.th/"> https://inet.co.th/</a></p></br>
                    <img src="https://inet.co.th/images/inetlogo.png"></br>
                  </body>
                </html>
        """
    server="mailtx.inet.co.th"

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(text, "html","utf-8"))

    try:
        smtp = smtplib.SMTP(server)
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.close()
        result = {'status' : 'done', 'statusDetail' : 'Send email has done'}
        return jsonify(result)
    except:
        result = {'status' : 'error', 'statusDetail' : 'Send email has error : This system cannot send email'}
        return jsonify(result)
