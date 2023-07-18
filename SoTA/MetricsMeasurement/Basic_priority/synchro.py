# -*- coding: utf-8 -*-
import pandas as pd
import datetime
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None 

def synchro(fp_pih1_send, fp_pih2_send, fp_pih1_receive, fp_pih2_receive):
    print(datetime.datetime.now(), "Import the data:")
    df_pih1_send = pd.read_csv(fp_pih1_send, sep=",")
    df_pih2_send = pd.read_csv(fp_pih2_send, sep=",")
    df_pih1_receive = pd.read_csv(fp_pih1_receive, sep=",")
    df_pih2_receive = pd.read_csv(fp_pih2_receive, sep=",")
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
        if abs((pih1_send_indicator - closest_time_pih2)).total_seconds() * 1000 > 1.5:
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
            
    return df_pair_receive['Synchro_receive'][df_pair_receive['Synchro_receive'].notna()]

def box_plot(data, edge_color, fill_color, labels):
    bp = ax.boxplot(data, patch_artist=True, showfliers=False, labels=labels)
    
    ax.grid(True)
    
    for element in ['boxes', 'whiskers', 'fliers', 'means', 'medians', 'caps']:
        plt.setp(bp[element], color=edge_color)

    for patch in bp['boxes']:
        patch.set(facecolor=fill_color)       
        
    return bp

if __name__ == "__main__":
    fp_baseline_pih1_send = "Baseline/pih1_Baseline_synchro_test_37.csv"
    fp_baseline_pih2_send = "Baseline/pih2_Baseline_synchro_test_37.csv"
    fp_baseline_pih1_receive = "Baseline/pi4_Baseline_synchro_test_37_pih1.csv"
    fp_baseline_pih2_receive = "Baseline/pi4_Baseline_synchro_test_37_pih2.csv"
    df_baseline = synchro(fp_baseline_pih1_send, fp_baseline_pih2_send, fp_baseline_pih1_receive, fp_baseline_pih2_receive)
  
    fp_codelpp_pih1_send = "Codelpp/pih1_Codelpp_synchro_test_44_2.csv"
    fp_codelpp_pih2_send = "Codelpp/pih2_Codelpp_synchro_test_44_2.csv"
    fp_codelpp_pih1_receive = "Codelpp/pi4_Codelpp_synchro_test_44_2_pih1.csv"
    fp_codelpp_pih2_receive = "Codelpp/pi4_Codelpp_synchro_test_44_2_pih2.csv"
    df_codelpp = synchro(fp_codelpp_pih1_send, fp_codelpp_pih2_send, fp_codelpp_pih1_receive, fp_codelpp_pih2_receive)
   
    fp_synPrio4_pih1_send = "prio_4/pih1_SynCodelpp_synchro_test_39.csv"
    fp_synPrio4_pih2_send = "prio_4/pih2_SynCodelpp_synchro_test_39.csv"
    fp_synPrio4_pih1_receive = "prio_4/pi4_SynCodelpp_synchro_test_39_pih1.csv"
    fp_synPrio4_pih2_receive = "prio_4/pi4_SynCodelpp_synchro_test_39_pih2.csv"
    df_synPrio4 = synchro(fp_synPrio4_pih1_send, fp_synPrio4_pih2_send, fp_synPrio4_pih1_receive, fp_synPrio4_pih2_receive)
   
    fp_synPrio5_pih1_send = "prio_5/pih1_SynCodelpp_synchro_test_40.csv"
    fp_synPrio5_pih2_send = "prio_5/pih2_SynCodelpp_synchro_test_40.csv"
    fp_synPrio5_pih1_receive = "prio_5/pi4_SynCodelpp_synchro_test_40_pih1.csv"
    fp_synPrio5_pih2_receive = "prio_5/pi4_SynCodelpp_synchro_test_40_pih2.csv"
    df_synPrio5 = synchro(fp_synPrio5_pih1_send, fp_synPrio5_pih2_send, fp_synPrio5_pih1_receive, fp_synPrio5_pih2_receive)
    
    fp_synPrio6_pih1_send = "prio_6/pih1_SynCodelpp_synchro_test_43_2.csv"
    fp_synPrio6_pih2_send = "prio_6/pih2_SynCodelpp_synchro_test_43_2.csv"
    fp_synPrio6_pih1_receive = "prio_6/pi4_SynCodelpp_synchro_test_43_2_pih1.csv"
    fp_synPrio6_pih2_receive = "prio_6/pi4_SynCodelpp_synchro_test_43_2_pih2.csv"
    df_synPrio6 = synchro(fp_synPrio6_pih1_send, fp_synPrio6_pih2_send, fp_synPrio6_pih1_receive, fp_synPrio6_pih2_receive)
   
    fp_synPrio7_pih1_send = "prio_7/pih1_SynCodelpp_synchro_test_42_4.csv"
    fp_synPrio7_pih2_send = "prio_7/pih2_SynCodelpp_synchro_test_42_4.csv"
    fp_synPrio7_pih1_receive = "prio_7/pi4_SynCodelpp_synchro_test_42_4_pih1.csv"
    fp_synPrio7_pih2_receive = "prio_7/pi4_SynCodelpp_synchro_test_42_4_pih2.csv"
    df_synPrio7 = synchro(fp_synPrio7_pih1_send, fp_synPrio7_pih2_send, fp_synPrio7_pih1_receive, fp_synPrio7_pih2_receive)
    
    dfs = [df_baseline, df_codelpp, df_synPrio4, df_synPrio5, df_synPrio6, df_synPrio7]
    
    fig, ax = plt.subplots(figsize=(12, 6))
        
    labels = ["Baseline", "Codelpp","SynCodelpp PRIO=4","SynCodelpp PRIO=5","SynCodelpp PRIO=6","SynCodelpp PRIO=7"]
    boxplots_h = box_plot(dfs, 'red', 'tan', labels)
    
    # Set y-axis label
    ax.set_ylabel('Sycnhronization Difference (ms)')
    
    # Set plot title
    plt.title('Sycnhronization Difference between Haptic & Video Flow: Target Priority as Variable')
    
    # Add a line graph
    # h_values = [codelpp_avr_pih1_latency, synPrio4_avr_pih1_latency, synPrio5_avr_pih1_latency, synPrio6_avr_pih1_latency, synPrio7_avr_pih1_latency]  
    # ax.plot(h_values, marker='o', linestyle='-', color='blue', label='Line Graph')
    
    ax.yaxis.set_major_locator(plt.MultipleLocator(base=50)) 
    plt.show()
   

