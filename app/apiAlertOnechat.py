# -*- coding: utf-8 -*
from dbConfig import *


@app.route('/api_notice_list_employee', methods=['POST'])
@connect_sql()
def api_notice_list_employee(cursor):
    try:
        sql_assessor = """SELECT * FROM `assessor_kpi` WHERE status ='active' AND type = 'main'"""
        cursor.execute(sql_assessor)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(), columns)

        for employee_assessor in result:
            payload = {"staff_id": employee_assessor['employeeid']}
            response_onechat_id = requests.request(
                "POST", url="http://203.151.50.47:9988/search_user_inet", json=payload, timeout=(60 * 1)).json()
            ond_id_leader = response_onechat_id['staff_data']['one_id']
            bot_id = "B0ff34ea97e845aa097d37a4e2c18696c"
            tokenBot = 'Bearer A2d011e83b0cc5a9ca4595ac2999ec065771615c167094eb38fb8ac19b604a0ce58a2f17296e246cf8c5cbc3f0ece2264'
            uuid_onechat = employee_assessor['uuid_onechat']
            quick_reply_element = []

            quick_reply_element.append({
                "label": "ตรวจสอบรายชื่อพนักงาน",
                "type": "webview",
                "url": "http://203.150.37.130/accessor/"+uuid_onechat,
                "size": "full"
            })

            payload_msg = {
                "to": ond_id_leader,
                "bot_id": bot_id,
                "message": "ขณะนี้อยู่ในช่วงการตรวจสอบรายชื่อพนักงานใต้บังคับบัญชา \nโปรดเลือกเมนูด้านล่าง \nหากไม่พบเมนู ลองทักน้องบอทมาใหม่นะคะ",
                "quick_reply":  quick_reply_element
            }
            response_msg = requests.request("POST", url="https://chat-public.one.th:8034/api/v1/push_quickreply",
                                            headers={'Authorization': tokenBot}, json=payload_msg, timeout=(60 * 1)).json()
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
        result = toJson(cursor.fetchall(), columns)

        for employee_assessor in result:
            payload = {"staff_id": employee_assessor['employeeid']}
            response_onechat_id = requests.request(
                "POST", url="http://203.151.50.47:9988/search_user_inet", json=payload, timeout=(60 * 1)).json()
            ond_id_leader = response_onechat_id['staff_data']['one_id']
            bot_id = "B0ff34ea97e845aa097d37a4e2c18696c"
            tokenBot = 'Bearer A2d011e83b0cc5a9ca4595ac2999ec065771615c167094eb38fb8ac19b604a0ce58a2f17296e246cf8c5cbc3f0ece2264'
            uuid_onechat = employee_assessor['uuid_onechat']
            quick_reply_element = []

            quick_reply_element.append({
                "label": "ตรวจสอบรายชื่อพนักงาน",
                "type": "webview",
                "url": "http://203.150.37.130/kpionline/"+uuid_onechat,
                "size": "full"
            })

            payload_msg = {
                "to": ond_id_leader,
                "bot_id": bot_id,
                "message": "โปรดประเมินพนักงานใต้บังคับบัญชา \nโดยเลือกจากเมนูด้านล่าง (ประเมินได้ตั้งแต่วันนี้ จนถึง .....) \nหากไม่พบเมนู ลองทักน้องบอทมาใหม่นะคะ",
                "quick_reply":  quick_reply_element
            }
            response_msg = requests.request("POST", url="https://chat-public.one.th:8034/api/v1/push_quickreply",
                                            headers={'Authorization': tokenBot}, json=payload_msg, timeout=(60 * 1)).json()
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"


@app.route('/api_update_grade_leader', methods=['POST'])
@connect_sql()
def api_update_grade_leader(cursor):
    try:
        year = '2562'
        term = 'lateYear'
        sql_employee = """SELECT employeeid, gradeCompareWithPoint, present_kpi FROM `employee_kpi` WHERE validstatus= 2 AND year=%s AND term=%s"""
        cursor.execute(sql_employee,(year,term))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        for employee in result:
            try:
                print employee['employeeid']
                payload = {"staff_id": employee['employeeid']}
                response_onechat_id = requests.request("POST", url="http://203.151.50.47:9988/search_user_inet", json=payload, timeout=(60 * 1)).json()
                ond_id =  response_onechat_id['staff_data']['one_id']
                bot_id = "B0ff34ea97e845aa097d37a4e2c18696c"
                tokenBot = 'Bearer A2d011e83b0cc5a9ca4595ac2999ec065771615c167094eb38fb8ac19b604a0ce58a2f17296e246cf8c5cbc3f0ece2264'
                try:
                    if employee['present_kpi'] == 'active':
                        payload_msg =  {
                            "bot_id":bot_id,
                            "to": ond_id,
                            "type":"text",
                            "message": "ในการประเมินปลายปี 2562 คุณได้รับเกรด: "+ employee['gradeCompareWithPoint']+"\nคุณได้รับสิทธิ์ในการเข้าพรีเซนต์ผลงาน \nรอน้องบอทติดต่อกลับเพื่อแจ้งรายละเอียดตารางเวลาและสถานที่พรีเซนต์ผลงานภายหลังนะคะ"
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
        year = '2562'
        term = 'lateYear'
        sql_employee = """SELECT employeeid FROM `employee_kpi` WHERE validstatus= 2 AND year=%s AND term=%s AND present_kpi = 'active'"""
        cursor.execute(sql_employee,(year,term))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(),columns)
        for employee in result:
            try:
                print employee['employeeid']
                payload = {"staff_id": employee['employeeid']}
                response_onechat_id = requests.request("POST", url="http://203.151.50.47:9988/search_user_inet", json=payload, timeout=(60 * 1)).json()
                ond_id =  response_onechat_id['staff_data']['one_id']
                bot_id = "B0ff34ea97e845aa097d37a4e2c18696c"
                tokenBot = 'Bearer A2d011e83b0cc5a9ca4595ac2999ec065771615c167094eb38fb8ac19b604a0ce58a2f17296e246cf8c5cbc3f0ece2264'
                try:
                    payload_msg =  {
                        "bot_id":bot_id,
                        "to": ond_id,
                        "type":"text",
                        "message": "ในการประเมินปลายปี 2562 คุณได้รับการเข้าประเมินพรีเซนต์ผลงาน ตารางวันเวลา และสถานที่เป็นไปตาม ภาพด้านล่าง หากติดปัญหาหรือมีข้อสงสัย แจ้งกับทางhr ได้เลยค่ะ"
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
        sql_employee = """SELECT * FROM `board_kpi_v2` WHERE validstatus=1 AND year=%s AND term=%s"""
        cursor.execute(sql_employee, (data_new['year'], data_new['term']))
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(), columns)
        for employee in result:
            payload = {"staff_id": employee['employeeid_board']}
            print 'employeeid_board', employee['employeeid_board']
            response_onechat_id = requests.request(
                "POST", url="http://203.151.50.47:9988/search_user_inet", json=payload, timeout=(60 * 1)).json()
            try:
                one_id_board = response_onechat_id['staff_data']['one_id']
                print 'oneid_board', one_id_board
                bot_id = "B0ff34ea97e845aa097d37a4e2c18696c"
                tokenBot = 'Bearer A2d011e83b0cc5a9ca4595ac2999ec065771615c167094eb38fb8ac19b604a0ce58a2f17296e246cf8c5cbc3f0ece2264'
                json = {
                    "to" : one_id_board,
                    "bot_id" : bot_id,
                    "type" : "text",
                    "message" : "คุณจะได้พรีเซ้นต์ห้อง .... เวลา 2134"
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


@app.route('/api_notice_upload_present', methods=['POST'])
@connect_sql()
def api_notice_upload_present(cursor):
    try:
        sql_assessor = """SELECT * FROM `assessor_kpi` WHERE status ='active' AND type = 'main'"""
        cursor.execute(sql_assessor)
        columns = [column[0] for column in cursor.description]
        result = toJson(cursor.fetchall(), columns)

        for employee_assessor in result:
            payload = {"staff_id": employee_assessor['employeeid']}
            response_onechat_id = requests.request(
                "POST", url="http://203.151.50.47:9988/search_user_inet", json=payload, timeout=(60 * 1)).json()
            ond_id_leader = response_onechat_id['staff_data']['one_id']
            bot_id = "B0ff34ea97e845aa097d37a4e2c18696c"
            tokenBot = 'Bearer A2d011e83b0cc5a9ca4595ac2999ec065771615c167094eb38fb8ac19b604a0ce58a2f17296e246cf8c5cbc3f0ece2264'
            uuid_onechat = employee_assessor['uuid_onechat']
            quick_reply_element = []

            quick_reply_element.append({
                "label": "ตรวจสอบรายชื่อพนักงาน",
                "type": "webview",
                "url": "http://203.150.37.130/kpiupload/"+uuid_onechat,
                "size": "full"
            })

            payload_msg = {
                "to": ond_id_leader,
                "bot_id": bot_id,
                "message": "อัปโหลดสไลด์ผลงานของพนักงานใต้บังคับบัญชาที่มีสิทธิ์เข้าพรีเซนต์ \nโดยสามารถอัปโหลดได้ตั้งแต่วันนี้ จนถึง ..... \nโปรดเลือกเมนูด้านล่างเพื่ออัปโหลดสไลด์ \nหากไม่พบเมนู ลองทักน้องบอทมาใหม่นะคะ",
                "quick_reply":  quick_reply_element
            }
            response_msg = requests.request("POST", url="https://chat-public.one.th:8034/api/v1/push_quickreply",
                                            headers={'Authorization': tokenBot}, json=payload_msg, timeout=(60 * 1)).json()
        return "Success"
    except Exception as e:
        logserver(e)
        return "fail"
