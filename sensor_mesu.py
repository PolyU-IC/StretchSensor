# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import time
import matplotlib.pyplot as plt
#import msvcrt
import numpy as np
from datetime import datetime
from scipy import stats
#from scipy.fft import fft, fftfreq
from sklearn import preprocessing
from scipy import signal
from scipy.signal import find_peaks
#mydata=ndata[0:2000]
#plt.plot(mydata[(mydata > 6700) & (mydata<6850)])
#mydata=ndata[2500:4000]
#plt.plot(mydata[(mydata > 6700) & (mydata<6850)])
#mydata=ndata[4000:5000]
#plt.plot(mydata[(mydata > 6700) & (mydata<6850)])

f = open("my_sensor02.csv", "r")
data=[]
for v in f:
    data.append(int(v))
f.close()
ndata=np.array(data)

ndata = ndata - np.mean(ndata)
#plt.plot(ndata)
spectrum = np.fft.rfft(ndata)
nLen=len(ndata)
SAMPLE_RATE=50

N=3000
K=60*5000/(100*N)
INC=200
start=0
end=start+N
#start=1400
#end=3400
while end <= nLen:

    xdata=ndata[start:end]
    seg=np.argmax(abs(np.gradient(xdata)))
    
    S1=xdata[0:seg]-np.mean(xdata[0:seg])
    S2=xdata[seg:]-np.mean(xdata[seg:])
    sdata=np.concatenate((S1, S2)) 

    sos = signal.butter(10, 0.2, 'low', output='sos')
    filtered = signal.sosfilt(sos, sdata)
    peaks, _ = find_peaks(filtered,distance=100,height=0)
    plt.plot(peaks,filtered[peaks],"x")
#    plt.plot(sdata)
    plt.plot(filtered)
    plt.show()
    print("{}-{}:RSR={}/min".format(start,end,len(peaks)*K))
    start=start+INC                 
    end = start+N
