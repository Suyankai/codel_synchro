# -*- coding: utf-8 -*-

import pandas as pd
import datetime
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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
    bp = ax.boxplot(data, patch_artist=True, showfliers=False, labels=labels, widths=0.6)
    
    #ax.grid(True)
    
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
    
    fp_codel_pih1_send = "Codel/pih1_Codelpp_synchro_test_91_6.csv"
    fp_codel_pih2_send = "Codel/pih2_Codelpp_synchro_test_91_6.csv"
    fp_codel_pih1_receive = "Codel/pi4_Codelpp_synchro_test_91_6_pih1.csv"
    fp_codel_pih2_receive = "Codel/pi4_Codelpp_synchro_test_91_6_pih2.csv"
    codel_pkt_loss_pih1, codel_pkt_loss_pih2, codel_df_pih1_receive, codel_df_pih2_receive, codel_avr_pih1_latency = latency_pktLoss(fp_codel_pih1_send, fp_codel_pih2_send, fp_codel_pih1_receive, fp_codel_pih2_receive)
    
    
    fp_codelpp_pih1_send = "Codelpp/pih1_Codelpp_synchro_test_44_2.csv"
    fp_codelpp_pih2_send = "Codelpp/pih2_Codelpp_synchro_test_44_2.csv"
    fp_codelpp_pih1_receive = "Codelpp/pi4_Codelpp_synchro_test_44_2_pih1.csv"
    fp_codelpp_pih2_receive = "Codelpp/pi4_Codelpp_synchro_test_44_2_pih2.csv"
    codelpp_pkt_loss_pih1, codelpp_pkt_loss_pih2, codelpp_df_pih1_receive, codelpp_df_pih2_receive, codelpp_avr_pih1_latency = latency_pktLoss(fp_codelpp_pih1_send, fp_codelpp_pih2_send, fp_codelpp_pih1_receive, fp_codelpp_pih2_receive)
    
    fp_inter3_pih1_send = "inter3/pih1_SynCodelpp_synchro_test_42_4.csv"
    fp_inter3_pih2_send = "inter3/pih2_SynCodelpp_synchro_test_42_4.csv"
    fp_inter3_pih1_receive = "inter3/pi4_SynCodelpp_synchro_test_42_4_pih1.csv"
    fp_inter3_pih2_receive = "inter3/pi4_SynCodelpp_synchro_test_42_4_pih2.csv"
    inter3_pkt_loss_pih1, inter3_pkt_loss_pih2, inter3_df_pih1_receive, inter3_df_pih2_receive, inter3_avr_pih1_latency= latency_pktLoss(fp_inter3_pih1_send, fp_inter3_pih2_send, fp_inter3_pih1_receive, fp_inter3_pih2_receive)
    
    fp_inter5_pih1_send = "inter5/pih1_SynCodelpp_synchro_test_46_1.csv"
    fp_inter5_pih2_send = "inter5/pih2_SynCodelpp_synchro_test_46_1.csv"
    fp_inter5_pih1_receive = "inter5/pi4_SynCodelpp_synchro_test_46_1_pih1.csv"
    fp_inter5_pih2_receive = "inter5/pi4_SynCodelpp_synchro_test_46_1_pih2.csv"
    inter5_pkt_loss_pih1, inter5_pkt_loss_pih2, inter5_df_pih1_receive, inter5_df_pih2_receive, inter5_avr_pih1_latency = latency_pktLoss(fp_inter5_pih1_send, fp_inter5_pih2_send, fp_inter5_pih1_receive, fp_inter5_pih2_receive)
    
    fp_inter7_pih1_send = "inter7/pih1_SynCodelpp_synchro_test_48_3.csv"
    fp_inter7_pih2_send = "inter7/pih2_SynCodelpp_synchro_test_48_3.csv"
    fp_inter7_pih1_receive = "inter7/pi4_SynCodelpp_synchro_test_48_3_pih1.csv"
    fp_inter7_pih2_receive = "inter7/pi4_SynCodelpp_synchro_test_48_3_pih2.csv"
    inter7_pkt_loss_pih1, inter7_pkt_loss_pih2, inter7_df_pih1_receive, inter7_df_pih2_receive, inter7_avr_pih1_latency = latency_pktLoss(fp_inter7_pih1_send, fp_inter7_pih2_send, fp_inter7_pih1_receive, fp_inter7_pih2_receive)
 
    
    fp_inter10_pih1_send = "inter10/pih1_SynCodelpp_synchro_test_47_4.csv"
    fp_inter10_pih2_send = "inter10/pih2_SynCodelpp_synchro_test_47_4.csv"
    fp_inter10_pih1_receive = "inter10/pi4_SynCodelpp_synchro_test_47_4_pih1.csv"
    fp_inter10_pih2_receive = "inter10/pi4_SynCodelpp_synchro_test_47_4_pih2.csv"
    inter10_pkt_loss_pih1, inter10_pkt_loss_pih2, inter10_df_pih1_receive, inter10_df_pih2_receive , inter10_avr_pih1_latency= latency_pktLoss(fp_inter10_pih1_send, fp_inter10_pih2_send, fp_inter10_pih1_receive, fp_inter10_pih2_receive)
    
    fp_inter15_pih1_send = "inter15/pih1_SynCodelpp_synchro_test_49_4.csv"
    fp_inter15_pih2_send = "inter15/pih2_SynCodelpp_synchro_test_49_4.csv"
    fp_inter15_pih1_receive = "inter15/pi4_SynCodelpp_synchro_test_49_4_pih1.csv"
    fp_inter15_pih2_receive = "inter15/pi4_SynCodelpp_synchro_test_49_4_pih2.csv"
    inter15_pkt_loss_pih1, inter15_pkt_loss_pih2, inter15_df_pih1_receive, inter15_df_pih2_receive, inter15_avr_pih1_latency = latency_pktLoss(fp_inter15_pih1_send, fp_inter15_pih2_send, fp_inter15_pih1_receive, fp_inter15_pih2_receive)
    
    dfs = [baseline_df_pih1_receive, baseline_df_pih2_receive, codel_df_pih1_receive, codel_df_pih2_receive, codelpp_df_pih1_receive, codelpp_df_pih2_receive, inter3_df_pih1_receive, inter3_df_pih2_receive, inter5_df_pih1_receive, inter5_df_pih2_receive, inter7_df_pih1_receive, inter7_df_pih2_receive, inter10_df_pih1_receive, inter10_df_pih2_receive, inter15_df_pih1_receive, inter15_df_pih2_receive]
    
    latency_values_haptic = []
    latency_values_haptic_only = []
    latency_values_video = []
    
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
    fig, ax = plt.subplots(figsize=(13, 6))
        
    boxplot_labels = ["                   Baseline","","                   Codel","", "                   Codelpp","","                    THRE=3ms","","                    THRE=5ms","","                    THRE=7ms","","                    THRE=10ms","","                    THRE=15ms",""]
    
    boxplots1 = box_plot(latency_values_haptic, 'red', 'tan', boxplot_labels)
    boxplots2 = box_plot(latency_values_video, 'blue', 'cyan', boxplot_labels)
    ax.legend([boxplots1["boxes"][0], boxplots2["boxes"][0]], ['Haptic', 'Video'])
    
    # Set y-axis label
    ax.set_ylabel('Latency (ms)')
    
    # Set plot title
    plt.title('Latency of Haptic and Video Flow: THRE as Variable')
    
    # Add vertical line to separate the groups
    ax.axvline(x=2.5, color='gray', linestyle='--')
    ax.axvline(x=4.5, color='gray', linestyle='--')
    ax.axvline(x=6.5, color='gray', linestyle='--')
    ax.axvline(x=8.5, color='gray', linestyle='--')
    ax.axvline(x=10.5, color='gray', linestyle='--')
    ax.axvline(x=12.5, color='gray', linestyle='--')
    ax.axvline(x=14.5, color='gray', linestyle='--')
    
    #ax.yaxis.set_major_locator(plt.MultipleLocator(base=500)) 
    
    # Display the plot
    plt.yscale("log")
    plt.xticks([]) 
    plt.show()
    
    #Try2
    grouped_dfs = pd.DataFrame()
    group = []
    latency = []
    sender = []
    
    i=0
    for df in dfs:
        for j in range(len(df)):
           if i == 0 :
                   group.append("Baseline")
                   latency.append(df["Latency"][j])
                   sender.append("Haptic") 
           elif i == 1:
               group.append("Baseline")
               latency.append(df["Latency"][j])
               sender.append("Video") 
           elif i == 2:
               group.append("Codel")
               latency.append(df["Latency"][j])
               sender.append("Haptic") 
           elif i == 3:
               group.append("Codel")
               latency.append(df["Latency"][j])
               sender.append("Video") 
           elif i == 4:
               group.append("Codelpp")
               latency.append(df["Latency"][j])
               sender.append("Haptic") 
           elif i == 5:
               group.append("Codelpp")
               latency.append(df["Latency"][j])
               sender.append("Video") 
           elif i == 6:
               group.append("THRE=3ms")
               latency.append(df["Latency"][j])
               sender.append("Haptic") 
           elif i == 7:
               group.append("THRE=3ms")
               latency.append(df["Latency"][j])
               sender.append("Video") 
           elif i == 8:
               group.append("THRE=5ms")
               latency.append(df["Latency"][j])
               sender.append("Haptic")
           elif i == 9:
               group.append("THRE=5ms")
               latency.append(df["Latency"][j])
               sender.append("Video") 
           elif i == 10:
               group.append("THRE=7ms")
               latency.append(df["Latency"][j])
               sender.append("Haptic")
           elif i == 11:
               group.append("THRE=7ms")
               latency.append(df["Latency"][j])
               sender.append("Video") 
           elif i == 12:
               group.append("THRE=10ms")
               latency.append(df["Latency"][j])
               sender.append("Haptic")
           elif i == 13:
               group.append("THRE=10ms")
               latency.append(df["Latency"][j])
               sender.append("Video") 
           elif i == 14:
               group.append("THRE=15ms")
               latency.append(df["Latency"][j])
               sender.append("Haptic")
           elif i == 15:
               group.append("THRE=15ms")
               latency.append(df["Latency"][j])
               sender.append("Video") 
        i = i+1
    
    
    grouped_dfs["Group"] = group
    grouped_dfs["Latency (ms)"] = latency
    grouped_dfs["Sender"] = sender
    plt.rcParams["figure.autolayout"] = True
    
    fig, ax = plt.subplots(figsize=(10, 6))
    # plt.figure(figsize=(10, 6))
    sns.boxplot(x=grouped_dfs["Group"], y=grouped_dfs["Latency (ms)"], hue=grouped_dfs["Sender"],showfliers = False,palette="colorblind")

    ax.axvline(x=2.5, color='black', linestyle='-', linewidth=1)
    plt.yscale("log")
    plt.show()
    

    
    #pkt lost evaluation
    # Sample data
    values = [baseline_pkt_loss_pih1, baseline_pkt_loss_pih2, codel_pkt_loss_pih1, codel_pkt_loss_pih2, codelpp_pkt_loss_pih1, codelpp_pkt_loss_pih2, inter3_pkt_loss_pih1,inter3_pkt_loss_pih2, inter5_pkt_loss_pih1,inter5_pkt_loss_pih2, inter7_pkt_loss_pih1,inter7_pkt_loss_pih2,inter10_pkt_loss_pih1,inter10_pkt_loss_pih2, inter15_pkt_loss_pih1, inter15_pkt_loss_pih2]
    
    # Create a Figure and Axes object
    fig, ax = plt.subplots(figsize=(19, 6))
    
    # Plotting the histogram
    ax.bar(range(len(values)), values, width=0.6)
    
    # Adding labels and title
    ax.set_ylabel('Packet loss rate (%)')
    ax.set_title('Packet Loss Rate of Haptic and Video Flow: THRE as Variable')
    
    # Customizing x-axis tick labels
    ax.set_xticks(range(len(values)))
    ax.set_xticklabels(boxplot_labels)
    
    # Add vertical line to separate the groups
    ax.axvline(x=1.5, color='gray', linestyle='--')
    ax.axvline(x=3.5, color='gray', linestyle='--')
    ax.axvline(x=5.5, color='gray', linestyle='--')
    ax.axvline(x=7.5, color='gray', linestyle='--')
    ax.axvline(x=9.5, color='gray', linestyle='--')
    ax.axvline(x=11.5, color='gray', linestyle='--')
    ax.axvline(x=13.5, color='gray', linestyle='--')
    
    ax.yaxis.set_major_locator(plt.MultipleLocator(base=10)) 
    
    #ax.grid(True)
    
    # Display the plot
    plt.show()
    
    #Try2
    grouped_dfs = pd.DataFrame()
    group = []
    pkt_lost = []
    sender = []
    
    for i in range(len(values)):
        if i == 0 :
            group.append("Baseline")
            pkt_lost.append(values[i])
            sender.append("Haptic") 
        elif i == 1:
            group.append("Baseline")
            pkt_lost.append(values[i])
            sender.append("Video") 
        elif i == 2:
            group.append("Codel")
            pkt_lost.append(values[i])
            sender.append("Haptic") 
        elif i == 3:
            group.append("Codel")
            pkt_lost.append(values[i])
            sender.append("Video") 
        elif i == 4:
            group.append("Codelpp")
            pkt_lost.append(values[i])
            sender.append("Haptic") 
        elif i == 5:
            group.append("Codelpp")
            pkt_lost.append(values[i])
            sender.append("Video") 
        elif i == 6:
            group.append("THRE=3ms")
            pkt_lost.append(values[i])
            sender.append("Haptic") 
        elif i == 7:
            group.append("THRE=3ms")
            pkt_lost.append(values[i])
            sender.append("Video") 
        elif i == 8:
            group.append("THRE=5ms")
            pkt_lost.append(values[i])
            sender.append("Haptic")
        elif i == 9:
            group.append("THRE=5ms")
            pkt_lost.append(values[i])
            sender.append("Video") 
        elif i == 10:
            group.append("THRE=7ms")
            pkt_lost.append(values[i])
            sender.append("Haptic")
        elif i == 11:
            group.append("THRE=7ms")
            pkt_lost.append(values[i])
            sender.append("Video") 
        elif i == 12:
            group.append("THRE=10ms")
            pkt_lost.append(values[i])
            sender.append("Haptic")
        elif i == 13:
            group.append("THRE=10ms")
            pkt_lost.append(values[i])
            sender.append("Video") 
        elif i == 14:
            group.append("THRE=15ms")
            pkt_lost.append(values[i])
            sender.append("Haptic")
        elif i == 15:
            group.append("THRE=15ms")
            pkt_lost.append(values[i])
            sender.append("Video") 

    grouped_dfs["Group"] = group
    grouped_dfs["Pkt lost rate (%)"] = pkt_lost
    grouped_dfs["Sender"] = sender
    plt.rcParams["figure.autolayout"] = True
    
    fig, ax = plt.subplots(figsize=(8.5, 4))
    # plt.figure(figsize=(10, 6))
    sns.barplot(x=grouped_dfs["Group"], y=grouped_dfs["Pkt lost rate (%)"], hue=grouped_dfs["Sender"], palette="colorblind")

    ax.axvline(x=2.5, color='black', linestyle='-', linewidth=1)
    plt.show()