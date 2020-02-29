This is my first try on Github.
The script below shows how to read FITS files and paints spectrum from SDSS(Sloan Digital Sky Survey).
If you wanna paint the whole spectrum of a mutliple-obervation source(which means it may be observing several times during different projects) in one picture,you can use this py script.You are expected to prepare something before running it:
1.You need prepare a csv catalog with some basic information of the whole fits files including PLATE,MJD,FiberID,GroupID,GroupSize,Z,specname at least.
To make this catalog,I recommand you to use `TOPCAT`,a very useful speardsheet software.You can match same sources with RA and DEC by using  'Internal match' in it,then you can get  a matched catalog with columns 'groupid' and 'groupsize' added .Other columns such as S/N,linearea_flux may also be needed.
2.Download all the needed FITS files at SDSS website.
3.This script use `Astropy`,a python package to read fits file,so please make sure you know the data structure of FITS and some basic functions in astropy.
4.In order to prevent too many files in an folder to open it,the script put 1000 pictures in one file,you can change the number.
5.The disadvantage of this script is your computer must have ample memory if  you wanna process a large number of fits  files at once(more than a thousand).
Another weakness is that if there are fewer fits  than the 'groupsize' shown in one group,some fits files in the next group will be drew in this one inveitably,please pay attention to it though it's a low probability event.
6.Pay attention to the paths in codes and remember to change them.
7.If you improved it, please let me know~

```python    
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import os
from astropy.io import fits
from scipy import fft,ifft
import math
import sys
import traceback
import time
colorlist=['b','orange','greenyellow','darkslateblue','blueviolet','darkviolet','mediumorchid','thistle','indigo','purple']
sys.setrecursionlimit(1000000) 

time_start=time.time()
mpl.rc('figure',max_open_warning=0)#work out the max_open_warning
data=pd.read_csv('/media/richard/Backup Plus/314kpair_DR16_final_Z_1.0.csv',usecols=['specname_new','GroupID','Z','GroupSize'])#chunksize=10 error:keyerror:0,might result of range(0,10)
path='/media/richard/Backup Plus/sdss_16_pair/'
specname=data['specname_new']
groupid=data['GroupID']
z=data['Z']
groupsize=data['GroupSize']
f=open('/media/richard/Backup Plus/error_log.txt',"a")
xx=280000
yy=xx+3000
while xx<yy:
    if os.path.exists('/media/richard/Backup Plus/eps%s'%xx)==False:
        os.mkdir('/media/richard/Backup Plus/eps%s'%xx)
    for i in range(xx,xx+1000):
        if i!=0:
            if groupid[i]==groupid[i-1]:
                continue
        n=groupsize[i]
        name_0=str(specname[i])
        print(n)
        m=0
        if os.path.exists("/media/richard/Backup Plus/eps%s/%s.eps"%(xx,str(groupid[i])))==True:
            continue
        fig=plt.figure(figsize=(10,5))
        try:
            while m<n:
              name=str(specname[i+m])
              ID=str(groupid[i])
              zname=str(z[i+m])
              ax1=fig.add_subplot(1,1,1)
              if os.path.exists(path+'%s'%name)==True:
                  #-----open fits and convert wavelength to wavelength in rest-frame
                  fit=fits.open(path+'%s'%name)#open fits
                  data1=fit[1].data
                  flux=data1.field('flux')+6*m
                  lam=10**(data1.field('loglam'))
                  lam_no_z=lam/((z[i+m])+1)
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
                  ax1.plot(lam_no_z,flux,color='gray',alpha=0.3,linewidth=0.2)
                  ax1.plot(lam_no_z,real_f,color=cc,linewidth=1,alpha=0.4,label='%s'%name)
                  #plt.xticks(np.linspace(a,b,15))
                  #plt.subplots_adjust(hspace=0.8)
                  #plt.xlim(a-100,b+100)
                  ax1.set_xlabel(r'wavelength($\mathring{A}$)')
                  ax1.set_ylabel('flux'+'('+r'$\ 10^{-17}$'+r'$\ ergs^{-1}$'+r'$\ cm^{-2}$'+r'$\ A^{-1}$'+')')
                  ax1.set_xlim(a-50,b+200)
                  ax1.set_ylim(-10,max(real_f)+5)
                  ax1.set_title("groupid=%s"%ID+" z=%s"%zname+" groupsize=%d"%n)
                  ax1.axvline(x=1549,c='black',ls='--',linewidth=0.3)
                  ax1.axvline(x=1907,c='black',ls='--',linewidth=0.3)
                  ax1.axvline(x=2802,c='black',ls='--',linewidth=0.3)
                  ax1.annotate(r'$\ C_{iv}$'+"1549",xy=(1400,-8),xycoords='data')
                  ax1.annotate(r'$\ C_{iii}$'+'1907',xy=(1755,-8),xycoords='data')
                  ax1.annotate(r'$\ Mg_{ii}$'+'2802',xy=(2640,-8),xycoords='data')
                  ax1.legend(loc='upper right')
              else:
                  print("no this fits:",name)
                  f.write("%s\n"%name)
              m+=1
            plt.savefig('/media/richard/Backup Plus/eps%s/%s.eps'%(xx,ID))
        except ValueError:
            print (ValueError)
            f.write('error=%s,groupid=%s'%(ValueError,ID))
            pass
        except IndexError:
            traceback.print_exc()
            f.write('error=%s,groupid=%s'%(IndexError,ID))
            pass
        except TypeError:
            print (TypeError)
            traceback.print_exc()
            f.write('error=%s,groupid=%s\n'%(TypeError,ID))
        except Exception:
            traceback.print_exc()
            f.write('error=OSError or others,groupid=%s\n'%ID)
            pass
    xx=xx+1000
    print(xx)
time_end=time.time()
print("done:",time_end-time_start)
f.close()
#plt.show()
```
