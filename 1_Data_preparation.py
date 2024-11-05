

#                         DATA SCIENCE COURSE PROJECT
#                              DATA PREPARATION
#                                  TEAM #1

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import matplotlib.ticker as ticker
from scipy import stats
from pandas.plotting import autocorrelation_plot
import os


# READING ALL THE DATAFRAMES.


# Path to access to the .csv files (It might need to be modified when working on local environment)
directory = 'C:/Users/kotar/OneDrive - The Institute of Sustainable Energy Stichting/1. INNOENERGY MASTER/2. UPC BARCELONA/Subjects/Data Science/Final Project_Lucas rep/datascience/datas'

# Dictionary to store all teh dataframes
dataframes = {}
# Counter just for verification
csvcount = 0

# Loop for reading all the dfs at once and storing them in a dictionary to easy handle it for common changes
    
for filename in os.listdir(directory):
    if filename.endswith(".csv"):  # Reads only the .csv files
        # Getting the file path
        filepath = os.path.join(directory, filename)
        df = pd.read_csv(filepath)
        
        # Use the file name without '.csv' as df name
        var_name = filename[:-4]
        # Storing each dataframe into a dictionary
        dataframes[var_name] = df
        
        #globals()[var_name] = df
        csvcount += 1
print(f"Number of files imported {csvcount}\n")


# PRE-PROCESSING DATASETS



# Change to datetime and also remove the timezone, keeping the local timezone, not the UTC one
#Change to datetime
for keys in dataframes:
    dataframes[keys]['datetime'] = pd.to_datetime(dataframes[keys]['datetime'])

#Remove timezone info
for keys in dataframes:
    dataframes[keys]['datetime'] = dataframes[keys]['datetime'].apply(lambda x: x.replace(tzinfo=None))

# Check for duplicates, they appear on October, when summer time shifts to winter time
for keys in dataframes:
    duplicates = dataframes[keys][dataframes[keys].duplicated(subset='datetime',keep=False)] 
    #print(duplicates)
    
#Remove duplicates, keep last value
for keys in dataframes:
    dataframes[keys] = dataframes[keys].drop_duplicates(subset='datetime',keep='last')

#Set datetime as index
for keys in dataframes:
    dataframes[keys] = dataframes[keys].set_index('datetime')

# Give a common date_range
date_range = pd.date_range(start=dataframes['price_DA'].index.min(), end=dataframes['price_DA'].index.max(), freq='H')
#print(date_range)

for keys in dataframes:
    dataframes[keys] = dataframes[keys].reindex(date_range)
    
    
# Some graphs of daily hourly profiles just to see if the data makes sense...
# Set up a 3xlen(dataframes) subplot grid
fig, axs = plt.subplots(3, len(dataframes)//3+1, figsize=(25, 6))
fig.suptitle("Average Hourly Profile of a Day for Different DataFrames")

# Loop over each DataFrame, calculate the average hourly profile, and plot
col = 0
row = 0
for keys in dataframes:
    # Group by hour of the day and calculate the mean for each hour
    average_hourly_profile = dataframes[keys].groupby(dataframes[keys].index.hour)['value'].mean()
    
    # Plot on the corresponding subplot
    axs[row, col].plot(average_hourly_profile, marker='o', color='b')
    axs[row, col].set_title(keys)
    axs[row, col].set_xlabel("Hour of the Day")
    axs[row, col].set_xticks(range(0, 24))
    axs[row, col].grid(True)
    col += 1
    if col > 5:
        col = 0
        row += 1

# Set a common y-label for all subplots
for ax in axs[:, 0]:  # Pour chaque ligne de la première colonne
    ax.set_ylabel("Average Value")

plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust layout to fit title
plt.show()


# Rename the 'value' columns in each DataFrame to reflect their data source
for keys in dataframes:
    dataframes[keys] = dataframes[keys].rename(columns={'value': f'{keys}'})

# Concatenate the DataFrames, aligning on the index of prices_DA_full
dataframes_to_concat = [dataframes['price_DA']['price_DA']]  # Start with the prices DataFrame

# Add the renamed DataFrames from the dataframes to the list
for keys in dataframes:
    if keys != 'price_DA':
        dataframes_to_concat.extend([dataframes[keys][keys]])


# *** MAIN DATASET WE WILL USE FROM NOW ON ***
full_data = pd.concat(dataframes_to_concat, axis=1)

full_data.to_csv('C:/Users/kotar/OneDrive - The Institute of Sustainable Energy Stichting/1. INNOENERGY MASTER/2. UPC BARCELONA/Subjects/Data Science/Final Project_Lucas rep/datascience/datas/1_full_data.csv', encoding='utf-8', index=True)



