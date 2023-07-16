# -*- coding: utf-8 -*-

import pandas as pd
import datetime
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None 

def bw(fp_pih1_send, fp_pih2_send, fp_pih1_receive, fp_pih2_receive):
    print(datetime.datetime.now(), "Import the data:")
    df_pih1_send = pd.read_csv(fp_pih1_send, sep=",")
    df_pih2_send = pd.read_csv(fp_pih2_send, sep=",")
    df_pih1_receive = pd.read_csv(fp_pih1_receive, sep=",")
    df_pih2_receive = pd.read_csv(fp_pih2_receive, sep=",")
    
    print(datetime.datetime.now(), "Reformat the data:")
    df_pih1_send = df_pih1_send[df_pih1_send['Filtered packets'] != 0]["Filtered packets"]/(1e6)
    df_pih2_send = df_pih2_send[df_pih2_send['Filtered packets'] != 0]["Filtered packets"]/(1e6)
    df_pih1_receive = df_pih1_receive[df_pih1_receive['Filtered packets'] != 0]["Filtered packets"]/(1e6)
    df_pih2_receive = df_pih2_receive[df_pih2_receive['Filtered packets'] != 0]["Filtered packets"]/(1e6)
    
    return df_pih1_send, df_pih2_send, df_pih1_receive, df_pih2_receive
    
def box_plot(data, edge_color, fill_color, labels):
    bp = ax.boxplot(data, patch_artist=True, showfliers=False, labels=labels)
    
    ax.grid(True)
    
    for element in ['boxes', 'whiskers', 'fliers', 'means', 'medians', 'caps']:
        plt.setp(bp[element], color=edge_color)

    for patch in bp['boxes']:
        patch.set(facecolor=fill_color)       
        
    return bp

if __name__ == "__main__":
    fp_baseline_pih1_send = "Baseline/pih1_Baseline_synchro_test_37BW.csv"
    fp_baseline_pih2_send = "Baseline/pih2_Baseline_synchro_test_37BW.csv"
    fp_baseline_pih1_receive = "Baseline/pi4_Baseline_synchro_test_37_pih1BW.csv"
    fp_baseline_pih2_receive = "Baseline/pi4_Baseline_synchro_test_37_pih2BW.csv"
    df_baseline_pih1_send, df_baseline_pih2_send, df_baseline_pih1_receive, df_baseline_pih2_receive= bw(fp_baseline_pih1_send, fp_baseline_pih2_send, fp_baseline_pih1_receive, fp_baseline_pih2_receive)
    
    fp_codelpp_pih1_send = "Codelpp/pih1_Codelpp_synchro_test_44_2BW.csv"
    fp_codelpp_pih2_send = "Codelpp/pih2_Codelpp_synchro_test_44_2BW.csv"
    fp_codelpp_pih1_receive = "Codelpp/pi4_Codelpp_synchro_test_44_2_pih1BW.csv"
    fp_codelpp_pih2_receive = "Codelpp/pi4_Codelpp_synchro_test_44_2_pih2BW.csv"
    df_codelpp_pih1_send, df_codelpp_pih2_send, df_codelpp_pih1_receive, df_codelpp_pih2_receive= bw(fp_codelpp_pih1_send, fp_codelpp_pih2_send, fp_codelpp_pih1_receive, fp_codelpp_pih2_receive)
    
    fp_synPrio4_pih1_send = "prio_4/pih1_SynCodelpp_synchro_test_39BW.csv"
    fp_synPrio4_pih2_send = "prio_4/pih2_SynCodelpp_synchro_test_39BW.csv"
    fp_synPrio4_pih1_receive = "prio_4/pi4_SynCodelpp_synchro_test_39_pih1BW.csv"
    fp_synPrio4_pih2_receive = "prio_4/pi4_SynCodelpp_synchro_test_39_pih2BW.csv"
    df_synPrio4_pih1_send, df_synPrio4_pih2_send, df_synPrio4_pih1_receive, df_synPrio4_pih2_receive= bw(fp_synPrio4_pih1_send, fp_synPrio4_pih2_send, fp_synPrio4_pih1_receive, fp_synPrio4_pih2_receive)
    
    fp_synPrio5_pih1_send = "prio_5/pih1_SynCodelpp_synchro_test_40BW.csv"
    fp_synPrio5_pih2_send = "prio_5/pih2_SynCodelpp_synchro_test_40BW.csv"
    fp_synPrio5_pih1_receive = "prio_5/pi4_SynCodelpp_synchro_test_40_pih1BW.csv"
    fp_synPrio5_pih2_receive = "prio_5/pi4_SynCodelpp_synchro_test_40_pih2BW.csv"
    df_synPrio5_pih1_send, df_synPrio5_pih2_send, df_synPrio5_pih1_receive, df_synPrio5_pih2_receive= bw(fp_synPrio5_pih1_send, fp_synPrio5_pih2_send, fp_synPrio5_pih1_receive, fp_synPrio5_pih2_receive)
    
    fp_synPrio6_pih1_send = "prio_6/pih1_SynCodelpp_synchro_test_43_2BW.csv"
    fp_synPrio6_pih2_send = "prio_6/pih2_SynCodelpp_synchro_test_43_2BW.csv"
    fp_synPrio6_pih1_receive = "prio_6/pi4_SynCodelpp_synchro_test_43_2_pih1BW.csv"
    fp_synPrio6_pih2_receive = "prio_6/pi4_SynCodelpp_synchro_test_43_2_pih2BW.csv"
    df_synPrio6_pih1_send, df_synPrio6_pih2_send, df_synPrio6_pih1_receive, df_synPrio6_pih2_receive= bw(fp_synPrio6_pih1_send, fp_synPrio6_pih2_send, fp_synPrio6_pih1_receive, fp_synPrio6_pih2_receive)
    
    fp_synPrio7_pih1_send = "prio_7/pih1_SynCodelpp_synchro_test_42_4BW.csv"
    fp_synPrio7_pih2_send = "prio_7/pih2_SynCodelpp_synchro_test_42_4BW.csv"
    fp_synPrio7_pih1_receive = "prio_7/pi4_SynCodelpp_synchro_test_42_4_pih1BW.csv"
    fp_synPrio7_pih2_receive = "prio_7/pi4_SynCodelpp_synchro_test_42_4_pih2BW.csv"
    df_synPrio7_pih1_send, df_synPrio7_pih2_send, df_synPrio7_pih1_receive, df_synPrio7_pih2_receive= bw(fp_synPrio7_pih1_send, fp_synPrio7_pih2_send, fp_synPrio7_pih1_receive, fp_synPrio7_pih2_receive)

    #Haptic BW
    dfs_haptic = [df_synPrio5_pih1_send, df_baseline_pih1_receive, df_codelpp_pih1_receive, df_synPrio4_pih1_receive, df_synPrio5_pih1_receive, df_synPrio6_pih1_receive, df_synPrio7_pih1_receive]
    
    fig, ax = plt.subplots(figsize=(14, 6))
        
    labels = ["Send","Baseline", "Codelpp","SynCodelpp prio=4","SynCodelpp prio=5","SynCodelpp prio=6","SynCodelpp prio=7"]
    boxplots_h = box_plot(dfs_haptic, 'red', 'tan', labels)
    
    # Set y-axis label
    ax.set_ylabel('Bandwidth (MB)')
    
    # Set plot title
    plt.title('Bandwidth of Haptic Flow: Target Priority as Variable')

    ax.yaxis.set_major_locator(plt.MultipleLocator(base=0.025)) 
    plt.show()
    
    #Video BW
    dfs_video = [df_synPrio5_pih2_send, df_baseline_pih2_receive, df_codelpp_pih2_receive, df_synPrio4_pih2_receive, df_synPrio5_pih2_receive, df_synPrio6_pih2_receive, df_synPrio7_pih2_receive]
    
    fig, ax = plt.subplots(figsize=(14, 6))
        
    labels = ["Send","Baseline", "Codelpp","SynCodelpp prio=4","SynCodelpp prio=5","SynCodelpp prio=6","SynCodelpp prio=7"]
    boxplots_v = box_plot(dfs_video, 'blue', 'cyan', labels)
    
    # Set y-axis label
    ax.set_ylabel('Bandwidth (MB)')
    
    # Set plot title
    plt.title('Bandwidth of Video Flow: Target Priority as Variable')

    #ax.yaxis.set_major_locator(plt.MultipleLocator(base=0.025)) 
    plt.show()