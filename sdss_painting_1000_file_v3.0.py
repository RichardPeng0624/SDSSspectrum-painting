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
colorlist=['b','orange','greenyellow','darkslateblue','blueviolet','darkviolet','mediumorchid','thistle','indigo','purple']
sys.setrecursionlimit(1000000)
path='/media/richard/Backup Plus/sdss_16_pair/'

time_start=time.time()
mpl.rc('figure',max_open_warning=0)#work out the max_open_warning
data=pd.read_csv('/home/richard/data/change-look-AGN/test0309.csv')
specname=data['specname_new']
groupid=data['GroupID_1']
z=data['Z']
groupsize=data['GroupSize_1']
f=open('/media/richard/Backup Plus/error_log.txt',"a")

for i in range(len(groupid)):
    if i!=0:
        if groupid[i]==groupid[i-1]:
            continue
        if groupid[i]!=groupid[i-1] and groupid[i]!=groupid[i+1]:
            continue
    df=data[data.GroupID_1==data.GroupID_1[i]]
    fig=plt.figure(figsize=(10,5))
    m=0
    for j in range(i,i+len(df.specname_new)):
        if os.path.exists(path+'%s'%df.specname_new[j])==True:
            #-----open fits and convert wavelength to wavelength in rest-frame
          fit=fits.open(path+'%s'%df.specname_new[j])#open fits
          data1=fit[1].data
          flux=data1.field('flux')+6*m
          lam=10**(data1.field('loglam'))
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
          #-----smooth
          s=fft(flux)
          u=len(s)
          v=200
          cutfun=np.ones([u,1])
          cutfun[20:u-20]=0
          ss=s
          ss[v:u-v]=0
          func=ifft(ss)
          real_f=np.real(func)
          #-----plot
          ax1=fig.add_subplot(1,1,1)
          ax1.plot(lam_no_z,flux,color='gray',alpha=0.3,linewidth=0.2)
          ax1.plot(lam_no_z,real_f,color=cc,linewidth=1,alpha=0.4,label='%s'%df.specname_new[j])
          ax1.set_xlabel(r'wavelength($\mathring{A}$)')
          ax1.set_ylabel('flux'+'('+r'$\ 10^{-17}$'+r'$\ ergs^{-1}$'+r'$\ cm^{-2}$'+r'$\ A^{-1}$'+')')
          ax1.set_xlim(a-50,b+200)
          ax1.set_ylim(-10,max(real_f)+5)
          ax1.set_title("groupid=%s"%groupid[i]+" z=%s"%z[i])
          ax1.axvline(x=1549,c='black',ls='--',linewidth=0.3)
          ax1.axvline(x=1907,c='black',ls='--',linewidth=0.3)
          ax1.axvline(x=2802,c='black',ls='--',linewidth=0.3)
          ax1.annotate(r'$\ C_{iv}$'+"1549",xy=(1400,-8),xycoords='data')
          ax1.annotate(r'$\ C_{iii}$'+'1907',xy=(1755,-8),xycoords='data')
          ax1.annotate(r'$\ Mg_{ii}$'+'2802',xy=(2640,-8),xycoords='data')
          ax1.legend(loc='upper right')
        else:
          print("no this fits:%s"%df.specname_new[j])
          f.write("%s\n"%df.specname_new[j])
        m+=1
    plt.savefig('/media/richard/Backup Plus/candidate_dr16_0.8/test0310/%s.eps'%groupid[i])
    print(groupid[i])
f.close()
