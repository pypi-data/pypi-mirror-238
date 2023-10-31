#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time :2023/3/2 
# @Author :wsli
# @File : py_super_2.py
# @Software: PyCharm
"""
继承父类方法
"""
class Tree:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def grow(self):
        print("{} tree is growing...now it's {} years old".format(self.name, self.age))

    def seed(self):
        print("{} tree is seeding...".format(self.name))


class Apple(Tree):
    """docstring for ClassName"""

    def __init__(self, name, age, color):
        super().__init__(name, age)
        self.color = color

    def price(self):
        print("One {} tree is 100 dollars".format(self.name))


class Pear(Tree):
    """docstring for ClassName"""

    def __init__(self, name, age, color):
        super().__init__(name, age)
        self.color = color

    def price(self):
        print("One {} {} tree is 80 dollars".format(self.color, self.name))

    def grow(self):
        # 重写父类的方法grow生长
        print("it was {} years old,now it is {} years old".format(self.age, int(self.age) + 1))
class orange(Tree):
    def grow(self):
		#调用父类Tree的方法grow
		super().grow()
		#直接调用Tree类的方法
		Tree('Apple','16').grow()
		#重写父类方法grow
		print("{} tree has changed...".format(self.name))

if __name__ == '__main__':
    a = Apple('White Apple', 8, 'white')
    a.grow()
    a.seed()
    a.price()
    b = Pear('Pear', 8, 'red')
    b.price()
    b.grow()
