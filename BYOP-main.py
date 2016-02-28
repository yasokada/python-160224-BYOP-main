#!/usr/bin/env python

#--- selection of import based on the package ---
''' 1. with python3-serial'''
import serial
''' 2. without python3-serial'''
#from dummySerial import CDummySerial
#serial = CDummySerial()
#-----------------

'''
v0.5 2016 Feb. 29
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

def read_name():
    debug_outputDebugString("read_name","Line49 > start")
    
def main():
    read_name()
    
    for idx in range (8):
        msg = cmdlines[idx] + "\n"
        print msg,
        con1.write(msg)
        time.sleep(5.0); # second

if __name__ == '__main__':
    main()
    con1.close()   
