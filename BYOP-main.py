#!/usr/bin/env python

#--- selection of import based on the package ---
''' 1. with python3-serial'''
import serial
''' 2. without python3-serial'''
#from dummySerial import CDummySerial
#serial = CDummySerial()
#-----------------

'''
v0.14 2016 Mar. 10
  - if NoneType in Main() before comm_post()
  - fix bug > read_fileModificationDate_sendText() > file not found
  - comm_get() reads [modiDate]
v0.13 2016 Mar. 10
  - add string_removeCRLF()
  - comm_post() takes [modiDate] arg
  - add read_fileModificationDate()
v0.12 2016 Mar. 7
  - impl proc_storage() to show storage usage
v0.11 2016 Mar. 7
  - impl proc_get()
      + return received strings to appened to [rcvd.txt]
      + get sender name
v0.10 2016 Mar. 3
  - add comm_get() in progress
  - update comm_hello() to take [mySrl(Serial)] parameter 
  - update comm_check()
v0.9 2016 Mar. 2
  - add trim_mySerial()
  - add read_mySerial()
v0.8 2016 Mar. 1
  - add Test_extractCsvRow()
  - add extractCsvRow()
  - add comm_check()
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

def string_removeCRLF(srcstr):
    return srcstr.rstrip()

def read_fileModificationDate_sendText():
    srcpath="/home/pi/BYOP/send.txt"    
    if os.path.isfile(srcpath) == False:
        return ""
    mddt = time.ctime(os.path.getmtime(srcpath))
    parsed = time.strptime(mddt)
    yyyymmdd = time.strftime("%Y%m%d", parsed)
    return yyyymmdd

def read_sendtext():
#    debug_outputDebugString("read_sendtext","Line52 > start")
    srcpath="/home/pi/BYOP/send.txt"

    if os.path.isfile(srcpath) == False:
#        debug_outputDebugString("read_sendtext","Line55 > send.txt not found");
        return
    rdfd = open(srcpath)
    lines = rdfd.readlines()
    rdfd.close()

#    debug_outputDebugString("read_sendtext","Line80 > lines:" + str(lines))

    return lines

def read_name():
#    debug_outputDebugString("read_name","Line49 > start")
    srcpath="/home/pi/BYOP/name.txt"

    if os.path.isfile(srcpath) == False:
        debug_outputDebugString("read_name","Line53 > name.txt not found");
        return
    with open(srcpath,"r") as nmfd:
        mynm = nmfd.read()
#        debug_outputDebugString("read_name","Line63 > name:" + mynm)
    return mynm

def append_rcvdtext(appends):
#    debug_outputDebugString("append_rcvdtext","Line82 > start")
    srcpath="/home/pi/BYOP/rcvd.txt"

    debug_outputDebugString("append_rcvdtext","Line85 > " + appends)

    orglines = ""
    if os.path.isfile(srcpath):
        rdfd = open(srcpath)
        orglines = rdfd.readlines()
        rdfd.close()

    wrfd = open(srcpath, "w")
    wrfd.writelines(orglines)
    wrfd.writelines(appends)
    wrfd.close()

#    debug_outputDebugString("append_rcvdtext","Line101 > fin")

def read_mySerial():
#    debug_outputDebugString("read_mySerial","Line105 > start")
    srcpath="/proc/cpuinfo"
    if os.path.isfile(srcpath) == False:
        debug_outputDebugString("read_mySerial","Line107 > no cpuinfo")
        return
    rdfd = open(srcpath)
    lines = rdfd.readlines()
    rdfd.close()
    mySerial = ""
    for line in lines:
        if "Serial" in line:
            items = line.split(" ")
            mySerial = items[1]
#            print line
    return mySerial

def trim_mySerial(mySrl):
    # use only three in order not to disclose information related to security
    return mySrl[13:-1]

def comm_post(sends, modiDate, dstcom):
    for line in sends:
        if "//" in line:
            continue
        line = string_removeCRLF(line)
        msg = "post," + line
        msg = msg + "," + modiDate + "\n"
#        print msg,
        debug_outputDebugString("comm_post","Line162 >" + msg)
        dstcom.write(msg)
        rcvd = dstcom.readline()
        time.sleep(5.0) # second

def comm_check(dstcom):
#    debug_outputDebugString("comm_check","Line112 > start")
    cmd="check\n"
    dstcom.write(cmd)
    rcvd = dstcom.readline()
    debug_outputDebugString("comm_check","Line119 >" + rcvd)
    if len(rcvd) == 0:
        return 0
    nummsg = extractCsvRow(rcvd, 1) # rcvd:[check,3\n]
    time.sleep(5.0) # second
    return int(nummsg)

def comm_storage(dstcom):
    cmd="storage\n"
    dstcom.write(cmd)
    rcvd = dstcom.readline()
    debug_outputDebugString("comm_storage","Line164 >" + rcvd)
    if len(rcvd) == 0:
        return

def comm_get(nummsg, dstcom):
#    debug_outputDebugString("comm_get","Line152 > start")
    retstr = ""
    for loop in range(nummsg):
        cmd = "get\n"
        dstcom.write(cmd)
        time.sleep(2.0) #second (for message station to show [sender] on LCD)

        rcvd = dstcom.readline()
        rcvd = rcvd.rstrip() # to remove <LF>
        if len(rcvd) == 0:
            continue
        sndr = extractCsvRow(rcvd, 1)
        msg = extractCsvRow(rcvd, 2)
        scrt = extractCsvRow(rcvd, 3)
        modidt = extractCsvRow(rcvd, 4)
#        debug_outputDebugString("comm_get","Line166 > sender:" + sndr)
#        debug_outputDebugString("comm_get","Line167 > message:" + msg)
#        debug_outputDebugString("comm_get","Line168 > secret:" + scrt)
        time.sleep(5.0) # second

        # TODO: 0c > add timestamp of the message post
        retstr = retstr + sndr + "," + msg + "," + scrt
        retstr = retstr + "," + modidt + "\n"
    return retstr


def comm_hello(name, mySrl, dstcom):
    msg="hello," + mySrl + "," + name
    debug_outputDebugString("comm_hello",msg)
    dstcom.write(msg)
    rcvd = dstcom.readline() # TODO: 0m > check when ESP8266 is not connected
    time.sleep(5.0) # second

def comm_bye(dstcom):
    msg="bye\n"
    debug_outputDebugString("comm_bye",msg)
    print msg
    dstcom.write(msg)
    rcvd = dstcom.readline()
    time.sleep(5.0) # second

def extractCsvRow(csvline, getIdx):
    lines = csvline.split(",")
    if getIdx >= len(lines):
        return ""
    return lines[getIdx]

def Test_extractCsvRow():
    csvline="AAA,BBB,CCC"
    print extractCsvRow(csvline, 0)
    print extractCsvRow(csvline, 2)
    print extractCsvRow(csvline, 4)    
    
def main():
#    Test_extractCsvRow()

    # read serial
    mySerial = read_mySerial()
    mySerial = trim_mySerial(mySerial)
#    debug_outputDebugString("main","Line175 > Serial:" + mySerial)
    
    # hello
    myname = read_name()
    comm_hello(myname, mySerial, con1)

    # check number of messages to receive
    nummsg = comm_check(con1)
#    debug_outputDebugString("main","Line194 > check:" + str(nummsg))

    # get message
    tomsg = comm_get(nummsg, con1)
    debug_outputDebugString("main","Line225 > comm_get:" + tomsg)     
    append_rcvdtext(tomsg)

    # post message
    sends = read_sendtext()
    if sends != None:
        modiDate = read_fileModificationDate_sendText()
        debug_outputDebugString("main","Line255 > modiDate:" + modiDate)     
        comm_post(sends, modiDate, con1)

    # if 1
    nummsg = comm_check(con1)

    # TODO: 0m > add proc_storage()

    # bye
    comm_bye(con1)

    # check storage
    comm_storage(con1)

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
