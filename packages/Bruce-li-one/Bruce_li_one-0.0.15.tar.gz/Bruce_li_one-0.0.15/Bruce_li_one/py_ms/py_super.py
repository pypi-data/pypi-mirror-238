#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time :2023/3/2 
# @Author :wsli
# @File : py_super.py
# @Software: PyCharm
# coding=utf-8
"""
继承关系
"""
class A(object):
    def __init__(self):
        print("class ---- A ----")
        print("a")


class B(A):
    def __init__(self):
        print("class ---- B ----")
        super(B, self).__init__()
        print("Blia")


class C(A):
    def __init__(self):
        print("class ---- C ----")
        super(C, self).__init__()
        print("CliA")


class D(B, C):
    def __init__(self):
        print("class ---- D ----")
        super(D, self).__init__()
        print("Dl")


d = D()
print(D.__mro__)
'''
#输出结果：
class ---- D ----
class ---- B ----
class ---- C ----
class ---- A ----
'''


