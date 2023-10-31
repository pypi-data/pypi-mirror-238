#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time :2023/2/25 
# @Author :wsli
# @File : py_mat.py
# @Software: PyCharm
from matplotlib import pyplot as plt
import numpy as np


class Bruce_li_matplotlib():
    def is_ch(self,data):
        """
        检验是否含有中文字符
        :param data:
        :return:
        """
        for _char in data:
            if '\u4e00' <= _char <= '\u9fa5':
                return True
        return False

    def temp_font_setting(self,ch_type="中文黑体"):
        """
        临时更改字体设置
        :return:
        """
        ch_type_data=None
        if ch_type=="中文黑体" or ch_type=="黑体":
            ch_type_data="SimHei"
        elif ch_type=="中文楷体" or ch_type=="楷体":
            ch_type_data = "Kaiti"
        elif ch_type=="中文隶书" or ch_type=="隶书":
            ch_type_data = "LiSu"
        elif ch_type == "中文仿宋" or ch_type == "仿宋":
            ch_type_data = "FangSong"
        elif ch_type == "中文幼圆" or ch_type == "幼圆":
            ch_type_data = "FangSong"
        elif ch_type == "华文宋体":
            ch_type_data = "STSong"
        plt.rcParams["font.sans-serif"]=[ch_type_data]
        #当字体设置为中文时,负号失效
        plt.rcParams["axes.unicode_minus"] = False

    def set_title(self,title,fontsize=16.0):
        plt.title(title,fontsize=fontsize)

    def set_x(self,name,fontsize=16.0):
        plt.xlabel(name,fontsize=fontsize)

    def set_y(self,name,fontsize=16.0):
        plt.ylabel(name,fontsize=fontsize)

    def set_x_scale(self,rottation,color):
        """
        设置x轴刻度
        :param rottation: 旋转
        :param color: 颜色
        :return:
        """
        plt.xticks(rottation=rottation,color=color)

    def set_y_scale(self):
        plt.yticks()

    def legend(self):
        """
        图例（哪个线段表示的什么含义）
        :return:
        """
        pass

    def range_default_table(self,title:str="",
                            x_name:str="",
                            y_name:str="",
                            linewidth:float=2.0
                            ):
        """
        绘制线性图表
        :return:
        """
        x = np.arange(-50, 51)
        y = x ** 2

        x1 = np.arange(-50, 51)
        y1 = x ** 1
        if self.is_ch(title):
            self.temp_font_setting()

        self.set_title(title)
        #x轴名称
        self.set_x(x_name)
        #y轴名称
        self.set_y(y_name)
        #self.set_x_scale()

        # 绘制线性图表

        plt.plot(x, y,linewidth)

        # plt.plot(x1, y1, linewidth)
        plt.plot(x,label="123")
        plt.plot(x1, label="1234")
        plt.legend()
        plt.show()

cc=Bruce_li_matplotlib()
# list1={
#     "title":"",
#     "data":[
#         {
#         "x":np.arange(-50, 51),
#         "y":np.arange(-50, 51)** 2,
#         "x_name":"",
#         "x_font_size":"",
#         "y_name":"",
#         "y_font_size":"",
#         "line_width":""
#         }
#     ]
#
# }
cc.range_default_table()