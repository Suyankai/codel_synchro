# -*- coding: utf-8 -*-

import re
import pandas as pd
import matplotlib.pyplot as plt

log_file = "SynCodelpp_p4_test_85_5.txt"  # Replace with the actual path to your log file

# Regular expressions to extract the required information
time_pattern = r"\[(\d{2}:\d{2}:\d{2}\.\d+)\]"
pkt_id_pattern = r"\[\d+\.\d+\]"
value_pattern = r"Wrote register 'r_SynSwitch' at index 0 with value (\d+)"
delta_egress_pattern = r"Wrote register 'r_Delta2_debug' at index 0 with value (\d+)"

value_list = []
time_list = []
pkt_id_list = []

delta_egress_list = []
pkt_id_e_list = []
time_e_list = []

with open(log_file, "r") as file:
    for line in file:
        value_match = re.search(value_pattern, line)
        if value_match:
            value_list.append(value_match.group(1))
            
            time_match = re.search(time_pattern, line)
            time_list.append(time_match.group(1))
            
            pkt_id_match = re.search(pkt_id_pattern, line)
            pkt_id_list.append(pkt_id_match.group(0)[1:(len(pkt_id_match.group(0))-1)])
        else:
            delta_egress_match = re.search(delta_egress_pattern, line)
            if delta_egress_match:
                delta_egress_list.append(delta_egress_match.group(1))
                
                pkt_id_e_match = re.search(pkt_id_pattern, line)
                pkt_id_e_list.append(pkt_id_e_match.group(0)[1:(len(pkt_id_e_match.group(0))-1)])
                
                time_e_match = re.search(time_pattern, line)
                time_e_list.append(time_e_match.group(1))

data1 = {
    "Time": time_list,
    "Pkt ID": pkt_id_list,
    "Value": value_list
}
data2 = {
    "Time": time_e_list,
    "Pkt ID": pkt_id_e_list,
    "Delta_egress": delta_egress_list
}

df_part1 = pd.DataFrame(data1)
df_part2 = pd.DataFrame(data2)

# Merge the two DataFrames based on the "Pkt ID" column
merged_df = df_part1.merge(df_part2, on="Pkt ID", how="left")

# Create a new column "Delta_egress" in df_part1 and fill it with the values from merged_df
df_part1["Delta_egress"] = merged_df["Delta_egress"]

for i in range(len(df_part1)):
    df_part1["Delta_egress"][i] = int(df_part1["Delta_egress"][i])/1000
for i in range(len(df_part2)):
    df_part2["Delta_egress"][i] = int(df_part2["Delta_egress"][i])/1000


#Draw the diagramm
# Convert "Time" column to datetime type
df_part2["Time"] = pd.to_datetime(df_part2["Time"])

# Calculate the time difference relative to the starting time
start_time2 = df_part2["Time"].iloc[0]
df_part2["TimeDelta"] = (df_part2["Time"] - start_time2).dt.total_seconds()

# Create the line plot with "TimeDelta" as the x-axis and "Delta_egress" as the y-axis
plt.plot(df_part2["TimeDelta"], df_part2["Delta_egress"], linestyle="-")
plt.xlabel("Time Delta (seconds)")
plt.ylabel("Delta_egress (ms)")


# Mark a specific point on the x-axis
x_mark = 11  # Replace this with the desired x-coordinate value
plt.axvline(x_mark, color="red", linestyle="--", label="Marked Point")

#Switch
# Create a twin Axes for plotting "Value" data on the right side
# Convert "Time" column to datetime type
df_part1["Time"] = pd.to_datetime(df_part1["Time"])

# Calculate the time difference relative to the starting time
start_time1 = df_part1["Time"].iloc[0]
df_part1["TimeDelta"] = (df_part1["Time"] - start_time1).dt.total_seconds()

#show the begining switch
tempList_time = []
tempList_value = []
delta = (start_time1 - start_time2).total_seconds()
if delta > 0:
    tempList_time.append(0)
    tempList_value.append("0")
    for i in range(len(df_part1)):
        tempList_time.append(df_part1["TimeDelta"][i] + delta)
        tempList_value.append(df_part1["Value"][i])
    
    data1_new = {
        "TimeDelta": tempList_time,
        "Value": tempList_value
        }
    df_part1_new = pd.DataFrame(data1_new)
else:
    df_part1_new = df_part1

ax2 = plt.twinx()
ax2.step(df_part1_new["TimeDelta"], df_part1_new["Value"], linestyle="-",where='post', color="tab:orange")

# Customize the plot
if (start_time1 - start_time2).total_seconds() > 0:
    ax2.set_ylim(-0.05, 1.05)
else:
    ax2.set_ylim(1.05, -0.05)
# ax2.set_ylim(1.05, -0.05)
#ax2.set_ylim(-0.05, 1.05)
ax2.set_yticklabels(["ON", "OFF"])

ax2.set_ylabel("Syn. Switch")
plt.title("Adaptive SynCodelpp")


# Combine the legends for both lines on a single plot
lines, labels = plt.gca().get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
plt.legend(lines + lines2, labels + labels2, loc="best")

# Show the plot
plt.show()