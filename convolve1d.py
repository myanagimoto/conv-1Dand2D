#coding:utf-8
import numpy as np
import pylab as plt


def signal(fs,#sampling rate[Hz]
           N,#time point
           fc#containing rates[Hz]
           ):
    fs=float(fs)
    fn=fs/2
    T=N/fs
    print('\tfs:\t{}[Hz]'.format(fs))
    print('\tfn:\t{}[Hz]'.format(fn))
    print('\tN:\t{}'.format(N))
    print('\tT:\t{}[sec]'.format(T))
    
    sig=np.zeros((N))
    for fi in fc:
        fi=float(fi)
        assert fi<=fn,'fc is larger than fn.'
        sig+=np.sin(2.*np.pi*fi*T*(np.arange(N)/float(N)))
        #sig+=np.cos(2.*np.pi*fi*T*(np.arange(N)/float(N)))
    
    xscale=np.arange(len(sig))
    plt.plot(xscale,sig)
    plt.xticks([xscale[-1]],[xscale[-1]*T/N])
    plt.xlabel('time [sec]')
    plt.title('input signal (time domain)')
    plt.show()
    return sig
    
    
def create_filter(fs,size=200,fc=[1.,10.]):
    tlen=size/fs
    print('\tfilter size:\t{}'.format(size))
    print('\ttime len:\t{}[sec]'.format(tlen))
    
    fil=np.zeros((size))
    for fi in fc:
        fi=float(fi)
        fil+=np.sin(2.*np.pi*fi*tlen*(np.arange(size)/float(size)))
        #fil+=np.cos(2.*np.pi*fi*tlen*(np.arange(size)/float(size)))
        
    xscale=np.arange(len(fil))
    plt.plot(xscale,fil)
    plt.xticks([xscale[-1]],[xscale[-1]/fs])
    plt.xlabel('time [sec]')
    plt.title('filter (time domain)')
    plt.show()
        
    return fil

if __name__=='__main__':
    #input condition
    fs=1000.
    N=2000
    fc=[1,2,3,10,20,30,100,200,300]
    #filter condition
    size=10
    ffc=[200]
            
    np.random.seed(10000)
    fs=float(fs)
    
    if fc=="random":
        fc=np.random.randint(fs/2,size=100)
        fc=np.sort(fc)
    else:
        fc=np.asarray(fc)
        
    print('\tfc:\t{}[Hz]\n'.format(fc))
    s=signal(fs=fs,N=N,fc=fc)
    
    S=np.fft.fft(s)
    S_=np.abs(S)
    
    Sfreq=np.fft.fftfreq(N,1./fs)
    plt.figure()
    plt.plot(Sfreq[:len(S_)//2],S_[:len(S_)//2])
    plt.xlabel('frequency [Hz]')
    plt.title('input signal (freq domain)')
    plt.show()
    
    print('*******************************************************')
    
    h=create_filter(fs=fs,size=size,fc=ffc)
    H=np.abs(np.fft.fft(h))
    Hfreq=np.fft.fftfreq(len(h),1./fs)
    Nh=len(H)
    plt.figure()
    plt.plot(Hfreq[:Nh//2],H[:Nh//2])
    plt.xlabel('frequency [Hz]')
    plt.title('filter (freq domain)')
    plt.show()
    
    print('*******************************************************')
    
    out=np.convolve(s,h,'same')
    xscale=np.arange(len(out))
    plt.figure()
    plt.plot(xscale,out)
    plt.title('output signal (time domain)')
    plt.show()
    Out=np.abs(np.fft.fft(out))
    No=len(out)
    Ofreq=np.fft.fftfreq(No,1./fs)
    plt.figure()
    plt.plot(Ofreq[:No//2],Out[:No//2])
    plt.xlabel('frequency [Hz]')
    plt.title('output signal (freq domain)')
    plt.show()
    
    