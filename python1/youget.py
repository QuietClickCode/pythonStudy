import _thread
import os
import time

# 为线程定义一个函数
def print_time( threadName, delay):
    os.system('you-get -o E:/hadoopvideo/ --format=flv360 https://www.bilibili.com/video/av15390641?p=' + str(delay))
    print ("%s: %s" % ( threadName, time.ctime(time.time()) ))

# 创建两个线程
try:
    for i in range(12,72):
        time.sleep(3)
        _thread.start_new_thread( print_time, ("Thread-"+str(i), i, ) )
except:
    print ("Error: 无法启动线程")

while 1:
    pass