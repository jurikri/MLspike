# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 14:38:49 2020

@author: msbak
"""


import os  # 경로 관리
# library import
import pickle # python 변수를 외부저장장치에 저장, 불러올 수 있게 해줌
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv


# set pathway
try:
    savepath = 'E:\\mscore\\syncbackup\\paindecoder\\save\\tensorData\\'; os.chdir(savepath)
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

savepath2 = 'D:\\mscore\\syncbackup\\Coding\\MLspike_ms\\data2\\'

N = msdata_load['N']

grouped_total_list = []
keylist = list(msGroup.keys())
for k in range(len(keylist)):
    grouped_total_list += msGroup[keylist[k]]

se3set = capsaicinGroup + pslGroup + shamGroup + adenosineGroup + CFAgroup

for SE in range(N):
    if SE in grouped_total_list:
        seFor = list(range(5))
        if SE in se3set:
            seFor = list(range(3))
        for se in seFor:
            mssignal = np.array(signalss[SE][se]) #[frame, ROI]
            mssignal2 = pd.DataFrame(np.transpose(mssignal))
            savepath3 = savepath2 + (str(SE)+'_'+str(se)) + '.csv'
            mssignal2.to_csv(savepath3, header=False, index=False)
















































