# -*- coding: utf-8 -*-

import pandas as pd
import datetime
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None 

def latency_pktLoss (fp_pih1_send, fp_pih2_send, fp_pih1_receive, fp_pih2_receive):
    print(datetime.datetime.now(), "Import the data:")
    df_pih1_send = pd.read_csv(fp_pih1_send, sep=",")
    df_pih2_send = pd.read_csv(fp_pih2_send, sep=",")
    df_pih1_receive = pd.read_csv(fp_pih1_receive, sep=",")
    df_pih2_receive = pd.read_csv(fp_pih2_receive, sep=",")

    print(datetime.datetime.now(), "Format the time in all dataset:")

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
    
    return pkt_loss_pih1, pkt_loss_pih2, df_pih1_receive, df_pih2_receive, avr_pih1_latency
    
def box_plot(data, edge_color, fill_color, labels):
    bp = ax.boxplot(data, patch_artist=True, showfliers=False, labels=labels)
    
    ax.grid(True)
    
    for element in ['boxes', 'whiskers', 'fliers', 'means', 'medians', 'caps']:
        plt.setp(bp[element], color=edge_color)

    for patch in bp['boxes']:
        patch.set(facecolor=fill_color)       
        
    return bp

def is_odd(number):
    if number % 2 == 1:
        return True
    else:
        return False

if __name__ == "__main__":
    fp_baseline_pih1_send = "Baseline/pih1_Baseline_synchro_test_37.csv"
    fp_baseline_pih2_send = "Baseline/pih2_Baseline_synchro_test_37.csv"
    fp_baseline_pih1_receive = "Baseline/pi4_Baseline_synchro_test_37_pih1.csv"
    fp_baseline_pih2_receive = "Baseline/pi4_Baseline_synchro_test_37_pih2.csv"
    baseline_pkt_loss_pih1, baseline_pkt_loss_pih2, baseline_df_pih1_receive, baseline_df_pih2_receive, baseline_avr_pih1_latency = latency_pktLoss(fp_baseline_pih1_send, fp_baseline_pih2_send, fp_baseline_pih1_receive, fp_baseline_pih2_receive)
    
    fp_codelpp_pih1_send = "Codelpp/pih1_Codelpp_synchro_test_44_2.csv"
    fp_codelpp_pih2_send = "Codelpp/pih2_Codelpp_synchro_test_44_2.csv"
    fp_codelpp_pih1_receive = "Codelpp/pi4_Codelpp_synchro_test_44_2_pih1.csv"
    fp_codelpp_pih2_receive = "Codelpp/pi4_Codelpp_synchro_test_44_2_pih2.csv"
    codelpp_pkt_loss_pih1, codelpp_pkt_loss_pih2, codelpp_df_pih1_receive, codelpp_df_pih2_receive, codelpp_avr_pih1_latency = latency_pktLoss(fp_codelpp_pih1_send, fp_codelpp_pih2_send, fp_codelpp_pih1_receive, fp_codelpp_pih2_receive)
    
    fp_synPrio4_pih1_send = "prio_4/pih1_SynCodelpp_synchro_test_39.csv"
    fp_synPrio4_pih2_send = "prio_4/pih2_SynCodelpp_synchro_test_39.csv"
    fp_synPrio4_pih1_receive = "prio_4/pi4_SynCodelpp_synchro_test_39_pih1.csv"
    fp_synPrio4_pih2_receive = "prio_4/pi4_SynCodelpp_synchro_test_39_pih2.csv"
    synPrio4_pkt_loss_pih1, synPrio4_pkt_loss_pih2, synPrio4_df_pih1_receive, synPrio4_df_pih2_receive, synPrio4_avr_pih1_latency= latency_pktLoss(fp_synPrio4_pih1_send, fp_synPrio4_pih2_send, fp_synPrio4_pih1_receive, fp_synPrio4_pih2_receive)
    
    fp_synPrio5_pih1_send = "prio_5/pih1_SynCodelpp_synchro_test_40.csv"
    fp_synPrio5_pih2_send = "prio_5/pih2_SynCodelpp_synchro_test_40.csv"
    fp_synPrio5_pih1_receive = "prio_5/pi4_SynCodelpp_synchro_test_40_pih1.csv"
    fp_synPrio5_pih2_receive = "prio_5/pi4_SynCodelpp_synchro_test_40_pih2.csv"
    synPrio5_pkt_loss_pih1, synPrio5_pkt_loss_pih2, synPrio5_df_pih1_receive, synPrio5_df_pih2_receive, synPrio5_avr_pih1_latency = latency_pktLoss(fp_synPrio5_pih1_send, fp_synPrio5_pih2_send, fp_synPrio5_pih1_receive, fp_synPrio5_pih2_receive)
    
    fp_synPrio6_pih1_send = "prio_6/pih1_SynCodelpp_synchro_test_43_2.csv"
    fp_synPrio6_pih2_send = "prio_6/pih2_SynCodelpp_synchro_test_43_2.csv"
    fp_synPrio6_pih1_receive = "prio_6/pi4_SynCodelpp_synchro_test_43_2_pih1.csv"
    fp_synPrio6_pih2_receive = "prio_6/pi4_SynCodelpp_synchro_test_43_2_pih2.csv"
    synPrio6_pkt_loss_pih1, synPrio6_pkt_loss_pih2, synPrio6_df_pih1_receive, synPrio6_df_pih2_receive , synPrio6_avr_pih1_latency= latency_pktLoss(fp_synPrio6_pih1_send, fp_synPrio6_pih2_send, fp_synPrio6_pih1_receive, fp_synPrio6_pih2_receive)
    
    fp_synPrio7_pih1_send = "prio_7/pih1_SynCodelpp_synchro_test_42_4.csv"
    fp_synPrio7_pih2_send = "prio_7/pih2_SynCodelpp_synchro_test_42_4.csv"
    fp_synPrio7_pih1_receive = "prio_7/pi4_SynCodelpp_synchro_test_42_4_pih1.csv"
    fp_synPrio7_pih2_receive = "prio_7/pi4_SynCodelpp_synchro_test_42_4_pih2.csv"
    synPrio7_pkt_loss_pih1, synPrio7_pkt_loss_pih2, synPrio7_df_pih1_receive, synPrio7_df_pih2_receive, synPrio7_avr_pih1_latency = latency_pktLoss(fp_synPrio7_pih1_send, fp_synPrio7_pih2_send, fp_synPrio7_pih1_receive, fp_synPrio7_pih2_receive)
    
    dfs = [baseline_df_pih1_receive, baseline_df_pih2_receive, codelpp_df_pih1_receive, codelpp_df_pih2_receive, synPrio4_df_pih1_receive, synPrio4_df_pih2_receive, synPrio5_df_pih1_receive, synPrio5_df_pih2_receive, synPrio6_df_pih1_receive, synPrio6_df_pih2_receive, synPrio7_df_pih1_receive, synPrio7_df_pih2_receive]
    
    latency_values_haptic = []
    latency_values_haptic_only = []
    latency_values_video = []

    # Draw the seperate haptic
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, df in enumerate(dfs):
        if i == 0:
            continue
        if not is_odd(i):
            latency_values_haptic_only.append(df['Latency'][df['Latency'].notna()])
        
    haptic_only_labels = ["Codelpp","SynCodelpp prio=4","SynCodelpp prio=5","SynCodelpp prio=6","SynCodelpp prio=7"]
    boxplots_h = box_plot(latency_values_haptic_only, 'red', 'tan',haptic_only_labels)
    
    # Set y-axis label
    ax.set_ylabel('Latency (ms)')
    
    # Set plot title
    plt.title('Latency of Haptic Flow: Target Priority as Variable')
    
    # Add a line graph
    # h_values = [codelpp_avr_pih1_latency, synPrio4_avr_pih1_latency, synPrio5_avr_pih1_latency, synPrio6_avr_pih1_latency, synPrio7_avr_pih1_latency]  
    # ax.plot(h_values, marker='o', linestyle='-', color='blue', label='Line Graph')
    
    ax.yaxis.set_major_locator(plt.MultipleLocator(base=10)) 
    plt.show()
    
    
    
    # Latency evaluation
    empty_series = pd.Series()
    for i, df in enumerate(dfs):
        if is_odd(i):
            latency_values_video.append(empty_series)
            latency_values_video.append(df['Latency'][df['Latency'].notna()])
        else:
            latency_values_haptic.append(df['Latency'][df['Latency'].notna()])
            latency_values_haptic.append(empty_series)
    
   # Create a figure and axis object
    fig, ax = plt.subplots(figsize=(12, 6))
        
    boxplot_labels = ["               Baseline","","               Codelpp","","                SynCodelpp pri=4","","                SynCodelpp pri=5","","                SynCodelpp pri=6","","                SynCodelpp pri=7",""]
    
    boxplots1 = box_plot(latency_values_haptic, 'red', 'tan', boxplot_labels)
    boxplots2 = box_plot(latency_values_video, 'blue', 'cyan', boxplot_labels)
    ax.legend([boxplots1["boxes"][0], boxplots2["boxes"][0]], ['Haptic', 'Video'])
    
    # Set y-axis label
    ax.set_ylabel('Latency (ms)')
    
    # Set plot title
    plt.title('Latency of Haptic and Video Flow: Target Priority as Variable')
    
    # Add vertical line to separate the groups
    ax.axvline(x=2.5, color='gray', linestyle='--')
    ax.axvline(x=4.5, color='gray', linestyle='--')
    ax.axvline(x=6.5, color='gray', linestyle='--')
    ax.axvline(x=8.5, color='gray', linestyle='--')
    ax.axvline(x=10.5, color='gray', linestyle='--')
    
    ax.yaxis.set_major_locator(plt.MultipleLocator(base=500)) 
    
    # Display the plot
    plt.show()
    
    
    #pkt lost evaluation
    # Sample data
    values = [baseline_pkt_loss_pih1, baseline_pkt_loss_pih2, codelpp_pkt_loss_pih1, codelpp_pkt_loss_pih2, synPrio4_pkt_loss_pih1,synPrio4_pkt_loss_pih2, synPrio5_pkt_loss_pih1,synPrio5_pkt_loss_pih2, synPrio6_pkt_loss_pih1,synPrio6_pkt_loss_pih2, synPrio7_pkt_loss_pih1, synPrio7_pkt_loss_pih2]
    
    # Create a Figure and Axes object
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plotting the histogram
    ax.bar(range(len(values)), values, width=0.6)
    
    # Adding labels and title
    ax.set_ylabel('Packet loss rate (%)')
    ax.set_title('Packet Loss Rate of Haptic and Video Flow: Target Priority as Variable')
    
    # Customizing x-axis tick labels
    ax.set_xticks(range(len(values)))
    ax.set_xticklabels(boxplot_labels)
    
    # Add vertical line to separate the groups
    ax.axvline(x=1.5, color='gray', linestyle='--')
    ax.axvline(x=3.5, color='gray', linestyle='--')
    ax.axvline(x=5.5, color='gray', linestyle='--')
    ax.axvline(x=7.5, color='gray', linestyle='--')
    ax.axvline(x=9.5, color='gray', linestyle='--')
    
    ax.yaxis.set_major_locator(plt.MultipleLocator(base=1)) 
    
    ax.grid(True)
    
    # Display the plot
    plt.show()