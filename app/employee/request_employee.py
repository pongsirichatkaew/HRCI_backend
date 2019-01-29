#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbConfig import *

@app.route('/QryEm_request', methods=['POST'])
@connect_sql()
def QryEm_request(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql = "SELECT employee.name_th,employee.employeeid,employee.surname_th,employee.citizenid,employee.salary,Personal.NicknameTh,Personal.Age,employee.start_work,employee.EndWork_probation,position.position_detail,org_name.org_name_detail,company.company_short_name FROM employee LEFT JOIN position ON position.position_id = employee.position_id\
                                      LEFT JOIN org_name ON org_name.org_name_id = employee.org_name_id\
                                      LEFT JOIN Personal ON Personal.ID_CardNo = employee.citizenid\
                                      LEFT JOIN company ON company.companyid = employee.company_id\
        WHERE employee.employeeid=%s"
        cursor.execute(sql,(data_new['employeeid']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        for item in result:
            salary_thai = []
            decodesalary = base64.b64decode(item['salary'])
            item['salary'] = decodesalary
            salary = decodesalary
            salary= (str(salary)[::-1])
            thai_number = ("ศูนย์","หนึ่ง","สอง","สาม","สี่","ห้า","หก","เจ็ด","แปด","เก้า")
            unit = ("","สิบ","ร้อย","พัน","หมื่น","แสน","ล้าน")
            length = len(salary) > 1
            resultSalary = ""
            for index, current in enumerate(map(int, salary)):
                if current:
                    if index:
                       resultSalary = unit[index] + resultSalary
                    if length and current == 1 and index == 0:
                        resultSalary += 'เอ็ด'
                    elif index == 1 and current == 2:
                        resultSalary = 'ยี่' + resultSalary
                    elif index != 1 or current != 1:
                        resultSalary = thai_number[current] + resultSalary
            item['salary_thai'] = resultSalary
            long_date = []
            date1 = result[0]['start_work']
            star_date = date1.split("-")
            Day_s = int(star_date[0])
            Mon_s = int(star_date[1])
            year_s = int(star_date[2])
            if   Mon_s==1:
                 Mounth_name_str ="ม.ค."
            elif Mon_s==2:
                 Mounth_name_str="ก.พ."
            elif Mon_s==3:
                 Mounth_name_str="มี.ค."
            elif Mon_s==4:
                 Mounth_name_str="เม.ย."
            elif Mon_s==5:
                 Mounth_name_str="พ.ค."
            elif Mon_s==6:
                 Mounth_name_str="มิ.ย."
            elif Mon_s==7:
                 Mounth_name_str="ก.ค."
            elif Mon_s==8:
                 Mounth_name_str="ส.ค."
            elif Mon_s==9:
                 Mounth_name_str="ก.ย."
            elif Mon_s==10:
                 Mounth_name_str="ต.ค."
            elif Mon_s==11:
                 Mounth_name_str="พ.ย."
            else:
                 Mounth_name_str="ธ.ค."
            year_str = str(year_s+543)
            yer_last_str = year_str[-2:]
            item['start_work']= str(Day_s)+" "+Mounth_name_str+""+yer_last_str
            next_3_m2 = result[0]['EndWork_probation']
            end_date = next_3_m2.split("-")
            int_day_e =int(end_date[0])
            int_mon_e = int(end_date[1])
            int_year_e = int(end_date[2])
            if   int_mon_e==1:
                 Mounth_name_end ="ม.ค."
            elif int_mon_e==2:
                 Mounth_name_end="ก.พ."
            elif int_mon_e==3:
                 Mounth_name_end="มี.ค."
            elif int_mon_e==4:
                 Mounth_name_end="เม.ย."
            elif int_mon_e==5:
                 Mounth_name_end="พ.ค."
            elif int_mon_e==6:
                 Mounth_name_end="มิ.ย."
            elif int_mon_e==7:
                 Mounth_name_end="ก.ค."
            elif int_mon_e==8:
                 Mounth_name_end="ส.ค."
            elif int_mon_e==9:
                 Mounth_name_end="ก.ย."
            elif int_mon_e==10:
                 Mounth_name_end="ต.ค."
            elif int_mon_e==11:
                 Mounth_name_end="พ.ย."
            else:
                 Mounth_name_end="ธ.ค."
            year_end = str(int_year_e+543)
            yer_last_end = year_end[-2:]
            item['EndWork_probation']= str(int_day_e)+" "+Mounth_name_end+""+yer_last_end
            d0 = date(year_s,Mon_s,Day_s)
            d1 = date(int_year_e,int_mon_e,int_day_e)
            delta = d1 - d0
            str_date = str(delta)
            split_str = str_date.split(",")
            last = split_str[0].split(" ")
            item['long_date_pro'] = str(int(last[0])+1)

        sql9 = "SELECT Education.EducationLevel,Education.Institute,Education.StartYear,Education.EndYear,Education.Qualification,Education.Major,Education.GradeAvg,Education.ExtraCurricularActivities FROM Education INNER JOIN Personal ON Personal.ID_CardNo=Education.ID_CardNo \
        WHERE Personal.ID_CardNo=%s"
        cursor.execute(sql9,result[0]['citizenid'])
        columns9 = [column[0] for column in cursor.description]
        result_Education = toJson(cursor.fetchall(),columns9)

        sql10 = "SELECT Employment.CompanyName,Employment.CompanyAddress,Employment.PositionHeld,Employment.StartSalary,Employment.EndSalary,Employment.StartYear,Employment.EndYear,Employment.Responsibility,Employment.ReasonOfLeaving,Employment.Descriptionofwork FROM Employment INNER JOIN Personal ON Personal.ID_CardNo=Employment.ID_CardNo \
        WHERE Personal.ID_CardNo=%s"
        cursor.execute(sql10,result[0]['citizenid'])
        columns10 = [column[0] for column in cursor.description]
        result_Employment = toJson(cursor.fetchall(),columns10)

        sql_be = "SELECT benefits.benefits_detail,benefits.type_benefits,employee_benefits.benefits_id,employee_benefits.benefits_values,employee_benefits.type_check FROM employee_benefits LEFT JOIN benefits ON employee_benefits.benefits_id = benefits.benefits_id \
         WHERE employee_benefits.citizenid=%s"
        cursor.execute(sql_be,result[0]['citizenid'])
        columns = [column[0] for column in cursor.description]
        result_benefits = toJson(cursor.fetchall(),columns)

        result_all={}
        result_all["employee"] = result
        result_all["employee_Education"] = result_Education
        result_all["employee_Employment"] = result_Employment
        result_all["employee_Benefits"] = result_benefits

        return jsonify(result_all)
    except Exception as e:
        logserver(e)
        return "fail"
