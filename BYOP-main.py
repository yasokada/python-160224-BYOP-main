#!/usr/bin/env python

#--- selection of import based on the package ---
''' 1. with python3-serial'''
import serial
''' 2. without python3-serial'''
#from dummySerial import CDummySerial
#serial = CDummySerial()
#-----------------

'''
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
usleep = lambda x: time.sleep(x/1000000.0)

con1 = serial.Serial('/dev/ttyAMA0', 115200, timeout=0.1)

cmdlines = [
    "hello,1,7of9",
    "check",
    "get",
    "post,Vital,hello_Vital,0"
    ]

def main():    
    for idx in range (4):
        msg = cmdlines[idx] + "\n"
        print msg,
        con1.write(msg)
        time.sleep(5.0); # second

if __name__ == '__main__':
    main()
    con1.close()   
