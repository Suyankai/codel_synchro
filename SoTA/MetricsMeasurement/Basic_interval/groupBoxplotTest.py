# -*- coding: utf-8 -*-
import seaborn as sns
import matplotlib.pyplot as plt

# Set the figure size
plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True

# Import a Seaborn dataset
data = sns.load_dataset('tips')

group = data['day']

# Create a grouped boxplot
sns.boxplot(x=group, y=data['total_bill'], hue=data['sex'])


plt.show()
