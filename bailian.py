# -*- coding: utf-8 -*-
"""
-------------------------------------------------
@ Author ：Ywx
@ Date ： 2024/5/25 
@ Project_Name : LLM
@ Description：
-------------------------------------------------
"""

# 业务空间模型调用请参考文档传入workspace信息: https://help.aliyun.com/document_detail/2746874.html
import os
import random
from http import HTTPStatus
from dashscope import Generation
from dotenv import load_dotenv

load_dotenv()
# os.environ["DASHSCOPE_API_KEY"] = "api_key"

api_key = os.environ.get("DASHSCOPE_API_KEY")

def call_stream_with_messages():
    messages = [
        {'role': 'user', 'content': '用萝卜、土豆、茄子做饭，给我个菜谱'}]
    responses = Generation.call(
        'qwen1.5-110b-chat',
        messages=messages,
        seed=random.randint(1, 10000),  # set the random seed, optional, default to 1234 if not set
        result_format='message',  # set the result to be "message"  format.
        stream=True,
        output_in_full=True,  # get streaming output incrementally
        api_key=api_key
    )
    full_content = ''
    for response in responses:
        if response.status_code == HTTPStatus.OK:
            full_content += response.output.choices[0]['message']['content']
            print(response)
        else:
            print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            ))
    print('Full content: \n' + full_content)


if __name__ == '__main__':
    call_stream_with_messages()