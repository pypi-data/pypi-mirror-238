#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time :2023/3/2 
# @Author :wsli
# @File : py_str_repr.py
# @Software: PyCharm
'''
python中 str 和 repr_python repr()与str()区别总结?
str() 的输出追求明确性和可读性，输出格式要便于理解，适合用于输出内容到用户终端。
repr() 的输出追求明确性，除了对象内容，还需要展示出对象的数据类型信息，适合开发和调试阶段使用。
'''


class TestClass:
    def __init__(self, name, age):
        self.name = name
        self.age = age


    def __repr__(self):
        return 'repr: ' + self.name + ' ,' + self.age

    def __str__(self):
        return self.name + ' ,' + self.age




tt = TestClass('tony', '23')
print(str(tt))
print(repr(tt))