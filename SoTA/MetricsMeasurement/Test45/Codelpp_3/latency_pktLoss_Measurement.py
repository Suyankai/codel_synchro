#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 09:58:25 2023

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
df_pih1_send = pd.read_csv("pih1_Codelpp_synchro_test_45_3.csv", sep=",")
df_pih2_send = pd.read_csv("pih2_Codelpp_synchro_test_45_3.csv", sep=",")
df_pih1_receive = pd.read_csv("pi4_Codelpp_synchro_test_45_3_pih1.csv", sep=",")
df_pih2_receive = pd.read_csv("pi4_Codelpp_synchro_test_45_3_pih2.csv", sep=",")

print(datetime.datetime.now(), "Format the time in all dataset:")
pd.options.mode.chained_assignment = None 
#warnings.filterwarnings('ignore', category=pd.core.common.SettingWithCopyWarning)
for i in range(len(df_pih1_send)):
    df_pih1_send['Time'][i] = datetime.datetime.strptime(df_pih1_send['Time'][i], '%Y-%m-%d %H:%M:%S,%f')

for i in range(len(df_pih2_send)):
    df_pih2_send['Time'][i] = datetime.datetime.strptime(df_pih2_send['Time'][i], '%Y-%m-%d %H:%M:%S,%f')

for i in range(len(df_pih1_receive)):
    df_pih1_receive['Time'][i] = datetime.datetime.strptime(df_pih1_receive['Time'][i], '%Y-%m-%d %H:%M:%S,%f')

for i in range(len(df_pih2_receive)):
    df_pih2_receive['Time'][i] = datetime.datetime.strptime(df_pih2_receive['Time'][i], '%Y-%m-%d %H:%M:%S,%f')

print(datetime.datetime.now(), "Calculate the latency:")
print(datetime.datetime.now(), "Format the send & receieve time in pih1:")
df_pih1_receive['Time_s'] = None
for i in range(len(df_pih1_receive)):
    temp = df_pih1_send.loc[df_pih1_send['Identification'] == df_pih1_receive['Identification'][i], 'Time']
    if len(temp) != 0:
        df_pih1_receive['Time_s'][i] = temp.values[0]


print(datetime.datetime.now(), "Calculate the latency of pih1:")
df_pih1_receive['Latency'] = None
for i in range(len(df_pih1_receive)):
    if df_pih1_receive['Time_s'][i] != None:
        df_pih1_receive['Latency'][i] = abs(df_pih1_receive['Time_s'][i] - df_pih1_receive['Time'][i])
        df_pih1_receive['Latency'][i] = df_pih1_receive['Latency'][i].total_seconds() * 1000
    
avr_pih1_latency = df_pih1_receive[df_pih1_receive['Latency'] != None]['Latency'].mean()
print(datetime.datetime.now(), "Average latency of pih1 is:", avr_pih1_latency,"ms")


print(datetime.datetime.now(), "Format the send & receieve time in pih2:")
df_pih2_receive['Time_s'] = None
for i in range(len(df_pih2_receive)):
    temp = df_pih2_send.loc[df_pih2_send['Identification'] == df_pih2_receive['Identification'][i], 'Time']
    if len(temp) != 0:
        df_pih2_receive['Time_s'][i] = temp.values[0]


print(datetime.datetime.now(), "Calculate the latency of pih2:")
df_pih2_receive['Latency'] = None
for i in range(len(df_pih2_receive)):
    if df_pih2_receive['Time_s'][i] != None:
        df_pih2_receive['Latency'][i] = abs(df_pih2_receive['Time_s'][i] - df_pih2_receive['Time'][i])
        df_pih2_receive['Latency'][i] = df_pih2_receive['Latency'][i].total_seconds() * 1000
    
avr_pih2_latency = df_pih2_receive[df_pih2_receive['Latency'] != None]['Latency'].mean()
print(datetime.datetime.now(), "Average latency of pih2 is:", avr_pih2_latency,"ms")

print(datetime.datetime.now(), "Calculate the pkt loss rate:")
pkt_loss_pih1 = (1 - df_pih1_receive[df_pih1_receive['Time_s'] != None]['Time_s'].count()/len(df_pih1_send)) * 100
print(datetime.datetime.now(), f"The pkt loss rate of pih1 is: {pkt_loss_pih1}%")
pkt_loss_pih2 = (1 - df_pih2_receive[df_pih2_receive['Time_s'] != None]['Time_s'].count()/len(df_pih2_send)) * 100
print(datetime.datetime.now(), f"The pkt loss rate of pih2 is: {pkt_loss_pih2}%")