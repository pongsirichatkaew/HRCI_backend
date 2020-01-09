# -*- coding: utf-8 -*
from dbConfig import *


@app.route('/api_notice_list_employee_one', methods=['POST'])
@connect_sql()
def api_notice_list_employee_one(cursor):
    try:
        employee_assessor = "62724"

        sql_assessor = """SELECT * FROM `assessor_kpi` WHERE status ='active' AND type = 'main' AND status_onechat = 0 AND employeeid=%s"""
        cursor.execute(sql_assessor, (employee_assessor))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(), columns)

        response_onechat_id = requests.request(
            "GET", url="https://chat-develop.one.th:8007/search_user_inet/"+employee_assessor).json()
        try:
            ond_id_leader = response_onechat_id['oneid']
            bot_id = botId()
            tokenBot = botToken()
            uuid_onechat = result[0]['uuid_onechat']
            quick_reply_element = []
            url = webmobile()
            quick_reply_element.append({
                "label": "ตรวจสอบรายชื่อพนักงาน",
                "type": "webview",
                "url": url+"/accessor/"+uuid_onechat,
                "size": "full"
            })

            payload_msg = {
                "to": ond_id_leader,
                "bot_id": bot_id,
                "message": "โปรดเลือกเมนูด้านล่างเพื่อตรวจสอบและแก้ไขรายชื่อพนักงาน \nหากไม่พบเมนู ลองทักน้องบอทมาใหม่นะคะ \n\nสามารถตรวจสอบและแก้ไขรายชื่อพนักงานใต้บังคับบัญชา ผ่านแอป one chat \n\nได้จนถึงวันที่ 1 ธันวาคม 2562 (หากต้องการแก้ไขหลังจากวันดังกล่าวสามารถทำผ่านเว็บไซต์ https://hr-management.inet.co.th)",
                "quick_reply":  quick_reply_element
            }
            response_msg = requests.request("POST", url="https://chat-public.one.th:8034/api/v1/push_quickreply",
                                            headers={'Authorization': tokenBot}, json=payload_msg, timeout=(60 * 1)).json()
            print employee_assessor, response_msg
        except Exception as e:
            pass
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"


@app.route('/api_notice_list_employee', methods=['POST'])
@connect_sql()
def api_notice_list_employee(cursor):
    try:
        sql_assessor = """SELECT * FROM `assessor_kpi` WHERE status ='active' AND status_onechat = 0"""
        cursor.execute(sql_assessor)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(), columns)

        for employee_assessor in result:
            response_onechat_id = requests.request("GET", url="https://chat-develop.one.th:8007/search_user_inet/"+employee_assessor['employeeid']).json()
            try:
                ond_id_leader = response_onechat_id['oneid']
                bot_id = botId()
                tokenBot = botToken()
                uuid_onechat = employee_assessor['uuid_onechat']
                quick_reply_element = []
                url = webmobile()
                quick_reply_element.append({
                    "label": "ตรวจสอบรายชื่อพนักงาน",
                    "type": "webview",
                    "url": url+"/accessor/"+uuid_onechat,
                    "size": "full"
                })

                payload_msg = {
                    "to": ond_id_leader,
                    "bot_id": bot_id,
                    "message": "โปรดเลือกเมนูด้านล่างเพื่อตรวจสอบและแก้ไขรายชื่อพนักงาน \nหากไม่พบเมนู ลองทักน้องบอทมาใหม่นะคะ \n\nสามารถตรวจสอบและแก้ไขรายชื่อพนักงานใต้บังคับบัญชา ผ่านแอป one chat \n\nได้จนถึงวันที่ 1 ธันวาคม 2562 (หากต้องการแก้ไขหลังจากวันดังกล่าวสามารถทำผ่านเว็บไซต์ https://hr-management.inet.co.th)",
                    "quick_reply":  quick_reply_element
                }
                response_msg = requests.request("POST", url="https://chat-public.one.th:8034/api/v1/push_quickreply",
                                                headers={'Authorization': tokenBot}, json=payload_msg, timeout=(60 * 1)).json()
                print employee_assessor['employeeid'], response_msg
            except Exception as e:
                pass
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"


@app.route('/api_notice_estimate_employee', methods=['POST'])
@connect_sql()
def api_notice_estimate_employee(cursor):
    try:
        sql_assessor = """SELECT * FROM `assessor_kpi` WHERE status ='active'"""
        cursor.execute(sql_assessor)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(), columns)

        for employee_assessor in result:
            response_onechat_id = requests.request(
                "GET", url="https://chat-develop.one.th:8007/search_user_inet/"+employee_assessor['employeeid']).json()
            try:
                ond_id_leader = response_onechat_id['oneid']
                bot_id = botId()
                tokenBot = botToken()
                url = webmobile()
                uuid_onechat = employee_assessor['uuid_onechat']
                quick_reply_element = []
                date = '12 ธันวาคม 2562'
                quick_reply_element.append({
                    "label": "ประเมินผล",
                    "type": "webview",
                    "url":  url+"/kpionline/"+uuid_onechat,
                    "size": "full"
                })

                payload_msg = {
                    "to": ond_id_leader,
                    "bot_id": bot_id,
                    "type": "text",
                    "message": "เหลือเวลาส่งผลประเมินอีก 30 นาทีนะคะ รบกวนหัวหน้างานทุกท่านส่งผลประเมินภายในเวลา 12.00 น. ค่ะ"

                }
                response_msg = requests.request("POST", url="https://chat-public.one.th:8034/api/v1/push_message",
                                                headers={'Authorization': tokenBot}, json=payload_msg, timeout=(60 * 1)).json()

                pl = {}
                pl['bot_id'] = bot_id
                pl['to'] = ond_id_leader
                pl['type'] = 'template'
                pl['elements'] = [
                    {
                        "image":"https://image.freepik.com/free-vector/grades-concept-illustration_114360-618.jpg",
                        "title":"ประเมินพนักงาน",
                        "detail":"กรุณากดปุ่มด้านล่างเพื่อประเมินพนักงาน",
                        "choice":[
                            {
                                "label" : "ประเมินพนักงาน",
                                "type" : "webview",
                                "url" : url+"/kpionline/"+uuid_onechat,
                                "size" : "full"
                            }
                        ]
                    }
                ]

                response = requests.request("POST", headers = {'Authorization': tokenBot},url="https://chat-public.one.th:8034/api/v1/push_message", json=pl,verify=False)
                print employee_assessor['employeeid'], response
            except Exception as e:
                pass
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"


@app.route('/api_notice_grade_employee', methods=['POST'])
@connect_sql()
def api_notice_grade_employee(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql_employee = """SELECT employeeid, name, surname, gradeCompareWithPoint, present_kpi FROM `employee_kpi` WHERE validstatus IN(2,3) AND year=%s AND term=%s AND employeeid = 62511"""
        cursor.execute(sql_employee, (data_new['year'], data_new['term']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(), columns)
        for employee in result:
            response_onechat_id = requests.request("GET", url="https://chat-develop.one.th:8007/search_user_inet/"+employee['employeeid']).json()
            try:
                ond_id =  response_onechat_id['oneid']
                bot_id = botId()
                tokenBot = botToken()
                url = webmobile()

                pl = {}
                pl['bot_id'] = bot_id
                pl['to'] = ond_id
                pl['type'] = 'template'
                pl['elements'] = [
                    {
                        "image":"https://image.freepik.com/free-vector/grades-concept-illustration_114360-618.jpg",
                        "title":"แจ้งผลการประเมิน",
                        "detail":"กรุณากดปุ่มด้านล่างเพื่ออ่านผลการประเมินและรับทราบการประกาศ",
                        "choice":[
                            {
                                "label" : "รายละเอียด",
                                "type" : "webview",
                                "url" : url+"/kpisuccess/"+employee['employeeid']+'/'+data_new['year']+'/'+data_new['term'],
                                "size" : "full"
                            }
                        ]
                    }
                ]
                print pl
                response = requests.request("POST", headers = {'Authorization': tokenBot},url="https://chat-public.one.th:8034/api/v1/push_message", json=pl,verify=False)
                print employee['employeeid'], response
            except Exception as e:
                logserver(e)
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"


@app.route('/api_notice_employee_present', methods=['POST'])
@connect_sql()
def api_notice_employee_present(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        loc = ("../app/3.xlsx")
        wb = xlrd.open_workbook(loc)
        sheet = wb.sheet_by_index(0)
        sheet.cell_value(0, 0)
        for i in range(sheet.nrows):
            sql_employee = """SELECT employeeid, em_id_leader,name,surname FROM `employee_kpi` WHERE employeeid = %s AND year=%s AND term=%s  """
            cursor.execute(sql_employee, (sheet.cell_value(i, 0), data_new['year'], data_new['term']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(), columns)
            response_onechat_id = requests.request("GET", url="https://chat-develop.one.th:8007/search_user_inet/"+result[0]['employeeid']).json()
            try:
                ond_id = response_onechat_id['oneid']
                bot_id = botId()
                tokenBot = botToken()
                date = "9 มกราคม 2563"
                time = str(sheet.cell_value(i, 2))
                room = "ห้อง Boardroom ชั้น IT"
                try:
                    payload_msg = {
                        "bot_id": bot_id,
                        "to": ond_id,
                        "type": "text",
                        "message": "โปรดอย่าลืม!!!\n\nการประเมินปลายปี 2562 \n\n"+result[0]['name']+" "+result[0]['surname']+" รหัส "+result[0]['employeeid']+"ได้รับการเข้าประเมินพรีเซนต์ผลงาน \nในวันพฤหัสบดีที่ "+date+"(วันนี้) เวลา "+time+" "+room+" \n\nหากติดปัญหาหรือมีข้อสงสัย แจ้งกับทางhr ได้เลยค่ะ\n0655029219(พิม hr)\0655083816(แป้ง hr)"
                    }
                    response_msg = requests.request("POST", url="https://chat-public.one.th:8034/api/v1/push_message",
                                                    headers={'Authorization': tokenBot}, json=payload_msg, timeout=(60 * 1)).json()
                    print response_msg
                except Exception as e:
                    pass
            except Exception as e:
                logserver(e)
            # response_onechat_id = requests.request("GET", url="https://chat-develop.one.th:8007/search_user_inet/"+result[0]['em_id_leader']).json()
            # try:
            #     ond_id = response_onechat_id['oneid']
            #     bot_id = botId()
            #     tokenBot = botToken()
            #     date = "9 มกราคม 2563"
            #     time = str(sheet.cell_value(i, 2))
            #     room = "ห้อง Boardroom ชั้น IT"
            #     try:
            #         payload_msg = {
            #             "bot_id": bot_id,
            #             "to": ond_id,
            #             "type": "text",
            #             "message": "ในการประเมินปลายปี 2562 ลูกน้องของคุณรหัสพนักงาน "+result[0]['employeeid']+"ได้รับการเข้าประเมินพรีเซนต์ผลงาน ในวันที่ "+date+" เวลา "+time+" "+room+" \n\nหากติดปัญหาหรือมีข้อสงสัย แจ้งกับทางhr ได้เลยค่ะ"
            #         }
            #         response_msg = requests.request("POST", url="https://chat-public.one.th:8034/api/v1/push_message",
            #                                         headers={'Authorization': tokenBot}, json=payload_msg, timeout=(60 * 1)).json()
            #         print response_msg
            #     except Exception as e:
            #         pass
            except Exception as e:
                logserver(e)
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"


@app.route('/api_notice_employee_before_present', methods=['POST'])
@connect_sql()
def api_notice_employee_before_present(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql_employee = """SELECT employeeid FROM `employee_kpi` WHERE validstatus IN(2,3) AND year=%s AND term=%s AND present_kpi = 'active'"""
        cursor.execute(sql_employee, (data_new['year'], data_new['term']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(), columns)
        for employee in result:
            response_onechat_id = requests.request(
                "GET", url="https://chat-develop.one.th:8007/search_user_inet/"+employee['employeeid']).json()
            try:
                ond_id = response_onechat_id['oneid']
                bot_id = botId()
                tokenBot = botToken()
                date = "15 ธันวาคม 2562"
                time = "10.30"
                room = "inet 3"
                json = {
                    "to": ond_id,
                    "bot_id": bot_id,
                    "type": "text",
                    "message": "วันที่ "+date+"(พรุ่งนี้) เวลา "+time+" น. \nอย่าลืม เข้าร่วมประเมินพรีเซนต์ผลงานที่ห้อง "+room+" นะคะ"
                }
                response_msg = requests.request("POST", url="https://chat-public.one.th:8034/api/v1/push_message",
                                                headers={'Authorization': tokenBot}, json=json, timeout=(60 * 1)).json()
            except Exception as e:
                print str(e)
                pass
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"

@app.route('/api_notice_employee_present_today', methods=['POST'])
@connect_sql()
def api_notice_employee_present_today(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql_employee = """SELECT employeeid FROM `employee_kpi` WHERE validstatus IN(2,3) AND year=%s AND term=%s AND present_kpi = 'active'"""
        cursor.execute(sql_employee, (data_new['year'], data_new['term']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(), columns)
        for employee in result:
            response_onechat_id = requests.request(
                "GET", url="https://chat-develop.one.th:8007/search_user_inet/"+employee['employeeid']).json()
            try:
                ond_id = response_onechat_id['oneid']
                bot_id = botId()
                tokenBot = botToken()
                date = "15 ธันวาคม 2562"
                time = "10.30"
                room = "inet 3"
                json = {
                    "to": ond_id,
                    "bot_id": bot_id,
                    "type": "text",
                    "message": "วันนี้ เวลา "+time+" น. \nอย่าลืม เข้าร่วมประเมินพรีเซนต์ผลงานที่ห้อง "+room+" นะคะ"
                }
                response_msg = requests.request("POST", url="https://chat-public.one.th:8034/api/v1/push_message",
                                                headers={'Authorization': tokenBot}, json=json, timeout=(60 * 1)).json()
            except Exception as e:
                print str(e)
                pass
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"

@app.route('/api_notice_board', methods=['POST'])
@connect_sql()
def api_notice_board(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        dataInput = request.json
        source = dataInput['source']
        data_new = source

        loc = ("../app/3.xlsx")
        wb = xlrd.open_workbook(loc)
        sheet = wb.sheet_by_index(0)
        sheet.cell_value(0, 0)

        for i in range(sheet.nrows):
            print sheet.cell_value(i, 4)
            sql_employee = """SELECT * FROM board_kpi_v2 WHERE validstatus=1 AND year=%s AND term=%s AND employeeid_board = %s"""
            cursor.execute(sql_employee, (data_new['year'], data_new['term'], sheet.cell_value(i, 4)))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(), columns)

            try:
                response_onechat_id = requests.request("GET", url="https://chat-develop.one.th:8007/search_user_inet/"+result[0]['employeeid_board']).json()
                one_id_board = response_onechat_id['oneid']
                bot_id = botId()
                tokenBot = botToken()
                url = webmobile()
                uuid_onechat = result[0]['uuid_onechat']
                date = "9 มกราคม 2563"
                time = str(sheet.cell_value(i, 6))
                room = "ณ ห้อง Boardroom ชั้น IT"
                json = {
                    "to": one_id_board,
                    "bot_id": bot_id,
                    "type": "text",
                    "message": "โปรดอย่าลืม!!!\n\nคุณได้รับเชิญเป็นกรรมการในการประเมินพรีเซนต์ผลงานปลายปี 2562 \n\nในวันพฤหัสบดีที่ "+date+" (วันนี้) "+time+" "+room+" \n\nหากติดปัญหาหรือมีข้อสงสัย แจ้งกับทางhr ได้เลยค่ะ\n0655029219(พิม hr)\0655083816(แป้ง hr)"
                }0655029219
                response_msg = requests.request("POST", url="https://chat-public.one.th:8034/api/v1/push_message",
                                                headers={'Authorization': tokenBot}, json=json, timeout=(60 * 1)).json()
                pl = {}
                pl['bot_id'] = bot_id
                pl['to'] = one_id_board
                pl['type'] = 'template'
                pl['elements'] = [
                    {
                        "image":"https://image.freepik.com/free-vector/grades-concept-illustration_114360-618.jpg",
                        "title":"ประเมินผล",
                        "detail":"กรุณากดปุ่มด้านล่างเพื่อประเมินผล",
                        "choice":[
                            {
                                "label" : "ประเมินผล",
                                "type" : "link",
                                "url" : url+"/kpiboard/"+uuid_onechat,
                                "size" : "full"
                            }
                        ]
                    }
                ]

                response = requests.request("POST", headers = {'Authorization': tokenBot},url="https://chat-public.one.th:8034/api/v1/push_message", json=pl,verify=False)
                print employee['employeeid_board'], response
            except Exception as e:
                print str(e)
                pass
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"


@app.route('/api_notice_board_before_present', methods=['POST'])
@connect_sql()
def api_notice_board_before_present(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql_employee = """SELECT * FROM board_kpi_v2 WHERE validstatus=1 AND year=%s AND term=%s"""
        cursor.execute(sql_employee, (data_new['year'], data_new['term']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(), columns)
        for employee in result:
            payload = {"staff_id": employee['employeeid_board']}
            response_onechat_id = requests.request(
                "GET", url="https://chat-develop.one.th:8007/search_user_inet/"+employee['employeeid_board']).json()
            try:
                one_id_board = response_onechat_id['oneid']
                bot_id = botId()
                tokenBot = botToken()
                date = "15 ธันวาคม 2562"
                time = "10.30"
                room = "inet 3"
                json = {
                    "to": one_id_board,
                    "bot_id": bot_id,
                    "type": "text",
                    "message": "วันที่ "+date+"(พรุ่งนี้) เวลา "+time+" น. \nอย่าลืม เข้าร่วมประเมินผลงานที่ห้อง "+room+" นะคะ"
                }
                response_msg = requests.request("POST", url="https://chat-public.one.th:8034/api/v1/push_message",
                                                headers={'Authorization': tokenBot}, json=json, timeout=(60 * 1)).json()
            except Exception as e:
                print str(e)
                pass
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"


@app.route('/api_notice_board_present', methods=['POST'])
@connect_sql()
def api_notice_board_present(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql_employee = """SELECT * FROM board_kpi_v2 WHERE validstatus=1 AND year=%s AND term=%s"""
        cursor.execute(sql_employee, (data_new['year'], data_new['term']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(), columns)

        for employee in result:
            payload = {"staff_id": employee['employeeid_board']}
            response_onechat_id = requests.request(
                "GET", url="https://chat-develop.one.th:8007/search_user_inet/"+employee['employeeid_board']).json()
            try:
                one_id_board = response_onechat_id['oneid']
                bot_id = botId()
                tokenBot = botToken()
                url = webmobile()
                uuid_onechat = employee['uuid_onechat']
                time = "10.30"
                room = "inet 3"
                payload_msg = {
                    "bot_id": bot_id,
                    "to": one_id_board,
                    "type": "text",
                    "message": "วันนี้ เวลา "+time+" น.\nอย่าลืม เข้าร่วมประเมินผลงานที่ห้อง "+room+" นะคะ \nหากไม่พบเมนู ลองทักน้องบอทมาใหม่นะคะ",
                }
                # print payload_msg
                response_msg = requests.request("POST", url="https://chat-public.one.th:8034/api/v1/push_message", json=payload_msg,
                                                headers={'Authorization': tokenBot}).json()

                pl = {}
                pl['bot_id'] = bot_id
                pl['to'] = one_id_board
                pl['type'] = 'template'
                pl['elements'] = [
                    {
                        "image":"https://image.freepik.com/free-vector/grades-concept-illustration_114360-618.jpg",
                        "title":"ประเมินผล",
                        "detail":"กรุณากดปุ่มด้านล่างเพื่อประเมินผล",
                        "choice":[
                            {
                                "label" : "ประเมินผล",
                                "type" : "webview",
                                "url" : url+"/kpiboard/"+uuid_onechat,
                                "size" : "full"
                            }
                        ]
                    }
                ]

                response = requests.request("POST", headers = {'Authorization': tokenBot},url="https://chat-public.one.th:8034/api/v1/push_message", json=pl,verify=False)
                print employee['employeeid_board'], response
            except Exception as e:
                print str(e)
                pass
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"


@app.route('/api_notice_upload_present', methods=['POST'])
@connect_sql()
def api_notice_upload_present(cursor):
    try:
        dataInput = request.json
        source = dataInput['source']
        data_new = source
        sql_leader = """SELECT * FROM `employee_kpi` WHERE `present_kpi`='active' AND year=%s AND term=%s GROUP BY `em_id_leader_default`"""
        cursor.execute(sql_leader, (data_new['year'], data_new['term']))
        columns = [column[0] for column in cursor.description]
        result_leader = toJson(cursor.fetchall(), columns)
        i = 0
        for employee_leader in result_leader:
            sql_assessor = """SELECT * FROM `assessor_kpi` WHERE employeeid =%s"""
            cursor.execute(sql_assessor,(employee_leader['em_id_leader_default']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(), columns)
            print employee_leader['em_id_leader_default']
            i+=1
            payload = {"staff_id": employee_leader['em_id_leader']}
            response_onechat_id = requests.request("GET", url="https://chat-develop.one.th:8007/search_user_inet/"+employee_leader['em_id_leader_default']).json()
            try:
                ond_id_leader = response_onechat_id['oneid']
                bot_id = botId()
                tokenBot = botToken()
                url = webmobile()
                uuid_onechat = result[0]['uuid_onechat']
                date = "9 มกราคม 2563 เวลา 9.00 น."
                payload_msg = {
                    "bot_id": bot_id,
                    "to": ond_id_leader,
                    "type": "text",
                    "message": "อัปโหลดสไลด์ผลงานของพนักงานใต้บังคับบัญชาที่มีสิทธิ์เข้าพรีเซนต์ \nโดยสามารถอัปโหลดได้ตั้งแต่วันนี้\n\nโปรดเลือกเมนูด้านล่างเพื่ออัปโหลดสไลด์ \nหากไม่พบเมนู ลองทักน้องบอทมาใหม่นะคะ",
                }
                # print payload_msg
                response_msg = requests.request("POST", url="https://chat-public.one.th:8034/api/v1/push_message", json=payload_msg,
                                                headers={'Authorization': tokenBot}).json()

                pl = {}
                pl['bot_id'] = bot_id
                pl['to'] = ond_id_leader
                pl['type'] = 'template'
                pl['elements'] = [
                    {
                        "image":"https://image.freepik.com/free-vector/grades-concept-illustration_114360-618.jpg",
                        "title":"อัปโหลดไฟล์พรีเซนต์",
                        "detail":"กรุณากดปุ่มด้านล่างเพื่ออัปโหลดไฟล์พรีเซนต์",
                        "choice":[
                            {
                                "label" : "อัปโหลดไฟล์พรีเซนต์",
                                "type" : "webview",
                                "url" : url+"/kpiupload/"+uuid_onechat,
                                "size" : "full"
                            }
                        ]
                    }
                ]
                print pl['elements'][0]['choice'][0]['url']
                response = requests.request("POST", headers = {'Authorization': tokenBot},url="https://chat-public.one.th:8034/api/v1/push_message", json=pl,verify=False)
                print response

            except Exception as e:
                print e
                pass
        print i
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"


@app.route('/api_notice_estimate_employee_timeout', methods=['POST'])
@connect_sql()
def api_notice_estimate_employee_timeout(cursor):
    try:
        sql_assessor = """SELECT * FROM `assessor_kpi` WHERE status ='active'"""
        cursor.execute(sql_assessor)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(), columns)

        delta = datetime(2019, 12, 16) - datetime.now()
        n = str(delta).split(" ")[0]
        n = int(n) + 2
        print n
        if (n == 0 ):
            for employee_assessor in result:

                sql_all_count = """SELECT COUNT(em_id_leader) as all_count FROM employee_kpi WHERE (em_id_leader = %s OR em_id_leader_default = %s) AND NOT validstatus=5"""
                cursor.execute(sql_all_count, (employee_assessor['employeeid'], employee_assessor['employeeid']))
                columns = [column[0] for column in cursor.description]
                allCount = toJson(cursor.fetchall(), columns)

                sql_count = """SELECT COUNT(em_id_leader) as count FROM employee_kpi WHERE (em_id_leader = %s OR em_id_leader_default = %s) AND validstatus IN(2,3)"""
                cursor.execute(sql_count, (employee_assessor['employeeid'], employee_assessor['employeeid']))
                columns = [column[0] for column in cursor.description]
                count = toJson(cursor.fetchall(), columns)

                check_estimate = int(allCount[0]['all_count']) - int(count[0]['count'])

                if check_estimate != 0:
                    payload = {"staff_id": employee_assessor['employeeid']}
                    response_onechat_id = requests.request(
                        "GET", url="https://chat-develop.one.th:8007/search_user_inet/"+employee_assessor['employeeid']).json()
                    try:
                        ond_id_leader = response_onechat_id['oneid']
                        bot_id = botId()
                        tokenBot = botToken()
                        url = webmobile()
                        uuid_onechat = employee_assessor['uuid_onechat']
                        quick_reply_element = []
                        date = '16 ธันวาคม 2562 เวลา 12.00 น.เท่านั้น'
                        if n == 0:
                            message = "ขณะนี้สิ้นสุดการประเมินแล้ว\nท่านยังเหลือพนักงานที่ยังไม่ได้ประเมินจำนวน "+str(check_estimate)+" คน"+"\nโปรดประเมินพนักงานใต้บังคับบัญชาภายในวันนี้เวลา 12.00 น. \nโดยเลือกจากเมนูด้านล่าง \nหากไม่พบเมนู ลองทักน้องบอทมาใหม่นะคะ"
                        else:
                            message = "ขณะนี้ HR ได้ขยายเวลาการประเมินผลการปฏิบัติงานปลายปี เป็นวันที่ 16 ธันวาคม 2562 เวลา 12.00 น.เท่านั้น \nขอความร่วมมือหัวหน้างานทุกท่านกรอกแบบประเมินผลการปฏิบัติงานของพนักงานในสังกัดท่านตามวันและเวลาที่กำหนดด้วยค่ะ"

                        payload_msg = {
                            "bot_id": bot_id,
                            "to": ond_id_leader,
                            "type": "text",
                            "message": message,
                        }
                        # print payload_msg
                        response_msg = requests.request("POST", url="https://chat-public.one.th:8034/api/v1/push_message", json=payload_msg,
                                                        headers={'Authorization': tokenBot}).json()

                        pl = {}
                        pl['bot_id'] = bot_id
                        pl['to'] = ond_id_leader
                        pl['type'] = 'template'
                        pl['elements'] = [
                            {
                                "image":"https://image.freepik.com/free-vector/grades-concept-illustration_114360-618.jpg",
                                "title":"ประเมินพนักงาน",
                                "detail":"กรุณากดปุ่มด้านล่างเพื่อประเมินพนักงาน",
                                "choice":[
                                    {
                                        "label" : "ประเมินพนักงาน",
                                        "type" : "webview",
                                        "url" : url+"/kpionline/"+uuid_onechat,
                                        "size" : "full"
                                    }
                                ]
                            }
                        ]

                        response = requests.request("POST", headers = {'Authorization': tokenBot},url="https://chat-public.one.th:8034/api/v1/push_message", json=pl,verify=False)
                        print employee_assessor['employeeid'], response
                    except Exception as e:
                        print e
                        pass

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"


@app.route('/api_send_file_kpi', methods=['GET'])
@connect_sql()
def api_send_file_kpi(cursor):
    try:
        sql_employee = """SELECT * FROM `assessor_kpi` WHERE status = 'active'  """
        cursor.execute(sql_employee)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(), columns)
        # result = [{'employeeid': '45035'},{'employeeid': '55013'}, {'employeeid': '58100'}, {'employeeid': '58143'}, {'employeeid': '43019'}, {'employeeid': '56087'}, {'employeeid': '19051'}, {'employeeid': '58163'}, {'employeeid': 'SC3357059'}, {'employeeid': '57026'}, {'employeeid': 'PC2155031'}, {'employeeid': '62296'}, {'employeeid': 'OC2247033'}, {'employeeid': 'MP2662002'}, {'employeeid': 'TM660001'}, {'employeeid': 'D20170003'}, {'employeeid': 'TD20160011'}, {'employeeid': 'OLS758150'}, {'employeeid': 'IM1455007'}, {'employeeid': 'OD1112069'}, {'employeeid': '58096'}, {'employeeid': '19050'}, {'employeeid': '58088'}, {'employeeid': '59187'}, {'employeeid': '61551'}, {'employeeid': '60033'}, {'employeeid': 'AL1661001'}, {'employeeid': '57071'}, {'employeeid': 'NP961001'}, {'employeeid': 'CM2962001'}, {'employeeid': 'OB1860368'}, {'employeeid': 'IM1456131'}, {'employeeid': 'IM1457047'}, {'employeeid': 'LG2762002'}, {'employeeid': 'MP2662004'}, {'employeeid': 'IM1456125'}, {'employeeid': 'MA2047006'}, {'employeeid': 'IG460001'}, {'employeeid': '58034'}, {'employeeid': '57061'}, {'employeeid': '19024'}, {'employeeid': 'IB1060157'}, {'employeeid': 'AM3062002'}, {'employeeid': 'i25540002'}, {'employeeid': '49012'}, {'employeeid': 'IM1456130'}, {'employeeid': 'IM1456097'}, {'employeeid': 'IB1017003'}, {'employeeid': '19036'}, {'employeeid': 'TM661006'}, {'employeeid': 'TM658039'}, {'employeeid': 'AG2361001'}, {'employeeid': '19052'}, {'employeeid': 'OC2259176'}]
        for employee in result:
            response_onechat_id = requests.request(
                "GET", url="https://chat-develop.one.th:8007/search_user_inet/"+employee['employeeid']).json()
            try:
                files = {'file': open('Example_slide_kpi.pdf'.encode('utf-8'), 'rb')}
                # files2 = {'file': open('kpi_outsource_2019.pdf'.encode('utf-8'), 'rb')}
                one_id = response_onechat_id['oneid']
                print 'ond_id', one_id
                bot_id = botId()
                tokenBot = botToken()
                payload_msg = {
                    "bot_id": bot_id,
                    "to": one_id,
                    "type": "text",
                    "message": "ตัวอย่างสไลด์ สำหรับพนักงานที่ต้องเข้าพรีเซ็นต์ค่ะ"
                }
                # print payload_msg
                response_msg = requests.request("POST", url="https://chat-public.one.th:8034/api/v1/push_message", json=payload_msg,
                                                headers={'Authorization': tokenBot}).json()
                payload_msg = {
                    "bot_id": bot_id,
                    "to": one_id,
                    "type": "file"
                }
                print payload_msg, 'success1'
                response_msg = requests.request("POST", url="https://chat-public.one.th:8034/api/v1/push_message", data=payload_msg, files=files,
                                                headers={'Authorization': tokenBot}).json()
                print employee['employeeid'], response_msg

                # payload_msg = {
                #     "bot_id": bot_id,
                #     "to": one_id,
                #     "type": "text",
                #     "message": "หลักเกณฑ์การประเมินผลปลายปี 2019 กลุ่มงาน Outsource"
                # }
                # # print payload_msg
                # response_msg = requests.request("POST", url="https://chat-public.one.th:8034/api/v1/push_message", json=payload_msg,
                #                                 headers={'Authorization': tokenBot}).json()
                # payload_msg = {
                #     "bot_id": bot_id,
                #     "to": one_id,
                #     "type": "file"
                # }
                # # print payload_msg
                # response_msg = requests.request("POST", url="https://chat-public.one.th:8034/api/v1/push_message", data=payload_msg, files=files2,
                #                                 headers={'Authorization': tokenBot}).json()
                # print employee['employeeid'], 'success2'
            except Exception as e:
                print employee['employeeid']+'not found/error'
                logserver(e)
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"

@app.route('/api_notice_list_template', methods=['POST'])
@connect_sql()
def api_notice_list_template(cursor):
    try:
        employee_assessor = "62511"

        sql_assessor = """SELECT * FROM `assessor_kpi` WHERE status ='active' AND employeeid=%s"""
        cursor.execute(sql_assessor,(employee_assessor))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        response_onechat_id = requests.request("GET", url="https://chat-develop.one.th:8007/search_user_inet/"+employee_assessor).json()
        try:
            ond_id_leader =  response_onechat_id['oneid']
            bot_id = botId()
            tokenBot = botToken()
            uuid_onechat = result[0]['uuid_onechat']
            url = webmobile()

            pl = {}
            pl['bot_id'] = bot_id
            pl['to'] = ond_id_leader
            pl['type'] = 'template'
            pl['elements'] = [
                {
                    "image":"https://image.freepik.com/free-vector/grades-concept-illustration_114360-618.jpg",
                    "title":"ประเมินพนักงาน",
                    "detail":"กรุณากดปุ่มด้านล่างเพื่อประเมินพนักงาน",
                    "choice":[
                        {
                            "label" : "ประเมินพนักงาน",
                            "type" : "webview",
                            "url" : url+"/kpionline/"+uuid_onechat,
                            "size" : "full"
                        }
                    ]
                }
            ]

            response = requests.request("POST", headers = {'Authorization': tokenBot},url="https://chat-public.one.th:8034/api/v1/push_message", json=pl,verify=False)
            print employee_assessor, response
        except Exception as e:
            print 'error',e
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"

@app.route('/check_leader_duplicate', methods=['POST'])
@connect_sql()
def check_leader_duplicate(cursor):
    sql = """SELECT * FROM `assessor_kpi`"""
    cursor.execute(sql)
    columns = [column[0] for column in cursor.description]
    result = toJson(cursor.fetchall(), columns)

    for employee in result:
        print employee['employeeid']
        sql2 = """SELECT * FROM `employee_kpi` WHERE em_id_leader=%s AND employeeid=%s"""
        cursor.execute(sql2, (employee['employeeid'], employee['employeeid']))
        columns = [column[0] for column in cursor.description]
        result2 = toJson(cursor.fetchall(), columns)
        print result2

    return 'succes'
