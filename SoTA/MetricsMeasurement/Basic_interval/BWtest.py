# -*- coding: utf-8 -*-

import pandas as pd
import datetime
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None 

fp_inter3_pih1_send = "inter3/pih1_SynCodelpp_synchro_test_42_4.csv"
fp_inter3_pih2_send = "inter3/pih2_SynCodelpp_synchro_test_42_4.csv"
fp_inter3_pih1_receive = "inter3/pi4_SynCodelpp_synchro_test_42_4_pih1.csv"
fp_inter3_pih2_receive = "inter3/pi4_SynCodelpp_synchro_test_42_4_pih2.csv"

print(datetime.datetime.now(), "Import the data:")
df_pih1_send = pd.read_csv(fp_inter3_pih1_send, sep=",")
df_pih2_send = pd.read_csv(fp_inter3_pih2_send, sep=",")
df_pih1_receive = pd.read_csv(fp_inter3_pih1_receive, sep=",")
df_pih2_receive = pd.read_csv(fp_inter3_pih2_receive, sep=",")

print(datetime.datetime.now(), "Reformat the data:")
df_pih1_send = df_pih1_send[df_pih1_send['Filtered packets'] != 0]["Filtered packets"]/(1e6)
df_pih2_send = df_pih2_send[df_pih2_send['Filtered packets'] != 0]["Filtered packets"]/(1e6)
df_pih1_receive = df_pih1_receive[df_pih1_receive['Filtered packets'] != 0]["Filtered packets"]/(1e6)
df_pih2_receive = df_pih2_receive[df_pih2_receive['Filtered packets'] != 0]["Filtered packets"]/(1e6)