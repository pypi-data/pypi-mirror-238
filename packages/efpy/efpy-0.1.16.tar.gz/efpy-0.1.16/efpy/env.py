'''TefPy.env
=====

TefPy.env是用于维护Python实验脚本环境的辅助函数集。该包包含如下函数：
1. 数printResult用于执行将Python实验的结果使用Json在控制台打印输出。
2. 函数getParams自动获取控制台调用时输入的参数信息。
3. 函数isExpEnv判断是否是实验框架调用的环境。
'''
import sys
import json
import threading
import time

isTimeThdAlive = True


def printResult(obj):
    '''函数printResult用于执行将Python实验的结果使用Json在控制台打印输出，该输出的结果将自动被实验框架解析。注意：如果自己输出的结果不按照规定格式，实验框架无法解析。
    参数如下：
    第一个参数obj: 以字典（dict）存储的实验结果或者实验结果的Json字符串'''
    if isinstance(obj, str):
        res = obj;
    else:
        res = json.dumps(obj);
    print('==>**ResultJson**<==');
    print(res);
    print('==>**End**<==');


def getParams():
    '''函数getParams自动获取控制台调用时输入的参数信息。
    返回结果如下：
    以字典（dict）存储的参数数据'''
    inputJson = sys.argv[1];
    res = json.loads(inputJson);
    return res;


def isExpEnv():
    '''函数isExpEnv判断是否是实验框架调用的环境，是的话返回True。
    只有实验框架调用的环境才能执行printResult和getParams'''
    res = True;
    try:
        json.loads(sys.argv[1]);
    except:
        res = False;
    return res;


def timed_output():
    interval = 60  # 输出间隔（秒）
    minute = 0
    while True:
        time.sleep(interval)
        if not isTimeThdAlive:
            break
        minute += 1
        if minute >= 60:
            h = minute // 60
            m = minute % 60
            if m > 0:
                print(f"The experiment has been running for {h} hour(s) and {minute % 60} minute(s).\n", end='')
            else:
                print(f"The experiment has been running for {h} hour(s).\n", end='')
        else:
            print(f"The experiment has been running for {minute} minute(s).\n", end='')

def startTimeThd():
    '''函数startTimeThd启动一个计时守护线程，每1分钟输出一次，以确保实验任务仍在执行。'''
    global isTimeThdAlive
    isTimeThdAlive = True
    time_thd = threading.Thread(target=timed_output, daemon=True)
    time_thd.start()

def stopTimeThd():
    '''函数stopTimeThd停止所有计时守护线程。'''
    global isTimeThdAlive
    isTimeThdAlive = False

startTimeThd()