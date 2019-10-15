from dbConfig import *

@connect_sql()
def readExcel(cursor):
    try:
        loc = ("../app/1.xlsx")
        wb = xlrd.open_workbook(loc) 
        sheet = wb.sheet_by_index(0) 
        sheet.cell_value(0, 0) 
        # arr_em_id = []
        for i in range(sheet.nrows):
            sql = "SELECT employeeid FROM `employee_kpi` WHERE employeeid = %s"
            cursor.execute(sql,(sheet.cell_value(i, 0)))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            if(len(result)>0):
                # print(result[0]['employeeid']) 
                sql_update = "UPDATE employee_kpi SET present_kpi = 'active' WHERE employeeid = %s"
                cursor.execute(sql_update,(result[0]['employeeid']))
                print 'update {}'.format(result[0]['employeeid'])
        return jsonify({'result':'success'})
    except Exception as e:
        print str(e)
        return str(e)