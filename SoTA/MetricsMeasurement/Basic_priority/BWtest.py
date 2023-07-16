# -*- coding: utf-8 -*-

import pandas as pd
import datetime
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None 
print(datetime.datetime.now(), "Import the data:")
df_pih1_send = pd.read_csv("Baseline/pih1_Baseline_synchro_test_37BW.csv", sep=",")
df_pih2_send = pd.read_csv("Baseline/pih2_Baseline_synchro_test_37BW.csv", sep=",")
df_pih1_receive = pd.read_csv("Baseline/pi4_Baseline_synchro_test_37_pih1BW.csv", sep=",")
df_pih2_receive = pd.read_csv("Baseline/pi4_Baseline_synchro_test_37_pih2BW.csv", sep=",")

print(datetime.datetime.now(), "Reformat the data:")
df_pih1_send = df_pih1_send[df_pih1_send['Filtered packets'] != 0]["Filtered packets"]/(1e6)
df_pih2_send = df_pih2_send[df_pih2_send['Filtered packets'] != 0]["Filtered packets"]/(1e6)
df_pih1_receive = df_pih1_receive[df_pih1_receive['Filtered packets'] != 0]["Filtered packets"]/(1e6)
df_pih2_receive = df_pih2_receive[df_pih2_receive['Filtered packets'] != 0]["Filtered packets"]/(1e6)

