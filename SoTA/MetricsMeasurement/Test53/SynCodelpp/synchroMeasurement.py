#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 24 14:53:24 2023

@author: su
"""


import pandas as pd
import datetime
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
#import warnings

# import the data
print(datetime.datetime.now(), "Import the data:")
df_pih1_send = pd.read_csv("pih1_SynCodelpp_synchro_test_53.csv", sep=",")
df_pih2_send = pd.read_csv("pih2_SynCodelpp_synchro_test_53.csv", sep=",")
df_pih1_receive = pd.read_csv("pi4_SynCodelpp_synchro_test_53_pih1.csv", sep=",")
df_pih2_receive = pd.read_csv("pi4_SynCodelpp_synchro_test_53_pih2.csv", sep=",")
pd.options.mode.chained_assignment = None 

print(datetime.datetime.now(), "Format the time in all dataset:")
#warnings.filterwarnings('ignore', category=pd.core.common.SettingWithCopyWarning)
for i in range(len(df_pih1_send)):
    df_pih1_send['Time'][i] = datetime.datetime.strptime(df_pih1_send['Time'][i], '%Y-%m-%d %H:%M:%S,%f')

for i in range(len(df_pih2_send)):
    df_pih2_send['Time'][i] = datetime.datetime.strptime(df_pih2_send['Time'][i], '%Y-%m-%d %H:%M:%S,%f')

for i in range(len(df_pih1_receive)):
    df_pih1_receive['Time'][i] = datetime.datetime.strptime(df_pih1_receive['Time'][i], '%Y-%m-%d %H:%M:%S,%f')

for i in range(len(df_pih2_receive)):
    df_pih2_receive['Time'][i] = datetime.datetime.strptime(df_pih2_receive['Time'][i], '%Y-%m-%d %H:%M:%S,%f')




print(datetime.datetime.now(), "Initialize the sending pkt pair:")
df_pair_send = pd.DataFrame()
ID_pih1 = []
time_pih1_send = []
ID_pih2 = []
time_pih2_send = []

print(datetime.datetime.now(), "Form the sending pkt pair: \n")
for i in tqdm(range(len(df_pih1_send))):
    pih1_send_indicator = df_pih1_send['Time'][i]
    closest_time_pih2 = min(df_pih2_send['Time'], key=lambda x: abs(x - pih1_send_indicator))
    if abs((pih1_send_indicator - closest_time_pih2)).total_seconds() * 1000 > 3:
        continue
    else:
        ID_pih1.append(df_pih1_send['Identification'][i])
        time_pih1_send.append(pih1_send_indicator)
        ID_pih2.append(df_pih2_send.loc[df_pih2_send['Time'] == closest_time_pih2, 'Identification'].values[0])
        time_pih2_send.append(closest_time_pih2)

print("\n", datetime.datetime.now(), "Form the sending pkt pair dataframe:")
df_pair_send['ID_pih1'] = ID_pih1
df_pair_send['time_pih1_send'] = time_pih1_send
df_pair_send['ID_pih2'] = ID_pih2
df_pair_send['time_pih2_send'] = time_pih2_send
df_pair_send['Synchro_send'] = abs(df_pair_send['time_pih1_send'] - df_pair_send['time_pih2_send'])
for i in range(len(df_pair_send)):
    df_pair_send['Synchro_send'][i] = df_pair_send['Synchro_send'][i].total_seconds() * 1000

print(datetime.datetime.now(), "Initialize the receiving pkt pair:")
df_pair_receive = pd.DataFrame()

time_pih1_receive = []
time_pih2_receive = []

print(datetime.datetime.now(), "Find pkts in receving end:\n")
for i in tqdm(range(len(df_pair_send))):
    flag_pih1 = df_pih1_receive.loc[df_pih1_receive['Identification'] == df_pair_send['ID_pih1'][i], 'Time']
    if len(flag_pih1) != 0:
        time_pih1_receive.append(flag_pih1.values[0])
    else:
        time_pih1_receive.append("Pkt lost")
    
    flag_pih2 = df_pih2_receive.loc[df_pih2_receive['Identification'] == df_pair_send['ID_pih2'][i], 'Time']
    if len(flag_pih2) != 0:
        time_pih2_receive.append(flag_pih2.values[0])
    else:
        time_pih2_receive.append("Pkt lost")

print("\n", datetime.datetime.now(), "Form the receiving pkt pair dataframe:")
df_pair_receive['ID_pih1'] = ID_pih1
df_pair_receive['time_pih1_receive'] = time_pih1_receive
df_pair_receive['ID_pih2'] = ID_pih2
df_pair_receive['time_pih2_receive'] = time_pih2_receive
df_pair_receive['Synchro_receive'] = None
for i in range(len(df_pair_receive)):
    if (df_pair_receive['time_pih1_receive'][i] != 'Pkt lost') and (df_pair_receive['time_pih2_receive'][i] != 'Pkt lost'):
        df_pair_receive['Synchro_receive'][i] = abs(df_pair_receive['time_pih1_receive'][i] - df_pair_receive['time_pih2_receive'][i])
        #df_pair_receive['Synchro_receive'][i] = df_pair_receive['time_pih1_receive'][i] - df_pair_receive['time_pih2_receive'][i]
        df_pair_receive['Synchro_receive'][i] = df_pair_receive['Synchro_receive'][i].total_seconds() * 1000


print(datetime.datetime.now(), "Result evaluation:")
avr_sychro_send = df_pair_send['Synchro_send'].mean()
avr_sychro_receive = df_pair_receive['Synchro_receive'][df_pair_receive['Synchro_receive'].notna()].mean()
event_pkt_loss = df_pair_receive['Synchro_receive'].isna().sum() / len(df_pair_receive) * 100


print("Average synchronization difference of sending is:", avr_sychro_send,"ms")
print("Average synchronization difference of receiving is:",avr_sychro_receive,"ms")
print("Event pair loss rate is:", event_pkt_loss,"%")

fig,ax = plt.subplots()
#ax.boxplot(df_pair_receive['Synchro_receive'][df_pair_receive['Synchro_receive'].notna()], showfliers=False)
ax.boxplot(df_pair_receive['Synchro_receive'][df_pair_receive['Synchro_receive'].notna()])
ax.grid(True)

# Calculate the median
data = df_pair_receive['Synchro_receive'][df_pair_receive['Synchro_receive'].notna()]
median = np.median(data)

# Count the number of points below the median
num_points_below_median = sum(1 for value in data if value < median)

print("Number of points below the median:", num_points_below_median)