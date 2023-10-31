#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time :2023/2/13 
# @Author :wsli
# @File : py_win.py
# @Software: PyCharm
import win32con
import win32api
import winreg
import os

class Bruce_win():

    def get_registry(self,
                     key_name,
                     reg_root=win32con.HKEY_CURRENT_USER,
                     reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"):
        """
        获取开机启动项
        :param key_name:
        :param reg_root:
        :param reg_path:
        :return:
        """
        reg_flags = win32con.WRITE_OWNER | win32con.KEY_WOW64_64KEY | win32con.KEY_ALL_ACCESS
        try:
            key = winreg.OpenKey(reg_root, reg_path, 0, reg_flags)
            location, type = winreg.QueryValueEx(key, key_name)
            print("键存在", "location（数据）:", location, "type:", type)
            feedback = 0
        except FileNotFoundError as e:
            print("键不存在", e)
            feedback = 1
        except PermissionError as e:
            print("权限不足", e)
            feedback = 2
        except Exception as e:
            print("Error",e)
            feedback = 3
        return feedback

    def autoRun(self,switch="open",  # 开：open # 关：close
                zdynames=None,
                current_file=None,
                abspath=os.path.abspath(os.path.dirname(__file__))):
        """
        :param switch: 注册表开启、关闭自启动
        :param zdynames: 当前文件名 test.py
        :param current_file: 获得文件名的前部分test
        :param abspath: 当前文件路径  D:\
        :return:
        """
        #print(zdynames)

        path = abspath + '\\' + zdynames  # 要添加的exe完整路径如：
        judge_key = self.get_registry(reg_root=win32con.HKEY_CURRENT_USER,
                              reg_path=r"Software\Microsoft\Windows\CurrentVersion\Run",  # 键的路径
                              key_name=current_file)
        # 注册表项名
        KeyName = r'Software\Microsoft\Windows\CurrentVersion\Run'
        key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, KeyName, 0, win32con.KEY_ALL_ACCESS)
        if switch == "open":
            # 异常处理
            try:
                if judge_key == 0:
                    print("已经开启了，无需再开启")
                elif judge_key == 1:
                    win32api.RegSetValueEx(key, current_file, 0, win32con.REG_SZ, path)
                    win32api.RegCloseKey(key)
                    print('开机自启动添加成功！')
            except:
                print('添加失败')
        elif switch == "close":
            try:
                if judge_key == 0:
                    win32api.RegDeleteValue(key, current_file)  # 删除值
                    win32api.RegCloseKey(key)
                    print('成功删除键！')
                elif judge_key == 1:
                    print("键不存在")
                elif judge_key == 2:
                    print("权限不足")
                else:
                    print("出现错误")
            except:
                print('删除失败')



