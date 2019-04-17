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
        sql = "SELECT * FROM employee WHERE employeeid=%s"
        cursor.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Resign"

        sqlEM_log = "INSERT INTO employee_log (employeeid,citizenid,name_th,name_eng,surname_th,surname_eng,nickname_employee,salary,email,phone_company,position_id,section_id,org_name_id,cost_center_name_id,company_id,start_work,EndWork_probation,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlEM_log,(result[0]['employeeid'],result[0]['citizenid'],result[0]['name_th'],result[0]['name_eng'],result[0]['surname_th'],result[0]['surname_eng'],result[0]['nickname_employee'],result[0]['salary'],result[0]['email'],result[0]['phone_company'],result[0]['position_id'],\
        result[0]['section_id'],result[0]['org_name_id'],result[0]['cost_center_name_id'],result[0]['company_id'],\
        result[0]['start_work'],result[0]['EndWork_probation'],data_new['createby'],type_action))

        sqlemployee = "DELETE FROM employee WHERE employeeid=%s"
        cursor.execute(sqlemployee,data_new['employeeid'])

        sqlemployee_ga = "DELETE FROM employee_benefits WHERE employeeid=%s"
        cursor.execute(sqlemployee_ga,data_new['employeeid'])

        sqlEmp_pro = "DELETE FROM Emp_probation WHERE employeeid=%s"
        cursor.execute(sqlEmp_pro,data_new['employeeid'])

        sqlIn4 = "INSERT INTO employee_resign (employeeid,name_th,surname_th,ID_CardNo,star_work,issue_date,createby,Description) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn4,(data_new['employeeid'],result[0]['name_th'],result[0]['surname_th'],result[0]['citizenid'],result[0]['start_work'],data_new['issue_date'],data_new['createby'],data_new['Descriptions']))

        try:
            UpAddress = "DELETE FROM Address  WHERE ID_CardNo=%s"
            cursor.execute(UpAddress,(result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpAttachment = "DELETE FROM Attachment  WHERE ID_CardNo=%s"
            cursor.execute(UpAttachment,(result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpComputerSkill = "DELETE FROM ComputerSkill  WHERE ID_CardNo=%s"
            cursor.execute(UpComputerSkill,(result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpContract = "DELETE FROM Contract WHERE ID_CardNo=%s"
            cursor.execute(UpContract,(result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpEducation = "DELETE FROM Education  WHERE ID_CardNo=%s"
            cursor.execute(UpEducation,(result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            Upemployee_benefits= "DELETE FROM employee_benefits WHERE ID_CardNo=%s"
            cursor.execute(Upemployee_benefits,(result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpEmployment= "DELETE FROM Employment  WHERE ID_CardNo=%s"
            cursor.execute(UpEmployment,(result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpEmp_probation= "DELETE FROM Emp_probation WHERE ID_CardNo=%s"
            cursor.execute(UpEmp_probation,(result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpFamily= "DELETE FROM Family  WHERE ID_CardNo=%s"
            cursor.execute(UpFamily,(result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpLanguagesSkill= "DELETE FROM LanguagesSkill  WHERE ID_CardNo=%s"
            cursor.execute(UpLanguagesSkill,(result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpReference= "DELETE FROM Reference  WHERE ID_CardNo=%s"
            cursor.execute(UpReference,(result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpRefPerson= "DELETE FROM RefPerson  WHERE ID_CardNo=%s"
            cursor.execute(UpRefPerson,(result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpSpecialSkill= "DELETE FROM SpecialSkill  WHERE ID_CardNo=%s"
            cursor.execute(UpSpecialSkill,(result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpTrainingCourse= "DELETE FROM TrainingCourse  WHERE ID_CardNo=%s"
            cursor.execute(UpTrainingCourse,(result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpApprove= "DELETE FROM approve_probation  WHERE employeeid=%s"
            cursor.execute(UpApprove,(data_new['employeeid']))
        except Exception as e:
            pass

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
        sql = "SELECT employee.name_th,employee.employeeid,employee.surname_th,employee.citizenid,employee.start_work,company.company_short_name,position.position_detail,section.sect_detail,org_name.org_name_detail,cost_center_name.cost_detail FROM employee LEFT JOIN company ON company.companyid = employee.company_id\
                                      LEFT JOIN position ON position.position_id = employee.position_id\
                                      LEFT JOIN section ON section.sect_id = employee.section_id\
                                      LEFT JOIN org_name ON org_name.org_name_id = employee.org_name_id\
                                      LEFT JOIN cost_center_name ON cost_center_name.cost_center_name_id = employee.cost_center_name_id"
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

        result_token = CheckTokenAdmin(data_new['createby'],data_new['token'])
        if result_token!='pass':
            return 'token fail'

        sqlEmployee = "SELECT * FROM employee LEFT JOIN company ON company.companyid = employee.company_id\
                                      LEFT JOIN position ON position.position_id = employee.position_id\
                                      LEFT JOIN section ON section.sect_id = employee.section_id\
                                      LEFT JOIN org_name ON org_name.org_name_id = employee.org_name_id\
                                      LEFT JOIN cost_center_name ON cost_center_name.cost_center_name_id = employee.cost_center_name_id\
        WHERE employee.employeeid=%s"
        cursor.execute(sqlEmployee,data_new['employeeid'])
        columnsEmployee = [column[0] for column in cursor.description]
        resultEmployee = toJson(cursor.fetchall(),columnsEmployee)
        try:
            decodesalary = base64.b64decode(resultEmployee[0]['salary'])
        except Exception as e:
            decodesalary = ""

        sqlEmployee_email = "SELECT email FROM employee WHERE employee.employeeid=%s"
        cursor.execute(sqlEmployee_email,data_new['employeeid'])
        columnsEmployeeEmail = [column[0] for column in cursor.description]
        resultEmployee_Email = toJson(cursor.fetchall(),columnsEmployeeEmail)

        try:
            sqlEm = "SELECT Address.AddressType,Address.HouseNo,Address.Street,Address.DISTRICT_ID,Address.AMPHUR_ID,Address.PROVINCE_ID,Address.PostCode,Address.Tel,Address.Fax FROM Address INNER JOIN Personal ON Personal.ID_CardNo=Address.ID_CardNo \
            WHERE Personal.ID_CardNo=%s AND Address.AddressType='Home'"
            cursor.execute(sqlEm,resultEmployee[0]['citizenid'])
            columnsEm = [column[0] for column in cursor.description]
            resultAddress_home = toJson(cursor.fetchall(),columnsEm)
        except Exception as e:
            resultAddress_home = ""
        try:
            sqlEm_persent = "SELECT Address.AddressType,Address.HouseNo,Address.Street,Address.DISTRICT_ID,Address.AMPHUR_ID,Address.PROVINCE_ID,Address.PostCode,Address.Tel,Address.Fax FROM Address INNER JOIN Personal ON Personal.ID_CardNo=Address.ID_CardNo \
            WHERE Personal.ID_CardNo=%s AND Address.AddressType='Present'"
            cursor.execute(sqlEm_persent,resultEmployee[0]['citizenid'])
            columnsEmAD = [column[0] for column in cursor.description]
            resultAddress_Present = toJson(cursor.fetchall(),columnsEmAD)
        except Exception as e:
            resultAddress_Present = ""
        try:
            sql4 = "SELECT Attachment.Type,Attachment.PathFile FROM Attachment INNER JOIN Personal ON Personal.ID_CardNo=Attachment.ID_CardNo \
            WHERE Personal.ID_CardNo=%s"
            cursor.execute(sql4,resultEmployee[0]['citizenid'])
            columns4 = [column[0] for column in cursor.description]
            result4 = toJson(cursor.fetchall(),columns4)
        except Exception as e:
            result4 = ""
        try:
            sql6 = "SELECT ComputerSkill.ComSkill,ComputerSkill.Level FROM ComputerSkill INNER JOIN Personal ON Personal.ID_CardNo=ComputerSkill.ID_CardNo \
            WHERE Personal.ID_CardNo=%s"
            cursor.execute(sql6,resultEmployee[0]['citizenid'])
            columns6 = [column[0] for column in cursor.description]
            result6 = toJson(cursor.fetchall(),columns6)
        except Exception as e:
            result6 = ""
        try:
            sql9 = "SELECT Education.EducationLevel,Education.Institute,Education.StartYear,Education.EndYear,Education.Qualification,Education.Major,Education.GradeAvg,Education.ExtraCurricularActivities FROM Education INNER JOIN Personal ON Personal.ID_CardNo=Education.ID_CardNo \
            WHERE Personal.ID_CardNo=%s"
            cursor.execute(sql9,resultEmployee[0]['citizenid'])
            columns9 = [column[0] for column in cursor.description]
            result9 = toJson(cursor.fetchall(),columns9)
        except Exception as e:
            result9 = ""
        try:
            sql10 = "SELECT Employment.CompanyName,Employment.CompanyAddress,Employment.PositionHeld,Employment.StartSalary,Employment.EndSalary,Employment.StartYear,Employment.EndYear,Employment.Responsibility,Employment.ReasonOfLeaving,Employment.Descriptionofwork FROM Employment INNER JOIN Personal ON Personal.ID_CardNo=Employment.ID_CardNo \
            WHERE Personal.ID_CardNo=%s"
            cursor.execute(sql10,resultEmployee[0]['citizenid'])
            columns10 = [column[0] for column in cursor.description]
            result10 = toJson(cursor.fetchall(),columns10)
        except Exception as e:
            result10 = ""
        try:
            sqlfa = "SELECT Family.MemberType,Family.Name,Family.Surname,Family.Occupation,Family.Address,Family.Tel,Family.Fax FROM Family INNER JOIN Personal ON Personal.ID_CardNo=Family.ID_CardNo \
            WHERE (Family.MemberType = 'Father' OR Family.MemberType = 'Mother')AND Personal.ID_CardNo=%s"
            cursor.execute(sqlfa,resultEmployee[0]['citizenid'])
            columnsfa = [column[0] for column in cursor.description]
            resultfa = toJson(cursor.fetchall(),columnsfa)
        except Exception as e:
            resultfa = ""
        try:
            sqlbro = "SELECT Family.MemberType,Family.Name,Family.Surname,Family.Occupation,Family.Address,Family.Tel,Family.Fax FROM Family INNER JOIN Personal ON Personal.ID_CardNo=Family.ID_CardNo \
            WHERE Family.MemberType = 'BrotherSister' AND Personal.ID_CardNo=%s"
            cursor.execute(sqlbro,resultEmployee[0]['citizenid'])
            columnsbro = [column[0] for column in cursor.description]
            resultbro = toJson(cursor.fetchall(),columnsbro)
        except Exception as e:
            resultbro = ""
        try:
            sql13 = "SELECT LanguagesSkill.Languages,LanguagesSkill.Speaking,LanguagesSkill.Reading,LanguagesSkill.Writting FROM LanguagesSkill INNER JOIN Personal ON Personal.ID_CardNo=LanguagesSkill.ID_CardNo \
            WHERE Personal.ID_CardNo=%s"
            cursor.execute(sql13,resultEmployee[0]['citizenid'])
            columns13 = [column[0] for column in cursor.description]
            result13 = toJson(cursor.fetchall(),columns13)
        except Exception as e:
            result13 = ""
        try:
            sql14 = "SELECT * FROM Personal \
            WHERE ID_CardNo=%s"
            cursor.execute(sql14,resultEmployee[0]['citizenid'])
            columns14 = [column[0] for column in cursor.description]
            result_Personal = toJson(cursor.fetchall(),columns14)
        except Exception as e:
            result_Personal = ""
        try:
            encoded_Image=str("http://intranet.inet.co.th/assets/upload/staff/"+str(data_new['employeeid'])+".jpg")
            open_path_ = urllib.urlopen(encoded_Image)
            htmlSource = open_path_.read()
            open_path_.close()
            test= htmlSource.decode('utf-8')
            encoded_Image=str("http://intranet.inet.co.th/assets/upload/staff/"+str(data_new['employeeid'])+"s.jpg")
        except Exception as e:
            encoded_Image=str("http://intranet.inet.co.th/assets/upload/staff/"+str(data_new['employeeid'])+".jpg")
        try:
            sql17 = "SELECT Reference.RelativeName,Reference.RelativeSurname,Reference.RelativePosition,Reference.RelativeRelationship,Reference.PhysicalHandicap,Reference.PhysicalHandicapDetail,Reference.KnowFrom FROM Reference INNER JOIN Personal ON Personal.ID_CardNo=Reference.ID_CardNo \
            WHERE Personal.ID_CardNo=%s"
            cursor.execute(sql17,resultEmployee[0]['citizenid'])
            columns17 = [column[0] for column in cursor.description]
            result17 = toJson(cursor.fetchall(),columns17)
        except Exception as e:
            result17 = ""
        try:
            sql18 = "SELECT RefPerson.RefName,RefPerson.RefPosition,RefPerson.RefAddress,RefPerson.RefTel FROM RefPerson INNER JOIN Personal ON Personal.ID_CardNo=RefPerson.ID_CardNo \
            WHERE Personal.ID_CardNo=%s"
            cursor.execute(sql18,resultEmployee[0]['citizenid'])
            columns18 = [column[0] for column in cursor.description]
            result18 = toJson(cursor.fetchall(),columns18)
        except Exception as e:
            result18 = ""
        try:
            sql20 = "SELECT SpecialSkill.CarDrivingLicense,SpecialSkill.MotorBicycleDrivingLicense,SpecialSkill.OwnCar,SpecialSkill.OwnMotorBicycle,SpecialSkill.WorkUpCountry,SpecialSkill.StartWorkEarliest,SpecialSkill.PhysicalDisabilityOrDisease,SpecialSkill.DischargeFromEmployment,SpecialSkill.DischargeFromEmploymentReason,SpecialSkill.Arrested,SpecialSkill.ArrestedReason FROM SpecialSkill INNER JOIN Personal ON Personal.ID_CardNo=SpecialSkill.ID_CardNo \
            WHERE Personal.ID_CardNo=%s"
            cursor.execute(sql20,resultEmployee[0]['citizenid'])
            columns20 = [column[0] for column in cursor.description]
            result20 = toJson(cursor.fetchall(),columns20)
        except Exception as e:
            result20 = ""
        try:
            sql23 = "SELECT TrainingCourse.Subject,TrainingCourse.Place,TrainingCourse.StartDate,TrainingCourse.EndDate FROM TrainingCourse INNER JOIN Personal ON Personal.ID_CardNo=TrainingCourse.ID_CardNo \
            WHERE Personal.ID_CardNo=%s"
            cursor.execute(sql23,resultEmployee[0]['citizenid'])
            columns23 = [column[0] for column in cursor.description]
            result23 = toJson(cursor.fetchall(),columns23)
        except Exception as e:
            result23 = ""
        try:
            sqlcontract = "SELECT Authority_Distrinct_Id_Card FROM Contract WHERE ID_CardNo=%s"
            cursor.execute(sqlcontract,resultEmployee[0]['citizenid'])
            columnscontract = [column[0] for column in cursor.description]
            resultcontract_all = toJson(cursor.fetchall(),columnscontract)
            resultcontract = resultcontract_all[0]['Authority_Distrinct_Id_Card']
        except Exception as e:
            resultcontract = ""

        arr={}
        arr["Address_home"] = resultAddress_home
        arr["Address_Present"] = resultAddress_Present
        arr["Authority_Distrinct"] = resultcontract
        # arr["Authority_Distrinct"] = resultcontract[0]['Authority_Distrinct_Id_Card']
        arr["employee"] = resultEmployee
        arr["Attachment"] = result4
        arr["Image_profile"] = encoded_Image
        arr["EmailEmp"] = resultEmployee_Email
        arr["Decodesalary"] = decodesalary
        arr["ComputerSkill"] = result6
        arr["Education"] = result9
        arr["Employment"] = result10
        arr['fatherAndmother'] = resultfa
        arr['BrotherSister'] = resultbro
        arr["LanguagesSkill"] = result13
        arr["Personal"] = result_Personal
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

        sql = "SELECT * FROM employee WHERE employeeid=%s"
        cursor.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Edit"

        sqlEM_log = "INSERT INTO employee_log (employeeid,citizenid,name_th,name_eng,surname_th,surname_eng,nickname_employee,salary,email,phone_company,position_id,section_id,org_name_id,cost_center_name_id,company_id,start_work,EndWork_probation,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlEM_log,(result[0]['employeeid'],result[0]['citizenid'],result[0]['name_th'],result[0]['name_eng'],result[0]['surname_th'],result[0]['surname_eng'],result[0]['nickname_employee'],result[0]['salary'],result[0]['email'],result[0]['phone_company'],result[0]['position_id'],\
        result[0]['section_id'],result[0]['org_name_id'],result[0]['cost_center_name_id'],result[0]['company_id'],result[0]['start_work'],result[0]['EndWork_probation'],data_new['createby'],type_action))

        try:
            sqlEM_pro_log = "INSERT INTO Emp_probation_log (employeeid,citizenid,name_th,name_eng,surname_th,surname_eng,nickname_employee,salary,email,phone_company,position_id,section_id,org_name_id,cost_center_name_id,company_id,start_work,EndWork_probation,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlEM_pro_log,(result[0]['employeeid'],result[0]['citizenid'],result[0]['name_th'],result[0]['name_eng'],result[0]['surname_th'],result[0]['surname_eng'],result[0]['nickname_employee'],result[0]['salary'],result[0]['email'],result[0]['phone_company'],result[0]['position_id'],\
            result[0]['section_id'],result[0]['org_name_id'],result[0]['cost_center_name_id'],result[0]['company_id'],result[0]['start_work'],result[0]['EndWork_probation'],data_new['createby'],type_action))

        except Exception as e:
            pass
        date1 = data_new['Start_contract']
        long_date = int(data_new['long_date'])-1
        star_date = date1.split("-")
        Day_s = int(star_date[0])
        Mon_s =int(star_date[1])
        year_s = int(star_date[2])
        next_3_m = date(year_s,Mon_s,Day_s) + relativedelta(days=long_date)
        next_3_m2 = str(next_3_m)
        end_date = next_3_m2.split("-")
        Day_e = end_date[2]
        Mon_e =end_date[1]
        year_e = end_date[0]
        End_probation_date = Day_e+"-"+Mon_e+"-"+year_e
        try:
            encodedsalary = base64.b64encode(data_new['salary'])
        except Exception as e:
            encodedsalary = ""
        sql_Up_EM = "DELETE FROM employee WHERE citizenid=%s AND employeeid=%s"
        cursor.execute(sql_Up_EM,(result[0]['citizenid'],data_new['employeeid']))

        sqlEM = "INSERT INTO employee (employeeid,citizenid,name_th,name_eng,surname_th,surname_eng,nickname_employee,salary,email,phone_company,position_id,section_id,org_name_id,cost_center_name_id,company_id,start_work,EndWork_probation,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlEM,(data_new['employeeid'],data_new['ID_CardNo'],data_new['NameTh'],data_new['NameEn'],data_new['SurnameTh'],data_new['SurnameEn'],data_new['NicknameEn'],encodedsalary,data_new['Email'],\
        data_new['phone_company'],data_new['position_id'],\
        data_new['section_id'],data_new['org_name_id'],data_new['cost_center_name_id'],data_new['company_id'],data_new['Start_contract'],End_probation_date,data_new['createby']))

        # sql_Up_EM_pro = "DELETE FROM Emp_probation WHERE citizenid=%s AND employeeid=%s"
        # cursor.execute(sql_Up_EM_pro,(result[0]['citizenid'],data_new['employeeid']))
        try:
            sqlEM_pro = "UPDATE Emp_probation SET  employeeid=%s,citizenid=%s,name_th=%s,name_eng=%s,surname_th=%s,surname_eng=%s,nickname_employee=%s,salary=%s,email=%s,phone_company=%s,position_id=%s,section_id=%s,org_name_id=%s,cost_center_name_id=%s,company_id=%s,start_work=%s,EndWork_probation=%s,createby=%s WHERE citizenid=%s AND employeeid=%s"
            cursor.execute(sqlEM_pro,(data_new['employeeid'],data_new['ID_CardNo'],data_new['NameTh'],data_new['NameEn'],data_new['SurnameTh'],data_new['SurnameEn'],data_new['NicknameEn'],encodedsalary,data_new['Email'],\
            data_new['phone_company'],data_new['position_id'],\
            data_new['section_id'],data_new['org_name_id'],data_new['cost_center_name_id'],data_new['company_id'],data_new['Start_contract'],End_probation_date,data_new['createby'],result[0]['citizenid'],data_new['employeeid']))
        except Exception as e:
            pass

        UpPersonal = "UPDATE Personal SET ID_CardNo=%s,NameTh=%s,SurnameTh=%s,NameEn=%s,SurnameEn=%s,NicknameEn=%s WHERE ID_CardNo=%s"
        cursor.execute(UpPersonal,(data_new['ID_CardNo'],data_new['NameTh'],data_new['SurnameTh'],data_new['NameEn'],data_new['SurnameEn'],data_new['NicknameEn'],result[0]['citizenid']))

        try:
            UpAddress = "UPDATE Address SET ID_CardNo=%s WHERE ID_CardNo=%s"
            cursor.execute(UpAddress,(data_new['ID_CardNo'],result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpAttachment = "UPDATE Attachment SET ID_CardNo=%s WHERE ID_CardNo=%s"
            cursor.execute(UpAttachment,(data_new['ID_CardNo'],result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpComputerSkill = "UPDATE ComputerSkill SET ID_CardNo=%s WHERE ID_CardNo=%s"
            cursor.execute(UpComputerSkill,(data_new['ID_CardNo'],result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpContract = "UPDATE Contract SET ID_CardNo=%s WHERE ID_CardNo=%s"
            cursor.execute(UpContract,(data_new['ID_CardNo'],result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpEducation = "UPDATE Education SET ID_CardNo=%s WHERE ID_CardNo=%s"
            cursor.execute(UpEducation,(data_new['ID_CardNo'],result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            Upemployee= "UPDATE employee SET ID_CardNo=%s WHERE ID_CardNo=%s"
            cursor.execute(Upemployee,(data_new['ID_CardNo'],result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            Upemployee_benefits= "UPDATE employee_benefits SET ID_CardNo=%s WHERE ID_CardNo=%s"
            cursor.execute(Upemployee_benefits,(data_new['ID_CardNo'],result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpEmployment= "UPDATE Employment SET ID_CardNo=%s WHERE ID_CardNo=%s"
            cursor.execute(UpEmployment,(data_new['ID_CardNo'],result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpEmp_probation= "UPDATE Emp_probation SET ID_CardNo=%s WHERE ID_CardNo=%s"
            cursor.execute(UpEmp_probation,(data_new['ID_CardNo'],result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpFamily= "UPDATE Family SET ID_CardNo=%s WHERE ID_CardNo=%s"
            cursor.execute(UpFamily,(data_new['ID_CardNo'],result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpLanguagesSkill= "UPDATE LanguagesSkill SET ID_CardNo=%s WHERE ID_CardNo=%s"
            cursor.execute(UpLanguagesSkill,(data_new['ID_CardNo'],result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpLanguagesSkill= "UPDATE LanguagesSkill SET ID_CardNo=%s WHERE ID_CardNo=%s"
            cursor.execute(UpLanguagesSkill,(data_new['ID_CardNo'],result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpReference= "UPDATE Reference SET ID_CardNo=%s WHERE ID_CardNo=%s"
            cursor.execute(UpReference,(data_new['ID_CardNo'],result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpRefPerson= "UPDATE RefPerson SET ID_CardNo=%s WHERE ID_CardNo=%s"
            cursor.execute(UpRefPerson,(data_new['ID_CardNo'],result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpRefPerson= "UPDATE RefPerson SET ID_CardNo=%s WHERE ID_CardNo=%s"
            cursor.execute(UpRefPerson,(data_new['ID_CardNo'],result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpSpecialSkill= "UPDATE SpecialSkill SET ID_CardNo=%s WHERE ID_CardNo=%s"
            cursor.execute(UpSpecialSkill,(data_new['ID_CardNo'],result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpTrainingCourse= "UPDATE TrainingCourse SET ID_CardNo=%s WHERE ID_CardNo=%s"
            cursor.execute(UpTrainingCourse,(data_new['ID_CardNo'],result[0]['citizenid']))
        except Exception as e:
            pass

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee_Personal', methods=['POST'])
@connect_sql()
def EditEmployee_Personal(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT citizenid FROM employee WHERE employeeid=%s"
        cursor.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sql_Select_Personal = "SELECT * FROM Personal WHERE ID_CardNo=%s"
        cursor.execute(sql_Select_Personal,(result[0]['citizenid']))
        columns = [column[0] for column in cursor.description]
        result_Personal = toJson(cursor.fetchall(),columns)

        type_action = "Edit"

        sqlIn14_log = """INSERT INTO Personal_log (NameTh,SurnameTh,NicknameTh,NameEn,SurnameEn,NicknameEn,Birthdate,Birthdate_name,BirthPlace,BirthProvince,BirthCountry,Age,Height,Weight,BloodGroup,Citizenship,Religion,ID_CardNo,IssueDate,ExpiryDate,MaritalStatus,NumberOfChildren,StudyChild,MilitaryService,Others,Worktel,Mobile,Email,EmergencyPerson,EmergencyRelation,EmergencyAddress,EmergencyTel,date,createby,type_action) \
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sqlIn14_log,(result_Personal[0]['NameTh'],result_Personal[0]['SurnameTh'],result_Personal[0]['NicknameTh'],result_Personal[0]['NameEn'],\
        result_Personal[0]['SurnameEn'],result_Personal[0]['NicknameEn'],result_Personal[0]['Birthdate'],result_Personal[0]['Birthdate_name'],result_Personal[0]['BirthPlace'],result_Personal[0]['BirthProvince'], \
        result_Personal[0]['BirthCountry'],result_Personal[0]['Age'],result_Personal[0]['Height'],result_Personal[0]['Weight'],result_Personal[0]['BloodGroup'],result_Personal[0]['Citizenship'],result_Personal[0]['Religion'],result_Personal[0]['ID_CardNo'], \
        result_Personal[0]['IssueDate'],result_Personal[0]['ExpiryDate'],result_Personal[0]['MaritalStatus'],result_Personal[0]['NumberOfChildren'],result_Personal[0]['StudyChild'],result_Personal[0]['MilitaryService'],result_Personal[0]['Others'], \
        result_Personal[0]['Worktel'],result_Personal[0]['Mobile'],result_Personal[0]['Email'],result_Personal[0]['EmergencyPerson'],result_Personal[0]['EmergencyRelation'],result_Personal[0]['EmergencyAddress'],result_Personal[0]['EmergencyTel'],result_Personal[0]['date'],data_new['createby'],type_action))

        sql_Up_Personal = "DELETE FROM Personal WHERE ID_CardNo=%s"
        cursor.execute(sql_Up_Personal,(result[0]['citizenid']))

        date_name = str(data_new['Birthdate'])
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

        sqlIn14 = """INSERT INTO Personal (NameTh,SurnameTh,NicknameTh,NameEn,SurnameEn,NicknameEn,Birthdate,Birthdate_name,BirthPlace,BirthProvince,BirthCountry,Age,Height,Weight,BloodGroup,Citizenship,Religion,ID_CardNo,IssueDate,ExpiryDate,MaritalStatus,NumberOfChildren,StudyChild,MilitaryService,Others,Worktel,Mobile,Email,EmergencyPerson,EmergencyRelation,EmergencyAddress, \
        EmergencyTel,date)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sqlIn14,(result_Personal[0]['NameTh'],result_Personal[0]['SurnameTh'],result_Personal[0]['NicknameTh'],result_Personal[0]['NameEn'],result_Personal[0]['SurnameEn'],result_Personal[0]['NicknameEn'],data_new['Birthdate'],Birthdate_name,data_new['BirthPlace'],data_new['BirthProvince'],data_new['BirthCountry'],\
        data_new['Age'],data_new['Height'],data_new['Weight'],data_new['BloodGroup'],data_new['Citizenship'],data_new['Religion'],data_new['ID_CardNo'],data_new['IssueDate'],data_new['ExpiryDate'],data_new['MaritalStatus'],data_new['NumberOfChildren'],data_new['StudyChild'],data_new['MilitaryService'],\
        data_new['Others'],result_Personal[0]['Worktel'],result_Personal[0]['Mobile'],result_Personal[0]['Email'],result_Personal[0]['EmergencyPerson'],result_Personal[0]['EmergencyRelation'],result_Personal[0]['EmergencyAddress'],result_Personal[0]['EmergencyTel'],result_Personal[0]['date']))

        sqlUpAuthority = "UPDATE Contract SET Authority_Distrinct_Id_Card=%s WHERE ID_CardNo=%s"
        cursor.execute(sqlUpAuthority,(data_new['Authority_Distrinct_Id_Card'],result[0]['citizenid']))

        try:
            UpAddress = "UPDATE Address SET ID_CardNo=%s WHERE ID_CardNo=%s"
            cursor.execute(UpAddress,(data_new['ID_CardNo'],result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpAttachment = "UPDATE Attachment SET ID_CardNo=%s WHERE ID_CardNo=%s"
            cursor.execute(UpAttachment,(data_new['ID_CardNo'],result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpComputerSkill = "UPDATE ComputerSkill SET ID_CardNo=%s WHERE ID_CardNo=%s"
            cursor.execute(UpComputerSkill,(data_new['ID_CardNo'],result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpContract = "UPDATE Contract SET ID_CardNo=%s WHERE ID_CardNo=%s"
            cursor.execute(UpContract,(data_new['ID_CardNo'],result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpEducation = "UPDATE Education SET ID_CardNo=%s WHERE ID_CardNo=%s"
            cursor.execute(UpEducation,(data_new['ID_CardNo'],result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            Upemployee= "UPDATE employee SET ID_CardNo=%s WHERE ID_CardNo=%s"
            cursor.execute(Upemployee,(data_new['ID_CardNo'],result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            Upemployee_benefits= "UPDATE employee_benefits SET ID_CardNo=%s WHERE ID_CardNo=%s"
            cursor.execute(Upemployee_benefits,(data_new['ID_CardNo'],result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpEmployment= "UPDATE Employment SET ID_CardNo=%s WHERE ID_CardNo=%s"
            cursor.execute(UpEmployment,(data_new['ID_CardNo'],result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpEmp_probation= "UPDATE Emp_probation SET ID_CardNo=%s WHERE ID_CardNo=%s"
            cursor.execute(UpEmp_probation,(data_new['ID_CardNo'],result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpFamily= "UPDATE Family SET ID_CardNo=%s WHERE ID_CardNo=%s"
            cursor.execute(UpFamily,(data_new['ID_CardNo'],result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpLanguagesSkill= "UPDATE LanguagesSkill SET ID_CardNo=%s WHERE ID_CardNo=%s"
            cursor.execute(UpLanguagesSkill,(data_new['ID_CardNo'],result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpLanguagesSkill= "UPDATE LanguagesSkill SET ID_CardNo=%s WHERE ID_CardNo=%s"
            cursor.execute(UpLanguagesSkill,(data_new['ID_CardNo'],result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpReference= "UPDATE Reference SET ID_CardNo=%s WHERE ID_CardNo=%s"
            cursor.execute(UpReference,(data_new['ID_CardNo'],result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpRefPerson= "UPDATE RefPerson SET ID_CardNo=%s WHERE ID_CardNo=%s"
            cursor.execute(UpRefPerson,(data_new['ID_CardNo'],result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpRefPerson= "UPDATE RefPerson SET ID_CardNo=%s WHERE ID_CardNo=%s"
            cursor.execute(UpRefPerson,(data_new['ID_CardNo'],result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpSpecialSkill= "UPDATE SpecialSkill SET ID_CardNo=%s WHERE ID_CardNo=%s"
            cursor.execute(UpSpecialSkill,(data_new['ID_CardNo'],result[0]['citizenid']))
        except Exception as e:
            pass
        try:
            UpTrainingCourse= "UPDATE TrainingCourse SET ID_CardNo=%s WHERE ID_CardNo=%s"
            cursor.execute(UpTrainingCourse,(data_new['ID_CardNo'],result[0]['citizenid']))
        except Exception as e:
            pass

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee_AddressType', methods=['POST'])
@connect_sql()
def EditEmployee_AddressType(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT citizenid FROM employee WHERE employeeid=%s"
        cursor.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sql2 = "SELECT * FROM Address WHERE ID_CardNo=%s"
        cursor.execute(sql2,result[0]['citizenid'])
        columns = [column[0] for column in cursor.description]
        result2 = toJson(cursor.fetchall(),columns)

        type_action = "Edit"

        i=0
        for i in xrange(len(result2)):
            sqlIn13_log = "INSERT INTO Address_log (ID_CardNo,AddressType,HouseNo,Street,DISTRICT_ID,AMPHUR_ID,PROVINCE_ID,PostCode,Tel,Fax,type_action,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn13_log,(result2[i]['ID_CardNo'],result2[i]['AddressType'],result2[i]['HouseNo'],result2[i]['Street'],result2[i]['DISTRICT_ID'],result2[i]['AMPHUR_ID'],result2[i]['PROVINCE_ID'],result2[i]['PostCode'],result2[i]['Tel'],result2[i]['Fax'],type_action,data_new['createby']))

        sql_Up_Address = "DELETE FROM Address WHERE ID_CardNo=%s"
        cursor.execute(sql_Up_Address,(result[0]['citizenid']))

        if data_new['AddressTypeHome']=='Home':
            sqlIn = "INSERT INTO Address (ID_CardNo,AddressType,HouseNo,Street,DISTRICT_ID,AMPHUR_ID,PROVINCE_ID,PostCode,Tel,Fax,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn,(data_new['ID_CardNo'],data_new['AddressTypeHome'],data_new['HomeNo'],
            data_new['HomeStreet'],data_new['HomeDistrict'],data_new['HomeAmphur'],data_new['HomeProvince'],data_new['HomePostCode'],data_new['HomeTel'],data_new['HomeFax'],data_new['createby']))
        if data_new['AddressTypePresent']=='Present':
            sqlIn = "INSERT INTO Address (ID_CardNo,AddressType,HouseNo,Street,DISTRICT_ID,AMPHUR_ID,PROVINCE_ID,PostCode,Tel,Fax,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn,(data_new['ID_CardNo'],data_new['AddressTypePresent'],data_new['PresentNo'],
            data_new['PresentStreet'],data_new['PresentDistrict'],data_new['PresentAmphur'],data_new['PresentProvince'],data_new['PresentPostCode'],data_new['PresentTel'],data_new['PresentFax'],data_new['createby']))
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee_EmergencyContact', methods=['POST'])
@connect_sql()
def EditEmployee_EmergencyContact(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT citizenid FROM employee WHERE employeeid=%s"
        cursor.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sql_Select_Personal = "SELECT * FROM Personal WHERE ID_CardNo=%s"
        cursor.execute(sql_Select_Personal,(result[0]['citizenid']))
        columns = [column[0] for column in cursor.description]
        result_Personal = toJson(cursor.fetchall(),columns)

        sqlUp_EmerContact = "UPDATE Personal SET EmergencyPerson=%s,EmergencyRelation=%s,EmergencyAddress=%s,EmergencyTel=%s WHERE ID_CardNo=%s"
        cursor.execute(sqlUp_EmerContact,(data_new['EmergencyPerson'],data_new['EmergencyRelation'],data_new['EmergencyAddress'],data_new['EmergencyTel'],result[0]['citizenid']))
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee_ComputerSkill', methods=['POST'])
@connect_sql()
def EditEmployee_ComputerSkill(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT citizenid FROM employee WHERE employeeid=%s"
        cursor.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sql2 = "SELECT * FROM ComputerSkill WHERE ID_CardNo=%s"
        cursor.execute(sql2,result[0]['citizenid'])
        columns = [column[0] for column in cursor.description]
        result2 = toJson(cursor.fetchall(),columns)

        type_action = "Edit"

        i=0
        for i in xrange(len(data_new['ComSkill'])):
            sqlIn6_log = "INSERT INTO ComputerSkill_log (ID_CardNo,ComSkill,Level,type_action,createby) VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn6_log,(data_new['ComSkill'][i]['ID_CardNo'],data_new['ComSkill'][i]['ComSkill'],data_new['ComSkill'][i]['Level'],type_action,data_new['createby']))

        sqlI6de = "DELETE FROM ComputerSkill WHERE ID_CardNo=%s"
        cursor.execute(sqlI6de,result[0]['citizenid'])

        i=0
        for i in xrange(len(data_new['ComSkill'])):
            sqlIn6 = "INSERT INTO ComputerSkill (ID_CardNo,ComSkill,Level,createby) VALUES (%s,%s,%s,%s)"
            cursor.execute(sqlIn6,(data_new['ComSkill'][i]['ID_CardNo'],data_new['ComSkill'][i]['ComSkill'],data_new['ComSkill'][i]['Level'],data_new['createby']))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee_Education', methods=['POST'])
@connect_sql()
def EditEmployee_Education(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT citizenid FROM employee WHERE employeeid=%s"
        cursor.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sql2 = "SELECT * FROM Education WHERE ID_CardNo=%s"
        cursor.execute(sql2,result[0]['citizenid'])
        columns = [column[0] for column in cursor.description]
        result2 = toJson(cursor.fetchall(),columns)

        type_action = "Edit"

        i=0
        for i in xrange(len(result2)):
            sqlIn9_log = "INSERT INTO Education_log (ID_CardNo,EducationLevel,Institute,StartYear,EndYear,Qualification,Major,GradeAvg,ExtraCurricularActivities,type_action,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn9_log,(result2[i]['ID_CardNo'],result2[i]['EducationLevel'],result2[i]['Institute'],result2[i]['StartYear'],result2[i]['EndYear'],result2[i]['Qualification'],\
            result2[i]['Major'],result2[i]['GradeAvg'],result2[i]['ExtraCurricularActivities'],type_action,data_new['createby']))

        sqlI9de = "DELETE FROM Education WHERE ID_CardNo=%s"
        cursor.execute(sqlI9de,result[0]['citizenid'])
        i=0
        for i in xrange(len(data_new['EducationLevel'])):
            sqlIn9 = "INSERT INTO Education (ID_CardNo,EducationLevel,Institute,StartYear,EndYear,Qualification,Major,GradeAvg,ExtraCurricularActivities) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn9,(data_new['EducationLevel'][i]['ID_CardNo'],data_new['EducationLevel'][i]['EducationLevel'],data_new['EducationLevel'][i]['Institute'],data_new['EducationLevel'][i]['StartYear'],data_new['EducationLevel'][i]['EndYear'],data_new['EducationLevel'][i]['Qualification'],\
            data_new['EducationLevel'][i]['Major'],data_new['EducationLevel'][i]['GradeAvg'],data_new['EducationLevel'][i]['ExtraCurricularActivities']))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee_Family', methods=['POST'])
@connect_sql()
def EditEmployee_Family(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT citizenid FROM employee WHERE employeeid=%s"
        cursor.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sql2 = "SELECT * FROM Family WHERE ID_CardNo=%s"
        cursor.execute(sql2,result[0]['citizenid'])
        columns = [column[0] for column in cursor.description]
        result2 = toJson(cursor.fetchall(),columns)

        type_action = "Edit"

        i=0
        for i in xrange(len(result2)):
            sqlIn13_log = "INSERT INTO Family_log (ID_CardNo,MemberType,Name,Surname,Occupation,Address,Tel,Fax,type_action,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn13_log,(result2[i]['ID_CardNo'],result2[i]['MemberType'],result2[i]['Name'],result2[i]['Surname'],result2[i]['Occupation'],result2[i]['Address'],result2[i]['Tel'],result2[i]['Fax'],type_action,data_new['createby']))

        sql_De_Family = "DELETE FROM Family WHERE ID_CardNo=%s"
        cursor.execute(sql_De_Family,(result[0]['citizenid']))

        if data_new['MemberTypeDad']=='Father':
            sqlIn = "INSERT INTO Family (ID_CardNo,MemberType,Name,Surname,Occupation,Address,Tel,Fax,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn,(data_new['ID_CardNoDad'],data_new['MemberTypeDad'],data_new['FatherName'],
            data_new['FatherSurName'],data_new['FatherJob'],data_new['FatherTel'],data_new['FatherFax'],data_new['FatherAddress'],data_new['createby']))
        if data_new['MemberTypeMom']=='Mother':
            sqlIn = "INSERT INTO Family (ID_CardNo,MemberType,Name,Surname,Occupation,Address,Tel,Fax,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn,(data_new['ID_CardNoMom'],data_new['MemberTypeMom'],data_new['MotherName'],
            data_new['MotherSurname'],data_new['MotherJob'],data_new['Mothertel'],data_new['MotherFax'],data_new['MotherAddress'],data_new['createby']))

        i=0
        for i in xrange(len(data_new['BrotherAndSister'])):
            sqlIn11 = "INSERT INTO Family (ID_CardNo,MemberType,Name,Surname,Occupation,Address,Tel,Fax,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn11,(data_new['BrotherAndSister'][i]['ID_CardNo'],data_new['BrotherAndSister'][i]['MemberType'],data_new['BrotherAndSister'][i]['BroAndSisName'],data_new['BrotherAndSister'][i]['BroAndSisSurName'],data_new['BrotherAndSister'][i]['BroAndSisJob'],\
            data_new['BrotherAndSister'][i]['BroAndSisTel'],data_new['BrotherAndSister'][i]['BroAndSisFax'],data_new['BrotherAndSister'][i]['BroAndSisAddress'],data_new['createby']))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee_LanguagesSkill', methods=['POST'])
@connect_sql()
def EditEmployee_LanguagesSkill(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT citizenid FROM employee WHERE employeeid=%s"
        cursor.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sql2 = "SELECT * FROM LanguagesSkill WHERE ID_CardNo=%s"
        cursor.execute(sql2,result[0]['citizenid'])
        columns = [column[0] for column in cursor.description]
        result2 = toJson(cursor.fetchall(),columns)

        type_action = "Edit"

        i=0
        for i in xrange(len(result2)):
            sqlIn13_log = "INSERT INTO LanguagesSkill_log (ID_CardNo,Languages,Speaking,Reading,Writting,type_action,createby) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn13_log,(result2[i]['ID_CardNo'],result2[i]['languageskill'],result2[i]['languagespeak'],result2[i]['languageread'],result2[i]['languagewrite'],type_action,data_new['createby']))

        sqlI13de = "DELETE FROM LanguagesSkill WHERE ID_CardNo=%s"
        cursor.execute(sqlI13de,result[0]['citizenid'])

        i=0
        for i in xrange(len(data_new['Languages'])):
            sqlIn13 = "INSERT INTO LanguagesSkill (ID_CardNo,Languages,Speaking,Reading,Writting,createby) VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn13,(data_new['Languages'][i]['ID_CardNo'],data_new['Languages'][i]['languageskill'],data_new['Languages'][i]['languagespeak'],data_new['Languages'][i]['languageread'],data_new['Languages'][i]['languagewrite'],data_new['createby']))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee_SpecialSkill', methods=['POST'])
@connect_sql()
def EditEmployee_SpecialSkill(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT citizenid FROM employee WHERE employeeid=%s"
        cursor.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        sql2 = "SELECT * FROM SpecialSkill WHERE ID_CardNo=%s"
        cursor.execute(sql2,(result[0]['citizenid']))
        columns = [column[0] for column in cursor.description]
        result2 = toJson(cursor.fetchall(),columns)

        type_action = "Edit"
        try:
            sqlIn20_log = "INSERT INTO SpecialSkill_log (ID_CardNo,CarDrivingLicense,MotorBicycleDrivingLicense,OwnCar,OwnMotorBicycle,WorkUpCountry,PhysicalDisabilityOrDisease,DischargeFromEmployment,DischargeFromEmploymentReason,Arrested,ArrestedReason,type_action,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn20_log,(result2[0]['ID_CardNo'],result2[0]['CarDrivingLicense'],result2[0]['MotorBicycleDrivingLicense'],result2[0]['OwnCar'],result2[0]['OwnMotorBicycle'], \
            result2[0]['WorkUpCountry'],result2[0]['PhysicalDisabilityOrDisease'],result2[0]['DischargeFromEmployment'],result2[0]['DischargeFromEmploymentReason'],result2[0]['Arrested'],result2[0]['ArrestedReason'],type_action,data_new['createby']))

        except Exception as e:
            pass

        sql_De_SpecialSkill = "DELETE FROM SpecialSkill WHERE ID_CardNo=%s"
        cursor.execute(sql_De_SpecialSkill,(result[0]['citizenid']))

        sqlIn20 = "INSERT INTO SpecialSkill (ID_CardNo,CarDrivingLicense,MotorBicycleDrivingLicense,OwnCar,OwnMotorBicycle,WorkUpCountry,PhysicalDisabilityOrDisease,DischargeFromEmployment,DischargeFromEmploymentReason,Arrested,ArrestedReason,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn20,(data_new['ID_CardNo'],data_new['CarDrivingLicense'],data_new['MotorBicycleDrivingLicense'],data_new['OwnCar'],data_new['OwnMotorBicycle'], \
        data_new['WorkUpCountry'],data_new['PhysicalDisabilityOrDisease'],data_new['DischargeFromEmployment'],data_new['DischargeFromEmploymentReason'],data_new['Arrested'],data_new['ArrestedReason'],data_new['createby']))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee_Employment', methods=['POST'])
@connect_sql()
def EditEmployee_Employment(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT citizenid FROM employee WHERE employeeid=%s"
        cursor.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        try:
            sql2 = "SELECT * FROM Employment WHERE ID_CardNo=%s"
            cursor.execute(sql2,result[0]['citizenid'])
            columns = [column[0] for column in cursor.description]
            result2 = toJson(cursor.fetchall(),columns)

            type_action = "Edit"

            i=0
            for i in xrange(len(result2)):
                sqlIn10_log = "INSERT INTO Employment_log (ID_CardNo,CompanyName,CompanyAddress,PositionHeld,StartSalary,EndSalary,StartYear,EndYear,Responsibility,ReasonOfLeaving,Descriptionofwork,type_action,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn10_log,(result2[i]['ID_CardNo'],result2[i]['CompanyName'],result2[i]['CompanyAddress'],result2[i]['PositionHeld'],result2[i]['StartSalary'],\
                result2[i]['EndSalary'],result2[i]['StartYear'],result2[i]['EndYear'], \
                result2[i]['Responsibility'],result2[i]['ReasonOfLeaving'],result2[i]['Descriptionofwork'],type_action,data_new['createby']))

            sqlI10de = "DELETE FROM Employment WHERE ID_CardNo=%s"
            cursor.execute(sqlI10de,result[0]['citizenid'])

            i=0
            for i in xrange(len(data_new['CompanyName'])):
                sqlIn10 = "INSERT INTO Employment (ID_CardNo,CompanyName,CompanyAddress,PositionHeld,StartSalary,EndSalary,StartYear,EndYear,Responsibility,ReasonOfLeaving,Descriptionofwork,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn10,(data_new['CompanyName'][i]['ID_CardNo'],data_new['CompanyName'][i]['CompanyName'],data_new['CompanyName'][i]['CompanyAddress'],data_new['CompanyName'][i]['PositionHeld'],data_new['CompanyName'][i]['StartSalary'],\
                data_new['CompanyName'][i]['EndSalary'],data_new['CompanyName'][i]['StartYear'],data_new['CompanyName'][i]['EndYear'], \
                data_new['CompanyName'][i]['Responsibility'],data_new['CompanyName'][i]['ReasonOfLeaving'],data_new['CompanyName'][i]['Descriptionofwork'],data_new['createby']))
        except Exception as e:
            pass
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee_TrainingCourse', methods=['POST'])
@connect_sql()
def EditEmployee_TrainingCourse(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT citizenid FROM employee WHERE employeeid=%s"
        cursor.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        try:

            sql2 = "SELECT * FROM TrainingCourse WHERE ID_CardNo=%s"
            cursor.execute(sql2,result[0]['citizenid'])
            columns = [column[0] for column in cursor.description]
            result2 = toJson(cursor.fetchall(),columns)

            type_action = "Edit"

            i=0
            for i in xrange(len(result2)):
                sqlIn23_log = "INSERT INTO TrainingCourse_log(ID_CardNo,Subject,Place,StartDate,EndDate,type_action,createby) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn23_log,(result2[i]['ID_CardNo'],result2[i]['Subject'],result2[i]['Place'],result2[i]['StartDate'],result2[i]['EndDate'],type_action,data_new['createby']))

            sqlI23de = "DELETE FROM TrainingCourse WHERE ID_CardNo=%s"
            cursor.execute(sqlI23de,result[0]['citizenid'])

            i=0
            for i in xrange(len(data_new['Subject'])):
                sqlIn23 = "INSERT INTO TrainingCourse(ID_CardNo,Subject,Place,StartDate,EndDate,createby) VALUES (%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn23,(data_new['Subject'][i]['ID_CardNo'],data_new['Subject'][i]['Subject'],data_new['Subject'][i]['Place'],data_new['Subject'][i]['StartDate'],data_new['Subject'][i]['EndDate'],data_new['createby']))
        except Exception as e:
            pass
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/EditEmployee_Employeeid', methods=['POST'])
@connect_sql()
def EditEmployee_Employeeid(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT citizenid FROM employee WHERE employeeid=%s"
        cursor.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        try:
            sql2 = "SELECT employeeid FROM employee WHERE employeeid=%s AND company_id=%s"
            cursor.execute(sql2,(data_new['employeeid'],data_new['company_id']))
            columns = [column[0] for column in cursor.description]
            result2 = toJson(cursor.fetchall(),columns)
            employeeid__ = result2[0]['employeeid']
            return "Duplicate_employeeid"
        except Exception as e:

            insert_emp_log = "INSERT INTO employee_id_log (old_employeeid,new_employeeid,create_by) VALUES (%s,%s,%s)"
            cursor.execute(insert_emp_log,(data_new['Old_EmpId'],data_new['employeeid'],data_new['createby']))

            sqlUp = "UPDATE employee SET employeeid=%s WHERE employeeid=%s"
            cursor.execute(sqlUp,(data_new['employeeid'],data_new['Old_EmpId']))

            sqlUp_gA = "UPDATE employee_benefits SET employeeid=%s WHERE employeeid=%s"
            cursor.execute(sqlUp_gA,(data_new['employeeid'],data_new['Old_EmpId']))

            sqlUp_pro = "UPDATE Emp_probation SET employeeid=%s WHERE employeeid=%s"
            cursor.execute(sqlUp_pro,(data_new['employeeid'],data_new['Old_EmpId']))

            try:
                sqlUp_prove = "UPDATE approve_probation SET employeeid=%s WHERE employeeid=%s"
                cursor.execute(sqlUp_prove,(data_new['employeeid'],data_new['Old_EmpId']))
            except Exception as e:
                pass

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/check_Employeeid', methods=['POST'])
@connect_sql()
def check_Employeeid(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql = "SELECT citizenid FROM employee WHERE employeeid=%s"
        cursor.execute(sql,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        try:
            sql2 = "SELECT employeeid FROM employee WHERE employeeid=%s AND company_id=%s"
            cursor.execute(sql2,(data_new['employeeid'],data_new['company_id']))
            columns = [column[0] for column in cursor.description]
            result2 = toJson(cursor.fetchall(),columns)
            employeeid__ = result2[0]['employeeid']
            return "Duplicate_employeeid"
        except Exception as e:
            pass
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/InsertEmployeeHRCI_Management', methods=['POST'])
@connect_sql()
def InsertEmployeeHRCI_Management(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sqlblack = "SELECT ID_CardNo FROM blacklist WHERE validstatus=1"
        cursor.execute(sqlblack)
        columnsblack = [column[0] for column in cursor.description]
        resultblacklist = toJson(cursor.fetchall(),columnsblack)
        if data_new['ID_CardNo']==resultblacklist[0]['ID_CardNo']:
            print("Person is blacklist")
        else:
            # i=0
            # for i in xrange(len(data_new['AddressType'])):
            #     sqlIn = "INSERT INTO Address (ID_CardNo,AddressType,HouseNo,Street,DISTRICT_ID,AMPHUR_ID,PROVINCE_ID,PostCode,Tel,Fax) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            #     cursor.execute(sqlIn,(data_new[i]['ID_CardNo'],data_new[i]['AddressType'],data_new[i]['HouseNo'],
            #     data_new[i]['Street'],data_new[i]['DISTRICT_NAME'],data_new[i]['AMPHUR_NAME'],data_new[i]['PROVINCE_NAME'],data_new[i]['PostCode'],data_new[i]['Tel'],data_new[i]['Fax']))

            type_action = "ADD"

            if data_new['AddressTypeHome']=='Home':
                sqlIn = "INSERT INTO Address (ID_CardNo,AddressType,HouseNo,Street,DISTRICT_ID,AMPHUR_ID,PROVINCE_ID,PostCode,Tel,Fax,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn,(data_new['ID_CardNo'],data_new['AddressTypeHome'],data_new['AddressHome'],
                data_new['StreetHome'],data_new['SubdistrictHome'],data_new['DistrictHome'],data_new['ProvinceHome'],data_new['PostalcodeHome'],data_new['PhoneHome'],data_new['FaxHome'],data_new['createby']))

                sqlIn_log = "INSERT INTO Address_log (ID_CardNo,AddressType,HouseNo,Street,DISTRICT_ID,AMPHUR_ID,PROVINCE_ID,PostCode,Tel,Fax,type_action,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn_log,(data_new['ID_CardNo'],data_new['AddressTypeHome'],data_new['AddressHome'],
                data_new['StreetHome'],data_new['SubdistrictHome'],data_new['DistrictHome'],data_new['ProvinceHome'],data_new['PostalcodeHome'],data_new['PhoneHome'],data_new['FaxHome'],type_action,data_new['createby']))

            if data_new['AddressTypePresent']=='Present':
                sqlIn = "INSERT INTO Address (ID_CardNo,AddressType,HouseNo,Street,DISTRICT_ID,AMPHUR_ID,PROVINCE_ID,PostCode,Tel,Fax,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn,(data_new['ID_CardNo'],data_new['AddressTypePresent'],data_new['AddressPresent'],
                data_new['StreetPresent'],data_new['SubDistrictPresent'],data_new['DistrictPresent'],data_new['ProvincePresent'],data_new['PostalCodePresent'],data_new['PhonePresent'],data_new['FaxPresent'],data_new['createby']))

                sqlIn_log = "INSERT INTO Address_log (ID_CardNo,AddressType,HouseNo,Street,DISTRICT_ID,AMPHUR_ID,PROVINCE_ID,PostCode,Tel,Fax,type_action,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn_log,(data_new['ID_CardNo'],data_new['AddressTypePresent'],data_new['AddressPresent'],
                data_new['StreetPresent'],data_new['SubDistrictPresent'],data_new['DistrictPresent'],data_new['ProvincePresent'],data_new['PostalCodePresent'],data_new['PhonePresent'],data_new['FaxPresent'],type_action,data_new['createby']))

            i=0
            for i in xrange(len(data_new['ComSkill'])):
                sqlIn6 = "INSERT INTO ComputerSkill (ID_CardNo,ComSkill,Level,createby) VALUES (%s,%s,%s,%s)"
                cursor.execute(sqlIn6,(data_new['ComSkill'][i]['ID_CardNo'],data_new['ComSkill'][i]['SkillCom'],data_new['ComSkill'][i]['LevelCom'],data_new['createby']))

            i=0
            for i in xrange(len(data_new['ComSkill'])):
                sqlIn6_log = "INSERT INTO ComputerSkill_log (ID_CardNo,ComSkill,Level,type_action,createby) VALUES (%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn6_log,(data_new['ComSkill'][i]['ID_CardNo'],data_new['ComSkill'][i]['SkillCom'],data_new['ComSkill'][i]['LevelCom'],type_action,data_new['createby']))

            # for dataSkillcomputer in data_new['ComSkill']:
            #     sqlIn6 = "INSERT INTO ComputerSkill (ID_CardNo,ComSkill,Level) VALUES (%s,%s,%s)"
            #     cursor.execute(sqlIn6,(dataSkillcomputer['ID_CardNo'],dataSkillcomputer['SkillCom'],dataSkillcomputer['LevelCom']))
            i=0
            for i in xrange(len(data_new['EducationLevel'])):
                sqlIn9 = "INSERT INTO Education (ID_CardNo,EducationLevel,Institute,StartYear,EndYear,Qualification,Major,GradeAvg,ExtraCurricularActivities,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn9,(data_new['EducationLevel'][i]['ID_CardNo'],data_new['EducationLevel'][i]['edulevel'],data_new['EducationLevel'][i]['eduName'],data_new['EducationLevel'][i]['eduStartyear'],data_new['EducationLevel'][i]['eduEndyear'], \
                data_new['EducationLevel'][i]['eduQua'],data_new['EducationLevel'][i]['edumajor'],data_new['EducationLevel'][i]['edugpa'],\
                data_new['EducationLevel'][i]['eduActivities'],data_new['createby']))

            i=0
            for i in xrange(len(data_new['EducationLevel'])):
                sqlIn9_log = "INSERT INTO Education_log (ID_CardNo,EducationLevel,Institute,StartYear,EndYear,Qualification,Major,GradeAvg,ExtraCurricularActivities,type_action,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn9_log,(data_new['EducationLevel'][i]['ID_CardNo'],data_new['EducationLevel'][i]['edulevel'],data_new['EducationLevel'][i]['eduName'],data_new['EducationLevel'][i]['eduStartyear'],data_new['EducationLevel'][i]['eduEndyear'], \
                data_new['EducationLevel'][i]['eduQua'],data_new['EducationLevel'][i]['edumajor'],data_new['EducationLevel'][i]['edugpa'],\
                data_new['EducationLevel'][i]['eduActivities'],type_action,data_new['createby']))

            if data_new['MemberTypeDad']=='Father':
                sqlIn = "INSERT INTO Family (ID_CardNo,MemberType,Name,Surname,Occupation,Address,Tel,Fax,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn,(data_new['ID_CardNoDad'],data_new['MemberTypeDad'],data_new['FatherName'],
                data_new['FatherSurName'],data_new['FatherJob'],data_new['FatherTel'],data_new['FatherFax'],data_new['FatherAddress'],data_new['createby']))

                sqlIn_log = "INSERT INTO Family_log (ID_CardNo,MemberType,Name,Surname,Occupation,Address,Tel,Fax,type_action,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn_log,(data_new['ID_CardNoDad'],data_new['MemberTypeDad'],data_new['FatherName'],
                data_new['FatherSurName'],data_new['FatherJob'],data_new['FatherTel'],data_new['FatherFax'],data_new['FatherAddress'],type_action,data_new['createby']))

            if data_new['MemberTypeMom']=='Mother':
                sqlIn = "INSERT INTO Family (ID_CardNo,MemberType,Name,Surname,Occupation,Address,Tel,Fax,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn,(data_new['ID_CardNoMom'],data_new['MemberTypeMom'],data_new['MotherName'],
                data_new['MotherSurname'],data_new['MotherJob'],data_new['Mothertel'],data_new['MotherFax'],data_new['MotherAddress'],data_new['createby']))

                sqlIn_log = "INSERT INTO Family_log (ID_CardNo,MemberType,Name,Surname,Occupation,Address,Tel,Fax,type_action,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn_log,(data_new['ID_CardNoMom'],data_new['MemberTypeMom'],data_new['MotherName'],
                data_new['MotherSurname'],data_new['MotherJob'],data_new['Mothertel'],data_new['MotherFax'],data_new['MotherAddress'],type_action,data_new['createby']))

            i=0
            for i in xrange(len(data_new['BrotherAndSister'])):
                sqlIn11 = "INSERT INTO Family (ID_CardNo,MemberType,Name,Surname,Occupation,Address,Tel,Fax,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn11,(data_new['BrotherAndSister'][i]['ID_CardNo'],data_new['BrotherAndSister'][i]['MemberType'],data_new['BrotherAndSister'][i]['BroAndSisName'],data_new['BrotherAndSister'][i]['BroAndSisSurName'],data_new['BrotherAndSister'][i]['BroAndSisJob'],\
                data_new['BrotherAndSister'][i]['BroAndSisTel'],data_new['BrotherAndSister'][i]['BroAndSisFax'],data_new['BrotherAndSister'][i]['BroAndSisAddress'],data_new['createby']))

            i=0
            for i in xrange(len(data_new['BrotherAndSister'])):
                sqlIn11_log = "INSERT INTO Family_log (ID_CardNo,MemberType,Name,Surname,Occupation,Address,Tel,Fax,type_action,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn11_log,(data_new['BrotherAndSister'][i]['ID_CardNo'],data_new['BrotherAndSister'][i]['MemberType'],data_new['BrotherAndSister'][i]['BroAndSisName'],data_new['BrotherAndSister'][i]['BroAndSisSurName'],data_new['BrotherAndSister'][i]['BroAndSisJob'],\
                data_new['BrotherAndSister'][i]['BroAndSisTel'],data_new['BrotherAndSister'][i]['BroAndSisFax'],data_new['BrotherAndSister'][i]['BroAndSisAddress'],type_action,data_new['createby']))
            # i=0
            # for i in xrange(len(data_new['MemberType'])):
            #     sqlIn11 = "INSERT INTO Family (ID_CardNo,MemberType,Name,Surname,Occupation,Address,Tel,Fax) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            #     cursor.execute(sqlIn11,(data_new['MemberType'][i]['ID_CardNo'],data_ne['MemberType'][i]['MemberType'],data_new['MemberType'][i]['Name'],data_new['MemberType'][i]['Surname'],data_new['MemberType'][i]['Occupation'], \
            #     data_new['MemberType'][i]['Address'],data_new['MemberType'][i]['Tel'],data_new['MemberType'][i]['Fax']))

            i=0
            for i in xrange(len(data_new['Languages'])):
                sqlIn13 = "INSERT INTO LanguagesSkill (ID_CardNo,Languages,Speaking,Reading,Writting,createby) VALUES (%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn13,(data_new['Languages'][i]['ID_CardNo'],data_new['Languages'][i]['languageskill'],data_new['Languages'][i]['languagespeak'],data_new['Languages'][i]['languageread'],data_new['Languages'][i]['languagewrite'],data_new['createby']))

            i=0
            for i in xrange(len(data_new['Languages'])):
                sqlIn13_log = "INSERT INTO LanguagesSkill_log (ID_CardNo,Languages,Speaking,Reading,Writting,type_action,createby) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn13_log,(data_new['Languages'][i]['ID_CardNo'],data_new['Languages'][i]['languageskill'],data_new['Languages'][i]['languagespeak'],data_new['Languages'][i]['languageread'],data_new['Languages'][i]['languagewrite'],type_action,data_new['createby']))

            date_name = str(data_new['Birthdate'])
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

            sqlIn14 = """INSERT INTO Personal (NameTh,SurnameTh,NicknameTh,NameEn,SurnameEn,NicknameEn,Birthdate,Birthdate_name,BirthPlace,BirthProvince,BirthCountry,Age,Height,Weight,BloodGroup,Citizenship,Religion,ID_CardNo,IssueDate,ExpiryDate,MaritalStatus,NumberOfChildren,StudyChild,MilitaryService,Others,Worktel,Mobile,Email,EmergencyPerson,EmergencyRelation,EmergencyAddress,EmergencyTel,createby) \
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(sqlIn14,(data_new['NameTh'],data_new['SurnameTh'],data_new['NicknameTh'],data_new['NameEn'],\
            data_new['SurnameEn'],data_new['NicknameEn'],data_new['Birthdate'],Birthdate_name,data_new['BirthPlace'],data_new['BirthProvince'], \
            data_new['BirthCountry'],data_new['Age'],data_new['Height'],data_new['Weight'],data_new['BloodGroup'],data_new['Citizenship'],data_new['Religion'],data_new['ID_CardNo'], \
            data_new['IssueDate'],data_new['ExpiryDate'],data_new['MaritalStatus'],data_new['NumberOfChildren'],data_new['StudyChild'],data_new['MilitaryService'],data_new['other'], \
            data_new['phone_company'],data_new['Mobile'],data_new['email'],data_new['EmergencyPerson'],data_new['EmergencyRelation'],data_new['EmergencyAddress'],data_new['EmergencyTel'],data_new['createby']))

            sqlIn14_log = """INSERT INTO Personal_log (NameTh,SurnameTh,NicknameTh,NameEn,SurnameEn,NicknameEn,Birthdate,Birthdate_name,BirthPlace,BirthProvince,BirthCountry,Age,Height,Weight,BloodGroup,Citizenship,Religion,ID_CardNo,IssueDate,ExpiryDate,MaritalStatus,NumberOfChildren,StudyChild,MilitaryService,Others,Worktel,Mobile,Email,EmergencyPerson,EmergencyRelation,EmergencyAddress,EmergencyTel,type_action,createby) \
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(sqlIn14_log,(data_new['NameTh'],data_new['SurnameTh'],data_new['NicknameTh'],data_new['NameEn'],\
            data_new['SurnameEn'],data_new['NicknameEn'],data_new['Birthdate'],Birthdate_name,data_new['BirthPlace'],data_new['BirthProvince'], \
            data_new['BirthCountry'],data_new['Age'],data_new['Height'],data_new['Weight'],data_new['BloodGroup'],data_new['Citizenship'],data_new['Religion'],data_new['ID_CardNo'], \
            data_new['IssueDate'],data_new['ExpiryDate'],data_new['MaritalStatus'],data_new['NumberOfChildren'],data_new['StudyChild'],data_new['MilitaryService'],data_new['other'], \
            data_new['phone_company'],data_new['Mobile'],data_new['email'],data_new['EmergencyPerson'],data_new['EmergencyRelation'],data_new['EmergencyAddress'],data_new['EmergencyTel'],type_action,data_new['createby']))
            # i=0
            # for i in xrange(len(data_new['RelativeName'])):
            #     sqlIn17 = "INSERT INTO Reference (ID_CardNo,RelativeName,RelativeSurname,RelativePosition,RelativeRelationship,PhysicalHandicap,PhysicalHandicapDetail,KnowFrom) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            #     cursor.execute(sqlIn17,(data_new['RelativeName'][i]['ID_CardNo'],data_new['RelativeName'][i]['RelativeName'],data_new['RelativeName'][i]['RelativeSurname'],data_new['RelativeName'][i]['RelativePosition'],data_new['RelativeName'][i]['RelativeRelationship'],data_new['RelativeName'][i]['PhysicalHandicap'],\
            #     data_new['RelativeName'][i]['PhysicalHandicapDetail'],data_new['RelativeName'][i]['KnowFrom']))
            # i=0
            # for i in xrange(len(data_new['RefName'])):
            #     sqlIn18 = "INSERT INTO RefPerson (ID_CardNo,RefName,RefPosition,RefAddress,RefTel) VALUES (%s,%s,%s,%s,%s)"
            #     cursor.execute(sqlIn18,(data_new['RefName'][i]['ID_CardNo'],data_new['RefName'][i]['RefName'],data_new['RefName'][i]['RefPosition'],data_new['RefName'][i]['RefAddress'],data_new['RefName'][i]['RefTel']))
            # WorkUpCountry ='ไม่ขัดข้อง'
            # StartWorkEarliest = 'test'
            sqlIn20 = "INSERT INTO SpecialSkill (ID_CardNo,CarDrivingLicense,MotorBicycleDrivingLicense,OwnCar,OwnMotorBicycle,WorkUpCountry,StartWorkEarliest,PhysicalDisabilityOrDisease,DischargeFromEmployment,DischargeFromEmploymentReason,Arrested,ArrestedReason,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn20,(data_new['ID_CardNo'],data_new['CarDrivingLicense'],data_new['MotorBicycleDrivingLicense'],data_new['OwnCar'],data_new['OwnMotorBicycle'], \
            data_new['WorkUpCountry'],data_new['StartWorkEarliest'],data_new['PhysicalDisabilityOrDisease'],data_new['DischargeFromEmployment'],data_new['DischargeFromEmploymentReason'],data_new['Arrested'],data_new['ArrestedReason'],data_new['createby']))

            sqlIn20_log = "INSERT INTO SpecialSkill_log (ID_CardNo,CarDrivingLicense,MotorBicycleDrivingLicense,OwnCar,OwnMotorBicycle,WorkUpCountry,StartWorkEarliest,PhysicalDisabilityOrDisease,DischargeFromEmployment,DischargeFromEmploymentReason,Arrested,ArrestedReason,type_action,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn20_log,(data_new['ID_CardNo'],data_new['CarDrivingLicense'],data_new['MotorBicycleDrivingLicense'],data_new['OwnCar'],data_new['OwnMotorBicycle'],\
            data_new['WorkUpCountry'],data_new['StartWorkEarliest'],data_new['PhysicalDisabilityOrDisease'],data_new['DischargeFromEmployment'],data_new['DischargeFromEmploymentReason'],data_new['Arrested'],data_new['ArrestedReason'],type_action,data_new['createby']))
            try:
                i=0
                for i in xrange(len(data_new['CompanyName'])):
                    sqlIn10 = "INSERT INTO Employment (ID_CardNo,CompanyName,CompanyAddress,PositionHeld,StartSalary,EndSalary,StartYear,EndYear,Responsibility,ReasonOfLeaving,Descriptionofwork,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sqlIn10,(data_new['CompanyName'][i]['ID_CardNo'],data_new['CompanyName'][i]['CompanyName'],data_new['CompanyName'][i]['CompanyAddress'],data_new['CompanyName'][i]['PositionHeld'],data_new['CompanyName'][i]['StartSalary'],data_new['CompanyName'][i]['EndSalary'], \
                    data_new['CompanyName'][i]['StartYear'],data_new['CompanyName'][i]['EndYear'], \
                    data_new['CompanyName'][i]['Responsibility'],data_new['CompanyName'][i]['ReasonOfLeaving'],data_new['CompanyName'][i]['Descriptionofwork'],data_new['createby']))

                i=0
                for i in xrange(len(data_new['CompanyName'])):
                    sqlIn10_log = "INSERT INTO Employment_log (ID_CardNo,CompanyName,CompanyAddress,PositionHeld,StartSalary,EndSalary,StartYear,EndYear,Responsibility,ReasonOfLeaving,Descriptionofwork,type_action,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sqlIn10_log,(data_new['CompanyName'][i]['ID_CardNo'],data_new['CompanyName'][i]['CompanyName'],data_new['CompanyName'][i]['CompanyAddress'],data_new['CompanyName'][i]['PositionHeld'],data_new['CompanyName'][i]['StartSalary'],data_new['CompanyName'][i]['EndSalary'], \
                    data_new['CompanyName'][i]['StartYear'],data_new['CompanyName'][i]['EndYear'], \
                    data_new['CompanyName'][i]['Responsibility'],data_new['CompanyName'][i]['ReasonOfLeaving'],data_new['CompanyName'][i]['Descriptionofwork'],type_action,data_new['createby']))
            except Exception as e:
                logserver(e)
            try:
                i=0
                for i in xrange(len(data_new['Subject'])):
                    sqlIn23 = "INSERT INTO TrainingCourse(ID_CardNo,Subject,Place,StartDate,EndDate,createby) VALUES (%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sqlIn23,(data_new['Subject'][i]['ID_CardNo'],data_new['Subject'][i]['Subject'],data_new['Subject'][i]['Place'],data_new['Subject'][i]['StartDate'],data_new['Subject'][i]['EndDate'],data_new['createby']))

                i=0
                for i in xrange(len(data_new['Subject'])):
                    sqlIn23_log = "INSERT INTO TrainingCourse_log(ID_CardNo,Subject,Place,StartDate,EndDate,type_action,createby) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sqlIn23_log,(data_new['Subject'][i]['ID_CardNo'],data_new['Subject'][i]['Subject'],data_new['Subject'][i]['Place'],data_new['Subject'][i]['StartDate'],data_new['Subject'][i]['EndDate'],type_action,data_new['createby']))
            except Exception as e:
                logserver(e)

            date1 = data_new['Start_contract']
            long_date = int(data_new['long_date'])-1
            star_date = date1.split("-")
            Day_s = int(star_date[0])
            Mon_s =int(star_date[1])
            year_s = int(star_date[2])
            next_3_m = date(year_s,Mon_s,Day_s) + relativedelta(days=long_date)
            next_3_m2 = str(next_3_m)
            end_date = next_3_m2.split("-")
            Day_e = end_date[2]
            Mon_e =end_date[1]
            year_e = end_date[0]
            End_probation_date = Day_e+"-"+Mon_e+"-"+year_e

            # salary ='15000'
            encodedsalary = base64.b64encode(data_new['Salary'])
            sqlEM = "INSERT INTO employee (employeeid,citizenid,name_th,name_eng,surname_th,surname_eng,nickname_employee,salary,email,phone_company,position_id,section_id,org_name_id,cost_center_name_id,company_id,start_work,EndWork_probation,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlEM,(employeeid,ID_CardNo,result_Personal[0]['NameTh'],result_Personal[0]['NameEn'],result_Personal[0]['SurnameTh'],result_Personal[0]['SurnameEn'],result_Personal[0]['NicknameEn'],encodedsalary,data_new['email'],data_new['phone_company'],data_new['position_id'],\
            data_new['section_id'],data_new['org_name_id'],data_new['cost_center_name_id'],data_new['company_id'],data_new['Start_contract'],End_probation_date,data_new['createby']))

            sqlEM_log = "INSERT INTO employee_log (employeeid,citizenid,name_th,name_eng,surname_th,surname_eng,nickname_employee,salary,email,phone_company,position_id,section_id,org_name_id,cost_center_name_id,company_id,start_work,EndWork_probation,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlEM_log,(employeeid,ID_CardNo,result_Personal[0]['NameTh'],result_Personal[0]['NameEn'],result_Personal[0]['SurnameTh'],result_Personal[0]['SurnameEn'],result_Personal[0]['NicknameEn'],encodedsalary,data_new['email'],data_new['phone_company'],data_new['position_id'],\
            data_new['section_id'],data_new['org_name_id'],data_new['cost_center_name_id'],data_new['company_id'],data_new['Start_contract'],End_probation_date,data_new['createby'],type_action))

            i=0
            for i in xrange(len(data_new['benefits'])):
                sqlIn_be = "INSERT INTO employee_benefits(employeeid,citizenid,benefits_id,benefits_values,type_check,createby) VALUES (%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn_be,(employeeid,ID_CardNo,data_new['benefits'][i]['benefits_id'],data_new['benefits'][i]['benefits_values'],data_new['benefits'][i]['type_check'],data_new['createby']))

            i=0
            for i in xrange(len(data_new['benefits'])):
                sqlIn_be_log = "INSERT INTO employee_benefits_log(employeeid,citizenid,benefits_id,benefits_values,type_check,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn_be_log,(employeeid,ID_CardNo,data_new['benefits'][i]['benefits_id'],data_new['benefits'][i]['benefits_values'],data_new['benefits'][i]['type_check'],data_new['createby'],type_action))

            sqlEM_pro = "INSERT INTO Emp_probation (employeeid,citizenid,name_th,name_eng,surname_th,surname_eng,nickname_employee,salary,email,phone_company,position_id,section_id,org_name_id,cost_center_name_id,company_id,start_work,EndWork_probation,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlEM_pro,(employeeid,ID_CardNo,result_Personal[0]['NameTh'],result_Personal[0]['NameEn'],result_Personal[0]['SurnameTh'],result_Personal[0]['SurnameEn'],result_Personal[0]['NicknameEn'],encodedsalary,data_new['email'],data_new['phone_company'],data_new['position_id'],\
            data_new['section_id'],data_new['org_name_id'],data_new['cost_center_name_id'],data_new['company_id'],data_new['Start_contract'],End_probation_date,data_new['createby']))

            sqlEM_pro_log = "INSERT INTO Emp_probation_log (employeeid,citizenid,name_th,name_eng,surname_th,surname_eng,nickname_employee,salary,email,phone_company,position_id,section_id,org_name_id,cost_center_name_id,company_id,start_work,EndWork_probation,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlEM_pro_log,(employeeid,ID_CardNo,result_Personal[0]['NameTh'],result_Personal[0]['NameEn'],result_Personal[0]['SurnameTh'],result_Personal[0]['SurnameEn'],result_Personal[0]['NicknameEn'],encodedsalary,data_new['email'],data_new['phone_company'],data_new['position_id'],\
            data_new['section_id'],data_new['org_name_id'],data_new['cost_center_name_id'],data_new['company_id'],data_new['Start_contract'],End_probation_date,data_new['createby'],type_action))
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Export_Employee_by_month', methods=['POST'])
@connect_sql()
def Export_Employee_by_month(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        year=str(data_new['year'])
        month=str(data_new['month'])
        companyid=str(data_new['companyid'])
        try:
            sql = """SELECT employee.employeeid,employee.name_th,employee.surname_th,employee.name_eng,employee.surname_eng,employee.nickname_employee,Personal.NicknameTh,employee.email,employee.start_work,Personal.Mobile,position.position_detail,section.sect_detail,org_name.org_name_detail,cost_center_name.cost_detail,company.companyname FROM employee LEFT JOIN company ON company.companyid = employee.company_id\
                                          LEFT JOIN position ON position.position_id = employee.position_id\
                                          LEFT JOIN section ON section.sect_id = employee.section_id\
                                          LEFT JOIN org_name ON org_name.org_name_id = employee.org_name_id\
                                          LEFT JOIN cost_center_name ON cost_center_name.cost_center_name_id = employee.cost_center_name_id\
                                          LEFT JOIN Personal ON Personal.ID_CardNo = employee.citizenid\
            WHERE employee.start_work LIKE '%""" + month + """-""" + year + """' AND employee.company_id='"""+companyid +"""'"""
            cursor.execute(sql)
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            companyname_ = result[0]['companyname']
        except Exception as e:
            logserver(e)
            return "No_Data"
        isSuccess = True
        reasonCode = 200
        reasonText = ""
        now = datetime.now()
        datetimeStr = now.strftime('%Y%m%d_%H%M%S%f')
        filename_tmp = secure_filename('{}_{}'.format(datetimeStr, 'Template_Employee_by.xlsx'))

        wb = load_workbook('../app/Template/Template_Employee_by.xlsx')
        if len(result) > 0:

            sheet = wb['Sheet1']
            sheet['B'+str(3)] = year + '/' + month
            sheet['C'+str(3)] = companyname_
            offset = 6
            i = 0
            for i in xrange(len(result)):
                sheet['A'+str(offset + i)] = result[i]['employeeid']
                sheet['B'+str(offset + i)] = result[i]['name_th'] + ' ' + result[i]['surname_th']
                sheet['C'+str(offset + i)] =  result[i]['name_eng'] + ' ' + result[i]['surname_eng']
                sheet['D'+str(offset + i)] = result[i]['nickname_employee'] + ' ' + result[i]['NicknameTh']
                sheet['E'+str(offset + i)] = result[i]['email']
                sheet['F'+str(offset + i)] = result[i]['position_detail']
                sheet['G'+str(offset + i)] = result[i]['sect_detail']
                sheet['H'+str(offset + i)] = result[i]['org_name_detail']
                sheet['I'+str(offset + i)] = result[i]['cost_detail']
                sheet['J'+str(offset + i)] = result[i]['Mobile']
                sheet['K'+str(offset + i)] = result[i]['start_work']
                i = i + 1
        wb.save(filename_tmp)
        with open(filename_tmp, "rb") as f:
            encoded_string = base64.b64encode(f.read())
        os.remove(filename_tmp)
        displayColumns = ['isSuccess','reasonCode','reasonText','excel_base64']
        displayData = [(isSuccess,reasonCode,reasonText,encoded_string)]
        return jsonify(toDict(displayData,displayColumns))
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qry_Employee_by_month', methods=['POST'])
@connect_sql()
def Qry_Employee_by_month(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        year=str(data_new['year'])
        month=str(data_new['month'])
        companyid=str(data_new['companyid'])
        sql = """SELECT employee.employeeid,employee.name_th,employee.surname_th,employee.name_eng,employee.surname_eng,employee.nickname_employee,employee.email,\
        employee.start_work,Personal.Mobile,position.position_detail,section.sect_detail,org_name.org_name_detail,cost_center_name.cost_detail,company.company_short_name FROM employee LEFT JOIN company ON company.companyid = employee.company_id\
                                      LEFT JOIN position ON position.position_id = employee.position_id\
                                      LEFT JOIN section ON section.sect_id = employee.section_id\
                                      LEFT JOIN org_name ON org_name.org_name_id = employee.org_name_id\
                                      LEFT JOIN cost_center_name ON cost_center_name.cost_center_name_id = employee.cost_center_name_id\
                                      LEFT JOIN Personal ON Personal.ID_CardNo = employee.citizenid\
        WHERE employee.start_work LIKE '%""" + month + """-""" + year + """' AND employee.company_id='"""+companyid +"""'"""
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Export_Employee_All_company', methods=['POST'])
@connect_sql()
def Export_Employee_All_company(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        year=str(data_new['year'])
        month=str(data_new['month'])
        try:
            sql = """SELECT employee.employeeid,employee.name_th,employee.surname_th,employee.name_eng,employee.surname_eng,employee.nickname_employee,Personal.NicknameTh,employee.email,employee.start_work,Personal.Mobile,position.position_detail,section.sect_detail,org_name.org_name_detail,cost_center_name.cost_detail,company.company_short_name FROM employee LEFT JOIN company ON company.companyid = employee.company_id\
                                          LEFT JOIN position ON position.position_id = employee.position_id\
                                          LEFT JOIN section ON section.sect_id = employee.section_id\
                                          LEFT JOIN org_name ON org_name.org_name_id = employee.org_name_id\
                                          LEFT JOIN cost_center_name ON cost_center_name.cost_center_name_id = employee.cost_center_name_id\
                                          LEFT JOIN Personal ON Personal.ID_CardNo = employee.citizenid\
            WHERE employee.start_work LIKE '%""" + month + """-""" + year + """'"""
            cursor.execute(sql)
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            companyname_ = result[0]['company_short_name']
        except Exception as e:
            logserver(e)
            return "No_Data"
        isSuccess = True
        reasonCode = 200
        reasonText = ""
        now = datetime.now()
        datetimeStr = now.strftime('%Y%m%d_%H%M%S%f')
        filename_tmp = secure_filename('{}_{}'.format(datetimeStr, 'Template_Employee_All.xlsx'))

        wb = load_workbook('../app/Template/Template_Employee_All.xlsx')
        if len(result) > 0:

            sheet = wb['Sheet1']
            sheet['C'+str(3)] = year + '/' + month
            offset = 6
            i = 0
            for i in xrange(len(result)):
                sheet['A'+str(offset + i)] = result[i]['company_short_name']
                sheet['B'+str(offset + i)] = result[i]['employeeid']
                sheet['C'+str(offset + i)] = result[i]['name_th'] + ' ' + result[i]['surname_th']
                sheet['D'+str(offset + i)] =  result[i]['name_eng'] + ' ' + result[i]['surname_eng']
                sheet['E'+str(offset + i)] = result[i]['nickname_employee'] + ' ' + result[i]['NicknameTh']
                sheet['F'+str(offset + i)] = result[i]['email']
                sheet['G'+str(offset + i)] = result[i]['position_detail']
                sheet['H'+str(offset + i)] = result[i]['sect_detail']
                sheet['I'+str(offset + i)] = result[i]['org_name_detail']
                sheet['J'+str(offset + i)] = result[i]['cost_detail']
                sheet['K'+str(offset + i)] = result[i]['Mobile']
                sheet['L'+str(offset + i)] = result[i]['start_work']
                i = i + 1
        wb.save(filename_tmp)
        with open(filename_tmp, "rb") as f:
            encoded_string = base64.b64encode(f.read())
        os.remove(filename_tmp)
        displayColumns = ['isSuccess','reasonCode','reasonText','excel_base64']
        displayData = [(isSuccess,reasonCode,reasonText,encoded_string)]
        return jsonify(toDict(displayData,displayColumns))
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Export_Emp_All', methods=['POST'])
@connect_sql()
def Export_Emp_All(cursor):
    try:
        try:
            sql = """SELECT employee.employeeid,employee.name_th,employee.surname_th,employee.name_eng,employee.surname_eng,employee.nickname_employee,Personal.NicknameTh,employee.email,employee.start_work,Personal.Mobile,position.position_detail,section.sect_detail,org_name.org_name_detail,cost_center_name.cost_detail,company.company_short_name FROM employee LEFT JOIN company ON company.companyid = employee.company_id\
                                          LEFT JOIN position ON position.position_id = employee.position_id\
                                          LEFT JOIN section ON section.sect_id = employee.section_id\
                                          LEFT JOIN org_name ON org_name.org_name_id = employee.org_name_id\
                                          LEFT JOIN cost_center_name ON cost_center_name.cost_center_name_id = employee.cost_center_name_id\
                                          LEFT JOIN Personal ON Personal.ID_CardNo = employee.citizenid"""
            cursor.execute(sql)
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            companyname_ = result[0]['company_short_name']
        except Exception as e:
            logserver(e)
            return "No_Data"
        isSuccess = True
        reasonCode = 200
        reasonText = ""
        now = datetime.now()
        datetimeStr = now.strftime('%Y%m%d_%H%M%S%f')
        filename_tmp = secure_filename('{}_{}'.format(datetimeStr, 'Template_Employee_All.xlsx'))

        wb = load_workbook('../app/Template/Template_Employee_All.xlsx')
        if len(result) > 0:

            sheet = wb['Sheet1']
            # sheet['C'+str(3)] = year + '/' + month
            offset = 6
            i = 0
            for i in xrange(len(result)):
                sheet['A'+str(offset + i)] = result[i]['company_short_name']
                sheet['B'+str(offset + i)] = result[i]['employeeid']
                sheet['C'+str(offset + i)] = result[i]['name_th'] + ' ' + result[i]['surname_th']
                sheet['D'+str(offset + i)] =  result[i]['name_eng'] + ' ' + result[i]['surname_eng']
                sheet['E'+str(offset + i)] = result[i]['nickname_employee'] + ' ' + result[i]['NicknameTh']
                sheet['F'+str(offset + i)] = result[i]['email']
                sheet['G'+str(offset + i)] = result[i]['position_detail']
                sheet['H'+str(offset + i)] = result[i]['sect_detail']
                sheet['I'+str(offset + i)] = result[i]['org_name_detail']
                sheet['J'+str(offset + i)] = result[i]['cost_detail']
                sheet['K'+str(offset + i)] = result[i]['Mobile']
                sheet['L'+str(offset + i)] = result[i]['start_work']
                i = i + 1
        wb.save(filename_tmp)
        with open(filename_tmp, "rb") as f:
            encoded_string = base64.b64encode(f.read())
        os.remove(filename_tmp)
        displayColumns = ['isSuccess','reasonCode','reasonText','excel_base64']
        displayData = [(isSuccess,reasonCode,reasonText,encoded_string)]
        return jsonify(toDict(displayData,displayColumns))
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Export_Emp_benefit_All_company', methods=['POST'])
@connect_sql()
def Export_Emp_benefit_All_company(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        year=str(data_new['year'])
        month=str(data_new['month'])
        try:
            sql = """SELECT employee.citizenid,employee.employeeid,employee.name_th,employee.surname_th,employee.salary,employee.start_work,position.position_detail,section.sect_detail,org_name.org_name_detail,cost_center_name.cost_detail,company.company_short_name FROM employee LEFT JOIN company ON company.companyid = employee.company_id\
                                          LEFT JOIN position ON position.position_id = employee.position_id\
                                          LEFT JOIN section ON section.sect_id = employee.section_id\
                                          LEFT JOIN org_name ON org_name.org_name_id = employee.org_name_id\
                                          LEFT JOIN cost_center_name ON cost_center_name.cost_center_name_id = employee.cost_center_name_id\
            WHERE employee.start_work LIKE '%""" + month + """-""" + year + """'"""
            cursor.execute(sql)
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            for item_ in result:
                item_['salary'] = base64.b64decode(item_['salary'])
            companyname_ = result[0]['company_short_name']
            for i1 in result:
                benefitsful = []
                workTime = []
                sql1 = """  SELECT employee_benefits.benefits_values AS benefitsName
                            FROM employee_benefits , employee
                            WHERE employee_benefits.citizenid =  %s
                            AND employee_benefits.employeeid = employee.employeeid ORDER BY employee_benefits.benefits_id ASC"""
                cursor.execute(sql1,(i1['citizenid']))
                columns = [column[0] for column in cursor.description]
                data2 = toJson(cursor.fetchall(),columns)
                for i2 in data2 :
                    benefitsful.append(i2)
                i1['benefitsful'] = benefitsful
            # return jsonify(result[1]['benefitsful'][2]['benefitsName'])
        except Exception as e:
            logserver(e)
            return "No_Data"
        isSuccess = True
        reasonCode = 200
        reasonText = ""
        now = datetime.now()
        datetimeStr = now.strftime('%Y%m%d_%H%M%S%f')
        filename_tmp = secure_filename('{}_{}'.format(datetimeStr, 'Template_Employee_benefit_All.xlsx'))

        wb = load_workbook('../app/Template/Template_Employee_benefit_All.xlsx')
        if len(result) > 0:

            sheet = wb['Sheet1']
            sheet['E'+str(3)] = year + '/' + month
            offset = 3
            i = 0
            for i in xrange(len(result)):
                sheet['A'+str(offset + i)] = i+1
                sheet['B'+str(offset + i)] = result[i]['company_short_name']
                sheet['C'+str(offset + i)] = result[i]['name_th'] + ' ' + result[i]['surname_th']
                sheet['D'+str(offset + i)] = result[i]['position_detail']
                sheet['E'+str(offset + i)] = result[i]['sect_detail']
                sheet['F'+str(offset + i)] = result[i]['org_name_detail']
                sheet['G'+str(offset + i)] = result[i]['cost_detail']
                sheet['H'+str(offset + i)] = result[i]['start_work']
                sheet['I'+str(offset + i)] = result[i]['salary']
                sheet['J'+str(offset + i)] = result[i]['benefitsful'][0]['benefitsName']
                sheet['K'+str(offset + i)] = result[i]['benefitsful'][1]['benefitsName']
                sheet['L'+str(offset + i)] = result[i]['benefitsful'][2]['benefitsName']
                sheet['M'+str(offset + i)] = result[i]['benefitsful'][3]['benefitsName']
                sheet['N'+str(offset + i)] = result[i]['benefitsful'][4]['benefitsName']
                sheet['O'+str(offset + i)] = result[i]['benefitsful'][5]['benefitsName']
                sheet['P'+str(offset + i)] = result[i]['benefitsful'][6]['benefitsName']
                i = i + 1
        wb.save(filename_tmp)
        with open(filename_tmp, "rb") as f:
            encoded_string = base64.b64encode(f.read())
        os.remove(filename_tmp)
        displayColumns = ['isSuccess','reasonCode','reasonText','excel_base64']
        displayData = [(isSuccess,reasonCode,reasonText,encoded_string)]
        return jsonify(toDict(displayData,displayColumns))
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Export_Emp_benefit_company', methods=['POST'])
@connect_sql()
def Export_Emp_benefit_company(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        year=str(data_new['year'])
        month=str(data_new['month'])
        companyid=str(data_new['companyid'])
        try:
            sql = """SELECT employee.citizenid,employee.employeeid,employee.name_th,employee.surname_th,employee.salary,employee.start_work,position.position_detail,section.sect_detail,org_name.org_name_detail,cost_center_name.cost_detail,company.company_short_name FROM employee LEFT JOIN company ON company.companyid = employee.company_id\
                                          LEFT JOIN position ON position.position_id = employee.position_id\
                                          LEFT JOIN section ON section.sect_id = employee.section_id\
                                          LEFT JOIN org_name ON org_name.org_name_id = employee.org_name_id\
                                          LEFT JOIN cost_center_name ON cost_center_name.cost_center_name_id = employee.cost_center_name_id\
            WHERE employee.start_work LIKE '%""" + month + """-""" + year + """' AND employee.company_id='"""+companyid +"""'"""
            cursor.execute(sql)
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            for item_ in result:
                item_['salary'] = base64.b64decode(item_['salary'])
            companyname_ = result[0]['company_short_name']
            for i1 in result:
                benefitsful = []
                workTime = []
                sql1 = """  SELECT employee_benefits.benefits_values AS benefitsName
                            FROM employee_benefits , employee
                            WHERE employee_benefits.citizenid = %s
                            AND employee_benefits.employeeid = employee.employeeid ORDER BY employee_benefits.benefits_id ASC"""
                cursor.execute(sql1,(i1['citizenid']))
                columns = [column[0] for column in cursor.description]
                data2 = toJson(cursor.fetchall(),columns)
                for i2 in data2 :
                    benefitsful.append(i2)
                i1['benefitsful'] = benefitsful
            # return jsonify(result[1]['benefitsful'][2]['benefitsName'])
        except Exception as e:
            logserver(e)
            return "No_Data"
        isSuccess = True
        reasonCode = 200
        reasonText = ""
        now = datetime.now()
        datetimeStr = now.strftime('%Y%m%d_%H%M%S%f')
        filename_tmp = secure_filename('{}_{}'.format(datetimeStr, 'Template_Employee_benefit_All.xlsx'))

        wb = load_workbook('../app/Template/Template_Employee_benefit_All.xlsx')
        if len(result) > 0:

            sheet = wb['Sheet1']
            sheet['E'+str(3)] = year + '/' + month
            offset = 3
            i = 0
            for i in xrange(len(result)):
                sheet['A'+str(offset + i)] = i+1
                sheet['B'+str(offset + i)] = result[i]['company_short_name']
                sheet['C'+str(offset + i)] = result[i]['name_th'] + ' ' + result[i]['surname_th']
                sheet['D'+str(offset + i)] = result[i]['position_detail']
                sheet['E'+str(offset + i)] = result[i]['sect_detail']
                sheet['F'+str(offset + i)] = result[i]['org_name_detail']
                sheet['G'+str(offset + i)] = result[i]['cost_detail']
                sheet['H'+str(offset + i)] = result[i]['start_work']
                sheet['I'+str(offset + i)] = result[i]['salary']
                sheet['J'+str(offset + i)] = result[i]['benefitsful'][0]['benefitsName']
                sheet['K'+str(offset + i)] = result[i]['benefitsful'][1]['benefitsName']
                sheet['L'+str(offset + i)] = result[i]['benefitsful'][2]['benefitsName']
                sheet['M'+str(offset + i)] = result[i]['benefitsful'][3]['benefitsName']
                sheet['N'+str(offset + i)] = result[i]['benefitsful'][4]['benefitsName']
                sheet['O'+str(offset + i)] = result[i]['benefitsful'][5]['benefitsName']
                sheet['P'+str(offset + i)] = result[i]['benefitsful'][6]['benefitsName']
                i = i + 1
        wb.save(filename_tmp)
        with open(filename_tmp, "rb") as f:
            encoded_string = base64.b64encode(f.read())
        os.remove(filename_tmp)
        displayColumns = ['isSuccess','reasonCode','reasonText','excel_base64']
        displayData = [(isSuccess,reasonCode,reasonText,encoded_string)]
        return jsonify(toDict(displayData,displayColumns))
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Export_Emp_Ga_All_company', methods=['POST'])
@connect_sql()
def Export_Emp_Ga_All_company(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        year=str(data_new['year'])
        month=str(data_new['month'])
        try:
            sql = """SELECT employee.citizenid,employee.employeeid,employee.name_th,employee.surname_th,employee.name_eng,employee.surname_eng,employee.salary,employee.start_work,position.position_detail,section.sect_detail,org_name.org_name_detail,cost_center_name.cost_detail,company.company_short_name FROM employee LEFT JOIN company ON company.companyid = employee.company_id\
                                          LEFT JOIN position ON position.position_id = employee.position_id\
                                          LEFT JOIN section ON section.sect_id = employee.section_id\
                                          LEFT JOIN org_name ON org_name.org_name_id = employee.org_name_id\
                                          LEFT JOIN cost_center_name ON cost_center_name.cost_center_name_id = employee.cost_center_name_id\
            WHERE employee.start_work LIKE '%""" + month + """-""" + year + """'"""
            cursor.execute(sql)
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            for item_ in result:
                item_['salary'] = base64.b64decode(item_['salary'])
            companyname_ = result[0]['company_short_name']
            for i1 in result:
                benefitsful = []
                workTime = []
                sql1 = """  SELECT (CASE WHEN employee_benefits.benefits_values = 1 THEN "✔"
                                         ELSE employee_benefits.benefits_values END) AS benefitsName
                            FROM employee_benefits , employee
                            WHERE employee_benefits.citizenid =  %s
                            AND employee_benefits.employeeid = employee.employeeid ORDER BY employee_benefits.benefits_id ASC"""
                cursor.execute(sql1,(i1['citizenid']))
                columns = [column[0] for column in cursor.description]
                data2 = toJson(cursor.fetchall(),columns)
                for i2 in data2 :
                    benefitsful.append(i2)
                i1['benefitsful'] = benefitsful
            # return jsonify(result[1]['benefitsful'][16]['benefitsName'])
        except Exception as e:
            logserver(e)
            return "No_Data"
        isSuccess = True
        reasonCode = 200
        reasonText = ""
        now = datetime.now()
        datetimeStr = now.strftime('%Y%m%d_%H%M%S%f')
        filename_tmp = secure_filename('{}_{}'.format(datetimeStr, 'Template_Employee_Ga_All.xlsx'))

        wb = load_workbook('../app/Template/Template_Employee_Ga_All.xlsx')
        if len(result) > 0:

            sheet = wb['Sheet1']
            sheet['E'+str(3)] = year + '/' + month
            offset = 3
            i = 0
            for i in xrange(len(result)):
                sheet['A'+str(offset + i)] = i+1
                sheet['B'+str(offset + i)] = result[i]['employeeid']
                sheet['C'+str(offset + i)] = result[i]['name_th']
                sheet['D'+str(offset + i)] = result[i]['surname_th']
                sheet['E'+str(offset + i)] = result[i]['name_eng']
                sheet['F'+str(offset + i)] = result[i]['surname_eng']
                sheet['G'+str(offset + i)] = result[i]['position_detail']
                sheet['H'+str(offset + i)] = result[i]['sect_detail']
                sheet['I'+str(offset + i)] = result[i]['org_name_detail']
                sheet['J'+str(offset + i)] = result[i]['cost_detail']
                sheet['K'+str(offset + i)] = result[i]['company_short_name']
                sheet['L'+str(offset + i)] = result[i]['start_work']
                sheet['M'+str(offset + i)] = result[i]['benefitsful'][5]['benefitsName']
                sheet['N'+str(offset + i)] = result[i]['benefitsful'][6]['benefitsName']
                sheet['O'+str(offset + i)] = result[i]['benefitsful'][7]['benefitsName']
                sheet['P'+str(offset + i)] = result[i]['benefitsful'][8]['benefitsName']
                sheet['Q'+str(offset + i)] = result[i]['benefitsful'][9]['benefitsName']
                sheet['R'+str(offset + i)] = result[i]['benefitsful'][10]['benefitsName']
                sheet['S'+str(offset + i)] = result[i]['benefitsful'][11]['benefitsName']
                sheet['T'+str(offset + i)] = result[i]['benefitsful'][12]['benefitsName']
                sheet['U'+str(offset + i)] = result[i]['benefitsful'][13]['benefitsName']
                sheet['V'+str(offset + i)] = result[i]['benefitsful'][14]['benefitsName']
                sheet['W'+str(offset + i)] = result[i]['benefitsful'][15]['benefitsName']
                sheet['X'+str(offset + i)] = result[i]['benefitsful'][16]['benefitsName']
                sheet['Y'+str(offset + i)] = result[i]['benefitsful'][17]['benefitsName']
                sheet['Z'+str(offset + i)] = result[i]['benefitsful'][18]['benefitsName']
                i = i + 1
        wb.save(filename_tmp)
        with open(filename_tmp, "rb") as f:
            encoded_string = base64.b64encode(f.read())
        os.remove(filename_tmp)
        displayColumns = ['isSuccess','reasonCode','reasonText','excel_base64']
        displayData = [(isSuccess,reasonCode,reasonText,encoded_string)]
        return jsonify(toDict(displayData,displayColumns))
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Export_Emp_Ga_company', methods=['POST'])
@connect_sql()
def Export_Emp_Ga_company(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        year=str(data_new['year'])
        month=str(data_new['month'])
        companyid=str(data_new['companyid'])
        try:
            sql = """SELECT employee.citizenid,employee.employeeid,employee.name_th,employee.surname_th,employee.name_eng,employee.surname_eng,employee.salary,employee.start_work,position.position_detail,section.sect_detail,org_name.org_name_detail,cost_center_name.cost_detail,company.company_short_name FROM employee LEFT JOIN company ON company.companyid = employee.company_id\
                                          LEFT JOIN position ON position.position_id = employee.position_id\
                                          LEFT JOIN section ON section.sect_id = employee.section_id\
                                          LEFT JOIN org_name ON org_name.org_name_id = employee.org_name_id\
                                          LEFT JOIN cost_center_name ON cost_center_name.cost_center_name_id = employee.cost_center_name_id\
            WHERE employee.start_work LIKE '%""" + month + """-""" + year + """' AND employee.company_id='"""+companyid +"""'"""
            cursor.execute(sql)
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            for item_ in result:
                item_['salary'] = base64.b64decode(item_['salary'])
            companyname_ = result[0]['company_short_name']
            for i1 in result:
                benefitsful = []
                workTime = []
                sql1 = """  SELECT (CASE WHEN employee_benefits.benefits_values = 1 THEN "✔"
                                         ELSE employee_benefits.benefits_values END) AS benefitsName
                            FROM employee_benefits , employee
                            WHERE employee_benefits.citizenid =  %s
                            AND employee_benefits.employeeid = employee.employeeid ORDER BY employee_benefits.benefits_id ASC"""
                cursor.execute(sql1,(i1['citizenid']))
                columns = [column[0] for column in cursor.description]
                data2 = toJson(cursor.fetchall(),columns)
                for i2 in data2 :
                    benefitsful.append(i2)
                i1['benefitsful'] = benefitsful
            # return jsonify(result[1]['benefitsful'][16]['benefitsName'])
        except Exception as e:
            logserver(e)
            return "No_Data"
        isSuccess = True
        reasonCode = 200
        reasonText = ""
        now = datetime.now()
        datetimeStr = now.strftime('%Y%m%d_%H%M%S%f')
        filename_tmp = secure_filename('{}_{}'.format(datetimeStr, 'Template_Employee_Ga_All.xlsx'))

        wb = load_workbook('../app/Template/Template_Employee_Ga_All.xlsx')
        if len(result) > 0:

            sheet = wb['Sheet1']
            sheet['E'+str(3)] = year + '/' + month
            offset = 3
            i = 0
            for i in xrange(len(result)):
                sheet['A'+str(offset + i)] = i+1
                sheet['B'+str(offset + i)] = result[i]['employeeid']
                sheet['C'+str(offset + i)] = result[i]['name_th']
                sheet['D'+str(offset + i)] = result[i]['surname_th']
                sheet['E'+str(offset + i)] = result[i]['name_eng']
                sheet['F'+str(offset + i)] = result[i]['surname_eng']
                sheet['G'+str(offset + i)] = result[i]['position_detail']
                sheet['H'+str(offset + i)] = result[i]['sect_detail']
                sheet['I'+str(offset + i)] = result[i]['org_name_detail']
                sheet['J'+str(offset + i)] = result[i]['cost_detail']
                sheet['K'+str(offset + i)] = result[i]['company_short_name']
                sheet['L'+str(offset + i)] = result[i]['start_work']
                sheet['M'+str(offset + i)] = result[i]['benefitsful'][5]['benefitsName']
                sheet['N'+str(offset + i)] = result[i]['benefitsful'][6]['benefitsName']
                sheet['O'+str(offset + i)] = result[i]['benefitsful'][7]['benefitsName']
                sheet['P'+str(offset + i)] = result[i]['benefitsful'][8]['benefitsName']
                sheet['Q'+str(offset + i)] = result[i]['benefitsful'][9]['benefitsName']
                sheet['R'+str(offset + i)] = result[i]['benefitsful'][10]['benefitsName']
                sheet['S'+str(offset + i)] = result[i]['benefitsful'][11]['benefitsName']
                sheet['T'+str(offset + i)] = result[i]['benefitsful'][12]['benefitsName']
                sheet['U'+str(offset + i)] = result[i]['benefitsful'][13]['benefitsName']
                sheet['V'+str(offset + i)] = result[i]['benefitsful'][14]['benefitsName']
                sheet['W'+str(offset + i)] = result[i]['benefitsful'][15]['benefitsName']
                sheet['X'+str(offset + i)] = result[i]['benefitsful'][16]['benefitsName']
                sheet['Y'+str(offset + i)] = result[i]['benefitsful'][17]['benefitsName']
                sheet['Z'+str(offset + i)] = result[i]['benefitsful'][18]['benefitsName']
                i = i + 1
        wb.save(filename_tmp)
        with open(filename_tmp, "rb") as f:
            encoded_string = base64.b64encode(f.read())
        os.remove(filename_tmp)
        displayColumns = ['isSuccess','reasonCode','reasonText','excel_base64']
        displayData = [(isSuccess,reasonCode,reasonText,encoded_string)]
        return jsonify(toDict(displayData,displayColumns))
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qry_Province', methods=['POST'])
@connect_sql3()
def Qry_Province(cursor3):
    try:
        sql = "SELECT PROVINCE_ID, PROVINCE_NAME FROM provinces ORDER BY PROVINCE_NAME ASC"
        cursor3.execute(sql)
        columns = [column[0] for column in cursor3.description]
        result = toJson(cursor3.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qry_All_Amphurs', methods=['POST'])
@connect_sql3()
def Qry_All_Amphurs(cursor3):
    try:
        sql = "SELECT AMPHUR_ID, AMPHUR_NAME FROM amphures ORDER BY AMPHUR_NAME ASC"
        cursor3.execute(sql)
        columns = [column[0] for column in cursor3.description]
        result = toJson(cursor3.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qry_All_Districts', methods=['POST'])
@connect_sql3()
def Qry_All_Districts(cursor3):
    try:
        sql = "SELECT DISTRICT_NAME FROM districts ORDER BY DISTRICT_NAME ASC"
        cursor3.execute(sql)
        columns = [column[0] for column in cursor3.description]
        result = toJson(cursor3.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qry_Amphurs', methods=['POST'])
@connect_sql3()
def Qry_Amphurs(cursor3):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT AMPHUR_ID, AMPHUR_NAME FROM amphures WHERE PROVINCE_ID=%s ORDER BY AMPHUR_NAME ASC"
        cursor3.execute(sql,data_new['PROVINCE_ID'])
        columns = [column[0] for column in cursor3.description]
        result = toJson(cursor3.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qry_Districts', methods=['POST'])
@connect_sql3()
def Qry_Districts(cursor3):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT DISTRICT_NAME FROM districts WHERE AMPHUR_ID=%s ORDER BY DISTRICT_NAME ASC"
        cursor3.execute(sql,data_new['AMPHUR_ID'])
        columns = [column[0] for column in cursor3.description]
        result = toJson(cursor3.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Insert_Employee_GA', methods=['POST'])
@connect_sql()
def Insert_Employee_GA(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        employeeid = data_new['employeeid']
        sql = "SELECT citizenid FROM employee WHERE employeeid=%s"
        cursor.execute(sql,(employeeid))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "ADD"

        i=0
        for i in xrange(len(data_new['benefits'])):
            sqlIn_be = "INSERT INTO employee_benefits(employeeid,citizenid,benefits_id,benefits_values,type_check,createby) VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_be,(employeeid,result[0]['citizenid'],data_new['benefits'][i]['benefits_id'],data_new['benefits'][i]['benefits_values'],data_new['benefits'][i]['type_check'],data_new['createby']))

        i=0
        for i in xrange(len(data_new['benefits'])):
            sqlIn_be_log = "INSERT INTO employee_benefits_log(employeeid,citizenid,benefits_id,benefits_values,type_check,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlIn_be_log,(employeeid,result[0]['citizenid'],data_new['benefits'][i]['benefits_id'],data_new['benefits'][i]['benefits_values'],data_new['benefits'][i]['type_check'],data_new['createby'],type_action))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Edit_Employee_GA', methods=['POST'])
@connect_sql()
def Edit_Employee_GA(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT citizenid,benefits_id,benefits_values,type_check FROM employee_benefits WHERE employeeid=%s AND benefits_id=%s"
        cursor.execute(sql,(data_new['employeeid'],data_new['benefits_id']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Edit"

        sqlIn = "INSERT INTO employee_benefits_log (employeeid,citizenid,benefits_id,benefits_values,type_check,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn,(data_new['employeeid'],result[0]['citizenid'],result[0]['benefits_id'],result[0]['benefits_values'],result[0]['type_check'],data_new['createby'],type_action))

        sqlde = "DELETE FROM employee_benefits WHERE employeeid=%s AND benefits_id=%s"
        cursor.execute(sqlde,(data_new['employeeid'],data_new['benefits_id']))

        sqlIn = "INSERT INTO employee_benefits(employeeid,citizenid,benefits_id,benefits_values,type_check,createby) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn,(data_new['employeeid'],data_new['citizenid'],data_new['benefits_id'],data_new['benefits_values'],data_new['type_check'],data_new['createby']))
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Delete_Employee_GA', methods=['POST'])
@connect_sql()
def Delete_Employee_GA(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT citizenid,benefits_id,benefits_values,type_check FROM employee_benefits WHERE employeeid=%s AND benefits_id=%s"
        cursor.execute(sql,(data_new['employeeid'],data_new['benefits_id']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "Delete"

        sqlIn = "INSERT INTO employee_benefits_log (employeeid,citizenid,benefits_id,benefits_values,type_check,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn,(data_new['employeeid'],result[0]['citizenid'],result[0]['benefits_id'],result[0]['benefits_values'],result[0]['type_check'],data_new['createby'],type_action))

        sqlde = "UPDATE employee_benefits SET validstatus=0 WHERE employeeid=%s AND benefits_id=%s"
        cursor.execute(sqlde,(data_new['employeeid'],data_new['benefits_id']))
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
@app.route('/Qry_Employee_GA', methods=['POST'])
@connect_sql()
def Qry_Employee_GA(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        sql_check_em = "SELECT citizenid FROM employee WHERE employeeid=%s"
        cursor.execute(sql_check_em,data_new['employeeid'])
        columns = [column[0] for column in cursor.description]
        result_em = toJson(cursor.fetchall(),columns)

        sql = "SELECT benefits.benefits_detail,benefits.type_benefits,employee_benefits.benefits_id,employee_benefits.benefits_values,employee_benefits.type_check FROM employee_benefits LEFT JOIN benefits ON employee_benefits.benefits_id = benefits.benefits_id \
         WHERE employee_benefits.citizenid=%s"
        cursor.execute(sql,result_em[0]['citizenid'])
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        return jsonify(result)
    except Exception as e:
        logserver(e)
        return "fail"
