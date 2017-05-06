#coding:utf-8

import numpy as np
import pylab as plt
from scipy import misc
from scipy import signal
from skimage.measure import block_reduce

def figout(s):
    plt.figure()    
    plt.imshow(abs(s).astype(np.uint8))
    plt.gray()
    plt.show()
        
def create_filter(size=100,T=range(1,50)):
    T=np.asarray(T).astype(float)
    fc=size/T
    fil=np.zeros((size,size))
            
    for _fc in fc:
        isig=np.cos(2*np.pi*_fc*np.arange(size)/size)
        isig=isig.reshape((1,size))
        jsig=isig.reshape((size,1))
        fil+=isig
        fil+=jsig

    return fil

def main(s,size=4,T=[2]):
    h=create_filter(size,T)
    figout(h)
    
    out=signal.convolve2d(s,h,'same')
    figout(out)       
        
if __name__=='__main__':
    
    sizes=[8,6,4,2]
    T=[2]
    down=8
    
    s=misc.face()[...,0]
    figout(s)
    ss=block_reduce(s,block_size=(down,down),func=np.mean)
    figout(ss)
    sss=np.ones(s.shape)
    for i in range(ss.shape[0]):
        for j in range(ss.shape[1]):
            sss[i*down:(i+1)*down,j*down:(j+1)*down]*=ss[i,j]
    figout(sss)
    
    for size in sizes:
        main(s,size,T)
        main(ss,size,T)
        main(sss,size,T)
    

    
    
    