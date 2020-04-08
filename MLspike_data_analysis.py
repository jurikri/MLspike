# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 17:10:04 2020

@author: msbak
"""

import hdf5storage
import os
import numpy as np
import pandas as pd

FPS = 4.3650966869
filepath = 'D:\\mscore\\syncbackup\\Coding\\MLspike_ms\\data\\'

# In
# library import
import pickle # python 변수를 외부저장장치에 저장, 불러올 수 있게 해줌
import matplotlib.pyplot as plt

# set pathway
try:
    savepath = 'D:\\mscore\\syncbackup\\paindecoder\\save\\tensorData\\'; os.chdir(savepath)
except:
    try:
        savepath = 'C:\\Users\\skklab\\Google 드라이브\\save\\tensorData\\'; os.chdir(savepath);
    except:
        try:
            savepath = 'D:\\painDecorder\\save\\tensorData\\'; os.chdir(savepath);
        except:
            savepath = ''; # os.chdir(savepath);
print('savepath', savepath)

pickleload = 'D:\\mscore\\syncbackup\\google_syn\\mspickle.pickle'
# var import
with open(pickleload, 'rb') as f:  # Python 3: open(..., 'rb')
    msdata_load = pickle.load(f)
    
signalss = msdata_load['signalss'] # 투포톤 이미징데이터 -> 시계열
msGroup = msdata_load['msGroup'] # 그룹정보
highGroup = msGroup['highGroup']    # 5% formalin
midleGroup = msGroup['midleGroup']  # 1% formalin
lowGroup = msGroup['lowGroup']      # 0.25% formalin
salineGroup = msGroup['salineGroup']    # saline control
restrictionGroup = msGroup['restrictionGroup']  # 5% formalin + restriciton
ketoGroup = msGroup['ketoGroup'] # 5% formalin + keto 100
lidocaineGroup = msGroup['lidocaineGroup'] # 5% formalin + lidocaine
capsaicinGroup = msGroup['capsaicinGroup'] # capsaicin
yohimbineGroup = msGroup['yohimbineGroup'] # 5% formalin + yohimbine
pslGroup = msGroup['pslGroup'] # partial sciatic nerve injury model
shamGroup = msGroup['shamGroup']
adenosineGroup = msGroup['adenosineGroup']
highGroup2 = msGroup['highGroup2']
CFAgroup = msGroup['CFAgroup']
chloroquineGroup = msGroup['chloroquineGroup']

N = msdata_load['N']

grouped_total_list = []
keylist = list(msGroup.keys())
for k in range(len(keylist)):
    grouped_total_list += msGroup[keylist[k]]

se3set = capsaicinGroup + pslGroup + shamGroup + adenosineGroup + CFAgroup

exceptlist = chloroquineGroup

sessionlist = []
for SE in range(N):
    if SE in grouped_total_list:
        seFor = list(range(5))
        if SE in se3set:
            seFor = list(range(3))
        for se in seFor:
            sessionlist.append(str(SE) + '_' + str(se))

# In[] ROI x frame , event peak(?) frame에서 amplitude를 저장

eventss=[]; [eventss.append([]) for u in range(N)]            
for SE in range(N):
    if SE in grouped_total_list and not SE in exceptlist:
        seFor = list(range(5))
        if SE in se3set:
            seFor = list(range(3))
        for se in seFor:
            [eventss[SE].append([]) for u in seFor]  
        
            print('processing...', SE, se)
            
            loadpath = filepath + str(SE) + '_' + str(se) + '.csv_MLSpike_data.mat'
            df = hdf5storage.loadmat(loadpath)
            spikest = df['spikest']
            mssignal = df['drift']
            
            tframe = mssignal[0,0].shape[0]
            event_amp_roisave = []
            for ROI in range(spikest.shape[1]):
                event_amp_tmp = np.zeros(tframe); event_amp_tmp[:] = np.nan
                spike_ix = np.array(spikest[0, ROI][0] * FPS, dtype=int)
                event_amp_tmp[spike_ix] = mssignal[0, ROI][spike_ix,0]
                event_amp_roisave.append(event_amp_tmp)
                
            eventss[SE][se] = event_amp_roisave

# In[]
frequency = np.zeros((N,5))
amplitude = np.zeros((N,5))
for SE in range(N):
    if SE in grouped_total_list and not SE in exceptlist:  
        seFor = list(range(5))
        if SE in se3set:
            seFor = list(range(3))
        for se in seFor:
            frequency[SE][se] = np.mean(np.array(eventss[SE][se]) > 0) * FPS   # ROI x frame
            amplitude[SE][se] = np.nanmean(np.array(eventss[SE][se]))
            

def msGrouping_nonexclude(msdata): 
    df3 = pd.concat([pd.DataFrame(msdata[salineGroup,0:4]) \
                                  ,pd.DataFrame(msdata[highGroup + highGroup2,0:4]) \
                                  ,pd.DataFrame(msdata[midleGroup,0:4]) \
                                  ,pd.DataFrame(msdata[ketoGroup,0:4]) \
                                  ,pd.DataFrame(msdata[lidocaineGroup,0:4])] \
                                  ,ignore_index=True, axis=1)
    
    df3 = np.array(df3)
    return df3

Aprism_frequency_formalin = msGrouping_nonexclude(frequency)
Aprism_amplitude_formalin = msGrouping_nonexclude(amplitude)

# In[] save

try:
    savepath = 'E:\\mscore\\syncbackup\\paindecoder\\save\\tensorData\\'; os.chdir(savepath)
except:
    try:
        savepath = 'C:\\Users\\msbak\\Documents\\tensor\\'; os.chdir(savepath);
    except:
        savepath = ''; # os.chdir(savepath);
print('savepath', savepath)

msdata = {
        'Aprism_frequency_formalin' : Aprism_frequency_formalin,
        'Aprism_amplitude_formalin' : Aprism_amplitude_formalin,
        }

with open('formalin_event_detection.pickle', 'wb') as f:  # Python 3: open(..., 'wb')
    pickle.dump(msdata, f, pickle.HIGHEST_PROTOCOL)
    print('formalin_event_detection.pickle 저장되었습니다.')







            
