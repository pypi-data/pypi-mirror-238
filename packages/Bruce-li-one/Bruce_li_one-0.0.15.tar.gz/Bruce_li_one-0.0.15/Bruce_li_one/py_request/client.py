#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time :2023/2/13 
# @Author :wsli
# @File : client.py
# @Software: PyCharm
import requests
class Bruce_requests():
    def get(self,url ,params=None, **kwargs):
        try:
            req=requests.get(url, params=params, **kwargs)
            return req.text
        except Exception as e:
            print(e)

    def post(self,url, data=None, json=None, **kwargs):
        try:
            req=requests.post(url, data=data, json=json, **kwargs)
            return req.text
        except Exception as e:
            print(e)
