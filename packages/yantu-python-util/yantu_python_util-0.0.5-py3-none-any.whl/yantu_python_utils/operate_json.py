#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunhb
# datetime： 2023/11/2 下午4:41 
# ide： PyCharm
# filename: yantu_python_utils.py
import json


def load_json(filepath: str):
    with open(filepath, "r", encoding='utf-8') as fr:
        data = json.load(fp=fr)
    fr.close()
    return data

def write_json(data: object,filepath:str):
    with open(filepath,"w",encoding='utf-8')as fw:
        json.dump(data,fp=fw,indent=4,ensure_ascii=False)
    fw.close()
