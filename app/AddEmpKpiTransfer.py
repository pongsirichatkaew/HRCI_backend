from dbConfig import *

@connect_sql()
def Add_emp_kpi_tranfer(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        print data_new
        
        employeeid_leadernew = str(data_new['employeeid_new'])
        try:
            sql44 = "SELECT name FROM employee_kpi WHERE employeeid=%s AND em_id_leader=%s AND year=%s AND term=%s"
            cursor.execute(sql44,(data_new['employeeid'],employeeid_leadernew,data_new['year'],data_new['term']))
            columns = [column[0] for column in cursor.description]
            result_44 = toJson(cursor.fetchall(),columns)
            name = result_44[0]['name']
            return "employee is duplicate"
        except Exception as e:
            pass

        try:
            sql44 = "SELECT name_asp FROM assessor_kpi WHERE companyid=%s AND employeeid=%s AND org_name_id=%s"
            cursor.execute(sql44,(data_new['companyid'],employeeid_leadernew,data_new['org_name_id']))
            columns = [column[0] for column in cursor.description]
            result_test = toJson(cursor.fetchall(),columns)
            name_test = result_test[0]['name_asp']
        except Exception as e:
            try:
                sqlQry = "SELECT assessor_kpi_id FROM assessor_kpi ORDER BY assessor_kpi_id DESC LIMIT 1"
                cursor.execute(sqlQry)
                columns = [column[0] for column in cursor.description]
                result_ass = toJson(cursor.fetchall(),columns)
                assessor_kpi_id_last = result_ass[0]['assessor_kpi_id']+1
            except Exception as e:
                assessor_kpi_id_last = 1
            type = 'submain'
            sql = "INSERT INTO assessor_kpi (assessor_kpi_id,employeeid,companyid,name_asp,surname_asp,org_name_id,email_asp,createby,type) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,(assessor_kpi_id_last,employeeid_leadernew,data_new['companyid'],data_new['name_asp'],data_new['surname_asp'],data_new['org_name_id'],data_new['email_asp'],data_new['createby'],type))

            type_action = "ADDtranfer"

            sql_log = "INSERT INTO assessor_kpi_log (assessor_kpi_id,employeeid,companyid,name_asp,surname_asp,org_name_id,email_asp,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql_log,(assessor_kpi_id_last,employeeid_leadernew,data_new['companyid'],data_new['name_asp'],data_new['surname_asp'],data_new['org_name_id'],data_new['email_asp'],data_new['createby'],type_action))


        sql_test = "SELECT * FROM employee_kpi WHERE employeeid=%s AND year=%s AND term=%s"
        cursor.execute(sql_test,(data_new['employeeid'],data_new['year'],data_new['term']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        type_action = "tranfer"

        sqlIn_be2 = "INSERT INTO employee_kpi_log(year,term,companyid,em_id_leader,structure_salary,employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,star_date_kpi,status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_be2,(result[0]['year'],result[0]['term'],result[0]['companyid'],result[0]['employeeid'],result[0]['structure_salary'],data_new['employeeid'],result[0]['name'],result[0]['surname'],result[0]['org_name'],result[0]['position'],result[0]['work_date'],result[0]['work_month'],result[0]['work_year'],result[0]['old_grade'],result[0]['star_date_kpi'],result[0]['status'],data_new['createby'],type_action))

        sqlIn_tran = "INSERT INTO employee_kpi_tranfer(year,term,employeeid,em_id_leader,name_asp,surname_asp,createby) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_tran,(result[0]['year'],result[0]['term'],data_new['employeeid'],employeeid_leadernew,data_new['name_asp'],data_new['surname_asp'],data_new['createby']))

        sqlI9de = "DELETE FROM employee_kpi WHERE employeeid=%s AND year=%s AND term=%s"
        cursor.execute(sqlI9de,(data_new['employeeid'],data_new['year'],data_new['term']))

        sqlIn_main = "INSERT INTO employee_kpi(year,term,companyid,em_id_leader,structure_salary,employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,star_date_kpi,status,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlIn_main,(result[0]['year'],result[0]['term'],result[0]['companyid'],employeeid_leadernew,result[0]['structure_salary'],result[0]['employeeid'],result[0]['name'],result[0]['surname'],result[0]['org_name'],result[0]['position'],result[0]['work_date'],result[0]['work_month'],result[0]['work_year'],result[0]['old_grade'],result[0]['star_date_kpi'],result[0]['status'],data_new['createby']))

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"


@connect_sql()
def readExcel(cursor):
    try:
        loc = ("../app/2.xlsx")
        wb = xlrd.open_workbook(loc) 
        sheet = wb.sheet_by_index(0) 
        sheet.cell_value(0, 0) 
        for i in range(sheet.nrows):
            try:
                # Check is duplicate
                try:
                    sql44 = "SELECT name FROM employee_kpi WHERE employeeid=%s AND em_id_leader=%s AND year=%s AND term=%s"
                    cursor.execute(sql44,(sheet.cell_value(i, 0),sheet.cell_value(i, 1),sheet.cell_value(0, 3),sheet.cell_value(0, 4)))
                    columns = [column[0] for column in cursor.description]
                    result_44 = toJson(cursor.fetchall(),columns)
                    name = result_44[0]['name']
                    print "employee {} is duplicate".format(sheet.cell_value(i, 0))
                except Exception as e:
                    pass

                sql44 = "SELECT * FROM employee WHERE employeeid=%s"
                cursor.execute(sql44,(int(sheet.cell_value(i, 1))))
                columns = [column[0] for column in cursor.description]
                employee_test = toJson(cursor.fetchall(),columns)
                print int(sheet.cell_value(i, 1))
                # Check duplicate accessor and available Employee
                try:
                    

                    sql44 = "SELECT name_asp FROM assessor_kpi WHERE companyid=%s AND employeeid=%s AND org_name_id=%s"
                    cursor.execute(sql44,(employee_test[0]['company_id'],sheet.cell_value(i, 1),employee_test[0]['org_name_id']))
                    columns = [column[0] for column in cursor.description]
                    result_test = toJson(cursor.fetchall(),columns)
                    name_test = result_test[0]['name_asp']

                except Exception as e:
                    try:
                        sqlQry = "SELECT assessor_kpi_id FROM assessor_kpi ORDER BY assessor_kpi_id DESC LIMIT 1"
                        cursor.execute(sqlQry)
                        columns = [column[0] for column in cursor.description]
                        result_ass = toJson(cursor.fetchall(),columns)
                        assessor_kpi_id_last = result_ass[0]['assessor_kpi_id']+1
                    except Exception as e:
                        assessor_kpi_id_last = 1

                    type = 'submain'
                    sql = "INSERT INTO assessor_kpi (assessor_kpi_id,employeeid,companyid,name_asp,surname_asp,org_name_id,email_asp,createby,type) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sql,(assessor_kpi_id_last,sheet.cell_value(i, 1),employee_test[0]['company_id'],employee_test[0]['name_th'],employee_test[0]['surname_th'],employee_test[0]['org_name_id'],employee_test[0]['email'],sheet.cell_value(0, 2),type))

                    type_action = "ADDtranfer"

                    sql_log = "INSERT INTO assessor_kpi_log (assessor_kpi_id,employeeid,companyid,name_asp,surname_asp,org_name_id,email_asp,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sql_log,(assessor_kpi_id_last,sheet.cell_value(i, 1),employee_test[0]['company_id'],employee_test[0]['name_th'],employee_test[0]['surname_th'],employee_test[0]['org_name_id'],employee_test[0]['email'],sheet.cell_value(0, 2),type_action))


                sql_test = "SELECT * FROM employee_kpi WHERE employeeid=%s AND year=%s AND term=%s"
                cursor.execute(sql_test,(sheet.cell_value(i, 0),sheet.cell_value(0, 3),sheet.cell_value(0, 4)))
                columns = [column[0] for column in cursor.description]
                result = toJson(cursor.fetchall(),columns)

                type_action = "tranfer"

                sqlIn_be2 = "INSERT INTO employee_kpi_log(year,term,companyid,em_id_leader,structure_salary,employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,star_date_kpi,status,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn_be2,(result[0]['year'],result[0]['term'],result[0]['companyid'],result[0]['employeeid'],result[0]['structure_salary'],sheet.cell_value(i, 0),result[0]['name'],result[0]['surname'],result[0]['org_name'],result[0]['position'],result[0]['work_date'],result[0]['work_month'],result[0]['work_year'],result[0]['old_grade'],result[0]['star_date_kpi'],result[0]['status'],sheet.cell_value(0, 2),type_action))

                sqlIn_tran = "INSERT INTO employee_kpi_tranfer(year,term,employeeid,em_id_leader,name_asp,surname_asp,createby) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn_tran,(result[0]['year'],result[0]['term'],sheet.cell_value(i, 0),sheet.cell_value(i, 1),employee_test[0]['name_th'],employee_test[0]['surname_th'],sheet.cell_value(0, 2)))

                sqlI9de = "DELETE FROM employee_kpi WHERE employeeid=%s AND year=%s AND term=%s"
                cursor.execute(sqlI9de,(sheet.cell_value(i, 0),sheet.cell_value(0, 3),sheet.cell_value(0, 4)))

                sqlIn_main = "INSERT INTO employee_kpi(year,term,companyid,em_id_leader,structure_salary,employeeid,name,surname,org_name,position,work_date,work_month,work_year,old_grade,star_date_kpi,status,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlIn_main,(result[0]['year'],result[0]['term'],result[0]['companyid'],sheet.cell_value(i, 1),result[0]['structure_salary'],result[0]['employeeid'],result[0]['name'],result[0]['surname'],result[0]['org_name'],result[0]['position'],result[0]['work_date'],result[0]['work_month'],result[0]['work_year'],result[0]['old_grade'],result[0]['star_date_kpi'],result[0]['status'],sheet.cell_value(0, 2)))

                print "{} Transfer Success".format(result[0]['employeeid'])
              
            except Exception as e:
                print str(e)
                pass
        
        print 'success'
    except Exception as e:
        print str(e)

readExcel()