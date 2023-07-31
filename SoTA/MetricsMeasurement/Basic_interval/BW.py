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
    
    fp_codel_pih1_send = "Codel/pih1_Codelpp_synchro_test_91_6BW.csv"
    fp_codel_pih2_send = "Codel/pih2_Codelpp_synchro_test_91_6BW.csv"
    fp_codel_pih1_receive = "Codel/pi4_Codelpp_synchro_test_91_6_pih1BW.csv"
    fp_codel_pih2_receive = "Codel/pi4_Codelpp_synchro_test_91_6_pih2BW.csv"
    df_codel_pih1_send, df_codel_pih2_send, df_codel_pih1_receive, df_codel_pih2_receive= bw(fp_codel_pih1_send, fp_codel_pih2_send, fp_codel_pih1_receive, fp_codel_pih2_receive)
    
    
    fp_codelpp_pih1_send = "Codelpp/pih1_Codelpp_synchro_test_44_2BW.csv"
    fp_codelpp_pih2_send = "Codelpp/pih2_Codelpp_synchro_test_44_2BW.csv"
    fp_codelpp_pih1_receive = "Codelpp/pi4_Codelpp_synchro_test_44_2_pih1BW.csv"
    fp_codelpp_pih2_receive = "Codelpp/pi4_Codelpp_synchro_test_44_2_pih2BW.csv"
    df_codelpp_pih1_send, df_codelpp_pih2_send, df_codelpp_pih1_receive, df_codelpp_pih2_receive= bw(fp_codelpp_pih1_send, fp_codelpp_pih2_send, fp_codelpp_pih1_receive, fp_codelpp_pih2_receive)
    
    fp_inter3_pih1_send = "inter3/pih1_SynCodelpp_synchro_test_42_4BW.csv"
    fp_inter3_pih2_send = "inter3/pih2_SynCodelpp_synchro_test_42_4BW.csv"
    fp_inter3_pih1_receive = "inter3/pi4_SynCodelpp_synchro_test_42_4_pih1BW.csv"
    fp_inter3_pih2_receive = "inter3/pi4_SynCodelpp_synchro_test_42_4_pih2BW.csv"
    df_inter3_pih1_send, df_inter3_pih2_send, df_inter3_pih1_receive, df_inter3_pih2_receive= bw(fp_inter3_pih1_send, fp_inter3_pih2_send, fp_inter3_pih1_receive, fp_inter3_pih2_receive)
    
    fp_inter5_pih1_send = "inter5/pih1_SynCodelpp_synchro_test_46_1BW.csv"
    fp_inter5_pih2_send = "inter5/pih2_SynCodelpp_synchro_test_46_1BW.csv"
    fp_inter5_pih1_receive = "inter5/pi4_SynCodelpp_synchro_test_46_1_pih1BW.csv"
    fp_inter5_pih2_receive = "inter5/pi4_SynCodelpp_synchro_test_46_1_pih2BW.csv"
    df_inter5_pih1_send, df_inter5_pih2_send, df_inter5_pih1_receive, df_inter5_pih2_receive= bw(fp_inter5_pih1_send, fp_inter5_pih2_send, fp_inter5_pih1_receive, fp_inter5_pih2_receive)
    
    fp_inter7_pih1_send = "inter7/pih1_SynCodelpp_synchro_test_48_3BW.csv"
    fp_inter7_pih2_send = "inter7/pih2_SynCodelpp_synchro_test_48_3BW.csv"
    fp_inter7_pih1_receive = "inter7/pi4_SynCodelpp_synchro_test_48_3_pih1BW.csv"
    fp_inter7_pih2_receive = "inter7/pi4_SynCodelpp_synchro_test_48_3_pih2BW.csv"
    df_inter7_pih1_send, df_inter7_pih2_send, df_inter7_pih1_receive, df_inter7_pih2_receive= bw(fp_inter7_pih1_send, fp_inter7_pih2_send, fp_inter7_pih1_receive, fp_inter7_pih2_receive)
    
    fp_inter10_pih1_send = "inter10/pih1_SynCodelpp_synchro_test_47_4BW.csv"
    fp_inter10_pih2_send = "inter10/pih2_SynCodelpp_synchro_test_47_4BW.csv"
    fp_inter10_pih1_receive = "inter10/pi4_SynCodelpp_synchro_test_47_4_pih1BW.csv"
    fp_inter10_pih2_receive = "inter10/pi4_SynCodelpp_synchro_test_47_4_pih2BW.csv"
    df_inter10_pih1_send, df_inter10_pih2_send, df_inter10_pih1_receive, df_inter10_pih2_receive= bw(fp_inter10_pih1_send, fp_inter10_pih2_send, fp_inter10_pih1_receive, fp_inter10_pih2_receive)

    fp_inter15_pih1_send = "inter15/pih1_SynCodelpp_synchro_test_49_4BW.csv"
    fp_inter15_pih2_send = "inter15/pih2_SynCodelpp_synchro_test_49_4BW.csv"
    fp_inter15_pih1_receive = "inter15/pi4_SynCodelpp_synchro_test_49_4_pih1BW.csv"
    fp_inter15_pih2_receive = "inter15/pi4_SynCodelpp_synchro_test_49_4_pih2BW.csv"
    df_inter15_pih1_send, df_inter15_pih2_send, df_inter15_pih1_receive, df_inter15_pih2_receive= bw(fp_inter15_pih1_send, fp_inter15_pih2_send, fp_inter15_pih1_receive, fp_inter15_pih2_receive)

    #Haptic BW
    dfs_haptic = [df_inter5_pih1_send, df_baseline_pih1_receive, df_codel_pih1_receive, df_codelpp_pih1_receive, df_inter3_pih1_receive, df_inter5_pih1_receive, df_inter7_pih1_receive, df_inter10_pih1_receive, df_inter15_pih1_receive]
    
    fig, ax = plt.subplots(figsize=(20, 6))
        
    labels = ["Send","Baseline", "Codel", "Codelpp","SynCodelpp THRE=3ms","SynCodelpp THRE=5ms","SynCodelpp THRE=7ms","SynCodelpp THRE=10ms","SynCodelpp THRE=15ms"]
    boxplots_h = box_plot(dfs_haptic, 'red', 'tan', labels)
    
    # Set y-axis label
    ax.set_ylabel('Bandwidth (MB)')
    
    # Set plot title
    plt.title('Bandwidth of Haptic Flow: Target Priority as Variable')

    ax.yaxis.set_major_locator(plt.MultipleLocator(base=0.025)) 
    plt.show()
    
    #Video BW
    dfs_video = [df_inter5_pih2_send, df_baseline_pih2_receive, df_codel_pih2_receive, df_codelpp_pih2_receive, df_inter3_pih2_receive, df_inter5_pih2_receive, df_inter7_pih2_receive, df_inter10_pih2_receive, df_inter15_pih2_receive]
    
    fig, ax = plt.subplots(figsize=(20, 6))
        
    labels = ["Send","Baseline","Codel","Codelpp","SynCodelpp THRE=3ms","SynCodelpp THRE=5ms","SynCodelpp THRE=7ms","SynCodelpp THRE=10ms","SynCodelpp THRE=15ms"]
    boxplots_v = box_plot(dfs_video, 'blue', 'cyan', labels)
    
    # Set y-axis label
    ax.set_ylabel('Bandwidth (MB)')
    
    # Set plot title
    plt.title('Bandwidth of Video Flow: Target Priority as Variable')

    ax.yaxis.set_major_locator(plt.MultipleLocator(base=0.25)) 
    plt.show()