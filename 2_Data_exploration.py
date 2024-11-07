

#                         DATA SCIENCE COURSE PROJECT
#                        DATA EXPLORATION & STATISTICS
#                                  TEAM #1


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import matplotlib.ticker as ticker
from scipy import stats
from pandas.plotting import autocorrelation_plot
import os


# Path to access to the .csv files (It might need to be modified when working on local environment)
full_data = pd.read_csv('C:/Users/kotar/OneDrive - The Institute of Sustainable Energy Stichting/1. INNOENERGY MASTER/2. UPC BARCELONA/Subjects/Data Science/Final Project_Lucas rep/datascience/datas/1_full_data.csv')

# Modifying some minor things
full_data.rename(columns = {'Unnamed: 0':'date','demand_prevista':'demand_fore',
                            'generacion_prevista_solar':'solar_gen_fore',
                            'generacion_prevista_solar_termic':'solar_thermal_fore',
                            'prevision_produccion_eolica':'wind_gen_fore',
                            'pbf_solar_fot':'pbf_solarPV'}, inplace = True)
full_data['date'] = pd.to_datetime(full_data['date'])
full_data.set_index('date', inplace = True)

# Stats
total_stats = full_data.agg(['mean', 'var'])
# Group by year and calculate mean, median, and variance for each numeric column
yearly_stats = full_data.groupby(full_data.index.year).agg(['mean', 'var'])
# Group by month and calculate statistics
monthly_stats = full_data.groupby(full_data.index.month).agg(['mean', 'var'])


# Adding some features to check correlation later on
# Day of the week
def get_dayofweek(date):
    day_of_week = date.dayofweek
    if day_of_week == 0:
        return 'Monday'
    elif day_of_week == 1:
        return 'Tuesday'
    elif day_of_week == 2:
        return 'Wednesday'
    elif day_of_week == 3:
        return 'Thursday'
    elif day_of_week == 4:
        return 'Friday'
    elif day_of_week == 5:
        return 'Saturday'
    else:
        return 'Sunday'
full_data['day_of_week'] = full_data.index.to_series().apply(get_dayofweek)

# Season
def get_season(date):
    month = date.month
    day = date.day
    if (month == 12 and day >= 21) or month in [1, 2] or (month == 3 and day < 20):
        return 'Winter'
    elif (month == 3 and day >= 20) or month in [4, 5] or (month == 6 and day < 21):
        return 'Spring'
    elif (month == 6 and day >= 21) or month in [7, 8] or (month == 9 and day < 23):
        return 'Summer'
    else:
        return 'Fall'
full_data['season'] = full_data.index.to_series().apply(get_season)

# Weekends
def get_weekends(day_of_week):
    if day_of_week in ['Saturday', 'Sunday']:
        return 'weekend'
    else:
        return 'No weekend'
full_data['weekend'] = full_data['day_of_week'].apply(get_weekends)

# Reorganizing the columns
full_data = full_data.iloc[:, [17,19,18,0,1,2,3,4,16,5,6,7,8,9,10,11,12,13,14,15]]



# Plotting the Day Ahead Price to identify trends.
plt.figure(figsize=(12,7))
plt.plot(full_data['price_DA'], color='grey')
plt.xlabel('Date', fontsize=15)
plt.ylabel('Day-ahead price', fontsize=15)
plt.title('Day-ahead price 2014 -2024', fontsize=15)
plt.show()

# Day ahead price per year.
for year, data in full_data.groupby(full_data.index.year):
    
    plt.figure(figsize=(12, 7))
    plt.plot(data['price_DA'], color = 'grey')
    plt.title(f'Day-Ahead Price for {year}')
    plt.xlabel('Date')
    plt.ylabel('Day ahead price', fontsize=15)
    plt.legend()
    plt.show()
    
# Forecasted demand & Programed demand per year
for year, data in full_data.groupby(full_data.index.year):
    
    plt.figure(figsize=(12, 7))
    plt.plot(data['demand_prog'], color = 'blue')
    plt.plot(data['demand_fore'], color = 'red')
    plt.title(f'Forecasted demand & Programed demand {year}')
    plt.xlabel('DATE')
    plt.ylabel('Demand', fontsize=15)
    plt.legend()
    plt.show()
    
# Forecasted generation (Solar, solar thermal & wind)
for year, data in full_data.groupby(full_data.index.year):
    
    plt.figure(figsize=(12, 7))
    plt.plot(data['solar_gen_fore'], color = 'lightblue', label = 'Solar generation forecast')
    plt.plot(data['solar_thermal_fore'], color = 'lightgray', label = 'Solar thermal generation forecast')
    plt.plot(data['wind_gen_fore'], color = 'yellow', label = 'Wind generation forecast')
    plt.title(f'Forecasted generation {year}')
    plt.xlabel('Date')
    plt.ylabel('Renewables generation', fontsize=15)
    plt.legend()
    plt.show()


# Plotting the stats for each variable to see their behaviour
for variable in yearly_stats.columns.levels[0]:  # Top-level columns
    fig, ax1 = plt.subplots(figsize=(12, 7))
    
    # Plot variance on the left y-axis
    ax1.plot(yearly_stats.index, yearly_stats[variable]['var'], label='Variance', color='lightgrey')
    ax1.set_xlabel('Year')
    ax1.set_ylabel(f'{variable} Variance')
    ax1.legend(loc='upper left')
    # Second y-axis for the mean
    ax2 = ax1.twinx()
    ax2.plot(yearly_stats.index, yearly_stats[variable]['mean'], label='Mean', color='grey')
    ax2.set_ylabel(f'{variable} Mean')
    ax2.legend(loc='upper right')
    plt.title(f'Yearly Statistics for {variable}')
    plt.show()




