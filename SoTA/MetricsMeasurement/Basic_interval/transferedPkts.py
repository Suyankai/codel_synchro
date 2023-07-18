# -*- coding: utf-8 -*-

import pandas as pd
import datetime
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None 

# Sample data
values = [253*100/1993,425*100/1992,582*100/2005, 606*100/1986, 733*100/1995]

# Create a Figure and Axes object
fig, ax = plt.subplots(figsize=(6, 7))

# Plotting the histogram
ax.bar(range(len(values)), values, width=0.5)

# Adding labels and title
ax.set_ylabel('Prioritizied Percentage (%)')
ax.set_title('Percentage of Prioritized Video Packets: THRE as Variable')

# Customizing x-axis tick labels
ax.set_xticks(range(len(values)))
ax.set_xticklabels(["THRE=3ms","THRE=5ms","THRE=7ms","THRE=10ms","THRE=15ms"])

ax.yaxis.set_major_locator(plt.MultipleLocator(base=1)) 

ax.grid(True)

# Display the plot
plt.show()