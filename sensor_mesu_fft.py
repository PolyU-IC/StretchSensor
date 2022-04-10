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
from scipy.fft import fft, fftfreq
from sklearn import preprocessing
from scipy import signal
from scipy.signal import find_peaks
#mydata=ndata[0:2000]
#plt.plot(mydata[(mydata > 6700) & (mydata<6850)])
#mydata=ndata[2500:4000]
#plt.plot(mydata[(mydata > 6700) & (mydata<6850)])
#mydata=ndata[4000:5000]
#plt.plot(mydata[(mydata > 6700) & (mydata<6850)])

f = open("my_sensor01.csv", "r")
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

N=2000
INC=200
start=0
end=start+N
start=1400
end=3400
while end <= nLen:

    sdata=ndata[start:end]
    seg=np.argmax(abs(np.gradient(sdata)))
    
    plt.plot(sdata)
    plt.show()
    plt.plot(abs(np.gradient(sdata)))
    plt.show()
    S1=sdata[0:seg]-np.mean(sdata[0:seg])
    S2=sdata[seg:]-np.mean(sdata[seg:])
    sdata=np.concatenate((S1, S2)) 
    plt.plot(sdata)
    plt.show()

    sos = signal.butter(10, 0.05, 'low', output='sos')
    filtered = signal.sosfilt(sos, sdata)
    plt.plot(filtered)
    peaks, _ = find_peaks(filtered, height=0)
    yf=fft(sdata)
    xf=fftfreq(N,1/SAMPLE_RATE)
    nRANGE=(xf>0.01) & (xf < 1)
    mIndex=np.argmax(np.abs(yf[nRANGE]))
    RSR=xf[mIndex]
    plt.plot(xf[nRANGE],np.abs(yf[nRANGE]))
    plt.show()
    plt.plot(sdata)
    plt.show()
    print("{}-{}:RSR={}/min".format(start,end,RSR*60))
    start=start+INC                 
    end = start+N
