'''
This script contains the configurations for the different graphs used in the dashboard.
'''

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from typing import Literal

# get colors for timeline series based on values
# values are taken and used as intended in the original tool from Umweltbundesamt Luftdaten API
luftdaten_color_ranges = {
    0: "#50f0e6", # sehr gut
    1: "#50cdaa", # gut 
    2: "#f0e641", # mäßig 
    3: "#ff5050", # schlecht 
    4: "#960032" # sehr schlecht
}

def get_color(value, mapper)-> str: 
    '''
    Function to get the color for the value based on the color ranges
    '''
    for index, color in mapper.items():
        if round(value) == index:
            return color
    return "#00000000"  # Transparent for NaN or out of range values


def get_air_data_index_timeline_plot(data: pd.DataFrame) -> None:
    """
    Function to plot the timeline graph of the airdata API (index)

    Args: 
        data : pd.DataFrame containing the weather data for one patient over a timeframe

    Returns: 
        None (plots the graph)
    """

    data['Date'] = pd.to_datetime(data['Date'])

    # Set the date as index
    data.set_index('Date', inplace=True)

    # Reindex to include all dates in the range, filling with NaN where data is missing
    data = data.reindex(pd.date_range(start=data.index.min(), end=data.index.max()), fill_value=None)

    data.index.name = 'Date'
    data['Color'] = data['Index'].apply(lambda x: get_color(value = x, mapper = luftdaten_color_ranges) if not np.isnan(x) else (0, 0, 0, 0))

    plt.figure(figsize=(10, 5))
    for i in range(1, len(data)):
        x = [data.index[i - 1], data.index[i]]
        y = [data['Index'].iloc[i - 1], data['Index'].iloc[i]]
        
        # Only plot if both points in the segment have values (not NaN)
        if not np.isnan(y).any():
            plt.plot(x, y, color=data['Color'].iloc[i])

    plt.ylim(0, 4)
    plt.title("Luftqualität index Timeline")
    plt.xlabel("Tage")
    plt.ylabel("Luftqualität Index")

    plt.show()

def get_air_data_component_timeline_plot(data: pd.DataFrame, component_name: str)-> None: 
    """
    Function to plot the timeline graph of the airdata API (components)

    Args: 
        data (pd.DataFrame): pd.DataFrame containing the weather data for one patient over a timeframe
        component_name (str): the name of the component to be plotted over time
    Returns: 
        None (plots the graph)
    """
    data = data.rename_axis('Date').reset_index()

    # Reindex to include all dates in the range, filling with NaN where data is missing
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)
    data = data.reindex(pd.date_range(start=data.index.min(), end=data.index.max()), fill_value=None)
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data[component_name])
    plt.title(f"{component_name} Timeline")
    plt.xlabel("Tage")
    plt.ylabel(f"{component_name}")
    plt.legend()
    plt.show()



def get_weatherdata_timeline_plot(data: pd.DataFrame, column: Literal["Niederschlag (mm)", "Luftdruck (hPa)", "Sonnenscheindauer (min)", "Temperatur (°C)","Windgeschwindigkeit (km / h)", "Relative Luftfeuchtigkeit (%)",])-> None:
    """
    Function to plot the timeline graph of the weather data.

    Args: 
        data : pd.DataFrame containing the weather data for one patient over a timeframe
        column : the column to be plotted over time
    Returns: 
        None (plots the graph)
    """

    data['Tag'] = pd.to_datetime(data['Tag'])  # Ensure 'Tag' is in datetime format

    # Plot the timeline graph
    plt.figure(figsize=(10, 6))
    plt.plot(data['Tag'], data[column], linestyle='-', color='b', label=column)
    plt.title(f'{column} über Zeit', fontsize=14)
    plt.xlabel('Tag', fontsize=12)
    plt.ylabel(f'{column}', fontsize=12)
    plt.grid(True)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()


def get_sewagedata_timeline_plot(data: pd.DataFrame, column: str)-> None:
    """
    Function to plot the timeline graph of the sewage data.

    Args: 
        data : pd.DataFrame containing the sewage data for one patient over a timeframe
        column : the column to be plotted over time
    Returns: 
        None (plots the graph)
    """

    data['datum'] = pd.to_datetime(data['datum'])
    

    # Plot the timeline graph
    plt.figure(figsize=(10, 6))
    plt.plot(data['datum'], data[column], linestyle='-', color='b', label=column)
    plt.title(f'{column} über Zeit', fontsize=14)
    plt.xlabel('datum', fontsize=12)
    plt.ylabel(f'{column}', fontsize=12)
    plt.grid(True)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()