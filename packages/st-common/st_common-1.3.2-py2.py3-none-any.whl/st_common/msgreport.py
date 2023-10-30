import requests
import json
import traceback
### time costs
from functools import wraps
def ISZ_main_exception_report_args(msg):
    def main_exception_report(function):
        @wraps(function)
        def function_main_exception_report(*args, **kwargs):
            try:
                person_msgreport = ISZMsgReport(webhook="http://192.168.6.241:5008/ding/sendByMembers")
                baselogger = function(*args, **kwargs)
            except Exception as e:
                person_msgreport.chatbot_text(title=f"{msg}",content=f"{msg}:<br>{e}<br><br>{traceback.format_exc()}")
            else:
                ### 原始
                # # 通过遍历handlers列表来找到名为'counting_handler'的handler
                # for handler in baselogger.logger.handlers:
                #     if handler.get_name() == 'counting_handler':
                #         if handler.error_count == 0 and handler.warning_count == 0:
                #             ## 无需通知
                #             None
                #         else:
                #             content = f"Run pass But have something : Error:{handler.error_count},Error_message:{handler.error_messages}; Warning:{handler.warning_count},Warning_message:{handler.warning_messages}"
                #             person_msgreport.chatbot_text(title=f"Run pass",content=content)
                
                """
                检查是否存在名为'counting_handler'且错误计数或警告计数不为零的处理程序，如果存在，则生成相应的消息并发送。
                第二个版本使得一旦找到符合条件的处理程序就立即停止搜索，对于大量处理程序的情况可能更有效率。
                """
                ### 版本一
                # content = "\n".join(
                #     f"Run pass But have something : Error:{handler.error_count},Error_message:{handler.error_messages}; Warning:{handler.warning_count},Warning_message:{handler.warning_messages}" 
                #     for handler in baselogger.logger.handlers 
                #     if handler.get_name() == 'counting_handler' and (handler.error_count != 0 or handler.warning_count != 0)
                # )
                # if content:
                #     person_msgreport.chatbot_text(title=f"Run pass", content=content)

                ### 版本二
                handler = next((h for h in baselogger.logger.handlers if h.get_name() == 'counting_handler'), None)
                if handler and (handler.error_count != 0 or handler.warning_count != 0):
                    content = f"Run pass But have something : Error:{handler.error_count},Error_message:{handler.error_messages}; Warning:{handler.warning_count},Warning_message:{handler.warning_messages}"
                    person_msgreport.chatbot_text(title=f"Run pass", content=content)
            return None
        return function_main_exception_report
    return main_exception_report

class ISZMsgReport():
    def __init__(self,webhook) -> None:
        self.webhook = webhook
        pass
    def chatbot_text(self, code="ipd", touser:list = ["011222671211-1181533439"], title:str = None, 
                     content:str = None,content_type="sampleMarkdown"):
        """
        Description:
            ISZ chatbot send message to user persions 
        Args:
            code (str): robot code 
            touser (list): users_id
            title (str): message title
            content (str): message content
            content_type (str): [sampleText/sampleMarkdown] message content_type
        Returns:
            reponse: api repose
        Example:
            
        Raises:
            Exception: error
        """
        pass
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            "code": code,
            "userIds": 
                touser
            ,
            "content": content,
            "title": title,
            "type":content_type
        }
        result = requests.post(self.webhook, json=data, headers=headers)
        return result
    
    def send_group_markdown(self,code = "weatherReport", conversation_id = "cidR59tfQt2vstqR25R2nW0PA==", content = None, title = None):
        payload = json.dumps({
            "code": code,
            "conversationId": conversation_id,
            "content": content,
            "title": title
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", self.webhook, headers=headers, data=payload)
        return response
