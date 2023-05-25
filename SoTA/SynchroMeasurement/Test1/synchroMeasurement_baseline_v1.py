import pandas as pd
import datetime
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

# import the data
df_pih1_send = pd.read_csv("pih1_baseline_1.csv", sep=",")
df_pih2_send = pd.read_csv("pih2_baseline_1.csv", sep=",")
df_pih1_receive = pd.read_csv("pi4_pih1_baseline_1_loss.csv", sep=",")
df_pih2_receive = pd.read_csv("pi4_pih2_baseline_1.csv", sep=",")


print("Form the df_pih1 & df_pih2")
# Merge the two dataframes based on the 'identification' column:pih1
merged_df_pih1 = pd.merge(df_pih1_receive, df_pih1_send, on='Identification', how='inner')

# Select the desired columns and rename:pih1
df_pih1 = merged_df_pih1[['Identification', 'Time_y', 'Time_x']]
df_pih1 = df_pih1.rename(columns={'Time_y':'time_sent','Time_x':'time_received'})

# format the time:pih1
for i in range(len(df_pih1)):
    df_pih1['time_sent'][i] = datetime.datetime.strptime(df_pih1['time_sent'][i], '%Y-%m-%d %H:%M:%S,%f')
    df_pih1['time_received'][i] = datetime.datetime.strptime(df_pih1['time_received'][i], '%Y-%m-%d %H:%M:%S,%f')

# Merge the two dataframes based on the 'identification' column:pih2
merged_df_pih2 = pd.merge(df_pih2_receive, df_pih2_send, on='Identification', how='inner')

# Select the desired columns and rename:pih2
df_pih2 = merged_df_pih2[['Identification', 'Time_y', 'Time_x']]
df_pih2 = df_pih2.rename(columns={'Time_y':'time_sent','Time_x':'time_received'})

# format the time:pih2
for i in range(len(df_pih2)):
    df_pih2['time_sent'][i] = datetime.datetime.strptime(df_pih2['time_sent'][i], '%Y-%m-%d %H:%M:%S,%f')
    df_pih2['time_received'][i] = datetime.datetime.strptime(df_pih2['time_received'][i], '%Y-%m-%d %H:%M:%S,%f')

print("Get the event pair")
# Get the event pair
# set up the starting flag and ending flag
print("set up the starting flag and ending flag")
if df_pih1['time_sent'][0] > df_pih2['time_sent'][0]:
    start_flag = df_pih1['time_sent'][0]
    end_flag = df_pih2['time_sent'][len(df_pih2)-1]
else:
    start_flag = df_pih2['time_sent'][0]
    end_flag = df_pih1['time_sent'][len(df_pih1)-1]
    
print("Initialize the pair dataframe")
step = datetime.timedelta(milliseconds=0.1)
indicator = start_flag
df_pair = pd.DataFrame()

time_step = []
ID_pih1 = []
time_send_pih1 = []
time_received_pih1 = []
ID_pih2 = []
time_send_pih2 = []
time_received_pih2 = []

print("Loop until the indicator reaches the end time")
# Loop until the indicator reaches the end time
while indicator <= end_flag:
    # Increment the indicator by the step size
    print(indicator,"/",end_flag)
    indicator += step
    
    # Find the closest value to the given timestamp
    closest_value_pih1 = min(df_pih1['time_sent'], key=lambda x: abs(x - indicator))
    closest_value_pih2 = min(df_pih2['time_sent'], key=lambda x: abs(x - closest_value_pih1))
    if abs((closest_value_pih2 - closest_value_pih1)).total_seconds() * 1000 > 0.5:
        print("Skip:time difference too high")
        continue
    
    # pih1
    # Retrieve the corresponding identification value
    closest_identification_pih1 = df_pih1.loc[df_pih1['time_sent'] == closest_value_pih1, 'Identification'].values[0]
    closest_time_received_pih1 = df_pih1.loc[df_pih1['time_sent'] == closest_value_pih1, 'time_received'].values[0]
    time_step.append(indicator)
    ID_pih1.append(closest_identification_pih1)
    time_send_pih1.append(closest_value_pih1)
    time_received_pih1.append(closest_time_received_pih1)
    
    
    # pih2
    # Retrieve the corresponding identification value
    closest_identification_pih2  = df_pih2.loc[df_pih2['time_sent'] == closest_value_pih2, 'Identification'].values[0]
    closest_time_received_pih2  = df_pih2.loc[df_pih2['time_sent'] == closest_value_pih2, 'time_received'].values[0]
    ID_pih2.append(closest_identification_pih2)
    time_send_pih2.append(closest_value_pih2)
    time_received_pih2.append(closest_time_received_pih2)

    
    

print("put the lists together")
# put the lists together
df_pair['time_step'] = time_step
df_pair['ID_pih1'] = ID_pih1
df_pair['time_send_pih1'] = time_send_pih1
df_pair['time_received_pih1'] = time_received_pih1
df_pair['ID_pih2'] = ID_pih2
df_pair['time_send_pih2'] = time_send_pih2
df_pair['time_received_pih2'] = time_received_pih2

print("calculate the synchronization difference")
# calculate the synchronization difference
df_pair['Synchro_send'] = abs(df_pair['time_send_pih1'] - df_pair['time_send_pih2'])
df_pair['Synchro_received'] = abs(df_pair['time_received_pih1'] - df_pair['time_received_pih2'])
for i in range(len(df_pair)):
    df_pair['Synchro_send'][i] = df_pair['Synchro_send'][i].total_seconds() * 1000
    df_pair['Synchro_received'][i] = df_pair['Synchro_received'][i].total_seconds() * 1000

# fig,ax = plt.subplots()
# ax.boxplot([df_pair['Synchro_send'],df_pair['Synchro_received']])

print("Average synchronization difference of sending is:", df_pair['Synchro_send'].mean(),"ms")
print("Average synchronization difference of receiving is:", df_pair['Synchro_received'].mean(),"ms")

    
    