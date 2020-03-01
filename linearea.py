from astropy.io import fits
import pandas as pd
import numpy as np
import time
import traceback
import os
flux1350=[]
flux3000=[]
df=pd.read_csv('/media/richard/Backup Plus/candidate_dr16_0.8_final.csv',low_memory=False)
groupid=df['GroupID_1']
specname=df['specname_new']
z=df['Z']
area_1350=df['LINEAREA_1350']
area_3000=df['LINEAREA_3000']
f=open('/media/richard/Backup Plus/error_log.txt',"a")

for i in range(len(specname)):
    try:
        if os.path.exists('/media/richard/Backup Plus/sdss_16_pair/'+str(specname[i]))==True:
            fit=fits.open('/media/richard/Backup Plus/sdss_16_pair/'+str(specname[i]))
            data_fit=fit[1].data
            for j in range(len(data_fit.field('loglam'))):
                lam=(10**(data_fit.field('loglam')[j]))/(z[i]+1)
                if lam>1350-25 and lam<1350+25:
                    flux1350.append(data_fit.field('flux')[j])
                elif lam>3000-25 and lam<3000+25:
                    flux3000.append(data_fit.field('flux')[j])
            df.loc[df.specname_new==df.specname_new[i],'LINEAREA_1350']=np.mean(flux1350)
            df.loc[df.specname_new==df.specname_new[i],'LINEAREA_3000']=np.mean(flux3000)
            print(specname[i])
            print(df['LINEAREA_1350'][i])
            print(df['LINEAREA_3000'][i])
            flux1350.clear()
            flux3000.clear()
        else:
            df.loc[df.specname_new==df.specname_new[i],'LINEAREA_1350']='nan'
            df.loc[df.specname_new==df.specname_new[i],'LINEAREA_3000']='nan'
            continue
    except TypeError:
        print(specname[i])
        traceback.print_exc()
        df.loc[df.specname_new==df.specname_new[i],'LINEAREA_1350']='nan'
        df.loc[df.specname_new==df.specname_new[i],'LINEAREA_3000']='nan'
        f.write('cannot caculate the area:%s'%specname[i])
        pass
    except Exception:
        df.loc[df.specname_new==df.specname_new[i],'LINEAREA_1350']='nan'
        df.loc[df.specname_new==df.specname_new[i],'LINEAREA_3000']='nan'
        print('failed')
        pass
df.to_csv('/home/richard/data/change-look-AGN/dr16_0.8_final.csv')
