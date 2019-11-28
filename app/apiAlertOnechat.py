# -*- coding: utf-8 -*
from dbConfig import *

@app.route('/api_notice_list_employee', methods=['POST'])
@connect_sql()
def api_notice_list_employee(cursor):
    try:
        sql_assessor = """SELECT * FROM `assessor_kpi` WHERE status ='active' AND type = 'main' AND status_onechat = 0"""
        cursor.execute(sql_assessor)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        for employee_assessor in result:
            response_onechat_id = requests.request("GET", url="https://chat-develop.one.th:8007/search_user_inet/"+employee_assessor['employeeid']).json()
            try:
                ond_id_leader =  response_onechat_id['oneid']
                bot_id = botId()
                tokenBot = botToken()
                uuid_onechat = employee_assessor['uuid_onechat']
                quick_reply_element = []
                url = webmobile()
                quick_reply_element.append({
                "label" : "ตรวจสอบรายชื่อพนักงาน",
                "type" : "webview",
                "url" : url+"/accessor/"+uuid_onechat,
                "size" : "full"
                })

                payload_msg =  {
                                "to" : ond_id_leader,
                                "bot_id" : bot_id,
                                "message": "โปรดเลือกเมนูด้านล่างเพื่อตรวจสอบและแก้ไขรายชื่อพนักงาน \nหากไม่พบเมนู ลองทักน้องบอทมาใหม่นะคะ \n\nสามารถตรวจสอบและแก้ไขรายชื่อพนักงานใต้บังคับบัญชา ผ่านแอป one chat \n\nได้จนถึงวันที่ 1 ธันวาคม 2562 (หากต้องการแก้ไขหลังจากวันดังกล่าวสามารถทำผ่านเว็บไซต์ https://hr-management.inet.co.th)",
                                "quick_reply" :  quick_reply_element
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
        sql_assessor = """SELECT * FROM `assessor_kpi` WHERE status ='active' AND type = 'main'"""
        cursor.execute(sql_assessor)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        for employee_assessor in result:
            response_onechat_id = requests.request("GET", url="https://chat-develop.one.th:8007/search_user_inet/"+employee_assessor['employeeid']).json()
            try:
                ond_id_leader =  response_onechat_id['oneid']
                bot_id = botId()
                tokenBot = botToken()
                url = webmobile()
                uuid_onechat = employee_assessor['uuid_onechat']
                quick_reply_element = []
                date = '12 ธันวาคม 2562'
                quick_reply_element.append({
                "label" : "ประเมินผล",
                "type" : "webview",
                "url" :  url+"/kpionline/"+uuid_onechat,
                "size" : "full"
                })

                payload_msg =  {
                                "to" : ond_id_leader,
                                "bot_id" : bot_id,
                                "message": "โปรดประเมินพนักงานใต้บังคับบัญชา \nโดยเลือกจากเมนูด้านล่าง (ประเมินได้ตั้งแต่วันนี้ จนถึง "+date+") \nหากไม่พบเมนู ลองทักน้องบอทมาใหม่นะคะ",
                                "quick_reply" :  quick_reply_element
                            }
                response_msg = requests.request("POST", url="https://chat-public.one.th:8034/api/v1/push_quickreply",
                headers={'Authorization': tokenBot}, json=payload_msg, timeout=(60 * 1)).json()
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
        cursor.execute(sql_employee,(data_new['year'], data_new['term']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        for employee in result:
            response_onechat_id = requests.request("GET", url="https://chat-develop.one.th:8007/search_user_inet/"+employee['employeeid']).json()
            try:
                ond_id =  response_onechat_id['oneid']
                bot_id = botId()
                tokenBot = botToken()
                try:
                    if employee['present_kpi'] == 'active':
                        payload_msg =  {
                            "bot_id":bot_id,
                            "to": ond_id,
                            "type":"text",
                            "message": "ในการประเมินปลายปี 2562 คุณได้รับเกรด: "+ employee['gradeCompareWithPoint']+"\nคุณได้รับสิทธิ์ในการเข้าพรีเซนต์ผลงาน \n\nรอน้องบอทติดต่อกลับเพื่อแจ้งรายละเอียดตารางเวลาและสถานที่พรีเซนต์ผลงานภายหลังนะคะ \n\nอย่าลืม!! จัดทำสไลด์พรีเซนต์ผลงานตนเองแล้วส่งมอบให้หัวหน้างานน้าาา"
                        }
                    else:
                        payload_msg =  {
                            "bot_id":bot_id,
                            "to": ond_id,
                            "type":"text",
                            "message": "ในการประเมินปลายปี 2562 คุณได้รับเกรด: "+ employee['gradeCompareWithPoint']
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
        cursor.execute(sql_employee,(data_new['year'], data_new['term']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        for employee in result:
            response_onechat_id = requests.request("GET", url="https://chat-develop.one.th:8007/search_user_inet/"+employee['employeeid']).json()
            try:
                ond_id =  response_onechat_id['oneid']
                bot_id = botId()
                tokenBot = botToken()
                date = "วันที่ เวลา สถานที่"
                try:
                    payload_msg =  {
                        "bot_id":bot_id,
                        "to": ond_id,
                        "type":"text",
                        "message": "ในการประเมินปลายปี 2562 คุณได้รับการเข้าประเมินพรีเซนต์ผลงาน ใน"+date+" \nหากติดปัญหาหรือมีข้อสงสัย แจ้งกับทางhr ได้เลยค่ะ"
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
            response_onechat_id = requests.request("GET", url="https://chat-develop.one.th:8007/search_user_inet/"+employee['employeeid_board']).json()
            try:
                one_id_board = response_onechat_id['oneid']
                bot_id = botId()
                tokenBot = botToken()
                date = "วันที่ เวลา สถานที่"
                json = {
                    "to" : one_id_board,
                    "bot_id" : bot_id,
                    "type" : "text",
                    "message" : "ในการประเมินปลายปี 2562 คุณเป็นกรรมการในการประเมินพรีเซนต์ผลงาน ใน"+date+" \n หากติดปัญหาหรือมีข้อสงสัย แจ้งกับทางhr ได้เลยค่ะ"
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
            response_onechat_id = requests.request("GET", url="https://chat-develop.one.th:8007/search_user_inet/"+employee['employeeid_board']).json()
            try:
                one_id_board = response_onechat_id['oneid']
                bot_id = botId()
                tokenBot = botToken()
                json = {
                    "to" : one_id_board,
                    "bot_id" : bot_id,
                    "type" : "text",
                    "message" : "วัน......(พรุ่งนี้) เวลา 10.30 น. \nอย่าลืม เข้าร่วมประเมินผลงานที่ห้อง .... นะคะ"
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
            response_onechat_id = requests.request("GET", url="https://chat-develop.one.th:8007/search_user_inet/"+employee['employeeid_board']).json()
            try:
                one_id_board = response_onechat_id['oneid']
                bot_id = botId()
                tokenBot = botToken()
                uuid_onechat = employee['uuid_onechat']
                quick_reply_element = []

                quick_reply_element.append({
                "label" : "ประเมินผล",
                "type" : "webview",
                "url" :  url+"/kpiboard/"+uuid_onechat,
                "size" : "full"
                })
                payload_msg =  {
                                "to" : one_id_board,
                                "bot_id" : bot_id,
                                "message": "วันนี้ เวลา 10.30 น.\nอย่าลืม เข้าร่วมประเมินผลงานที่ห้อง .... นะคะ \nหากไม่พบเมนู ลองทักน้องบอทมาใหม่นะคะ",
                                "quick_reply" :  quick_reply_element
                            }

                response_msg = requests.request("POST", url="https://chat-public.one.th:8034/api/v1/push_quickreply",
                headers={'Authorization': tokenBot}, json=payload_msg, timeout=(60 * 1)).json()
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
        sql_assessor = """SELECT * FROM `assessor_kpi` WHERE status ='active' AND type = 'main'"""
        cursor.execute(sql_assessor)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)

        for employee_assessor in result:
            payload = {"staff_id": employee_assessor['employeeid']}
            response_onechat_id = requests.request("GET", url="https://chat-develop.one.th:8007/search_user_inet/"+employee_assessor['employeeid']).json()
            try:
                ond_id_leader =  response_onechat_id['oneid']
                bot_id = botId()
                tokenBot = botToken()
                url = webmobile()
                uuid_onechat = employee_assessor['uuid_onechat']
                quick_reply_element = []

                quick_reply_element.append({
                "label" : "อัปโหลดไฟล์พรีเซนต์",
                "type" : "webview",
                "url" :  url+"/kpiupload/"+uuid_onechat,
                "size" : "full"
                })
                date = "...."
                payload_msg =  {
                                "to" : ond_id_leader,
                                "bot_id" : bot_id,
                                "message": "อัปโหลดสไลด์ผลงานของพนักงานใต้บังคับบัญชาที่มีสิทธิ์เข้าพรีเซนต์ \nโดยสามารถอัปโหลดได้ตั้งแต่วันนี้ จนถึง "+date+" \nโปรดเลือกเมนูด้านล่างเพื่ออัปโหลดสไลด์ \nหากไม่พบเมนู ลองทักน้องบอทมาใหม่นะคะ",
                                "quick_reply" :  quick_reply_element
                            }
                response_msg = requests.request("POST", url="https://chat-public.one.th:8034/api/v1/push_quickreply",
                headers={'Authorization': tokenBot}, json=payload_msg, timeout=(60 * 1)).json()
            except Exception as e:
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
        result = toJson(cursor.fetchall(),columns)

        delta = datetime(2019,12,12) - datetime.now()
        n = str(delta).split(" ")[0]

        if (n == 7 or n == 5 or n == 3 or n == 2 or n == 1):
            for employee_assessor in result:
                sql_all_count = """SELECT COUNT(em_id_leader) as all_count FROM employee_kpi WHERE em_id_leader = %s"""
                cursor.execute(sql_all_count,(employee_assessor['employeeid']))
                columns = [column[0] for column in cursor.description]
                allCount = toJson(cursor.fetchall(),columns)

                sql_count = """SELECT COUNT(em_id_leader) as count FROM employee_kpi WHERE em_id_leader = %s AND validstatus IN(2,3)"""
                cursor.execute(sql_count,(employee_assessor['employeeid']))
                columns = [column[0] for column in cursor.description]
                count = toJson(cursor.fetchall(),columns)

                check_estimate = int(allCount[0]['all_count']) - int(count[0]['count'])

                if check_estimate!=0:
                    print check_estimate
                    payload = {"staff_id": employee_assessor['employeeid']}
                    response_onechat_id = requests.request("GET", url="https://chat-develop.one.th:8007/search_user_inet/"+employee_assessor['employeeid']).json()
                    try:
                        ond_id_leader =  response_onechat_id['oneid']
                        bot_id = botId()
                        tokenBot = botToken()
                        url = webmobile()
                        uuid_onechat = employee_assessor['uuid_onechat']
                        quick_reply_element = []
                        date = '12 ธันวาคม 2562'
                        quick_reply_element.append({
                        "label" : "ประเมินผล",
                        "type" : "webview",
                        "url" :  url+"/kpionline/"+uuid_onechat,
                        "size" : "full"
                        })

                        payload_msg =  {
                                        "to" : ond_id_leader,
                                        "bot_id" : bot_id,
                                        "message": "ขณะนี้เหลือเวลาในการประเมินอีก "+ str(n) +" วัน \nท่านยังเหลือพนักงานที่ยังไม่ได้ประเมินจำนวน "+str(check_estimate)+" คน"+"\nโปรดประเมินพนักงานใต้บังคับบัญชา \nโดยเลือกจากเมนูด้านล่าง (ประเมินได้ตั้งแต่วันนี้ จนถึง "+date+") \nหากไม่พบเมนู ลองทักน้องบอทมาใหม่นะคะ",
                                        "quick_reply" :  quick_reply_element
                                    }
                        response_msg = requests.request("POST", url="https://chat-public.one.th:8034/api/v1/push_quickreply",
                        headers={'Authorization': tokenBot}, json=payload_msg, timeout=(60 * 1)).json()
                    except Exception as e:
                        print e
                        pass

        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
