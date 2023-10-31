#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time :2023/3/8 
# @Author :wsli
# @File : mitsubishi_plc.py
# @Software: PyCharm
"""
输入继电器："X100","X1A0"            // 字符串为十六进制机制
输出继电器："Y100" ,"Y1A0"           // 字符串为十六进制机制
内部继电器："M100","M200"           // 字符串为十进制
锁存继电器："L100"  ,"L200"           // 字符串为十进制
报警器：   "F100", "F200"            // 字符串为十进制
边沿继电器："V100" , "V200"          // 字符串为十进制
链接继电器："B100" , "B1A0"          // 字符串为十六进制
步进继电器："S100" , "S200"          // 字符串为十进制
数据寄存器："D100", "D200"           // 字符串为十进制
链接寄存器："W100" ,"W1A0"         // 字符串为十六进制
文件寄存器："R100","R200"            // 字符串为十进制
"""
from pymelsec import Type3E, Type4E
from pymelsec.constants import DT
class Bruce_mitsubishi_plc_client(Type4E):
    def __init__(self,ip,port=5002,plc_type="Q"):
        """
        初始化三菱plc通信对象
        :param ip:
        :param port:5002-5007
        :param return_data_type: Q or
        """
        super(Bruce_mitsubishi_plc_client, self).__init__(host=ip,port=port,plc_type='Q')



    def do_connect(self):
        """
        连接
        :return:
        """
        pass

    def close(self):
        """
        关闭
        :return:
        """
        pass

    # def read(self):
    #     pass
    #
    # def write(self):
    #     pass

    def auto_close(self,address,length,data_type):
        with Type4E(host='',port=1,plc_type='') as plc:
            plc.set_access_opt(comm_type="binary")
            read_result=plc.batch_read(
                ref_device='',
                read_size=5,
                data_type=''
            )
            print(read_result)


