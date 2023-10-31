#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time :2023/2/6 
# @Author :wsli
# @File : siemens_plc.py
# @Software: PyCharm
import snap7
import struct
from decimal import Decimal
"""
西门子plc
'PE': 0x81, #input,I
'PA': 0x82, #output,Q
'MK': 0x83, #bit memory,M
'DB': 0x84, #DB,DBX
'CT': 0x1C, #counters
'TM': 0x1D, #Timers
"""
class Bruce_siemens_plc_client():
    def __init__(self, ip: str, rack: int = 0, slot: int = 1):
        """
        连接初始化
        :param ip:
        :param rack: 通常为0
        :param slot:根据plc安装，一般为0或1
        """
        try:
            self.Client = snap7.client.Client()
            self.Client.connect(ip, rack, slot)
        except Exception as e:
            #b' TCP : Connection refused' 未连接
            #CLI: function refused by CPU 未授权
            print("e", e)

    def get_connected(self)->bool:
        """
        plc连接状态
        :return:
        """
        return self.Client.get_connected()

    def close(self):
        """
        连接关闭
        :return:
        """
        status=self.Client.disconnect()
        return status

    def read_area(self, dbnumber:int, start: int, size: int,area="DB"):
        """
        从PLC读取数据区
        有了它，您可以读取DB，输入，输出，默克，定时器和计数器
        :param dbnumber:需要读取的db编号,数据块
        :param start:开始索引
        :param size:读取字节数
        :param area:读取区域
        :return:
        """
        if area=="DB":
            area_type = snap7.types.Areas.DB
        elif area=="PE":
            area_type = snap7.types.Areas.PE
        elif area == "PA":
            area_type = snap7.types.Areas.PA
        elif area=="MK":
            area_type = snap7.types.Areas.MK
        elif area == "CT":
            area_type = snap7.types.Areas.CT
        elif area == "TM":
            area_type = snap7.types.Areas.TM
        else:
            area_type=None
        buffer=self.Client.read_area(area_type, dbnumber, start, size)
        return buffer

    def read_data_get_real(self,data:bytearray,byte_index:int=0,save_float:int=1):
        """
        获取real的值
        :param data:
        :param byte_index:
        :param save_float:保留小数点后几位
        :return:
        """
        try:
            data=snap7.util.get_real(data,byte_index)
            temp="0."
            if save_float==0:
                temp="0"
            else:
                for i in range(0,save_float):
                    temp=temp+"0"
            float_data_2=Decimal(data).quantize(Decimal(temp))
            return float_data_2
        except Exception as e:
            print(e)

    def py_data_int(self,data:bytearray)->int:
        """
        转为整数型
        :param data:
        :return:
        """
        selfInt = int.from_bytes(data, byteorder='big')
        return selfInt

    def py_data_real(self,data):
        selfReal=struct.unpack('>f',data)
        return selfReal
