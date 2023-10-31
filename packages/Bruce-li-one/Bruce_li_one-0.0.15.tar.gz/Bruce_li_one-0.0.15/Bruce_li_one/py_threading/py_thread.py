#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time :2023/2/13 
# @Author :wsli
# @File : py_thread.py
# @Software: PyCharm
import inspect
import ctypes
import threading
import time

class Bruce_threading():
    def __init__(self,Thread_list:list,stop_time:int=-1):
        """
        初始化
        :param Thread_list:
        :param stop_time: 休眠多少秒停止所有线程运行
        """
        #线程列表
        self.Thread=Thread_list
        self._append_stop(stop_time)
    def start(self):
        """
        开启所有线程
        :return:
        """
        for i in self.Thread:
            i.setDaemon(True)
            i.start()
        for i in self.Thread:
            i.join()

    def _async_raise(self,tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")
    def _append_stop(self,sleep_time):
        if sleep_time !=-1:
            t1=threading.Thread(target=self.stop_thread,args=(self.Thread,sleep_time,))
            self.Thread.append(t1)
    def stop_thread(self,thread_list,sleep_time):
        """
        停止线程运行
        :param thread:
        :return:
        """
        time.sleep(sleep_time)
        for thread in thread_list:
            try:
                self._async_raise(thread.ident, SystemExit)
            except Exception as e:
                print(e)

