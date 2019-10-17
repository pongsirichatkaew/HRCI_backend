from dbConfig import *

@connect_sql()
def readExcel(cursor):
    try:
        loc = ("../app/1.xlsx")
        wb = xlrd.open_workbook(loc) 
        sheet = wb.sheet_by_index(0) 
        sheet.cell_value(0, 0) 
        print sheet.cell_value(0, 1),sheet.cell_value(0, 2)
        # arr_em_id = []
        for i in range(sheet.nrows):
            sql = "SELECT employeeid FROM `employee_kpi` WHERE employeeid = %s AND year = %s AND term = %s"
            cursor.execute(sql,(sheet.cell_value(i, 0),int(sheet.cell_value(0, 1)),sheet.cell_value(0, 2)))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(),columns)
            if(len(result)>0):
                # print(result[0]['employeeid']) 
                sql_update = "UPDATE employee_kpi SET present_kpi = 'active' WHERE employeeid = %s AND year = %s AND term = %s"
                cursor.execute(sql_update,(result[0]['employeeid'],int(sheet.cell_value(0, 1)),sheet.cell_value(0, 2)))
                print 'update {}'.format(result[0]['employeeid'])
        print 'success'
        # return jsonify({'result':'success'})
    except Exception as e:
        print str(e)
        # return str(e)

readExcel()