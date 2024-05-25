# -*- coding: utf-8 -*-
"""
-------------------------------------------------
@ Author ：Ywx
@ Date ： 2024/5/25 
@ Project_Name : LLM
@ Description：
-------------------------------------------------
"""

# agent入口

# 环境变量
"""
TODO：
    1.加载环境变量
    2.工具的引入
    3.prompt模板
    4.模型的初始化，封装和调用
"""

import time
from tools import tools_map
from prompt import gen_prompt, user_prompt
from model_provider import ModelProvider


mp = ModelProvider()

def parse_thoughts(response):
    try:
        thoughts = response.get("thoughts")
        plan = thoughts.get("plan")
        criticism = thoughts.get("criticism")
        reasoning = thoughts.get("reasoning")
        observation = thoughts.get("speak")
        prompt = f"plan:{plan} \n reasoning:{reasoning} \n criticism:{criticism} \n observation:{observation}"
        return prompt
    except Exception as err:
        print("parse thought error")
        return "".format(err)


def agent_execute(query, max_request_time):
    current_request_time = 0
    chat_history = []
    agent_scratch = ''

    while current_request_time < max_request_time:
        current_request_time += 1
        """
        如果达到预期直接返回
        """
        prompt = gen_prompt(query, agent_scratch)
        start_time = time.time()
        print("************{}.开始调用模型".format(current_request_time),flush=True)
        # call llm
        """
            sys_prompt
            user_msg
            assistant_msg
            history
        """
        response = mp.chat(prompt, chat_history)

        end_time = time.time()
        print("************{}.调用模型结束，耗时:{}".format(current_request_time,end_time-start_time), flush=True)

        if not response or not isinstance(response, dict):
            print("调用LLM出错，即将重试", response)
            continue
        """
        response的格式：
            {
                "action"{
                    "name": "action_name"
                    "args":{
                        "args name": "args value"
                    }
                }
                "thoughts":
                {
                    "text": "thought",
                    "plan": "plan",
                    "criticism": "criticism",
                    "speak": "返回给用户的总结"
                    "reasoning": ""
                }
            }
        """
        action_info = response.get("action")
        action_name = action_info.get('name')
        action_args = action_info.get('args')
        print("当前action name:", action_name, action_args)
        if action_name == "finish":
            final_answer = action_args.get("answer")
            print("final_answer:", final_answer)
            break
        observation = response.get("thoughts").get("speak")
        try:
            """
                action_name -> func的映射，通过map实现
                map->{action_name,func}
            """
            func = tools_map.get(action_name)
            observation = func(**action_args)

        except Exception as err:
            print("调用工具异常:", err)

        agent_scratch = agent_scratch + "\n" + observation
        assistant_msg = parse_thoughts(response)
        chat_history.append([user_prompt, assistant_msg])

    if current_request_time == max_request_time:
        print("本次任务失败")
    else:
        print("恭喜你，任务完成")


def main():
    max_request_time = 10
    # 与用户交互
    while True:
        query = input("请输入您的目标:")
        if query == "exit":
            return
        agent_execute(query, max_request_time=max_request_time)


if __name__ == "__main__":
    main()