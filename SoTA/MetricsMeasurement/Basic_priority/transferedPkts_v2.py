# -*- coding: utf-8 -*-

import pandas as pd
import datetime
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None 

# Sample data
values = [294*100/1993,272*100/1952,242*100/1951, 253*100/1978]

# Create a Figure and Axes object
fig, ax = plt.subplots(figsize=(4, 4))

# Plotting the histogram
ax.bar(range(len(values)), values, width=0.5, color='dimgrey')

# Adding labels and title
ax.set_ylabel('Prioritizied Percentage (%)')
ax.set_title('Percentage of Prioritized Video Packets: THRE as Variable')

# Customizing x-axis tick labels
ax.set_xticks(range(len(values)))
ax.set_xticklabels(["PRIO=4","PRIO=5","PRIO=6","PRIO=7"])

#ax.yaxis.set_major_locator(plt.MultipleLocator(base=1)) 

# Display the plot
plt.show()
