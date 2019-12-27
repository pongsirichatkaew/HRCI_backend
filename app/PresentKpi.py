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
                sql_update = "UPDATE employee_kpi SET present_kpi = 'active',status_confirm = 0 WHERE employeeid = %s AND year = %s AND term = %s"
                cursor.execute(sql_update,(result[0]['employeeid'],int(sheet.cell_value(0, 1)),sheet.cell_value(0, 2)))
                print 'update {}'.format(result[0]['employeeid'])
        print 'success'


        sql_board="""SELECT board_kpi_v2.year,board_kpi_v2.term,board_kpi_v2.employeeid_board,employee.name_th,employee.surname_th,position.position_detail FROM `board_kpi_v2`
                        LEFT JOIN employee ON board_kpi_v2.employeeid_board = employee.employeeid
                        LEFT JOIN position ON employee.position_id = position.position_id
                        WHERE year = %s AND term = %s AND validstatus = 1"""
        cursor.execute(sql_board,(int(sheet.cell_value(0, 1)),sheet.cell_value(0, 2)))
        columns = [column[0] for column in cursor.description]
        result_board = toJson(cursor.fetchall(),columns)

        group_kpi_id = 'WHERE year='+'"'+str(int(sheet.cell_value(0, 1)))+'"'+' AND term='+'"'+str(sheet.cell_value(0, 2))+'" AND present_kpi = "active" '
        for board in result_board:
            try:
                sql_emp_kpi = "SELECT employee_kpi.year,employee_kpi.term,employee_kpi.employeeid FROM employee_kpi INNER JOIN board_kpi ON employee_kpi.employeeid = board_kpi.employeeid "+group_kpi_id+" AND board_kpi.validstatus=1 GROUP BY board_kpi.employeeid"
                cursor.execute(sql_emp_kpi)
                columns = [column[0] for column in cursor.description]
                result = toJson(cursor.fetchall(),columns)
                check_emid = result[0]['employeeid']
            except Exception as e:
                sql_emp_kpi = "SELECT * FROM employee_kpi "+group_kpi_id+" "
                cursor.execute(sql_emp_kpi)
                columns = [column[0] for column in cursor.description]
                result = toJson(cursor.fetchall(),columns)

            type_action = "ADD"

            for i in xrange(len(result)):
                check_em_id = str(result[i]['employeeid'])
                check_em_board = str(board['employeeid_board'])
                # print check_em_id #62226 result of employee_kpi
                # print check_em_board #62224 board_kpi add
                if check_em_id==check_em_board: #if the same guys pass
                    pass
                else:
                    sqlIn_bet = "INSERT INTO board_kpi(year,term,employeeid,employeeid_board,name_kpi,surname_kpi,position_kpi,createby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sqlIn_bet,(result[i]['year'],result[i]['term'],result[i]['employeeid'],str(board['employeeid_board']),board['name_th'],board['surname_th'],board['position_detail'],'Admin'))

            for i in xrange(len(result)):
                check_em_id = str(result[i]['employeeid'])
                check_em_board = str(board['employeeid_board'])
                if check_em_id==check_em_board:
                    type_action = "Copy_board"
                    sqlIn_be_2 = "INSERT INTO board_kpi_log(year,term,employeeid,employeeid_board,name_kpi,surname_kpi,position_kpi,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sqlIn_be_2,(result[i]['year'],result[i]['term'],result[i]['employeeid'],str(board['employeeid_board']),board['name_th'],board['surname_th'],board['position_detail'],'Admin',type_action))
                else:
                    sqlIn_be_2 = "INSERT INTO board_kpi_log(year,term,employeeid,employeeid_board,name_kpi,surname_kpi,position_kpi,createby,type_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sqlIn_be_2,(result[i]['year'],result[i]['term'],result[i]['employeeid'],str(board['employeeid_board']),board['name_th'],board['surname_th'],board['position_detail'],'Admin',type_action))
        # return jsonify({'result':'success'})
    except Exception as e:
        print str(e)
        # return str(e)

readExcel()
