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
#from sklearn import preprocessing
from scipy import signal
from scipy.signal import find_peaks

data=[]
state=0
x1=0
x2=0
done=True
Num=0
N=3000
K=60*5000/(100*N)
INC=200
startIdx=0
ndata=np.zeros(5000)

def getRP(ndata):
    start=0
    end=start+N
    xdata=ndata[start:end]
    seg=np.argmax(abs(np.gradient(xdata)))
    
    S1=xdata[0:seg]-np.mean(xdata[0:seg])
    S2=xdata[seg:]-np.mean(xdata[seg:])
    sdata=np.concatenate((S1, S2)) 

    sos = signal.butter(10, 0.2, 'low', output='sos')
    filtered = signal.sosfilt(sos, sdata)
    peaks, _ = find_peaks(filtered,distance=100,height=0)
#    plt.plot(peaks,filtered[peaks],"x")
#    plt.plot(sdata)
#    plt.plot(filtered)
#    plt.show()
#    print("{}-{}:RSR={}/min".format(start,end,len(peaks)*K))
    return len(peaks)*K


s = serial.Serial(
    port="/dev/ttyUSB0", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
)
s.write(str.encode("AT"))
while (1):
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
        ndata[startIdx]=result
        startIdx=startIdx+1
        if (startIdx < N) & ((startIdx %500)==0):
           print(startIdx)	


    if (startIdx >N):
        print("{},{},{}".format(getRP(ndata),max(ndata),min(ndata)))
        ndata=np.roll(ndata,-INC)
        startIdx=startIdx-INC
    
