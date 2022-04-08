# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import serial
import time
#import matplotlib.pyplot as plt
#import msvcrt
import numpy as np
from datetime import datetime

s = serial.Serial(
    port="/dev/ttyUSB0", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
)
s.write(str.encode("AT"))
data=[]
state=0
x1=0
x2=0
done=True
Num=0
start = datetime.now()
while (Num < 5000):
    res = s.read(1)
    if (state==0): 
        if (res==b'\xaa'):
            state=1
    elif (state==1): 
        if (res==b'\xfa'):
            state=2
    elif (state==2):
        x1=int.from_bytes(res,"little")
        state=3
    else:
        x2=int.from_bytes(res,"little")
        state=0
        result=256*x1+x2
        data.append(result)
#        print(Num,result)
        Num=Num+1
#    print(res)
s.close()
end = datetime.now()
current_time = start.strftime("%H:%M:%S")
print("Start Time =", current_time)
current_time = end.strftime("%H:%M:%S")
print("Stop Time =", current_time)
print(end-start)

ndata=np.array(data)
#mydata=ndata[0:2000]
#plt.plot(mydata[(mydata > 6700) & (mydata<6850)])
#mydata=ndata[2500:4000]
#plt.plot(mydata[(mydata > 6700) & (mydata<6850)])
#mydata=ndata[4000:5000]
#plt.plot(mydata[(mydata > 6700) & (mydata<6850)])

f = open("my_sensor.csv", "w")
for v in ndata:
    f.write("%s\n" % v)
f.close()
