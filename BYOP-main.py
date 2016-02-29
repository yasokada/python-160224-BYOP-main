#!/usr/bin/env python

#--- selection of import based on the package ---
''' 1. with python3-serial'''
import serial
''' 2. without python3-serial'''
#from dummySerial import CDummySerial
#serial = CDummySerial()
#-----------------

'''
v0.6 2016 Feb. 29
  - add comm_post()
  - add read_sendtext()
v0.5 2016 Feb. 29
  - add read_name()
  - add debug_outputDebugString()
v0.4 2016 Feb. 24
  - add contact by Vital
v0.3 2016 Feb. 24
  - group_run commands
      + hello
      + check
      + get
      + post
v0.2 2016 Feb. 24
  - add serial print
v0.1 2016 Feb. 24
  - just hello
'''

import time
import os.path
usleep = lambda x: time.sleep(x/1000000.0)
s_name = "WHO_AM_I"

con1 = serial.Serial('/dev/ttyAMA0', 115200, timeout=0.1)

cmdlines = [
    "hello,1,7of9",
    "check",
    "get",
    "post,Vital,hello_Vital,0",
    "hello,2,Vital",
    "check",
    "get",
    "post,7of9,hello_7of9,0"
    ]

def debug_outputDebugString(prfx, msg):
    print "[DEBUG]" + prfx + "," + msg

def read_sendtext():
#    debug_outputDebugString("read_sendtext","Line52 > start")
    srcpath="/home/pi/BYOP/send.txt"

    if os.path.isfile(srcpath) == False:
#        debug_outputDebugString("read_sendtext","Line55 > send.txt not found");
        return
    rdfd = open(srcpath)
    lines = rdfd.readlines()
    rdfd.close()

    return lines

def read_name():
#    debug_outputDebugString("read_name","Line49 > start")
    srcpath="/home/pi/BYOP/name.txt"

    if os.path.isfile(srcpath) == False:
#        debug_outputDebugString("read_name","Line53 > name.txt not found");
        return
    with open(srcpath,"r") as nmfd:
        s_name = nmfd.read()
        debug_outputDebugString("read_name","Line63 > name:" + s_name)

def comm_post(sends, dstcon):
    for line in sends:
        if "//" in line:
            continue
        msg="post," + line
        print msg,
        con1.write(msg)
        time.sleep(5.0) # second
    
def main():
    read_name()
    sends = read_sendtext()
    comm_post(sends,con1)
    
    for idx in range (8):
        msg = cmdlines[idx] + "\n"
        print msg,
        con1.write(msg)
        time.sleep(5.0); # second

if __name__ == '__main__':
    main()
    con1.close()   
