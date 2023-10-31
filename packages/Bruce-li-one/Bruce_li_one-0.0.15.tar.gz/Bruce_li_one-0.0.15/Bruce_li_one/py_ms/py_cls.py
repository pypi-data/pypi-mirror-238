#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time :2023/2/14 
# @Author :wsli
# @File : py_cls.py
# @Software: PyCharm

"""
1.Staticmethod和classmethod的区别?
"""
class A(object):
    def foo(self, x):
        #实例方法
        print(f"executing foo({self}, {x})")

    @classmethod
    def class_foo(cls, x):
        #类方法
        print(f"executing class_foo({cls}, {x})")

    @staticmethod
    def static_foo(x):
        #静态方法
        print(f"executing static_foo({x})")

a = A()
a.foo(1)
a.class_foo(1)
A.class_foo(1)
a.static_foo(1)
A.static_foo(1)

"""
2.Staticmethod和classmethod使用场景?
"""



