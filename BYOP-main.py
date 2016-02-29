#!/usr/bin/env python

#--- selection of import based on the package ---
''' 1. with python3-serial'''
import serial
''' 2. without python3-serial'''
#from dummySerial import CDummySerial
#serial = CDummySerial()
#-----------------

'''
v0.8 2016 Feb. 29
  - add append_rcvdtext()
v0.7 2016 Feb. 29
  - add comm_bye()
  - add comm_hello()
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
    debug_outputDebugString("read_name","Line49 > start")
    srcpath="/home/pi/BYOP/name.txt"

    if os.path.isfile(srcpath) == False:
        debug_outputDebugString("read_name","Line53 > name.txt not found");
        return
    with open(srcpath,"r") as nmfd:
        mynm = nmfd.read()
        debug_outputDebugString("read_name","Line63 > name:" + mynm)
    return mynm

def append_rcvdtext(appends):
    debug_outputDebugString("append_rcvdtext","Line82 > start")
    srcpath="/home/pi/BYOP/rcvd.txt"

    debug_outputDebugString("append_rcvdtext","Line85 > " + appends)

    wrlines = ""
    if os.path.isfile(srcpath):
        rdfd = open(srcpath)
        wrlines = rdfd.readlines()
        rdfd.close()

    wrfd = open(srcpath, "w")
    wrfd.writelines(wrlines)
    wrfd.writelines(appends)
    wrfd.close()

    debug_outputDebugString("append_rcvdtext","Line101 > fin")
    

def comm_post(sends, dstcon):
    for line in sends:
        if "//" in line:
            continue
        msg="post," + line
        print msg,
        con1.write(msg)
        time.sleep(5.0) # second

def comm_hello(name,dstcon):
    msg="hello,1," + name # TODO: 0m > serial number > not 1
    debug_outputDebugString("comm_hello",msg)
    dstcon.write(msg)
    time.sleep(5.0) # second

def comm_bye(dstcon):
    msg="bye\n"
    debug_outputDebugString("comm_bye",msg)
    print msg
    dstcon.write(msg)
    time.sleep(5.0) # second
    
def main():
    myname = read_name()
    comm_hello(myname, con1)

    tomsg = "1stline\n"
    tomsg = tomsg + "2ndline\n"
    tomsg = tomsg + "3rdline\n"    
    append_rcvdtext(tomsg)
    
    sends = read_sendtext()
    comm_post(sends,con1)

    comm_bye(con1)

'''    
    for idx in range (8):
        msg = cmdlines[idx] + "\n"
        print msg,
        con1.write(msg)
        time.sleep(5.0); # second
'''        

if __name__ == '__main__':
    main()
    con1.close()   
