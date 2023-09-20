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
            
            #log
            #df_pair_receive['Synchro_receive'][i] = np.log(df_pair_receive['Synchro_receive'][i])
            df_pair_receive['Synchro_receive'][i] = df_pair_receive['Synchro_receive'][i]
            
    return df_pair_receive['Synchro_receive'][df_pair_receive['Synchro_receive'].notna()]

def box_plot(data, edge_color, fill_color, labels):
    bp = ax.boxplot(data, patch_artist=True, vert=True, showfliers=False, labels=labels)
    #bp = ax.boxplot(data, patch_artist=True, vert=False, showfliers=False, labels=labels)
    
    #ax.grid(True)
    
    #for element in ['boxes', 'whiskers', 'fliers', 'means', 'medians', 'caps']:
    for element in ['boxes', 'whiskers', 'fliers', 'means', 'caps']:
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
    
    fp_codel_pih1_send = "Codel/pih1_Codelpp_synchro_test_91_6.csv"
    fp_codel_pih2_send = "Codel/pih2_Codelpp_synchro_test_91_6.csv"
    fp_codel_pih1_receive = "Codel/pi4_Codelpp_synchro_test_91_6_pih1.csv"
    fp_codel_pih2_receive = "Codel/pi4_Codelpp_synchro_test_91_6_pih2.csv"
    df_codel = synchro(fp_codel_pih1_send, fp_codel_pih2_send, fp_codel_pih1_receive, fp_codel_pih2_receive)
   
    fp_inter3_pih1_send = "inter3/pih1_SynCodelpp_synchro_test_42_4.csv"
    fp_inter3_pih2_send = "inter3/pih2_SynCodelpp_synchro_test_42_4.csv"
    fp_inter3_pih1_receive = "inter3/pi4_SynCodelpp_synchro_test_42_4_pih1.csv"
    fp_inter3_pih2_receive = "inter3/pi4_SynCodelpp_synchro_test_42_4_pih2.csv"
    df_inter3 = synchro(fp_inter3_pih1_send, fp_inter3_pih2_send, fp_inter3_pih1_receive, fp_inter3_pih2_receive)
   
    fp_inter5_pih1_send = "inter5/pih1_SynCodelpp_synchro_test_46_1.csv"
    fp_inter5_pih2_send = "inter5/pih2_SynCodelpp_synchro_test_46_1.csv"
    fp_inter5_pih1_receive = "inter5/pi4_SynCodelpp_synchro_test_46_1_pih1.csv"
    fp_inter5_pih2_receive = "inter5/pi4_SynCodelpp_synchro_test_46_1_pih2.csv"
    df_inter5 = synchro(fp_inter5_pih1_send, fp_inter5_pih2_send, fp_inter5_pih1_receive, fp_inter5_pih2_receive)
    
    fp_inter7_pih1_send = "inter7/pih1_SynCodelpp_synchro_test_48_3.csv"
    fp_inter7_pih2_send = "inter7/pih2_SynCodelpp_synchro_test_48_3.csv"
    fp_inter7_pih1_receive = "inter7/pi4_SynCodelpp_synchro_test_48_3_pih1.csv"
    fp_inter7_pih2_receive = "inter7/pi4_SynCodelpp_synchro_test_48_3_pih2.csv"
    df_inter7 = synchro(fp_inter7_pih1_send, fp_inter7_pih2_send, fp_inter7_pih1_receive, fp_inter7_pih2_receive)
    
    fp_inter10_pih1_send = "inter10/pih1_SynCodelpp_synchro_test_47_4.csv"
    fp_inter10_pih2_send = "inter10/pih2_SynCodelpp_synchro_test_47_4.csv"
    fp_inter10_pih1_receive = "inter10/pi4_SynCodelpp_synchro_test_47_4_pih1.csv"
    fp_inter10_pih2_receive = "inter10/pi4_SynCodelpp_synchro_test_47_4_pih2.csv"
    df_inter10 = synchro(fp_inter10_pih1_send, fp_inter10_pih2_send, fp_inter10_pih1_receive, fp_inter10_pih2_receive)
   
    fp_inter15_pih1_send = "inter15/pih1_SynCodelpp_synchro_test_49_4.csv"
    fp_inter15_pih2_send = "inter15/pih2_SynCodelpp_synchro_test_49_4.csv"
    fp_inter15_pih1_receive = "inter15/pi4_SynCodelpp_synchro_test_49_4_pih1.csv"
    fp_inter15_pih2_receive = "inter15/pi4_SynCodelpp_synchro_test_49_4_pih2.csv"
    df_inter15 = synchro(fp_inter15_pih1_send, fp_inter15_pih2_send, fp_inter15_pih1_receive, fp_inter15_pih2_receive)
    
    # All the synchro
    dfs = [df_baseline, df_codel, df_codelpp, df_inter3, df_inter5, df_inter7, df_inter10, df_inter15]
    
    fig, ax = plt.subplots(figsize=(10, 6))
        
    labels = ["Baseline", "CoDel", "CoDel++","THRE=3ms","THRE=5ms","THRE=7ms","THRE=10ms","THRE=15ms"]
    boxplots_h = box_plot(dfs, 'black', 'lightblue', labels)
    
    
    # Set y-axis label
    ax.set_ylabel('Sycnhronization Difference (ms)')
    plt.yscale("log")  
    
    # Set plot title
    #plt.title('Sycnhronization Difference between Haptic & Video Flow: THRE as Variable')
    
    #ax.yaxis.set_major_locator(plt.MultipleLocator(base=50)) 
    ax.axvline(x=3.5, color='black', linestyle='-', linewidth=1)
    plt.show()
    whiskers = [item.get_ydata()[1] for item in boxplots_h['whiskers']]
    medians = [item.get_ydata()[1] for item in boxplots_h['medians']]
    
    
    
