# -*- coding: utf-8 -*-
"""
-------------------------------------------------
@ Author ：Ywx
@ Date ： 2024/5/25 
@ Project_Name : LLM
@ Description：
-------------------------------------------------
"""
import os.path
import json
from langchain_community.tools.tavily_search import TavilySearchResults
"""
    1.写文件
    2.读文件
    3.追加写
    4.网络搜索
"""
# 获取根目录
def _get_workdir_root():
    workdir_root = os.environ.get("WORKDIR_ROOT", '\\llm_result')
    return workdir_root

WORKDIR_ROOT = "D:\Develop\LLM\Agent\data" + _get_workdir_root()

# 读文件
def read_file(filename):
    filename = os.path.join(WORKDIR_ROOT, filename)
    if not os.path.exists(filename):
        return f"{filename} not exist, please check file"
    with open(filename, "r") as f:
        return "\n".join(f.readlines())

# 追加文件
def append_to_file(filename, content):
    filename = os.path.join(WORKDIR_ROOT, filename)
    if not os.path.exists(filename):
        return f"{filename} not exist, please check file"
    with open(filename, "a") as f:
        f.write(content)
    return "append success"

# 写文件
def write_to_file(filename, content):
    filename = os.path.join(WORKDIR_ROOT, filename)
    if not os.path.exists(WORKDIR_ROOT):
        os.makedirs(WORKDIR_ROOT)

    with open(filename, "a") as f:
        f.write(content)
    return "write success"

# 搜索功能
def search(query):
    tavily = TavilySearchResults(max_results=5)
    try:
        ret = tavily.invoke(input=query)
        content_list = [obj['content'] for obj in ret]
        return "\n".join(content_list)
    except Exception as err:
        return "search err:{}".format(err)

tools_info = [
    {
        "name": "append_to_file",
        "description": "append llm content to file ",
        "args": [{
            "name": "filename",
            "type": "string",
            "description": "append file name"
        }, {
            "name": "content",
            "type": "string",
            "description": "append to file content"
        }]
    },
    {
        "name": "read_file",
        "description": "read file from agent generate, should write file before read",
        "args": [{
            "name": "filename",
            "type": "string",
            "description": "append file name"
        }]
    },
    {
        "name": "write_to_file",
        "description": "write llm content to file ",
        "args": [{
            "name": "filename",
            "type": "string",
            "description": "write file name"
        }, {
            "name": "content",
            "type": "string",
            "description": "write to file content"
        }]
    },
    {
        "name": "finish",
        "description": "完成用户目标",
        "args": [{
            "name": "answer",
            "type": "string",
            "description": "the goal's final answer"
        }, {
            "name": "content",
            "type": "string",
            "description": "最后的目标结果"
        }]
    },
    # {
    #     "name": "search",
    #     "description": "this is a search engine, you can gain additional knowledge through this search engine when you are "
    #                    "unsure of what large model return",
    #     "args": [{
    #         "name": "query",
    #         "type": "string",
    #         "description": "search query to look up"
    #     }]
    # }
]


tools_map = {
    "read_file": read_file,
    "append_to_file": append_to_file,
    "write_to_file": write_to_file,
    "search": search
}


def gen_tools_desc():
    tools_desc = []
    for idx, t in enumerate(tools_info):
        args_desc = []
        for info in t['args']:
            args_desc.append({
                "name": info["name"],
                "description": info["description"],
                "type": info["type"]
            })
        args_desc = json.dumps(args_desc, ensure_ascii=False)
        tool_desc = f"{idx+1}. {t['name']}:{t['description']},args:{args_desc}"
        tools_desc.append(tool_desc)
    tools_prompt = "\n".join(tools_desc)
    return tools_prompt