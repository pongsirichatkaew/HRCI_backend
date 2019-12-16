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
        sql_employee = """SELECT employeeid, gradeCompareWithPoint, present_kpi FROM `employee_kpi` WHERE validstatus IN(2,3) AND year=%s AND term=%s"""
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
                try:
                    if employee['present_kpi'] == 'active':
                        payload_msg = {
                            "bot_id": bot_id,
                            "to": ond_id,
                            "type": "text",
                            "message": "ในการประเมินปลายปี 2562 คุณได้รับเกรด: " + employee['gradeCompareWithPoint']+"\nคุณได้รับสิทธิ์ในการเข้าพรีเซนต์ผลงาน \n\nรอน้องบอทติดต่อกลับเพื่อแจ้งรายละเอียดตารางเวลาและสถานที่พรีเซนต์ผลงานภายหลังนะคะ \n\nอย่าลืม!! จัดทำสไลด์พรีเซนต์ผลงานตนเองแล้วส่งมอบให้หัวหน้างานน้าาา"
                        }
                    else:
                        payload_msg = {
                            "bot_id": bot_id,
                            "to": ond_id,
                            "type": "text",
                            "message": "ในการประเมินปลายปี 2562 คุณได้รับเกรด: " + employee['gradeCompareWithPoint']
                        }
                    response_msg = requests.request("POST", url="https://chat-public.one.th:8034/api/v1/push_message",
                                                    headers={'Authorization': tokenBot}, json=payload_msg, timeout=(60 * 1)).json()
                except Exception as e:
                    pass
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
                try:
                    payload_msg = {
                        "bot_id": bot_id,
                        "to": ond_id,
                        "type": "text",
                        "message": "ในการประเมินปลายปี 2562 คุณได้รับการเข้าประเมินพรีเซนต์ผลงาน ใน"+date+" "+time+" "+room+" \nหากติดปัญหาหรือมีข้อสงสัย แจ้งกับทางhr ได้เลยค่ะ"
                    }
                    response_msg = requests.request("POST", url="https://chat-public.one.th:8034/api/v1/push_message",
                                                    headers={'Authorization': tokenBot}, json=payload_msg, timeout=(60 * 1)).json()
                except Exception as e:
                    pass
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
                    "message": "ในการประเมินปลายปี 2562 คุณเป็นกรรมการในการประเมินพรีเซนต์ผลงาน ใน"+date+" "+time+" "+room+" \n หากติดปัญหาหรือมีข้อสงสัย แจ้งกับทางhr ได้เลยค่ะ"
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
        sql_leader = """SELECT * FROM `employee_kpi` WHERE `present_kpi`='active' AND year=%s AND term=%s GROUP BY `em_id_leader`"""
        cursor.execute(sql_leader, (data_new['year'], data_new['term']))
        columns = [column[0] for column in cursor.description]
        result_leader = toJson(cursor.fetchall(), columns)
        for employee_leader in result_leader:
            sql_assessor = """SELECT * FROM `assessor_kpi` WHERE employeeid =%s"""
            cursor.execute(sql_assessor,(employee_leader['em_id_leader']))
            columns = [column[0] for column in cursor.description]
            result = toJson(cursor.fetchall(), columns)
            print result
            payload = {"staff_id": employee_leader['em_id_leader']}
            response_onechat_id = requests.request("GET", url="https://chat-develop.one.th:8007/search_user_inet/"+employee_leader['em_id_leader']).json()
            try:
                ond_id_leader = response_onechat_id['oneid']
                bot_id = botId()
                tokenBot = botToken()
                url = webmobile()
                uuid_onechat = result[0]['uuid_onechat']
                date = "15 ธันวาคม 2562"
                payload_msg = {
                    "bot_id": bot_id,
                    "to": ond_id_leader,
                    "type": "text",
                    "message": "อัปโหลดสไลด์ผลงานของพนักงานใต้บังคับบัญชาที่มีสิทธิ์เข้าพรีเซนต์ \nโดยสามารถอัปโหลดได้ตั้งแต่วันนี้ จนถึง "+date+" \nโปรดเลือกเมนูด้านล่างเพื่ออัปโหลดสไลด์ \nหากไม่พบเมนู ลองทักน้องบอทมาใหม่นะคะ",
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

                response = requests.request("POST", headers = {'Authorization': tokenBot},url="https://chat-public.one.th:8034/api/v1/push_message", json=pl,verify=False)
                print response

            except Exception as e:
                print e
                pass
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

        if (n !=0 ):
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
                        if n == 1:
                            message = "ขณะนี้เป็นวันสุดท้ายในการประเมิน\nท่านยังเหลือพนักงานที่ยังไม่ได้ประเมินจำนวน "+str(check_estimate)+" คน"+"\nโปรดประเมินพนักงานใต้บังคับบัญชา \nโดยเลือกจากเมนูด้านล่าง (ประเมินได้ตั้งแต่วันนี้ จนถึง "+date+") \nหากไม่พบเมนู ลองทักน้องบอทมาใหม่นะคะ"
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
        for employee in result:
            response_onechat_id = requests.request(
                "GET", url="https://chat-develop.one.th:8007/search_user_inet/"+employee['employeeid']).json()
            try:
                files = {'file': open('One_Chat_Employee_Assessment.pdf'.encode('utf-8'), 'rb')}
                # files2 = {'file': open('kpi_outsource_2019.pdf'.encode('utf-8'), 'rb')}
                one_id = response_onechat_id['oneid']
                print 'ond_id', one_id
                bot_id = botId()
                tokenBot = botToken()
                payload_msg = {
                    "bot_id": bot_id,
                    "to": one_id,
                    "type": "text",
                    "message": "คู่มือการประเมินพนักงานผ่านone chat ค่ะ"
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
                # print employee['employeeid'], response_msg

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
            quick_reply_element = []
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
