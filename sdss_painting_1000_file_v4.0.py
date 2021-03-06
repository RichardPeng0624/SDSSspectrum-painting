import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
from astropy.io import fits
from scipy import fft,ifft
import sys
import time
import math
import traceback
colorlist=['deepskyblue','orange','greenyellow','darkslateblue','blueviolet','darkviolet','mediumorchid','thistle','indigo','purple']
sys.setrecursionlimit(1000000)
path='/media/richard/Backup Plus/951/'

mpl.rc('figure',max_open_warning=0)#work out the max_open_warning
ff=open('/media/richard/Backup Plus/951/test_smooth.csv')
data=pd.read_csv(ff)
specname=data['specname']
groupid=data['GroupID']
z=data['Z']
groupsize=data['GroupSize']
f=open('/media/richard/Backup Plus/error_log.txt',"a")
mpl.rc('font',family='Times New Roman')
mpl.rcParams['agg.path.chunksize']=20
FLUX=[]

for i in range(0,len(groupid)):
    if i!=0:
        if groupid[i]==groupid[i-1]:
            continue
    #if os.path.exists('/media/richard/Backup Plus/test0414/%s.png'%groupid[i])==True:
        #continue
    df=data[data.GroupID==data.GroupID[i]]
    fig=plt.figure(figsize=(10,5))
    m=0
    for j in range(i,i+len(df.specname)):
        if os.path.exists(path+'%s'%df.specname[j])==True:
            #-----open fits and convert wavelength to wavelength in rest-frame,and remove the and_mask values
            spectra = fits.open(path+specname[j])[1].data
            ind = np.where((spectra['and_mask'] == 0) & (spectra['flux'] >= 0),True,False)
            ind1 = np.where((spectra['flux'] >= 0),True,False)
            if np.sum(ind) > 1000:
                lam = 10**spectra['loglam'][ind]
                flux = spectra['flux'][ind]
            else:
                lam= 10**spectra['loglam'][ind1]
                flux = spectra['flux'][ind1]#open fits
            lam_no_z=lam/((z[j])+1)
            a=int(min(lam_no_z))
            b=math.ceil(max(lam_no_z))
            #-----set up color
            if m>10 and m%10!=0:
                x=int(m/10)*10+1
            elif m>=10 and m%10==0:
                x=((m//10)-1)*10+1
            else:
                x=0
            cc=colorlist[0+m-x]
            #-----smooth,use Fourier low pass filter but maybe the Fourier convolution method is better
            s=fft(flux)
            u=len(s)
            v=300
            #cutfun=np.ones([u,1])
            #cutfun[20:u-20]=0
            ss=s
            ss[v:u-v]=0
            func=ifft(ss)
            real_f=np.real(func)
            #-----plot
            FLUX.append(max(real_f))
            ax1=fig.add_subplot(1,1,1)
            ax1.plot(lam_no_z,flux,color='lightgray',alpha=0.8,linewidth=0.2)
            ax1.plot(lam_no_z,real_f,color=cc,linewidth=0.5,alpha=0.8,label='%s'%str(df.specname[j])[5:-4])
            ax1.set_xlabel(r'wavelength($\mathring{A}$)')
            ax1.set_ylabel('flux'+'('+r'$\ 10^{-17}$'+r'$\ ergs^{-1}$'+r'$\ cm^{-2}$'+r'${\mathring{A}^{-1}}$'+')')
        else:
            print("no this fits:%s"%df.specname[j])
            f.write("%s\n"%df.specname[j])
        m+=1
    plt.xlim(a,b)
    plt.ylim(-2,max(FLUX))
    plt.title("groupid=%s"%groupid[i]+" z=%s"%z[i])
    plt.axvline(x=1549,c='gray',ls='--',linewidth=1)
    plt.axvline(x=1907,c='gray',ls='--',linewidth=1)
    plt.axvline(x=2802,c='gray',ls='--',linewidth=1)
    plt.annotate('C IV',xy=(1549,max(FLUX)-1.5),xycoords='data')
    plt.annotate('C III',xy=(1907,max(FLUX)-1.5),xycoords='data')
    plt.annotate('Mg II',xy=(2802,max(FLUX)-1.5),xycoords='data')
    plt.legend(loc='upper right',frameon=False)
    plt.savefig('/media/richard/Backup Plus/test0414/%s.png'%groupid[i],dpi=300)
    print(groupid[i])
    FLUX.clear()
f.close()
