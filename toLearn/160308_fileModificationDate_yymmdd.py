import os.path
import time

filepath = "/home/pi/BYOP/send.txt"
mddt = time.ctime(os.path.getmtime(filepath))
print mddt
parsed = time.strptime(mddt)
yymmdd = time.strftime("%Y%m%d", parsed)
print yymmdd

