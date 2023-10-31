#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time :2023/3/2 
# @Author :wsli
# @File : py_new_init.py
# @Software: PyCharm
"""
python中__new__和__init__的区别?
1.__new__是在实例创建之前被调用的，用于创建实例，然后返回该实例对象，是个静态方法。
2.__init__是当实例对象创建完成后被调用的，用于初始化一个类实例，是个实例方法
注意事项：

1.如果__new__没有返回cls(即当前类)的实例，那么当前类的__init__方法是不会被调用的；
"""
class A():
    def __new__(cls, *args, **kwargs):
        print('this is A __new__')
        # return super(A, cls).__new__(cls)  # 或者下面这种形式，两种都可
        return object.__new__(cls)

    def __init__(self, title):
        print('this is A __init__')
        self.title = title


a = A('python book')
"""
__new__和__init__使用场景
"""